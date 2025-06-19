# 🚨 Module 22: Error Recovery Playbook

## When Things Go Wrong (And They Will!)

### 🔴 CRITICAL: Service Won't Start

#### PostgreSQL Connection Error
```bash
# Error: "FATAL: password authentication failed"
# Fix:
docker-compose down -v
docker-compose up -d postgres
sleep 5

# Create database manually
docker exec -it challenge_postgres_1 psql -U postgres -c "
CREATE USER challenge WITH PASSWORD 'challenge123';
CREATE DATABASE transactions OWNER challenge;
GRANT ALL PRIVILEGES ON DATABASE transactions TO challenge;
"
```

#### Redis Connection Refused
```bash
# Quick fix
docker-compose stop redis
docker-compose rm -f redis
docker-compose up -d redis

# Test connection
docker exec -it challenge_redis_1 redis-cli ping
# Should return: PONG
```

#### Port Already in Use
```bash
# Find and kill process
sudo lsof -ti:8001 | xargs kill -9
sudo lsof -ti:8002 | xargs kill -9
sudo lsof -ti:8003 | xargs kill -9

# Or change ports in docker-compose.yml
# 8001 -> 9001, 8002 -> 9002, etc.
```

### 🟡 MEDIUM: API Errors

#### 500 Internal Server Error
```python
# Add this to EVERY endpoint for debugging:
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    print(f"ERROR: {exc}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )
```

#### Timeout Errors
```python
# Fix 1: Add timeouts everywhere
async def call_service_with_timeout(url: str, data: dict, timeout: float = 1.0):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=timeout)
            return response.json()
    except httpx.TimeoutError:
        # Return default response
        return {"status": "timeout", "risk_score": 50}
```

#### JSON Decode Errors
```python
# Safe JSON parsing
def safe_json_parse(text: str, default=None):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {text[:100]}")
        return default or {}
```

### 🟢 QUICK: Performance Issues

#### Slow Database Queries
```python
# Emergency performance mode
class QuickCache:
    def __init__(self):
        self.cache = {}
    
    async def get_account(self, account_id: str):
        if account_id in self.cache:
            return self.cache[account_id]
        
        # Simplified account (skip DB)
        account = {
            "account_number": account_id,
            "balance": 10000.00,
            "account_type": "C"
        }
        self.cache[account_id] = account
        return account

# Use in emergency
cache = QuickCache()
```

#### High Latency
```python
# Disable non-critical features
ENABLE_FRAUD_CHECK = False  # Temporarily disable
ENABLE_ANALYTICS = False
ENABLE_DETAILED_LOGGING = False

@app.post("/api/v1/transactions")
async def process_transaction(transaction: dict):
    # Skip fraud check if disabled
    if not ENABLE_FRAUD_CHECK:
        fraud_score = 0
    else:
        fraud_score = await check_fraud(transaction)
    
    # Process quickly
    return {
        "transaction_id": str(uuid.uuid4()),
        "status": "completed",
        "risk_score": fraud_score
    }
```

## 🔧 Fix-It Scripts

### `scripts/emergency-fix.py`
```python
#!/usr/bin/env python3
"""Emergency fixes for common issues"""

import subprocess
import time
import sys

def fix_docker():
    """Reset Docker completely"""
    print("🔧 Fixing Docker...")
    commands = [
        "docker-compose down -v",
        "docker system prune -f",
        "docker-compose up -d postgres redis",
        "sleep 5",
        "docker-compose up -d"
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)
        time.sleep(2)

def fix_database():
    """Reset database with test data"""
    print("🔧 Fixing Database...")
    subprocess.run("""
    docker exec -it challenge_postgres_1 psql -U challenge -d transactions -c "
    DROP TABLE IF EXISTS accounts CASCADE;
    DROP TABLE IF EXISTS transactions CASCADE;
    
    CREATE TABLE accounts (
        account_number VARCHAR(10) PRIMARY KEY,
        balance DECIMAL(15,2) DEFAULT 10000.00,
        account_type CHAR(1) DEFAULT 'C'
    );
    
    INSERT INTO accounts VALUES 
        ('1111111111', 10000.00, 'C'),
        ('2222222222', 50000.00, 'S'),
        ('3333333333', 100000.00, 'B'),
        ('9999999999', 100.00, 'C');
    "
    """, shell=True)

def fix_python():
    """Fix Python environment"""
    print("🔧 Fixing Python...")
    commands = [
        "pip install --upgrade pip",
        "pip install -r requirements.txt --force-reinstall",
        "export PYTHONPATH=$PWD/src:$PYTHONPATH"
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "docker":
            fix_docker()
        elif sys.argv[1] == "database":
            fix_database()
        elif sys.argv[1] == "python":
            fix_python()
        else:
            print("Usage: emergency-fix.py [docker|database|python]")
    else:
        # Fix everything
        fix_docker()
        fix_database()
        fix_python()
        print("✅ All fixes applied!")
```

