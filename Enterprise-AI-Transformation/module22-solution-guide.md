# Module 22: Solution Architecture Guide

## 🏗️ Recommended Architecture Pattern

This guide provides a recommended architecture without complete implementation details, helping you structure your solution effectively.

## 📐 High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│   Transaction   │────▶│     Fraud       │
│  (Rate Limit)   │     │    Service      │     │   Detection     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   PostgreSQL    │     │  Azure OpenAI   │
                        │    + Redis      │     │   GPT-4 API     │
                        └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   Event Hub     │
                        │  (Streaming)    │
                        └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   Analytics     │────▶│   Dashboard     │
                        │    Service      │     │   (React/WS)    │
                        └─────────────────┘     └─────────────────┘
```

## 🔧 Service Responsibilities

### 1. Transaction Service (Port 8001)
**Primary Responsibilities:**
- Transaction validation
- Business rule enforcement
- Account balance management
- Fee calculation
- Event publishing

**Key Components:**
```python
# Suggested structure
src/transaction-service/
├── main.py              # FastAPI app
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── validators.py        # Business rule validators
├── repositories.py      # Database operations
├── services.py          # Business logic
├── events.py           # Event publishing
└── dependencies.py     # Dependency injection
```

**Critical Functions:**
```python
# validators.py
async def validate_transaction(transaction: TransactionRequest) -> ValidationResult:
    # Check amount limits
    # Verify account format
    # Ensure different accounts
    # Check daily limits
    pass

# services.py
async def process_transaction(transaction: TransactionRequest) -> TransactionResponse:
    # 1. Validate
    # 2. Check fraud
    # 3. Lock accounts
    # 4. Verify balance
    # 5. Execute atomically
    # 6. Publish event
    pass
```

### 2. Fraud Detection Service (Port 8002)
**Primary Responsibilities:**
- Multi-layer fraud analysis
- AI-powered risk assessment
- Pattern recognition
- Real-time scoring

**Key Components:**
```python
src/fraud-service/
├── main.py              # FastAPI app
├── detectors/
│   ├── rule_engine.py   # Traditional rules
│   ├── ml_detector.py   # ML models
│   └── ai_analyzer.py   # Azure OpenAI
├── models.py            # Fraud models
├── prompts.py          # AI prompts
└── risk_calculator.py  # Score aggregation
```

**AI Integration Pattern:**
```python
# ai_analyzer.py
class AIFraudAnalyzer:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01"
        )
    
    async def analyze(self, context: TransactionContext) -> FraudAnalysis:
        # Build comprehensive prompt
        # Include transaction details
        # Add historical context
        # Request structured output
        pass
```

### 3. Analytics Service (Port 8003)
**Primary Responsibilities:**
- Event stream processing
- Real-time aggregations
- WebSocket broadcasting
- Metrics calculation

**Key Components:**
```python
src/analytics-service/
├── main.py              # FastAPI + WebSocket
├── stream_processor.py  # Event Hub consumer
├── aggregators.py       # Metric calculations
├── websocket_manager.py # Client connections
└── storage.py          # Cosmos DB interface
```

**WebSocket Pattern:**
```python
# websocket_manager.py
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.metric_cache = {}
    
    async def broadcast_metrics(self):
        while True:
            metrics = await self.calculate_current_metrics()
            await self.send_to_all(json.dumps(metrics))
            await asyncio.sleep(1)  # Update every second
```

## 💾 Data Models

### Transaction Model
```python
class Transaction(BaseModel):
    transaction_id: str
    from_account: str
    to_account: str
    amount: Decimal
    currency: str = "USD"
    transaction_type: TransactionType
    status: TransactionStatus
    risk_score: Optional[int]
    fees: Decimal
    created_at: datetime
    completed_at: Optional[datetime]
```

### Account Model
```python
class Account(BaseModel):
    account_number: str
    account_type: AccountType
    balance: Decimal
    available_balance: Decimal
    daily_limit: Decimal = Decimal("5000000.00")
    daily_used: Decimal = Decimal("0.00")
    is_vip: bool = False
    overdraft_limit: Decimal = Decimal("0.00")
    last_transaction: Optional[datetime]
    transaction_count: int = 0
```

### Fraud Analysis Model
```python
class FraudAnalysis(BaseModel):
    transaction_id: str
    risk_score: int  # 0-100
    risk_level: RiskLevel  # low/medium/high/critical
    risk_factors: List[str]
    ai_explanation: str
    recommendation: str  # allow/review/block
    confidence: float  # 0.0-1.0
    analysis_time_ms: float
