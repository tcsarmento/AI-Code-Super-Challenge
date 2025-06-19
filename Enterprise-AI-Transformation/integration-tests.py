#!/usr/bin/env python3
"""
Integration Test Suite for Super Challenge
Tests the complete transaction flow with all services
"""

import pytest
import asyncio
import httpx
import json
import time
import websockets
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any, List
import redis
import psycopg2
from kafka import KafkaConsumer, KafkaProducer

# Test configuration
BASE_URL = "http://localhost:8001"
FRAUD_SERVICE_URL = "http://localhost:8002"
ANALYTICS_URL = "http://localhost:8003"
WS_URL = "ws://localhost:8003/ws/metrics"

# Test data
TEST_ACCOUNTS = [
    ("1111111111", "C", 10000.00, "TESTCUST001", False),
    ("2222222222", "S", 50000.00, "TESTCUST002", True),   # VIP
    ("3333333333", "B", 100000.00, "TESTCUST003", True),  # Business with overdraft
    ("9999999999", "C", 100.00, "FRAUDTEST001", False),   # Low balance for fraud test
]

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def http_client():
    """Async HTTP client for API testing"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client

@pytest.fixture
def kafka_producer():
    """Kafka producer for sending test events"""
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    yield producer
    producer.close()

@pytest.fixture
def kafka_consumer():
    """Kafka consumer for event verification"""
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=5000
    )
    yield consumer
    consumer.close()

@pytest.fixture
def redis_client():
    """Redis client for cache testing"""
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    yield client
    client.close()

@pytest.fixture
def test_accounts():
    """Create test accounts in database"""
    conn = psycopg2.connect(
        "postgresql://challenge:challenge123@localhost:5432/transactions"
    )
    cur = conn.cursor()
    
    # Create accounts table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number VARCHAR(10) PRIMARY KEY,
            account_type CHAR(1),
            balance DECIMAL(15,2),
            available_balance DECIMAL(15,2),
            daily_limit DECIMAL(15,2) DEFAULT 5000000.00,
            daily_used DECIMAL(15,2) DEFAULT 0.00,
            customer_id VARCHAR(20),
            is_vip BOOLEAN DEFAULT FALSE,
            risk_score INTEGER DEFAULT 0,
            overdraft_limit DECIMAL(15,2) DEFAULT 0.00,
            last_transaction TIMESTAMP,
            transaction_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert test accounts
    for account in TEST_ACCOUNTS:
        cur.execute("""
            INSERT INTO accounts (
                account_number, account_type, balance, available_balance,
                customer_id, is_vip, overdraft_limit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (account_number) DO UPDATE
            SET balance = EXCLUDED.balance,
                available_balance = EXCLUDED.available_balance,
                daily_used = 0.00
        """, (
            account[0], account[1], account[2], 
            account[2] + (100000 if account[1] == 'B' else 0),  # Available balance
            account[3], account[4],
            100000.00 if account[1] == 'B' else 0.00  # Overdraft for business
        ))
    
    conn.commit()
    yield TEST_ACCOUNTS
    
    # Cleanup
    for account in TEST_ACCOUNTS:
        cur.execute("DELETE FROM accounts WHERE account_number = %s", (account[0],))
    conn.commit()
    cur.close()
    conn.close()

class TestTransactionFlow:
    """Test complete transaction processing flow"""
    
    @pytest.mark.asyncio
    async def test_successful_transaction(self, http_client, test_accounts, kafka_consumer):
        """Test a successful transaction from end to end"""
        
        # Prepare transaction
        transaction = {
            "from_account": "1111111111",
            "to_account": "2222222222",
            "amount": 100.00,
            "currency": "USD",
            "transaction_type": "DM"
        }
        
        # Submit transaction
        start_time = time.time()
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        end_time = time.time()
        
        # Verify response
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "completed"
        assert "transaction_id" in result
        transaction_id = result["transaction_id"]
        
        # Verify performance
        processing_time = (end_time - start_time) * 1000
        assert processing_time < 100, f"Processing time {processing_time}ms exceeds 100ms"
        
        # Verify account balances updated
        await asyncio.sleep(0.5)  # Allow time for DB update
        
        # Check from account (should have fee deducted)
        from_account = await http_client.get(f"{BASE_URL}/api/v1/accounts/1111111111")
        assert from_account.status_code == 200
        # 10000 - 100 - 2.50 (fee) = 9897.50
        assert float(from_account.json()["balance"]) == 9897.50
        
        # Check to account
        to_account = await http_client.get(f"{BASE_URL}/api/v1/accounts/2222222222")
        assert to_account.status_code == 200
        assert float(to_account.json()["balance"]) == 50100.00  # 50000 + 100
        
        # Verify event published to Kafka
        event_received = False
        for message in kafka_consumer:
            if message.value.get("transaction_id") == transaction_id:
                event_received = True
                assert message.value["status"] == "completed"
                assert message.value["event_type"] == "transaction.completed"
                break
        
        assert event_received, "Transaction event not received in Kafka"
    
    @pytest.mark.asyncio
    async def test_vip_no_fees(self, http_client, test_accounts):
        """Test that VIP customers have no transaction fees"""
        
        transaction = {
            "from_account": "2222222222",  # VIP account
            "to_account": "1111111111",
            "amount": 200.00,
            "currency": "USD",
            "transaction_type": "WT"  # Wire transfer normally has $35 fee
        }
        
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        
        assert response.status_code == 200
        
        # Check balance - no fee should be deducted
        await asyncio.sleep(0.5)
        account = await http_client.get(f"{BASE_URL}/api/v1/accounts/2222222222")
        assert float(account.json()["balance"]) == 49800.00  # 50000 - 200 (no fee)
    
    @pytest.mark.asyncio
    async def test_business_overdraft(self, http_client, test_accounts):
        """Test business account can use overdraft"""
        
        transaction = {
            "from_account": "3333333333",  # Business account with 100k + 100k overdraft
            "to_account": "1111111111",
            "amount": 150000.00,  # More than balance but within overdraft
            "currency": "USD",
            "transaction_type": "WT"
        }
        
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        
        assert response.status_code == 200
        
        # Check balance went negative
        await asyncio.sleep(0.5)
        account = await http_client.get(f"{BASE_URL}/api/v1/accounts/3333333333")
        balance = float(account.json()["balance"])
        assert balance < 0, "Business account should have negative balance"
        assert balance > -100000, "Should not exceed overdraft limit"
    
    @pytest.mark.asyncio
    async def test_fraud_detection_high_risk(self, http_client, test_accounts):
        """Test that high-risk transactions are blocked"""
        
        # First, check fraud service directly
        fraud_check_request = {
            "from_account": "9999999999",
            "to_account": "2222222222",
            "amount": 99999.00,
            "currency": "USD",
            "transaction_type": "WT"
        }
        
        fraud_response = await http_client.post(
            f"{FRAUD_SERVICE_URL}/api/v1/analyze",
            json=fraud_check_request
        )
        assert fraud_response.status_code == 200
        fraud_result = fraud_response.json()
        assert fraud_result["risk_score"] > 60, "Should be high risk"
        
        # Now submit transaction - should be blocked
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=fraud_check_request
        )
        
        assert response.status_code == 403
        assert "fraud" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_insufficient_funds(self, http_client, test_accounts):
        """Test transaction with insufficient funds"""
        
        transaction = {
            "from_account": "9999999999",  # Has only 100.00
            "to_account": "2222222222",
            "amount": 200.00,
            "currency": "USD",
            "transaction_type": "DM"
        }
        
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        
        assert response.status_code == 400
        assert "insufficient funds" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_validation_errors(self, http_client, test_accounts):
        """Test various validation errors"""
        
        # Test 1: Invalid account format
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json={
                "from_account": "123",  # Too short
                "to_account": "2222222222",
                "amount": 100.00
            }
        )
        assert response.status_code == 422
        
        # Test 2: Same account transfer
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json={
                "from_account": "1111111111",
                "to_account": "1111111111",
                "amount": 100.00
            }
        )
        assert response.status_code == 422
        
        # Test 3: Amount too high
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json={
                "from_account": "1111111111",
                "to_account": "2222222222",
                "amount": 2000000.00  # Over $1M limit
            }
        )
        assert response.status_code == 422
        
        # Test 4: Negative amount
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json={
                "from_account": "1111111111",
                "to_account": "2222222222",
                "amount": -100.00
            }
        )
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_idempotency(self, http_client, test_accounts, redis_client):
        """Test idempotency - same request returns same result"""
        
        idempotency_key = f"test-idemp-{time.time()}"
        transaction = {
            "from_account": "1111111111",
            "to_account": "2222222222",
            "amount": 50.00,
            "currency": "USD",
            "idempotency_key": idempotency_key
        }
        
        # First request
        response1 = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        assert response1.status_code == 200
        result1 = response1.json()
        
        # Second request with same idempotency key
        response2 = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        assert response2.status_code == 200
        result2 = response2.json()
        
        # Should return same transaction ID
        assert result1["transaction_id"] == result2["transaction_id"]
        
        # Check only one transaction was processed
        await asyncio.sleep(0.5)
        account = await http_client.get(f"{BASE_URL}/api/v1/accounts/1111111111")
        # Should only have one transaction deducted
        assert float(account.json()["balance"]) == 9947.50  # 10000 - 50 - 2.50
    
    @pytest.mark.asyncio
    async def test_concurrent_transactions(self, http_client, test_accounts):
        """Test system handles concurrent transactions correctly"""
        
        initial_balance = 10000.00
        transaction_amount = 10.00
        fee = 2.50
        concurrent_count = 20
        
        # Create concurrent transactions
        tasks = []
        for i in range(concurrent_count):
            transaction = {
                "from_account": "1111111111",
                "to_account": "2222222222",
                "amount": transaction_amount,
                "currency": "USD",
                "transaction_type": "DM"
            }
            task = http_client.post(
                f"{BASE_URL}/api/v1/transactions",
                json=transaction
            )
            tasks.append(task)
        
        # Execute concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful transactions
        successful = sum(
            1 for r in responses 
            if not isinstance(r, Exception) and r.status_code == 200
        )
        
        print(f"Successful concurrent transactions: {successful}/{concurrent_count}")
        
        # Verify final balance is correct
        await asyncio.sleep(1)  # Allow all updates to complete
        account = await http_client.get(f"{BASE_URL}/api/v1/accounts/1111111111")
        final_balance = float(account.json()["balance"])
        
        expected_balance = initial_balance - (successful * (transaction_amount + fee))
        assert abs(final_balance - expected_balance) < 0.01, \
            f"Balance mismatch: expected {expected_balance}, got {final_balance}"


class TestAnalyticsIntegration:
    """Test real-time analytics functionality"""
    
    @pytest.mark.asyncio
    async def test_websocket_metrics_update(self, http_client, test_accounts):
        """Test that WebSocket broadcasts real-time metrics"""
        
        metrics_updates = []
        
        async with websockets.connect(WS_URL) as websocket:
            # Get initial metrics
            initial_msg = await websocket.recv()
            initial_data = json.loads(initial_msg)
            initial_count = initial_data["metrics"]["totalTransactions"]
            
            # Submit a transaction
            transaction = {
                "from_account": "1111111111",
                "to_account": "2222222222",
                "amount": 100.00,
                "currency": "USD"
            }
            
            response = await http_client.post(
                f"{BASE_URL}/api/v1/transactions",
                json=transaction
            )
            assert response.status_code == 200
            
            # Wait for analytics update (with timeout)
            try:
                while True:
                    msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(msg)
                    metrics_updates.append(data)
                    
                    if data["metrics"]["totalTransactions"] > initial_count:
                        # Verify metrics updated correctly
                        assert data["metrics"]["totalTransactions"] == initial_count + 1
                        assert data["metrics"]["totalVolume"] > 0
                        break
            except asyncio.TimeoutError:
                pytest.fail("Analytics did not update within timeout")
    
    @pytest.mark.asyncio
    async def test_fraud_metrics_tracking(self, http_client, test_accounts):
        """Test that fraud blocks are tracked in analytics"""
        
        # Get initial fraud count
        response = await http_client.get(f"{ANALYTICS_URL}/api/v1/metrics/summary")
        initial_fraud_count = response.json()["metrics"]["fraudBlocked"]
        
        # Submit high-risk transaction
        high_risk_transaction = {
            "from_account": "9999999999",
            "to_account": "1111111111",
            "amount": 99999.00,
            "currency": "USD",
            "transaction_type": "WT"
        }
        
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=high_risk_transaction
        )
        assert response.status_code == 403  # Should be blocked
        
        # Check fraud metrics updated
        await asyncio.sleep(1)
        response = await http_client.get(f"{ANALYTICS_URL}/api/v1/metrics/summary")
        new_fraud_count = response.json()["metrics"]["fraudBlocked"]
        
        assert new_fraud_count == initial_fraud_count + 1


class TestPerformance:
    """Performance and load tests"""
    
    @pytest.mark.asyncio
    @pytest.mark.performance
    async def test_transaction_latency_p99(self, http_client, test_accounts):
        """Test that p99 latency is under 100ms"""
        
        latencies = []
        
        for i in range(100):
            transaction = {
                "from_account": "3333333333",  # Business account with high limit
                "to_account": "2222222222",
                "amount": 10.00,
                "currency": "USD"
            }
            
            start_time = time.time()
            response = await http_client.post(
                f"{BASE_URL}/api/v1/transactions",
                json=transaction
            )
            end_time = time.time()
            
            if response.status_code == 200:
                latencies.append((end_time - start_time) * 1000)
        
        # Calculate percentiles
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        
        print(f"\nLatency Results:")
        print(f"P50: {p50:.2f}ms")
        print(f"P95: {p95:.2f}ms")
        print(f"P99: {p99:.2f}ms")
        print(f"Min: {latencies[0]:.2f}ms")
        print(f"Max: {latencies[-1]:.2f}ms")
        
        # Assert performance requirement
        assert p99 < 100, f"P99 latency {p99:.2f}ms exceeds 100ms requirement"
    
    @pytest.mark.asyncio
    @pytest.mark.load
    async def test_concurrent_load(self, http_client, test_accounts):
        """Test system under concurrent load"""
        
        async def submit_transaction():
            transaction = {
                "from_account": "3333333333",
                "to_account": "2222222222",
                "amount": 1.00,
                "currency": "USD"
            }
            try:
                response = await http_client.post(
                    f"{BASE_URL}/api/v1/transactions",
                    json=transaction,
                    timeout=5.0
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Request failed: {e}")
                return False
        
        # Submit 100 concurrent requests
        start_time = time.time()
        tasks = [submit_transaction() for _ in range(100)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Calculate metrics
        successful = sum(results)
        duration = end_time - start_time
        throughput = successful / duration
        
        print(f"\nLoad Test Results:")
        print(f"Total Requests: 100")
        print(f"Successful: {successful}")
        print(f"Failed: {100 - successful}")
        print(f"Success Rate: {successful}%")
        print(f"Duration: {duration:.2f}s")
        print(f"Throughput: {throughput:.2f} TPS")
        
        # Assert requirements
        assert successful > 95, f"Success rate {successful}% below 95%"
        assert throughput > 50, f"Throughput {throughput:.2f} TPS below requirement"


class TestSecurity:
    """Security-focused tests"""
    
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self, http_client):
        """Test SQL injection prevention"""
        
        # Try various SQL injection attempts
        injection_attempts = [
            "1111111111'; DROP TABLE accounts; --",
            "1111111111' OR '1'='1",
            "1111111111); DELETE FROM transactions; --",
            "1111111111' UNION SELECT * FROM accounts --"
        ]
        
        for attempt in injection_attempts:
            transaction = {
                "from_account": attempt,
                "to_account": "2222222222",
                "amount": 100.00,
                "currency": "USD"
            }
            
            response = await http_client.post(
                f"{BASE_URL}/api/v1/transactions",
                json=transaction
            )
            
            # Should be rejected by validation
            assert response.status_code == 422, \
                f"SQL injection attempt not blocked: {attempt}"
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, http_client):
        """Test rate limiting is enforced"""
        
        # Send many requests rapidly
        responses = []
        for _ in range(150):  # Assuming limit is ~100/minute
            response = await http_client.get(f"{BASE_URL}/health")
            responses.append(response.status_code)
            
            # Stop if we get rate limited
            if response.status_code == 429:
                break
        
        # Should see rate limiting kick in
        rate_limited = sum(1 for r in responses if r == 429)
        assert rate_limited > 0, "Rate limiting not enforced"
    
    @pytest.mark.asyncio
    async def test_authentication_required(self, http_client):
        """Test endpoints require authentication"""
        
        # Try accessing protected endpoints without auth
        protected_endpoints = [
            "/api/v1/transactions",
            "/api/v1/accounts/1111111111",
            "/api/v1/metrics/summary"
        ]
        
        # Note: This test assumes authentication is implemented
        # Adjust based on actual auth implementation
        for endpoint in protected_endpoints:
            response = await http_client.get(
                f"{BASE_URL}{endpoint}",
                headers={}  # No auth headers
            )
            
            # Should require authentication
            # (May return 401 or 403 depending on implementation)
            assert response.status_code in [401, 403], \
                f"Endpoint {endpoint} accessible without auth"


class TestIntegrationScenarios:
    """Complex integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_daily_limit_enforcement(self, http_client, test_accounts):
        """Test daily transaction limit is enforced"""
        
        # Try to exceed daily limit with multiple transactions
        daily_limit = 5000000.00
        large_amount = 2000000.00  # Under single limit but multiple will exceed daily
        
        transactions_sent = 0
        total_amount = 0
        
        for i in range(5):  # Try 5 x 2M = 10M (exceeds 5M daily limit)
            transaction = {
                "from_account": "3333333333",  # Business account
                "to_account": "1111111111",
                "amount": large_amount,
                "currency": "USD"
            }
            
            response = await http_client.post(
                f"{BASE_URL}/api/v1/transactions",
                json=transaction
            )
            
            if response.status_code == 200:
                transactions_sent += 1
                total_amount += large_amount
            else:
                # Should fail due to daily limit
                assert "daily limit" in response.json()["detail"].lower()
                break
        
        assert total_amount < daily_limit + large_amount, \
            "Daily limit not properly enforced"
    
    @pytest.mark.asyncio
    async def test_business_continuity(self, http_client, test_accounts):
        """Test system continues operating if fraud service is slow"""
        
        # This simulates fraud service being slow
        # The transaction service should timeout and proceed with caution
        
        transaction = {
            "from_account": "1111111111",
            "to_account": "2222222222",
            "amount": 50.00,
            "currency": "USD",
            "metadata": {
                "test": "fraud_service_timeout"
            }
        }
        
        start_time = time.time()
        response = await http_client.post(
            f"{BASE_URL}/api/v1/transactions",
            json=transaction
        )
        end_time = time.time()
        
        # Should complete even if fraud service times out
        assert response.status_code == 200
        
        # Should complete within reasonable time (not wait forever)
        processing_time = (end_time - start_time) * 1000
        assert processing_time < 1000, "Transaction took too long with fraud timeout"


if __name__ == "__main__":
    # Run tests with detailed output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-k", "not load",  # Skip load tests by default
        "--asyncio-mode=auto",
        "--color=yes"
    ])
