# 🎯 Ultimate Cheat Sheet

## ⏱️ Time Breakdown (4 hours = 240 minutes)

```
[0-15 min]    Setup & Planning (DON'T SKIP!)
[15-45 min]   Transaction Service (Core)
[45-75 min]   Fraud Service + AI
[75-105 min]  Analytics + Dashboard
[105-135 min] Integration + Testing
[135-165 min] Performance + Deploy
[165-180 min] Demo Prep
```

## 🚀 Copy-Paste Starters

### Transaction Service Quick Start
```python
# src/transaction-service/main.py
from fastapi import FastAPI, HTTPException, Depends
from decimal import Decimal
import asyncio
import httpx

app = FastAPI()

# BUSINESS RULES FROM COBOL
MIN_AMOUNT = Decimal("0.01")
MAX_AMOUNT = Decimal("1000000.00")
DAILY_LIMIT = Decimal("5000000.00")

FEES = {
    "DM": Decimal("2.50"),   # Domestic
    "IN": Decimal("25.00"),  # International
    "WT": Decimal("35.00")   # Wire
}

@app.post("/api/v1/transactions")
async def process_transaction(transaction: dict):
    # Step 1: Validate amount
    if transaction["amount"] < MIN_AMOUNT or transaction["amount"] > MAX_AMOUNT:
        raise HTTPException(422, "Invalid amount")
    
    # Step 2: Check accounts different
    if transaction["from_account"] == transaction["to_account"]:
        raise HTTPException(422, "Same account transfer not allowed")
    
    # Step 3: Call fraud service (with timeout!)
    try:
        async with httpx.AsyncClient() as client:
            fraud_response = await client.post(
                "http://fraud-service:8002/api/v1/analyze",
                json=transaction,
                timeout=0.5  # 500ms max
            )
            fraud_result = fraud_response.json()
            
            if fraud_result["risk_score"] > 80:
                raise HTTPException(403, "Transaction blocked: High fraud risk")
    except httpx.TimeoutError:
        # Continue with medium risk if fraud service slow
        fraud_result = {"risk_score": 50}
    
    # Step 4: Process transaction
    # TODO: Add database operations
    
    return {
        "transaction_id": f"TXN{int(asyncio.get_event_loop().time())}",
        "status": "completed",
        "risk_score": fraud_result.get("risk_score", 0)
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Fraud Service with AI
```python
# src/fraud-service/main.py
from fastapi import FastAPI
from openai import AzureOpenAI
import os
import json

app = FastAPI()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01"
)