```

## 🔄 Event Flow

### Transaction Event Flow
```
1. Client → POST /api/v1/transactions
2. Transaction Service validates request
3. Transaction Service → Fraud Service (async)
4. Fraud Service → Azure OpenAI
5. If approved:
   - Lock accounts (Redis)
   - Update balances (PostgreSQL)
   - Publish event (Event Hub)
6. Analytics Service consumes event
7. Dashboard updates via WebSocket
```

### Event Schema
```json
{
  "event_id": "evt_1234567890",
  "event_type": "transaction.completed",
  "timestamp": "2024-01-20T10:30:00Z",
  "data": {
    "transaction_id": "TXN1234567890",
    "from_account": "1111111111",
    "to_account": "2222222222",
    "amount": 100.00,
    "currency": "USD",
    "risk_score": 15,
    "processing_time_ms": 45
  }
}
```

## 🚀 Performance Optimization Strategies

### 1. Caching Strategy
```python
# Use Redis for:
- Idempotency keys (5 min TTL)
- Account balances (1 min TTL)
- Fraud scores (10 min TTL)
- Rate limiting counters

# Implementation
async def get_account_cached(account_id: str) -> Account:
    # Check Redis first
    cached = await redis.get(f"account:{account_id}")
    if cached:
        return Account.parse_raw(cached)
    
    # Fetch from DB
    account = await db.get_account(account_id)
    
    # Cache for 1 minute
    await redis.setex(f"account:{account_id}", 60, account.json())
    return account
```

### 2. Connection Pooling
```python
# PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Redis
redis_pool = ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True
)
```

### 3. Async Processing
```python
# Process fraud check in parallel
async def process_with_fraud_check(transaction):
    # Start fraud check asynchronously
    fraud_task = asyncio.create_task(
        check_fraud_with_timeout(transaction)
    )
    
    # Do other validations in parallel
    validation_task = asyncio.create_task(
        validate_business_rules(transaction)
    )
    
    # Wait for both
    fraud_result, validation_result = await asyncio.gather(
        fraud_task, validation_task
    )
```

## 🔐 Security Considerations

### API Security
```python
# Rate limiting per IP
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/transactions")
@limiter.limit("100/minute")
async def process_transaction(request: Request):
    pass
```

### Input Validation
```python
# Strict validation with Pydantic
class TransactionRequest(BaseModel):
    from_account: str = Field(..., regex="^[0-9]{10}$")
    to_account: str = Field(..., regex="^[0-9]{10}$")
    amount: Decimal = Field(..., gt=0, le=1000000)
    
    @validator('from_account')
    def validate_different_accounts(cls, v, values):
        if 'to_account' in values and v == values['to_account']:
            raise ValueError('Cannot transfer to same account')
        return v
```

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/unit/test_validators.py
async def test_transaction_validation():
    # Test valid transaction
    # Test amount limits
    # Test account format
    # Test business rules
    pass
```

### Integration Tests
```python
# tests/integration/test_transaction_flow.py
async def test_end_to_end_transaction():
    # Create test accounts
    # Submit transaction
    # Verify balances updated
    # Check events published
    pass
```

### Performance Tests
```python
# tests/performance/test_latency.py
async def test_transaction_latency():
    # Submit 100 transactions
    # Measure latencies
    # Assert p99 < 100ms
    pass
```

## 📈 Monitoring & Observability

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "transaction-service",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    # Check database connection
    # Check Redis connection
    # Check external service availability
    pass
```

### Metrics Collection
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

transaction_counter = Counter(
    'transactions_total',
    'Total transactions processed',
    ['status', 'type']
)

transaction_duration = Histogram(
    'transaction_duration_seconds',
    'Transaction processing duration'
)
```

## 🎯 Success Criteria

Your implementation should:
1. ✅ Process valid transactions in < 100ms
2. ✅ Block fraudulent transactions accurately
3. ✅ Update account balances atomically
4. ✅ Stream real-time analytics
5. ✅ Handle 100+ concurrent requests
6. ✅ Maintain data consistency
7. ✅ Provide comprehensive error handling
8. ✅ Include meaningful logging
9. ✅ Pass all integration tests
10. ✅ Deploy successfully to Kubernetes

---

**Remember**: This is a guide, not a complete solution. Use it to structure your thinking, but implement your own creative solutions!