## 📝 Minimal Working Solution

If running out of time, here's the ABSOLUTE MINIMUM that passes:

### `minimal-solution.py`
```python
from fastapi import FastAPI, HTTPException
from datetime import datetime
import uuid

app = FastAPI()

# In-memory storage (no database needed!)
accounts = {
    "1111111111": {"balance": 10000.00, "type": "C"},
    "2222222222": {"balance": 50000.00, "type": "S"},
    "3333333333": {"balance": 100000.00, "type": "B"},
}

transactions = []

@app.post("/api/v1/transactions")
async def process_transaction(transaction: dict):
    # Basic validation
    if transaction["amount"] <= 0 or transaction["amount"] > 1000000:
        raise HTTPException(422, "Invalid amount")
    
    if transaction["from_account"] == transaction["to_account"]:
        raise HTTPException(422, "Same account transfer")
    
    # Check balance (simplified)
    from_account = accounts.get(transaction["from_account"])
    if not from_account or from_account["balance"] < transaction["amount"]:
        raise HTTPException(400, "Insufficient funds")
    
    # Process transaction
    from_account["balance"] -= transaction["amount"]
    to_account = accounts.get(transaction["to_account"], {"balance": 0})
    to_account["balance"] += transaction["amount"]
    
    # Record transaction
    txn = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        **transaction,
        "status": "completed"
    }
    transactions.append(txn)
    
    return {
        "transaction_id": txn["transaction_id"],
        "status": "completed",
        "message": "Transaction processed"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "transaction-service"}

@app.get("/api/v1/accounts/{account_id}")
async def get_account(account_id: str):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(404, "Account not found")
    return {
        "account_number": account_id,
        "balance": account["balance"],
        "account_type": account["type"]
    }

# Minimal fraud service
@app.post("/api/v1/analyze")
async def analyze_fraud(transaction: dict):
    # Super simple fraud detection
    risk_score = 0
    if transaction["amount"] > 50000:
        risk_score = 70
    elif transaction["amount"] > 10000:
        risk_score = 40
    else:
        risk_score = 10
    
    return {
        "risk_score": risk_score,
        "risk_level": "high" if risk_score > 60 else "low",
        "recommendation": "block" if risk_score > 80 else "allow"
    }

if __name__ == "__main__":
    import uvicorn
    # Run on different ports for different services
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## 🎯 Priority Fixes (When Time is Running Out)

### Last 30 Minutes Strategy
1. **STOP adding features**
2. **Get ONE transaction working end-to-end**
3. **Make sure health endpoints work**
4. **Write basic README**
5. **Commit everything**

### Bare Minimum Checklist
```bash
# These MUST work:
curl http://localhost:8001/health
curl http://localhost:8002/health

# This MUST process successfully:
curl -X POST http://localhost:8001/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{"from_account":"1111111111","to_account":"2222222222","amount":100}'
```

### Emergency README.md
```markdown
# Super Challenge Solution

## Quick Start
```bash
docker-compose up -d
python src/transaction-service/main.py
```

## API Endpoints
- POST /api/v1/transactions - Process transaction
- GET /health - Health check

## Architecture
- Transaction Service (port 8001) - Handles transactions
- Fraud Service (port 8002) - Basic fraud detection
- PostgreSQL - Data storage
- Redis - Caching

## Business Rules Implemented
- Min amount: $0.01
- Max amount: $1,000,000
- No same-account transfers
- Balance validation
```

## 🆘 Last Resort Commands

```bash
# Nuclear option - reset EVERYTHING
rm -rf ./* && \
git clone https://github.com/workshop/module-22-super-challenge.git . && \
./scripts/setup-challenge-env.sh && \
docker-compose up -d

# Save work before reset
tar -czf my-work-backup.tar.gz src/ tests/ *.md

# Get minimal services running
pkill -f python
docker-compose up -d postgres redis
cd src/transaction-service && python main.py &
cd src/fraud-service && python main.py &

# Test minimal functionality
sleep 5
curl http://localhost:8001/health
curl http://localhost:8002/health
```

---

**Remember**: A partially working solution that runs is worth more than a perfect solution that doesn't! 🚀

**Emergency Help**: challenge-911@workshop.com (5-minute response time)