@app.post("/api/v1/analyze")
async def analyze_fraud(transaction: dict):
    # Quick rule checks first
    risk_score = 0
    
    # Rule 1: High amount
    if transaction["amount"] > 50000:
        risk_score += 25
    
    # Rule 2: International
    if transaction.get("transaction_type") == "IN":
        risk_score += 15
    
    # Rule 3: Use AI for pattern analysis
    prompt = f"""
    Analyze this transaction for fraud risk:
    Amount: ${transaction['amount']}
    Type: {transaction.get('transaction_type', 'DM')}
    
    Return JSON with risk_score (0-100) and reason.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        ai_result = json.loads(response.choices[0].message.content)
        risk_score += ai_result.get("risk_score", 0)
    except:
        # AI failed, use rules only
        pass
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_level": "high" if risk_score > 60 else "medium" if risk_score > 30 else "low",
        "recommendation": "block" if risk_score > 80 else "review" if risk_score > 60 else "allow"
    }
```

### Docker Compose Essential Services
```yaml
# docker-compose.yml
version: '3.9'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: transactions
      POSTGRES_USER: challenge
      POSTGRES_PASSWORD: challenge123
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U challenge"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  transaction-service:
    build: ./src/transaction-service
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql://challenge:challenge123@postgres:5432/transactions
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

## 🔥 Performance Hacks

### 1. Connection Pool (MUST HAVE!)
```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Important!
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### 2. Redis Caching (Quick Win)
```python
import redis.asyncio as redis
import json

redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)

async def get_cached_account(account_id: str):
    # Check cache first
    cached = await redis_client.get(f"acc:{account_id}")
    if cached:
        return json.loads(cached)
    
    # Get from DB
    account = await db.get_account(account_id)
    
    # Cache for 60 seconds
    await redis_client.setex(
        f"acc:{account_id}", 
        60, 
        json.dumps(account)
    )
    return account
```

### 3. Async Everything
```python
# GOOD - Parallel execution
async def process_transaction(txn):
    # Run in parallel
    fraud_task = asyncio.create_task(check_fraud(txn))
    balance_task = asyncio.create_task(get_balance(txn["from_account"]))
    
    fraud_result, balance = await asyncio.gather(fraud_task, balance_task)
    return process_with_results(fraud_result, balance)
```

## 🧪 Test Commands (Copy & Run)

### Health Check All Services
```bash
for port in 8001 8002 8003; do
  echo "Service on port $port:"
  curl -s http://localhost:$port/health | jq
done
```

### Submit Test Transaction
```bash
curl -X POST http://localhost:8001/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "1111111111",
    "to_account": "2222222222",
    "amount": 100.00,
    "currency": "USD",
    "transaction_type": "DM"
  }' | jq
```

### Quick Performance Test
```bash
# Install hey if needed: go install github.com/rakyll/hey@latest
hey -n 1000 -c 50 -m POST \
  -H "Content-Type: application/json" \
  -d '{"from_account":"1111111111","to_account":"2222222222","amount":10}' \
  http://localhost:8001/api/v1/transactions
```

## 🐛 Common Fixes

### "Connection refused"
```bash
# Check service is running
docker-compose ps
# Restart specific service
docker-compose restart transaction-service
```

### "Import error"
```bash
# Fix Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
# Or in code:
import sys
sys.path.append('/app/src')
```

### "Timeout error"
```python
# Add timeout to all external calls
timeout = httpx.Timeout(5.0, connect=2.0)
async with httpx.AsyncClient(timeout=timeout) as client:
    response = await client.post(...)
```

### Database locked
```sql
-- Kill all connections
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'transactions' AND pid <> pg_backend_pid();
```

## 📊 Dashboard Quick Start

### React WebSocket Component
```jsx
// src/dashboard/App.js
import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [metrics, setMetrics] = useState({
    totalTransactions: 0,
    fraudBlocked: 0,
    avgResponseTime: 0
  });

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8003/ws/metrics');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data.metrics);
    };
    
    return () => ws.close();
  }, []);

  return (
    <div>
      <h1>Transaction Dashboard</h1>
      <div>Total: {metrics.totalTransactions}</div>
      <div>Blocked: {metrics.fraudBlocked}</div>
      <div>Avg Time: {metrics.avgResponseTime}ms</div>
    </div>
  );
}
```

## 🚀 Kubernetes Quick Deploy

### Minimal Deployment
```yaml
# k8s/quick-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transaction-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: transaction-service
  template:
    metadata:
      labels:
        app: transaction-service
    spec:
      containers:
      - name: app
        image: transaction-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          value: "postgresql://challenge:challenge123@postgres:5432/transactions"
---
apiVersion: v1
kind: Service
metadata:
  name: transaction-service
spec:
  selector:
    app: transaction-service
  ports:
  - port: 80
    targetPort: 8001
```

## 🎬 Demo Script (Last 15 min)

```bash
# 1. Show services running
docker-compose ps

# 2. Submit successful transaction
./demo/valid-transaction.sh

# 3. Show fraud blocking
./demo/fraud-transaction.sh

# 4. Open dashboard
open http://localhost:3000

# 5. Show performance
cat performance-results.json | jq '.summary'

# 6. Talk about AI integration
grep -r "openai" src/ | head -5
```

## ⚡ Last Minute Checklist

- [ ] All 3 services have `/health` endpoint
- [ ] Transaction service validates business rules
- [ ] Fraud service returns risk_score
- [ ] At least basic error handling (try/except)
- [ ] Docker compose works: `docker-compose up`
- [ ] One working test: `pytest tests/test_health.py`
- [ ] README has setup instructions
- [ ] Can demo 1 successful transaction

---

**Remember**: Working > Perfect! Focus on core requirements first! 🚀
