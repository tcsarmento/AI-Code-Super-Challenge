# Super Challenge - AI-Powered Enterprise Transformation

## 🏆 The Ultimate Workshop Challenge

**Duration:** 3 hours  
**Difficulty:** Expert  
**Type:** Comprehensive hands-on challenge  

## 📋 Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Business Scenario](#business-scenario)
3. [Technical Requirements](#technical-requirements)
4. [Architecture Design](#architecture-design)
5. [Implementation Guide](#implementation-guide)
6. [Evaluation Criteria](#evaluation-criteria)
7. [Resources and Support](#resources-and-support)

## 🎯 Challenge Overview

### Mission Statement

You are the lead architect at **TechCorp Global**, tasked with modernizing **LegacyFinance Inc.**'s 40-year-old COBOL-based transaction processing system. This $500M transformation project requires you to demonstrate mastery of AI-powered development, cloud architecture, and modern engineering practices.

### What Makes This Challenge Unique

1. **Real-World Complexity**: Based on actual enterprise transformation scenarios
2. **Time Pressure**: 3-hour limit simulates real project constraints
3. **Comprehensive Scope**: Integrates all workshop learnings
4. **AI-First Approach**: Leverages GitHub Copilot and Azure OpenAI throughout
5. **Production Standards**: Requires enterprise-grade quality

### Success Metrics

- **Performance**: Transaction processing < 100ms (p99)
- **Scale**: Support 10,000+ concurrent users
- **Reliability**: 99.99% uptime design
- **Security**: Zero critical vulnerabilities
- **AI Integration**: 95%+ fraud detection accuracy

## 🏢 Business Scenario

### Company Background

**LegacyFinance Inc.** processes $2 billion in daily transactions across 50 million accounts. Their current system:
- Runs on IBM mainframes from the 1980s
- Processes 100,000 transactions per hour
- Costs $50M annually to maintain
- Requires 200+ COBOL developers
- Has 15-minute batch processing delays

### Transformation Goals

1. **Modernize Technology Stack**
   - Migrate from COBOL to cloud-native microservices
   - Implement real-time processing
   - Enable AI-powered fraud detection

2. **Reduce Operational Costs**
   - 60% reduction in infrastructure costs
   - 80% reduction in maintenance effort
   - Automated scaling and management

3. **Improve Business Metrics**
   - Real-time fraud detection (< 500ms)
   - 99.99% transaction accuracy
   - 10x improvement in processing speed

4. **Enable Innovation**
   - API-first architecture
   - Mobile and web interfaces
   - Advanced analytics capabilities

## 🛠️ Technical Requirements

### Core Functional Requirements

#### 1. Transaction Processing Service
- **Endpoints Required**:
  - `POST /api/v1/transactions` - Process new transaction
  - `GET /api/v1/transactions/{id}` - Get transaction status
  - `GET /api/v1/accounts/{id}` - Get account details
  - `POST /api/v1/accounts/{id}/balance` - Update balance

- **Business Rules** (from COBOL):
  ```
  - Minimum transaction: $0.01
  - Maximum single transaction: $1,000,000
  - Daily limit per account: $5,000,000
  - Business accounts allow overdraft up to $100,000
  - VIP customers have no transaction fees
  ```

- **Performance Requirements**:
  - Response time: < 100ms (p99)
  - Throughput: 10,000 TPS
  - Concurrent connections: 50,000+

#### 2. AI-Powered Fraud Detection
- **Detection Layers**:
  1. Rule-based checks (from COBOL logic)
  2. ML pattern recognition
  3. AI behavior analysis
  4. Real-time risk scoring

- **AI Requirements**:
  - Use Azure OpenAI for pattern analysis
  - Implement explainable AI decisions
  - Self-learning from confirmed fraud cases
  - Real-time scoring < 50ms

- **Risk Scoring Algorithm**:
  ```python
  # Base risk calculation
  risk_score = 0
  
  # Factor 1: Transaction amount anomaly
  if amount > account.avg_transaction * 3:
      risk_score += 25
      
  # Factor 2: Velocity check
  if transactions_last_hour > 10:
      risk_score += 30
      
  # Factor 3: Geographic anomaly
  if new_country and amount > 1000:
      risk_score += 20
      
  # Factor 4: Time pattern
  if transaction_time between 2AM and 5AM:
      risk_score += 15
      
  # Factor 5: AI analysis
  ai_score = analyze_with_openai(transaction_context)
  risk_score += ai_score
  
  # Action thresholds
  if risk_score > 80:
      action = "BLOCK"
  elif risk_score > 60:
      action = "REVIEW"
  else:
      action = "ALLOW"
  ```

#### 3. Real-time Analytics Dashboard
- **Metrics to Display**:
  - Transactions per second
  - Total volume ($)
  - Fraud detection rate
  - System health status
  - Geographic distribution
  - Top merchants

- **Technical Requirements**:
  - WebSocket for real-time updates
  - React/TypeScript frontend
  - Mobile responsive design
  - Data refresh < 2 seconds

#### 4. Legacy System Integration
- **COBOL File Processing**:
  - Parse and understand business logic
  - Maintain data integrity
  - Support parallel run mode
  - Enable gradual migration

### Non-Functional Requirements

#### Security
- OAuth 2.0 authentication
- End-to-end encryption
- Azure Key Vault for secrets
- Network isolation
- Audit logging

#### Scalability
- Horizontal scaling
- Auto-scaling policies
- Load balancing
- Circuit breakers
- Rate limiting

#### Reliability
- 99.99% uptime SLA
- Automated failover
- Data replication
- Disaster recovery
- Zero data loss

#### Monitoring
- Application Insights
- Custom metrics
- Alert automation
- Performance tracking
- Cost monitoring

## 🏗️ Architecture Design

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Dashboard]
        MOB[Mobile App]
        API[Partner APIs]
    end
    
    subgraph "API Gateway"
        GW[Azure API Management]
    end
    
    subgraph "Microservices"
        TS[Transaction Service]
        FS[Fraud Service]
        AS[Analytics Service]
        NS[Notification Service]
    end
    
    subgraph "AI Layer"
        OAI[Azure OpenAI]
        ML[Azure ML]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL)]
        RD[(Redis Cache)]
        CS[(Cosmos DB)]
        EH[Event Hubs]
    end
    
    subgraph "Legacy Integration"
        COBOL[COBOL Gateway]
        MF[(Mainframe DB)]
    end
    
    WEB --> GW
    MOB --> GW
    API --> GW
    
    GW --> TS
    GW --> AS
    
    TS --> FS
    TS --> PG
    TS --> RD
    TS --> EH
    
    FS --> OAI
    FS --> ML
    FS --> RD
    
    AS --> CS
    AS --> EH
    
    TS --> COBOL
    COBOL --> MF
```

### Technology Stack

#### Backend Services
- **Language**: Python 3.11+ (FastAPI)
- **Alternative**: .NET 8 (ASP.NET Core)
- **Database**: PostgreSQL 15 + Redis 7
- **Message Queue**: Azure Event Hubs
- **Container**: Docker + Kubernetes

#### AI/ML Stack
- **Azure OpenAI**: GPT-4 for fraud analysis
- **LangChain**: AI orchestration
- **Model Context Protocol**: Integration layer
- **Azure ML**: Custom models

#### Frontend
- **Framework**: React 18 + TypeScript
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI / Tailwind
- **Real-time**: Socket.io

#### Infrastructure
- **Cloud**: Azure
- **Orchestration**: Azure Kubernetes Service
- **IaC**: Terraform + Bicep
- **CI/CD**: GitHub Actions
- **Monitoring**: Application Insights + Grafana

## 📝 Implementation Guide

### Phase 1: Foundation (45 minutes)

#### Step 1.1: Environment Setup (10 minutes)
```bash
# Clone challenge repository
git clone https://github.com/workshop/module-22-challenge
cd module-22-challenge

# Run setup script
./scripts/setup-environment.sh

# Verify setup
./scripts/verify-setup.sh
```

#### Step 1.2: COBOL Analysis (15 minutes)
```python
# analyze_cobol.py
import re
from pathlib import Path

class COBOLAnalyzer:
    def __init__(self, cobol_file):
        self.cobol_file = cobol_file
        self.business_rules = []
        self.data_structures = []
        
    def extract_business_rules(self):
        """Extract business logic from COBOL"""
        with open(self.cobol_file, 'r') as f:
            content = f.read()
            
        # Extract validation rules
        validations = re.findall(
            r'IF\s+(.*?)\s+THEN\s+(.*?)\s+END-IF', 
            content, 
            re.DOTALL
        )
        
        # Extract calculations
        calculations = re.findall(
            r'COMPUTE\s+(.*?)\s+=\s+(.*?)\.', 
            content
        )
        
        return {
            'validations': validations,
            'calculations': calculations
        }
```

#### Step 1.3: Architecture Planning (20 minutes)
```yaml
# architecture/services.yaml
services:
  transaction-service:
    type: API
    language: Python
    framework: FastAPI
    database: PostgreSQL
    cache: Redis
    features:
      - Transaction validation
      - Balance management
      - Event publishing
      - COBOL integration
    
  fraud-detection-service:
    type: AI-Service
    language: Python
    framework: FastAPI
    ai-platform: Azure OpenAI
    ml-platform: Azure ML
    features:
      - Real-time scoring
      - Pattern analysis
      - Rule engine
      - Self-learning
    
  analytics-service:
    type: Stream-Processor
    language: Python
    framework: FastAPI
    streaming: Event Hubs
    database: Cosmos DB
    features:
      - Real-time aggregation
      - Dashboard API
      - Historical analysis
      - Alerting
```

### Phase 2: Core Services (60 minutes)

#### Step 2.1: Transaction Service Implementation (20 minutes)

<details>
<summary>Click to expand Transaction Service code</summary>

```python
# src/transaction_service/main.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import asyncio
from decimal import Decimal
import httpx
from datetime import datetime
import redis.asyncio as redis

from .database import get_db, get_redis
from .models import Transaction, Account
from .schemas import (
    TransactionRequest, 
    TransactionResponse,
    AccountResponse,
    FraudCheckResponse
)
from .events import EventPublisher
from .validators import TransactionValidator
from .cobol_gateway import COBOLGateway

app = FastAPI(
    title="Transaction Service",
    version="2.0.0",
    description="Modernized transaction processing system"
)

# Initialize components
event_publisher = EventPublisher()
validator = TransactionValidator()
cobol_gateway = COBOLGateway()

@app.on_event("startup")
async def startup_event():
    """Initialize connections and warmup"""
    await event_publisher.connect()
    await cobol_gateway.initialize()
    
@app.post("/api/v1/transactions", response_model=TransactionResponse)
async def process_transaction(
    request: TransactionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    """
    Process a financial transaction with fraud detection
    """
    start_time = datetime.utcnow()
    
    # Step 1: Quick cache check for duplicate
    cache_key = f"txn:{request.idempotency_key}"
    cached = await cache.get(cache_key)
    if cached:
        return TransactionResponse.parse_raw(cached)
    
    # Step 2: Validate transaction
    validation_result = await validator.validate(request, db)
    if not validation_result.is_valid:
        raise HTTPException(
            status_code=400, 
            detail=validation_result.error_message
        )
    
    # Step 3: Check fraud (async with timeout)
    try:
        fraud_check = await asyncio.wait_for(
            check_fraud_async(request),
            timeout=0.5  # 500ms timeout
        )
        
        if fraud_check.risk_score > 80:
            # Log high-risk transaction
            await event_publisher.publish("transaction.blocked", {
                "transaction_id": request.transaction_id,
                "reason": "High fraud risk",
                "risk_score": fraud_check.risk_score,
                "factors": fraud_check.risk_factors
            })
            
            raise HTTPException(
                status_code=403,
                detail=f"Transaction blocked: {fraud_check.recommendation}"
            )
            
    except asyncio.TimeoutError:
        # Fraud check timeout - proceed with caution
        fraud_check = FraudCheckResponse(
            risk_score=50,
            risk_level="medium",
            recommendation="proceed_with_monitoring"
        )
    
    # Step 4: Execute transaction atomically
    transaction = None
    try:
        async with db.begin():
            # Lock accounts for update
            from_account = await db.get(
                Account, 
                request.from_account,
                with_for_update=True
            )
            to_account = await db.get(
                Account,
                request.to_account,
                with_for_update=True
            )
            
            if not from_account or not to_account:
                raise HTTPException(404, "Account not found")
            
            # Check balance
            total_amount = request.amount + calculate_fee(request, from_account)
            
            if from_account.available_balance < total_amount:
                if not (from_account.account_type == 'B' and 
                       from_account.overdraft_limit >= total_amount):
                    raise HTTPException(400, "Insufficient funds")
            
            # Update balances
            from_account.balance -= total_amount
            from_account.available_balance -= total_amount
            from_account.daily_used += request.amount
            from_account.last_transaction = datetime.utcnow()
            from_account.transaction_count += 1
            
            to_account.balance += request.amount
            to_account.available_balance += request.amount
            to_account.last_transaction = datetime.utcnow()
            
            # Create transaction record
            transaction = Transaction(
                transaction_id=request.transaction_id,
                from_account=request.from_account,
                to_account=request.to_account,
                amount=request.amount,
                currency=request.currency,
                transaction_type=request.transaction_type,
                status="completed",
                risk_score=fraud_check.risk_score,
                processing_time=(datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            db.add(transaction)
            await db.flush()
            
            # Update COBOL system (async)
            background_tasks.add_task(
                cobol_gateway.sync_transaction,
                transaction.dict()
            )
    
    except Exception as e:
        # Rollback handled by context manager
        await event_publisher.publish("transaction.failed", {
            "transaction_id": request.transaction_id,
            "error": str(e)
        })
        raise
    
    # Step 5: Post-processing
    # Publish success event
    await event_publisher.publish("transaction.completed", {
        "transaction_id": transaction.transaction_id,
        "amount": str(request.amount),
        "risk_score": fraud_check.risk_score,
        "processing_time": transaction.processing_time
    })
    
    # Cache response
    response = TransactionResponse(
        transaction_id=transaction.transaction_id,
        status="completed",
        message="Transaction processed successfully",
        risk_score=fraud_check.risk_score,
        processing_time=transaction.processing_time
    )
    
    await cache.setex(
        cache_key,
        300,  # 5 minutes
        response.json()
    )
    
    return response

async def check_fraud_async(transaction: TransactionRequest) -> FraudCheckResponse:
    """Async fraud detection service call"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://fraud-service:8002/api/v1/analyze",
            json=transaction.dict(),
            timeout=0.5
        )
        return FraudCheckResponse(**response.json())

def calculate_fee(transaction: TransactionRequest, account: Account) -> Decimal:
    """Calculate transaction fee based on business rules"""
    if account.is_vip:
        return Decimal("0.00")
    
    fee_map = {
        "DM": Decimal("2.50"),   # Domestic
        "IN": Decimal("25.00"),  # International
        "WT": Decimal("35.00"),  # Wire Transfer
    }
    
    base_fee = fee_map.get(transaction.transaction_type, Decimal("0.00"))
    
    # Volume discount
    if account.transaction_count > 1000:
        base_fee *= Decimal("0.70")  # 30% discount
    elif account.transaction_count > 500:
        base_fee *= Decimal("0.80")  # 20% discount
    elif account.transaction_count > 100:
        base_fee *= Decimal("0.90")  # 10% discount
    
    return base_fee

@app.get("/api/v1/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get account details"""
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(404, "Account not found")
    
    return AccountResponse.from_orm(account)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "transaction-service",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    """Readiness check - verify all dependencies"""
    try:
        # Check database
        await db.execute("SELECT 1")
        
        # Check cache
        await cache.ping()
        
        # Check event publisher
        if not event_publisher.is_connected:
            raise Exception("Event publisher not connected")
        
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(503, f"Service not ready: {str(e)}")
```

</details>

#### Step 2.2: Fraud Detection Service (20 minutes)

<details>
<summary>Click to expand Fraud Detection Service code</summary>

```python
# src/fraud_service/main.py
from fastapi import FastAPI, HTTPException
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import asyncio
from datetime import datetime, timedelta
import numpy as np

app = FastAPI(
    title="Fraud Detection Service",
    version="2.0.0",
    description="AI-powered fraud detection system"
)

class FraudAnalysis(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str = Field(..., pattern="^(low|medium|high|critical)$")
    risk_factors: List[str]
    recommendation: str
    confidence: float = Field(..., ge=0, le=1)
    explanation: str

class TransactionContext(BaseModel):
    """Enhanced transaction data with context"""
    transaction_id: str
    from_account: str
    to_account: str
    amount: float
    currency: str
    transaction_type: str
    timestamp: datetime
    device_id: Optional[str]
    ip_address: Optional[str]
    location: Optional[Dict[str, str]]
    account_history: Optional[Dict[str, any]]
    recent_transactions: Optional[List[Dict]]

class AIFraudDetector:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01",
            deployment_name="gpt-4",
            temperature=0,
            max_tokens=500
        )
        
        self.parser = PydanticOutputParser(pydantic_object=FraudAnalysis)
        
        self.analysis_prompt = ChatPromptTemplate.from_template("""
        You are an expert fraud detection system. Analyze this financial transaction for fraud risk.
        
        Transaction Details:
        - Amount: ${amount} {currency}
        - From Account: {from_account} (Type: {from_type}, Age: {account_age} days)
        - To Account: {to_account} (First time: {is_new_recipient})
        - Transaction Type: {transaction_type}
        - Time: {timestamp}
        - Location: {location}
        - Device: {device_info}
        
        Account History:
        - Average Transaction: ${avg_amount}
        - Largest Transaction: ${max_amount}
        - Transactions Today: {daily_count}
        - Recent Locations: {recent_locations}
        
        Recent Activity:
        {recent_activity}
        
        Known Fraud Patterns:
        1. Rapid succession of transactions (velocity attack)
        2. Unusual amount compared to history
        3. New recipient with large amount
        4. Geographic impossibility
        5. Known compromised device/IP
        
        Analyze this transaction and provide:
        1. Risk score (0-100)
        2. Risk level (low/medium/high/critical)
        3. Specific risk factors identified
        4. Clear recommendation (allow/review/block)
        5. Confidence in assessment (0-1)
        6. Brief explanation for the decision
        
        {format_instructions}
        """)
        
        self.pattern_analyzer = PatternAnalyzer()
        self.rule_engine = RuleEngine()
        self.ml_model = load_ml_model()  # Pre-trained model
    
    async def analyze(self, transaction_data: Dict) -> FraudAnalysis:
        """Multi-layer fraud analysis"""
        
        # Layer 1: Quick rule-based checks
        rule_score = self.rule_engine.evaluate(transaction_data)
        if rule_score >= 90:
            # Immediate high-risk determination
            return FraudAnalysis(
                risk_score=rule_score,
                risk_level="critical",
                risk_factors=self.rule_engine.get_triggered_rules(),
                recommendation="block",
                confidence=0.99,
                explanation="Transaction violates critical security rules"
            )
        
        # Layer 2: ML model prediction
        ml_features = self._extract_features(transaction_data)
        ml_score = self.ml_model.predict_proba(ml_features)[0, 1] * 100
        
        # Layer 3: Pattern analysis
        pattern_results = await self.pattern_analyzer.analyze(transaction_data)
        
        # Layer 4: AI deep analysis (only for medium-high risk)
        if rule_score > 30 or ml_score > 40:
            context = await self._enrich_context(transaction_data)
            ai_analysis = await self._ai_analysis(context)
        else:
            # Low risk - quick approval
            ai_analysis = FraudAnalysis(
                risk_score=int((rule_score + ml_score) / 2),
                risk_level="low",
                risk_factors=[],
                recommendation="allow",
                confidence=0.85,
                explanation="Transaction matches normal patterns"
            )
        
        # Combine all scores with weights
        final_score = (
            rule_score * 0.3 +
            ml_score * 0.3 +
            pattern_results.score * 0.2 +
            ai_analysis.risk_score * 0.2
        )
        
        # Determine final recommendation
        if final_score >= 80:
            recommendation = "block"
            risk_level = "critical"
        elif final_score >= 60:
            recommendation = "review"
            risk_level = "high"
        elif final_score >= 40:
            recommendation = "allow_with_monitoring"
            risk_level = "medium"
        else:
            recommendation = "allow"
            risk_level = "low"
        
        return FraudAnalysis(
            risk_score=int(final_score),
            risk_level=risk_level,
            risk_factors=self._combine_risk_factors([
                self.rule_engine.get_triggered_rules(),
                pattern_results.factors,
                ai_analysis.risk_factors
            ]),
            recommendation=recommendation,
            confidence=self._calculate_confidence([
                rule_score, ml_score, pattern_results.score, ai_analysis.risk_score
            ]),
            explanation=self._generate_explanation(
                rule_score, ml_score, pattern_results, ai_analysis
            )
        )
    
    async def _enrich_context(self, transaction: Dict) -> TransactionContext:
        """Enrich transaction with historical context"""
        # Fetch account history
        account_history = await fetch_account_history(transaction["from_account"])
        
        # Get recent transactions
        recent_transactions = await fetch_recent_transactions(
            transaction["from_account"],
            limit=10
        )
        
        # Get device/location info
        device_info = await fetch_device_info(transaction.get("device_id"))
        
        return TransactionContext(
            **transaction,
            account_history=account_history,
            recent_transactions=recent_transactions,
            location=device_info.get("location"),
            device_info=device_info
        )
    
    async def _ai_analysis(self, context: TransactionContext) -> FraudAnalysis:
        """Deep AI analysis using GPT-4"""
        
        # Prepare context for prompt
        prompt_value = self.analysis_prompt.format_prompt(
            amount=context.amount,
            currency=context.currency,
            from_account=context.from_account[-4:],  # Last 4 digits only
            from_type=context.account_history.get("type", "Unknown"),
            account_age=(datetime.now() - context.account_history.get(
                "created_date", datetime.now()
            )).days,
            to_account=context.to_account[-4:],
            is_new_recipient=context.to_account not in [
                t["to_account"] for t in context.recent_transactions
            ],
            transaction_type=context.transaction_type,
            timestamp=context.timestamp,
            location=context.location or "Unknown",
            device_info=context.device_id or "Unknown",
            avg_amount=context.account_history.get("avg_transaction", 0),
            max_amount=context.account_history.get("max_transaction", 0),
            daily_count=len([
                t for t in context.recent_transactions
                if datetime.fromisoformat(t["timestamp"]).date() == datetime.now().date()
            ]),
            recent_locations=list(set([
                t.get("location", "Unknown") for t in context.recent_transactions[-5:]
            ])),
            recent_activity=self._format_recent_activity(context.recent_transactions),
            format_instructions=self.parser.get_format_instructions()
        )
        
        # Get AI response
        response = await self.llm.agenerate([prompt_value.to_messages()])
        
        # Parse response
        return self.parser.parse(response.generations[0][0].text)
    
    def _calculate_confidence(self, scores: List[float]) -> float:
        """Calculate confidence based on score agreement"""
        std_dev = np.std(scores)
        # Lower std dev = higher confidence
        confidence = 1 - (std_dev / 50)  # Normalize
        return max(0.5, min(0.99, confidence))

class RuleEngine:
    """Traditional rule-based fraud detection"""
    
    def __init__(self):
        self.rules = [
            {
                "name": "excessive_amount",
                "check": lambda t: t["amount"] > 100000,
                "score": 50
            },
            {
                "name": "rapid_succession",
                "check": lambda t: self._check_velocity(t),
                "score": 60
            },
            {
                "name": "sanctioned_country",
                "check": lambda t: self._check_sanctions(t),
                "score": 100
            },
            {
                "name": "unusual_time",
                "check": lambda t: self._check_time_pattern(t),
                "score": 20
            }
        ]
        self.triggered_rules = []
    
    def evaluate(self, transaction: Dict) -> int:
        """Evaluate all rules and return cumulative score"""
        total_score = 0
        self.triggered_rules = []
        
        for rule in self.rules:
            try:
                if rule["check"](transaction):
                    total_score += rule["score"]
                    self.triggered_rules.append(rule["name"])
            except Exception:
                continue
        
        return min(100, total_score)
    
    def get_triggered_rules(self) -> List[str]:
        return self.triggered_rules

@app.post("/api/v1/analyze", response_model=FraudAnalysis)
async def analyze_transaction(transaction: Dict):
    """Analyze transaction for fraud"""
    detector = AIFraudDetector()
    
    try:
        analysis = await detector.analyze(transaction)
        
        # Log high-risk transactions
        if analysis.risk_score > 60:
            await log_high_risk_transaction(transaction, analysis)
        
        return analysis
        
    except Exception as e:
        # Fail open - allow transaction but flag for review
        return FraudAnalysis(
            risk_score=50,
            risk_level="medium",
            risk_factors=["analysis_error"],
            recommendation="allow_with_monitoring",
            confidence=0.5,
            explanation=f"Analysis error: {str(e)}. Transaction allowed with monitoring."
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fraud-service"}
```

</details>

#### Step 2.3: Analytics Service (20 minutes)

<details>
<summary>Click to expand Analytics Service code</summary>

```python
# src/analytics_service/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from typing import List, Dict
from datetime import datetime, timedelta
import json
from collections import defaultdict
import numpy as np

from azure.eventhub.aio import EventHubConsumerClient
from azure.cosmos.aio import CosmosClient
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title="Analytics Service",
    version="2.0.0",
    description="Real-time transaction analytics"
)

class ConnectionManager:
    """Manage WebSocket connections"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

class StreamProcessor:
    def __init__(self):
        self.event_hub_client = EventHubConsumerClient.from_connection_string(
            conn_str=os.getenv("EVENT_HUB_CONNECTION_STRING"),
            consumer_group="analytics-consumer-group",
            eventhub_name="transactions"
        )
        
        self.cosmos_client = CosmosClient.from_connection_string(
            os.getenv("COSMOS_CONNECTION_STRING")
        )
        self.database = self.cosmos_client.get_database_client("analytics")
        self.container = self.database.get_container_client("metrics")
        
        # In-memory metrics for real-time updates
        self.metrics = {
            "total_count": 0,
            "total_amount": 0,
            "fraud_blocked": 0,
            "fraud_amount": 0,
            "avg_response_time": 0,
            "transactions_per_minute": defaultdict(int),
            "by_type": defaultdict(int),
            "by_currency": defaultdict(lambda: defaultdict(float)),
            "geographic_distribution": defaultdict(int),
            "hourly_volume": defaultdict(float),
            "risk_distribution": defaultdict(int)
        }
        
        self.response_times = []
        self.last_broadcast = datetime.utcnow()
    
    async def start(self):
        """Start consuming events"""
        async with self.event_hub_client:
            await self.event_hub_client.receive(
                on_event=self.process_event,
                starting_position="-1",  # From beginning
            )
    
    async def process_event(self, partition_context, event):
        """Process incoming transaction event"""
        try:
            data = json.loads(event.body_as_str())
            event_type = data.get("event_type")
            
            if event_type == "transaction.completed":
                await self._process_completed_transaction(data)
            elif event_type == "transaction.blocked":
                await self._process_blocked_transaction(data)
            
            # Update partition checkpoint
            await partition_context.update_checkpoint(event)
            
            # Broadcast updates every second
            if (datetime.utcnow() - self.last_broadcast).total_seconds() >= 1:
                await self._broadcast_metrics()
                self.last_broadcast = datetime.utcnow()
                
        except Exception as e:
            print(f"Error processing event: {e}")
    
    async def _process_completed_transaction(self, data: Dict):
        """Update metrics for completed transaction"""
        # Update counters
        self.metrics["total_count"] += 1
        self.metrics["total_amount"] += data["amount"]
        
        # Response time tracking
        response_time = data.get("processing_time", 0)
        self.response_times.append(response_time)
        if len(self.response_times) > 1000:
            self.response_times.pop(0)
        self.metrics["avg_response_time"] = np.mean(self.response_times)
        
        # Time-based metrics
        minute_key = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        self.metrics["transactions_per_minute"][minute_key] += 1
        
        # Type distribution
        tx_type = data.get("transaction_type", "unknown")
        self.metrics["by_type"][tx_type] += 1
        
        # Currency metrics
        currency = data.get("currency", "USD")
        self.metrics["by_currency"][currency]["count"] += 1
        self.metrics["by_currency"][currency]["volume"] += data["amount"]
        
        # Risk distribution
        risk_score = data.get("risk_score", 0)
        risk_bucket = (risk_score // 20) * 20  # 0-20, 20-40, etc.
        self.metrics["risk_distribution"][f"{risk_bucket}-{risk_bucket+20}"] += 1
        
        # Persist to Cosmos DB (async)
        await self._persist_metrics(data)
    
    async def _process_blocked_transaction(self, data: Dict):
        """Update metrics for blocked transaction"""
        self.metrics["fraud_blocked"] += 1
        self.metrics["fraud_amount"] += data.get("amount", 0)
        
        # Track fraud patterns
        await self._analyze_fraud_pattern(data)
    
    async def _broadcast_metrics(self):
        """Broadcast current metrics to all connected clients"""
        # Calculate derived metrics
        current_minute = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        tpm = self.metrics["transactions_per_minute"].get(current_minute, 0)
        
        # Prepare broadcast message
        broadcast_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "totalTransactions": self.metrics["total_count"],
                "totalVolume": round(self.metrics["total_amount"], 2),
                "fraudBlocked": self.metrics["fraud_blocked"],
                "fraudVolume": round(self.metrics["fraud_amount"], 2),
                "avgResponseTime": round(self.metrics["avg_response_time"], 2),
                "transactionsPerMinute": tpm,
                "byType": dict(self.metrics["by_type"]),
                "byCurrency": {
                    k: {
                        "count": v["count"],
                        "volume": round(v["volume"], 2)
                    } for k, v in self.metrics["by_currency"].items()
                },
                "riskDistribution": dict(self.metrics["risk_distribution"])
            },
            "charts": {
                "timeSeries": self._get_time_series_data(),
                "geographic": self._get_geographic_data(),
                "fraudTrends": self._get_fraud_trends()
            }
        }
        
        await manager.broadcast(json.dumps(broadcast_data))
    
    def _get_time_series_data(self) -> List[Dict]:
        """Get time series data for charts"""
        # Last 60 minutes
        now = datetime.utcnow()
        time_series = []
        
        for i in range(60):
            time_point = now - timedelta(minutes=i)
            minute_key = time_point.strftime("%Y-%m-%d %H:%M")
            
            time_series.append({
                "time": time_point.isoformat(),
                "transactions": self.metrics["transactions_per_minute"].get(minute_key, 0)
            })
        
        return list(reversed(time_series))
    
    async def _persist_metrics(self, transaction_data: Dict):
        """Persist metrics to Cosmos DB"""
        metric_doc = {
            "id": transaction_data["transaction_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "type": "transaction_metric",
            "amount": transaction_data["amount"],
            "currency": transaction_data.get("currency", "USD"),
            "transaction_type": transaction_data.get("transaction_type"),
            "risk_score": transaction_data.get("risk_score", 0),
            "processing_time": transaction_data.get("processing_time", 0),
            "partition_key": datetime.utcnow().strftime("%Y-%m-%d")
        }
        
        await self.container.create_item(body=metric_doc)

# Global stream processor instance
stream_processor = StreamProcessor()

@app.on_event("startup")
async def startup_event():
    """Start stream processing on startup"""
    asyncio.create_task(stream_processor.start())

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics"""
    await manager.connect(websocket)
    
    try:
        # Send initial metrics
        await websocket.send_text(json.dumps({
            "type": "initial",
            "metrics": stream_processor.metrics
        }))
        
        # Keep connection alive
        while True:
            # Wait for any message (ping/pong)
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/v1/metrics/summary")
async def get_metrics_summary():
    """Get current metrics summary"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": stream_processor.metrics
    }

@app.get("/api/v1/metrics/historical")
async def get_historical_metrics(
    start_date: str,
    end_date: str,
    aggregation: str = "hourly"
):
    """Get historical metrics from Cosmos DB"""
    query = """
    SELECT 
        c.timestamp,
        COUNT(1) as transaction_count,
        SUM(c.amount) as total_volume,
        AVG(c.processing_time) as avg_response_time,
        AVG(c.risk_score) as avg_risk_score
    FROM c
    WHERE c.timestamp >= @start_date 
    AND c.timestamp <= @end_date
    AND c.type = 'transaction_metric'
    GROUP BY DateTimePart("hh", c.timestamp)
    """
    
    parameters = [
        {"name": "@start_date", "value": start_date},
        {"name": "@end_date", "value": end_date}
    ]
    
    items = stream_processor.container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    )
    
    results = []
    async for item in items:
        results.append(item)
    
    return {
        "period": f"{start_date} to {end_date}",
        "aggregation": aggregation,
        "data": results
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "analytics-service"}
```

</details>

### Phase 3: Dashboard & Integration (45 minutes)

#### Step 3.1: React Dashboard (20 minutes)

<details>
<summary>Click to expand Dashboard code</summary>

```typescript
// src/dashboard/App.tsx
import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { 
  TrendingUp, 
  Warning, 
  CheckCircle, 
  AttachMoney,
  Speed,
  Security
} from '@mui/icons-material';

interface Metrics {
  totalTransactions: number;
  totalVolume: number;
  fraudBlocked: number;
  fraudVolume: number;
  avgResponseTime: number;
  transactionsPerMinute: number;
  byType: Record<string, number>;
  byCurrency: Record<string, { count: number; volume: number }>;
  riskDistribution: Record<string, number>;
}

interface WebSocketData {
  timestamp: string;
  metrics: Metrics;
  charts: {
    timeSeries: Array<{ time: string; transactions: number }>;
    geographic: Array<{ country: string; count: number }>;
    fraudTrends: Array<{ time: string; rate: number }>;
  };
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard: React.FC = () => {
  const [data, setData] = useState<WebSocketData | null>(null);
  const [connected, setConnected] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket
    const websocket = new WebSocket('ws://localhost:8003/ws/metrics');
    
    websocket.onopen = () => {
      console.log('Connected to analytics service');
      setConnected(true);
    };
    
    websocket.onmessage = (event) => {
      const messageData = JSON.parse(event.data);
      setData(messageData);
    };
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    websocket.onclose = () => {
      console.log('Disconnected from analytics service');
      setConnected(false);
      // Attempt reconnection after 5 seconds
      setTimeout(() => {
        window.location.reload();
      }, 5000);
    };
    
    setWs(websocket);
    
    // Cleanup on unmount
    return () => {
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, []);

  if (!connected || !data) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography variant="h6" align="center" sx={{ mt: 2 }}>
          Connecting to analytics service...
        </Typography>
      </Box>
    );
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('en-US').format(value);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" gutterBottom align="center">
        Transaction Processing Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Transactions
                  </Typography>
                  <Typography variant="h4">
                    {formatNumber(data.metrics.totalTransactions)}
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    <TrendingUp fontSize="small" /> {data.metrics.transactionsPerMinute}/min
                  </Typography>
                </Box>
                <CheckCircle color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Volume
                  </Typography>
                  <Typography variant="h4">
                    {formatCurrency(data.metrics.totalVolume)}
                  </Typography>
                  <Typography variant="body2">
                    Across all currencies
                  </Typography>
                </Box>
                <AttachMoney color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Fraud Blocked
                  </Typography>
                  <Typography variant="h4" color="error.main">
                    {formatNumber(data.metrics.fraudBlocked)}
                  </Typography>
                  <Typography variant="body2">
                    {formatCurrency(data.metrics.fraudVolume)} saved
                  </Typography>
                </Box>
                <Security color="error" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Response Time
                  </Typography>
                  <Typography variant="h4">
                    {data.metrics.avgResponseTime.toFixed(0)}ms
                  </Typography>
                  <Chip 
                    label={data.metrics.avgResponseTime < 100 ? "Excellent" : "Good"}
                    color={data.metrics.avgResponseTime < 100 ? "success" : "warning"}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </Box>
                <Speed color="info" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Transaction Volume Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Transaction Volume (Last Hour)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.charts.timeSeries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="time" 
                  tickFormatter={(time) => new Date(time).toLocaleTimeString()}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(time) => new Date(time).toLocaleString()}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="transactions" 
                  stroke="#8884d8" 
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Risk Distribution */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Risk Score Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={Object.entries(data.metrics.riskDistribution).map(([range, count]) => ({
                    name: range,
                    value: count
                  }))}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {Object.entries(data.metrics.riskDistribution).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Transaction Types */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Transaction Types
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={Object.entries(data.metrics.byType).map(([type, count]) => ({
                type,
                count
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Currency Breakdown */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Currency Breakdown
            </Typography>
            <Box sx={{ mt: 2 }}>
              {Object.entries(data.metrics.byCurrency).map(([currency, stats]) => (
                <Box key={currency} sx={{ mb: 2 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body1">{currency}</Typography>
                    <Box>
                      <Chip 
                        label={`${formatNumber(stats.count)} transactions`} 
                        size="small" 
                        sx={{ mr: 1 }}
                      />
                      <Chip 
                        label={formatCurrency(stats.volume)} 
                        size="small" 
                        color="primary"
                      />
                    </Box>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={(stats.count / data.metrics.totalTransactions) * 100} 
                    sx={{ mt: 1 }}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* System Status */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Status
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Box display="flex" alignItems="center">
                  <CheckCircle color="success" sx={{ mr: 1 }} />
                  <Typography>Transaction Service: Healthy</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box display="flex" alignItems="center">
                  <CheckCircle color="success" sx={{ mr: 1 }} />
                  <Typography>Fraud Detection: Healthy</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box display="flex" alignItems="center">
                  <CheckCircle color="success" sx={{ mr: 1 }} />
                  <Typography>Analytics: Connected</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
```

</details>

### Phase 4: Deployment & Testing (30 minutes)

#### Step 4.1: Kubernetes Deployment (10 minutes)

<details>
<summary>Click to expand Kubernetes manifests</summary>

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fintech-challenge
  labels:
    name: fintech-challenge

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: fintech-challenge
data:
  ENVIRONMENT: "production"
  EVENT_HUB_NAME: "transactions"
  COSMOS_DATABASE: "analytics"
  LOG_LEVEL: "INFO"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: fintech-challenge
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@postgres:5432/transactions"
  REDIS_URL: "redis://redis:6379"
  AZURE_OPENAI_ENDPOINT: "https://your-openai.openai.azure.com/"
  AZURE_OPENAI_KEY: "your-key-here"
  EVENT_HUB_CONNECTION_STRING: "your-connection-string"
  COSMOS_CONNECTION_STRING: "your-cosmos-string"

---
# k8s/transaction-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transaction-service
  namespace: fintech-challenge
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
      - name: transaction-service
        image: challenge.azurecr.io/transaction-service:v2.0.0
        ports:
        - containerPort: 8001
        env:
        - name: SERVICE_NAME
          value: "transaction-service"
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: transaction-service
  namespace: fintech-challenge
spec:
  selector:
    app: transaction-service
  ports:
  - port: 80
    targetPort: 8001
  type: ClusterIP

---
# k8s/fraud-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-service
  namespace: fintech-challenge
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fraud-service
  template:
    metadata:
      labels:
        app: fraud-service
    spec:
      containers:
      - name: fraud-service
        image: challenge.azurecr.io/fraud-service:v2.0.0
        ports:
        - containerPort: 8002
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "2000m"

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: transaction-service-hpa
  namespace: fintech-challenge
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: transaction-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: fintech-challenge
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.challenge.azure.com
    secretName: api-tls
  rules:
  - host: api.challenge.azure.com
    http:
      paths:
      - path: /api/v1/transactions
        pathType: Prefix
        backend:
          service:
            name: transaction-service
            port:
              number: 80
      - path: /api/v1/fraud
        pathType: Prefix
        backend:
          service:
            name: fraud-service
            port:
              number: 80
```

</details>

#### Step 4.2: Integration Tests (10 minutes)

<details>
<summary>Click to expand Integration Tests</summary>

```python
# tests/integration/test_end_to_end.py
import pytest
import asyncio
import httpx
from decimal import Decimal
import json
import time
from typing import Dict, List

class TestEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.fixture
    async def api_client(self):
        """HTTP client for API testing"""
        async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
            yield client
    
    @pytest.fixture
    async def test_accounts(self, api_client):
        """Create test accounts"""
        accounts = [
            {
                "account_number": "1234567890",
                "account_type": "C",
                "balance": 10000.00,
                "customer_id": "TEST001"
            },
            {
                "account_number": "0987654321",
                "account_type": "S",
                "balance": 50000.00,
                "customer_id": "TEST002"
            }
        ]
        
        # Create accounts via API
        for account in accounts:
            response = await api_client.post(
                "/api/v1/accounts",
                json=account
            )
            assert response.status_code == 201
        
        yield accounts
        
        # Cleanup
        for account in accounts:
            await api_client.delete(f"/api/v1/accounts/{account['account_number']}")
    
    @pytest.mark.asyncio
    async def test_successful_transaction_flow(self, api_client, test_accounts):
        """Test complete successful transaction flow"""
        
        # 1. Submit transaction
        transaction = {
            "from_account": "1234567890",
            "to_account": "0987654321",
            "amount": 100.00,
            "currency": "USD",
            "transaction_type": "DM"
        }
        
        start_time = time.time()
        response = await api_client.post(
            "/api/v1/transactions",
            json=transaction
        )
        end_time = time.time()
        
        # Verify response
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "completed"
        assert "transaction_id" in result
        
        # Verify performance
        response_time = (end_time - start_time) * 1000
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms requirement"
        
        # 2. Verify account balances updated
        from_account = await api_client.get("/api/v1/accounts/1234567890")
        assert from_account.json()["balance"] == 9897.50  # 10000 - 100 - 2.50 fee
        
        to_account = await api_client.get("/api/v1/accounts/0987654321")
        assert to_account.json()["balance"] == 50100.00  # 50000 + 100
        
        # 3. Verify transaction appears in history
        history = await api_client.get(
            f"/api/v1/transactions?account={transaction['from_account']}"
        )
        assert len(history.json()) > 0
        assert history.json()[0]["transaction_id"] == result["transaction_id"]
    
    @pytest.mark.asyncio
    async def test_fraud_detection_blocks_suspicious(self, api_client, test_accounts):
        """Test that suspicious transactions are blocked"""
        
        # Create suspicious transaction pattern
        suspicious_transactions = []
        
        # Rapid succession of transactions
        for i in range(5):
            transaction = {
                "from_account": "1234567890",
                "to_account": f"999999{i:04d}",
                "amount": 9999.00,
                "currency": "USD",
                "transaction_type": "WT"
            }
            suspicious_transactions.append(transaction)
        
        # Submit rapidly
        tasks = []
        for txn in suspicious_transactions:
            task = api_client.post("/api/v1/transactions", json=txn)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # At least some should be blocked
        blocked_count = sum(
            1 for r in responses 
            if not isinstance(r, Exception) and r.status_code == 403
        )
        assert blocked_count > 0, "Fraud detection failed to block suspicious pattern"
    
    @pytest.mark.asyncio
    async def test_concurrent_transactions_consistency(self, api_client, test_accounts):
        """Test system maintains consistency under concurrent load"""
        
        initial_balance = 10000.00
        transaction_amount = 10.00
        concurrent_count = 50
        
        # Submit many concurrent transactions from same account
        tasks = []
        for i in range(concurrent_count):
            transaction = {
                "from_account": "1234567890",
                "to_account": "0987654321",
                "amount": transaction_amount,
                "currency": "USD"
            }
            task = api_client.post("/api/v1/transactions", json=transaction)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful transactions
        successful = sum(
            1 for r in responses
            if not isinstance(r, Exception) and r.status_code == 200
        )
        
        # Verify final balance matches successful transactions
        final_account = await api_client.get("/api/v1/accounts/1234567890")
        final_balance = final_account.json()["balance"]
        
        expected_balance = initial_balance - (successful * (transaction_amount + 2.50))
        assert abs(final_balance - expected_balance) < 0.01, "Balance inconsistency detected"
    
    @pytest.mark.asyncio
    async def test_analytics_real_time_updates(self, api_client, test_accounts):
        """Test real-time analytics updates"""
        
        # Connect to analytics WebSocket
        import websockets
        
        metrics_before = None
        metrics_after = None
        
        async with websockets.connect("ws://localhost:8003/ws/metrics") as ws:
            # Get initial metrics
            initial_msg = await ws.recv()
            metrics_before = json.loads(initial_msg)["metrics"]
            
            # Submit transaction
            transaction = {
                "from_account": "1234567890",
                "to_account": "0987654321",
                "amount": 500.00,
                "currency": "USD"
            }
            
            response = await api_client.post(
                "/api/v1/transactions",
                json=transaction
            )
            assert response.status_code == 200
            
            # Wait for analytics update
            timeout = time.time() + 5  # 5 second timeout
            while time.time() < timeout:
                msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                metrics_after = json.loads(msg)["metrics"]
                
                if metrics_after["totalTransactions"] > metrics_before["totalTransactions"]:
                    break
            
            # Verify metrics updated
            assert metrics_after["totalTransactions"] == metrics_before["totalTransactions"] + 1
            assert metrics_after["totalVolume"] == metrics_before["totalVolume"] + 500.00

class TestPerformance:
    """Performance and load tests"""
    
    @pytest.mark.asyncio
    @pytest.mark.performance
    async def test_transaction_latency(self, api_client, test_accounts):
        """Test transaction processing latency"""
        
        latencies = []
        
        for _ in range(100):
            transaction = {
                "from_account": "1234567890",
                "to_account": "0987654321",
                "amount": 10.00,
                "currency": "USD"
            }
            
            start = time.time()
            response = await api_client.post(
                "/api/v1/transactions",
                json=transaction
            )
            end = time.time()
            
            if response.status_code == 200:
                latencies.append((end - start) * 1000)
        
        # Calculate percentiles
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        
        print(f"\nLatency Results:")
        print(f"P50: {p50:.2f}ms")
        print(f"P95: {p95:.2f}ms")
        print(f"P99: {p99:.2f}ms")
        
        # Assert performance requirements
        assert p99 < 100, f"P99 latency {p99}ms exceeds 100ms requirement"
    
    @pytest.mark.asyncio
    @pytest.mark.load
    async def test_sustained_load(self, api_client, test_accounts):
        """Test system under sustained load"""
        
        duration = 60  # 1 minute
        target_tps = 100
        
        start_time = time.time()
        successful = 0
        failed = 0
        
        async def submit_transaction():
            transaction = {
                "from_account": "1234567890",
                "to_account": "0987654321",
                "amount": 1.00,
                "currency": "USD"
            }
            
            try:
                response = await api_client.post(
                    "/api/v1/transactions",
                    json=transaction,
                    timeout=5.0
                )
                return response.status_code == 200
            except:
                return False
        
        # Submit transactions at target rate
        while time.time() - start_time < duration:
            batch_start = time.time()
            
            # Submit batch
            tasks = [submit_transaction() for _ in range(target_tps)]
            results = await asyncio.gather(*tasks)
            
            successful += sum(results)
            failed += len(results) - sum(results)
            
            # Wait to maintain rate
            batch_duration = time.time() - batch_start
            if batch_duration < 1.0:
                await asyncio.sleep(1.0 - batch_duration)
        
        # Calculate results
        total = successful + failed
        success_rate = successful / total * 100
        actual_tps = total / duration
        
        print(f"\nLoad Test Results:")
        print(f"Total Requests: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Actual TPS: {actual_tps:.2f}")
        
        # Assert requirements
        assert success_rate > 95, f"Success rate {success_rate}% below 95% requirement"
        assert actual_tps > 90, f"TPS {actual_tps} below 90% of target"
```

</details>

#### Step 4.3: Demo Preparation (10 minutes)

<details>
<summary>Click to expand Demo Script</summary>

```markdown
# Demo Script - Super Challenge

## 1. Architecture Overview (1 minute)

"I've successfully modernized LegacyFinance's COBOL-based system into a cloud-native microservices architecture. Let me show you the key components..."

[Show architecture diagram]

- **Transaction Service**: Handles all financial transactions with sub-100ms latency
- **AI-Powered Fraud Detection**: Uses Azure OpenAI for intelligent risk assessment
- **Real-time Analytics**: Processes events through Azure Event Hubs
- **Modern Dashboard**: React-based UI with WebSocket updates

## 2. Live Demo (3 minutes)

### 2.1 Normal Transaction Flow

"Let me demonstrate a typical transaction..."

```bash
# Submit valid transaction
curl -X POST https://api.challenge.azure.com/api/v1/transactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "from_account": "1234567890",
    "to_account": "0987654321",
    "amount": 500.00,
    "currency": "USD"
  }'
```

[Show response with < 100ms processing time]

### 2.2 Fraud Detection in Action

"Now let's see how the AI detects suspicious activity..."

```bash
# Submit suspicious transaction
curl -X POST https://api.challenge.azure.com/api/v1/transactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "from_account": "9999999999",
    "to_account": "1111111111",
    "amount": 999999.00,
    "currency": "USD",
    "location": "North Korea"
  }'
```

[Show fraud detection blocking the transaction]

### 2.3 Real-time Dashboard

"The dashboard updates in real-time as transactions are processed..."

[Navigate to dashboard, show live metrics updating]

- Transaction volume increasing
- Fraud detection saving money
- Geographic distribution
- Performance metrics all green

### 2.4 Scalability Test

"Let me demonstrate the system handling high load..."

```bash
# Run load test
./scripts/run-load-test.sh --tps 1000 --duration 30s
```

[Show system auto-scaling and maintaining performance]

## 3. Technical Highlights (1 minute)

### AI Integration
- **GitHub Copilot**: Generated 70% of the code
- **Azure OpenAI**: Analyzes patterns in milliseconds
- **Self-learning**: Improves accuracy over time

### Performance Optimizations
- **Caching**: Redis for hot data
- **Async Processing**: Non-blocking I/O throughout
- **Connection Pooling**: Efficient resource usage
- **Circuit Breakers**: Graceful degradation

### Security Implementation
- **OAuth 2.0**: Secure authentication
- **Encryption**: Data at rest and in transit
- **Key Vault**: Secrets management
- **Network Isolation**: Private endpoints

### Cost Optimization
- **60% reduction** in infrastructure costs
- **Serverless** for variable workloads
- **Auto-scaling** prevents over-provisioning

## 4. Business Impact

"This solution delivers significant business value..."

- **Performance**: 10x faster than legacy system
- **Cost**: 60% reduction in operational expenses
- **Reliability**: 99.99% uptime architecture
- **Innovation**: API-first enables new products
- **Compliance**: Full audit trail maintained

</details>

## 📊 Evaluation Criteria

### Detailed Scoring Rubric

#### 1. Functionality (30 points)
- Transaction Processing API (10 points)
  - All endpoints working correctly
  - Business rules properly implemented
  - Error handling comprehensive
- Fraud Detection (10 points)
  - Multi-layer detection working
  - AI integration functional
  - Risk scoring accurate
- Real-time Analytics (10 points)
  - Dashboard updates live
  - Metrics calculated correctly
  - Historical data available

#### 2. Architecture Quality (25 points)
- Microservices Design (10 points)
  - Clear service boundaries
  - Proper API contracts
  - Loose coupling
- Scalability (8 points)
  - Horizontal scaling configured
  - Performance under load
  - Resource efficiency
- Security (7 points)
  - Authentication implemented
  - Data encrypted
  - Secrets managed properly

#### 3. AI Integration (20 points)
- GitHub Copilot Usage (5 points)
  - Evidence in commit history
  - Complex code generation
  - Productivity gains
- Azure OpenAI (10 points)
  - Proper integration
  - Effective prompts
  - Meaningful insights
- Innovation (5 points)
  - Creative AI applications
  - Beyond basic requirements

#### 4. Code Quality (15 points)
- Clean Code (5 points)
  - Readable and maintainable
  - Proper documentation
  - Consistent style
- Testing (5 points)
  - Unit tests present
  - Integration tests working
  - Good coverage
- Error Handling (5 points)
  - Graceful failures
  - Meaningful messages
  - Proper logging

#### 5. Innovation Bonus (10 points)
- Beyond Requirements (5 points)
  - Additional features
  - Creative solutions
  - Technical excellence
- Business Value (5 points)
  - Cost optimizations
  - Performance improvements
  - User experience

### Helpful Commands

```bash
# Quick health check
curl -s http://localhost:8001/health | jq

# View logs
kubectl logs -f deployment/transaction-service -n fintech-challenge

# Get metrics
kubectl top pods -n fintech-challenge

# Test transaction
./scripts/test-transaction.sh

# Run all tests
pytest tests/ -v --cov=src --cov-report=html
```

## 🎉 Good Luck!

You have all the tools and knowledge needed to succeed. Trust your training, leverage AI effectively, and build something amazing!

**Remember**: The goal is not perfection but a working solution that demonstrates your mastery of AI-powered development.

**Start Time**: When you run `./scripts/start-challenge.sh`  
**End Time**: Exactly 3 hours later  

May your code compile, your tests pass, and your AI be helpful! 🚀
