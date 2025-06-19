# Module 22: Super Challenge - Troubleshooting Guide

## 🚨 Common Issues and Solutions

This guide helps you quickly resolve common problems during the challenge.

## 🐳 Docker Issues

### Problem: Docker services won't start
```bash
# Error: "Cannot connect to the Docker daemon"
```

**Solution:**
```bash
# 1. Check Docker is running
docker --version
systemctl status docker  # Linux
open -a Docker  # macOS

# 2. Reset Docker
docker system prune -af
docker-compose down -v
docker-compose up -d

# 3. Check port conflicts
sudo lsof -i :5432  # PostgreSQL
sudo lsof -i :6379  # Redis
sudo lsof -i :8001  # Transaction service
```

### Problem: "No space left on device"
```bash
# Error during image build or container start
```

**Solution:**
```bash
# 1. Clean up Docker
docker system prune -af --volumes
docker builder prune -af

# 2. Check disk space
df -h

# 3. Remove old images
docker images | grep "none" | awk '{print $3}' | xargs docker rmi
```

### Problem: Container keeps restarting
```bash
# Container status shows "Restarting"
```

**Solution:**
```bash
# 1. Check logs
docker-compose logs -f [service-name]

# 2. Common fixes:
# - Check environment variables in .env
# - Verify database connection strings
# - Ensure dependencies are running first

# 3. Debug mode
docker-compose run --rm [service-name] /bin/sh
```

## 🐍 Python/FastAPI Issues

### Problem: ModuleNotFoundError
```python
# Error: ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# 1. Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Reinstall dependencies
pip install -r requirements.txt

# 3. Check Python path
python -c "import sys; print(sys.path)"

# 4. For shared module imports
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

### Problem: FastAPI not responding
```python
# Service starts but endpoints return 404
```

**Solution:**
```python
# 1. Check route definitions
# Ensure you have the correct path
@app.post("/api/v1/transactions")  # Not just "/transactions"

# 2. Check app initialization
app = FastAPI()  # At module level

# 3. Verify Uvicorn binding
uvicorn.run(app, host="0.0.0.0", port=8001)  # Not localhost
```

### Problem: Async function errors
```python
# Error: "coroutine was never awaited"
```

**Solution:**
```python
# 1. Use await for async functions
result = await async_function()  # Not: result = async_function()

# 2. Make endpoints async
@app.post("/api/v1/transactions")
async def process_transaction():  # async def, not def
    pass

# 3. Use async context managers
async with httpx.AsyncClient() as client:
    response = await client.post(...)
```

## 🗄️ Database Issues

### Problem: PostgreSQL connection refused
```bash
# Error: "could not connect to server: Connection refused"
```

**Solution:**
```bash
# 1. Check PostgreSQL is running
docker-compose ps | grep postgres
docker-compose logs postgres

# 2. Verify connection string
# Should be: postgresql://challenge:challenge123@localhost:5432/transactions

# 3. Test connection
docker exec -it [postgres-container] psql -U challenge -d transactions

# 4. Reset database
docker-compose down -v postgres
docker-compose up -d postgres
```

### Problem: Redis connection errors
```bash
# Error: "Error 111 connecting to localhost:6379. Connection refused."
```

**Solution:**
```bash
# 1. Check Redis is running
docker-compose ps | grep redis
redis-cli ping  # Should return PONG

# 2. For async Redis in Python
import redis.asyncio as redis
# Not: import redis

# 3. Connection pool
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    decode_responses=True
)
```

## 🤖 AI/Azure OpenAI Issues

### Problem: Azure OpenAI authentication failed
```python
# Error: "Access denied due to invalid subscription key"
```

**Solution:**
```bash
# 1. Check environment variables
echo $AZURE_OPENAI_ENDPOINT
echo $AZURE_OPENAI_KEY

# 2. Verify .env file
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-32-char-key

# 3. Test with curl
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/deployments/gpt-4/completions?api-version=2024-02-01" \
  -H "api-key: $AZURE_OPENAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "max_tokens": 5}'
```

### Problem: Timeout calling fraud service
```python
# Fraud detection takes too long
```

**Solution:**
```python
# 1. Add timeout to fraud check
try:
    fraud_result = await asyncio.wait_for(
        check_fraud_async(transaction),
        timeout=0.5  # 500ms max
    )
except asyncio.TimeoutError:
    # Default to medium risk
    fraud_result = FraudCheckResponse(
        risk_score=50,
        risk_level="medium",
        recommendation="review"
    )

# 2. Use concurrent execution
fraud_task = asyncio.create_task(check_fraud_async(transaction))
other_task = asyncio.create_task(other_operation())
fraud_result, other_result = await asyncio.gather(fraud_task, other_task)
```

## 🌐 API/Network Issues

### Problem: CORS errors in browser
```javascript
// Error: "Access to fetch at 'http://localhost:8001' from origin 'http://localhost:3000' has been blocked by CORS policy"
```

**Solution:**
```python
# In FastAPI services, add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problem: WebSocket connection fails
```javascript
// Error: "WebSocket connection to 'ws://localhost:8003/ws/metrics' failed"
```

**Solution:**
```python
# 1. Ensure WebSocket endpoint is correct
@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # ...

# 2. Check CORS for WebSocket
# WebSocket doesn't use CORS, but check origin if validating

# 3. Test with wscat
npm install -g wscat
wscat -c ws://localhost:8003/ws/metrics
```

## 🧪 Testing Issues

### Problem: Tests hang or timeout
```bash
# pytest seems stuck
```

**Solution:**
```bash
# 1. Run with timeout
pytest --timeout=10 tests/

# 2. Skip slow tests during development
pytest -m "not slow"

# 3. Run specific test
pytest tests/test_transactions.py::test_valid_transaction -v

# 4. Debug mode
pytest --pdb tests/test_failing.py
```

### Problem: Integration tests fail with connection errors
```python
# Cannot connect to services during tests
```

**Solution:**
```python
# 1. Use proper async fixtures
@pytest.fixture
async def http_client():
    async with httpx.AsyncClient() as client:
        yield client

# 2. Mark async tests
@pytest.mark.asyncio
async def test_something(http_client):
    response = await http_client.get("/health")

# 3. Ensure services are running
# Run: docker-compose up -d
# Before: pytest tests/integration/
```

## ⚡ Performance Issues

### Problem: High latency (> 100ms)
```bash
# P99 latency exceeds requirement
```

**Solution:**
```python
# 1. Use connection pooling
# PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
)

# Redis
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50
)

# 2. Implement caching
@app.post("/api/v1/transactions")
async def process_transaction(transaction: TransactionRequest):
    # Check cache first
    cache_key = f"txn:{transaction.idempotency_key}"
    cached = await redis.get(cache_key)
    if cached:
        return TransactionResponse.parse_raw(cached)

# 3. Use async everywhere
# Bad: requests.post()
# Good: await httpx_client.post()
```

### Problem: Memory leaks
```bash
# Container memory usage keeps growing
```

**Solution:**
```python
# 1. Close connections properly
async with httpx.AsyncClient() as client:
    # Client is automatically closed
    pass

# 2. Limit cache size
from cachetools import TTLCache
cache = TTLCache(maxsize=1000, ttl=300)

# 3. Monitor memory
import tracemalloc
tracemalloc.start()
# ... code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6}MB")
```

## 🚀 Deployment Issues

### Problem: Kubernetes pods crash
```bash
# Pods in CrashLoopBackOff state
```

**Solution:**
```bash
# 1. Check pod logs
kubectl logs -f pod-name -n super-challenge
kubectl describe pod pod-name -n super-challenge

# 2. Common fixes:
# - Increase memory/CPU limits
# - Fix liveness/readiness probes
# - Check environment variables
# - Verify image exists

# 3. Debug with shell
kubectl run debug --image=ubuntu:22.04 --rm -it -- /bin/bash
```

### Problem: Terraform errors
```bash
# Error: "Error creating Resource Group"
```

**Solution:**
```bash
# 1. Check Azure login
az account show
az account set --subscription "correct-subscription"

# 2. Initialize Terraform
cd infrastructure/terraform
terraform init -upgrade

# 3. Validate configuration
terraform validate

# 4. Plan with minimal resources
terraform plan -target=azurerm_resource_group.main
```

## 💡 Quick Fixes Cheat Sheet

```bash
# Reset everything
docker-compose down -v && docker-compose up -d

# Restart specific service
docker-compose restart transaction-service

# View all logs
docker-compose logs -f

# Check service health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health

# Reset database
docker exec -it [postgres-container] psql -U challenge -c "DROP DATABASE transactions; CREATE DATABASE transactions;"

# Clear Redis
docker exec -it [redis-container] redis-cli FLUSHALL

# Python dependency issues
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Port already in use
sudo lsof -ti:8001 | xargs kill -9

# Git issues
git add .
git commit -m "WIP: Challenge progress"
git stash  # Save work temporarily
```

## 🆘 When All Else Fails

1. **Take a breath** - Debugging under pressure is hard
2. **Check the logs** - The answer is usually there
3. **Simplify** - Comment out complex parts, get basics working
4. **Use hints** - `python scripts/get_hint.py --task X`
5. **Ask for help** - challenge-911@workshop.com

Remember: A partial working solution is better than a perfect non-working one!

---

**Pro tip**: Keep this guide open in a browser tab during the challenge for quick reference.