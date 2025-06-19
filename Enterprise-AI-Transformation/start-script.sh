#!/bin/bash
# Module 22 - Super Challenge Setup Script
# This script sets up the complete challenge environment

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Challenge configuration
CHALLENGE_NAME="super-challenge"
CHALLENGE_ID=$(date +%s)
START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
TIME_LIMIT_SECONDS=10800  # 3 hours

# Functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_banner() {
    clear
    cat << "EOF"
    _____ _   _ ____  _____ ____     ____ _   _    _    _     _     _____ _   _  ____ _____ 
   / ____| | | |  _ \| ____|  _ \   / ___| | | |  / \  | |   | |   | ____| \ | |/ ___| ____|
  | (___ | | | | |_) |  _| | |_) | | |   | |_| | / _ \ | |   | |   |  _| |  \| | |  _|  _|  
   \___ \| | | |  __/| |___|  _ <  | |___|  _  |/ ___ \| |___| |___| |___| |\  | |_| | |___ 
   ____) | |_| | |   |_____|_| \_\  \____|_| |_/_/   \_\_____|_____|_____|_| \_|\____|_____|
  |_____/ \___/|_|                                                                           

                    MODULE 22: AI-POWERED ENTERPRISE TRANSFORMATION
                              TIME LIMIT: 3 HOURS
                              AZURE-FOCUSED IMPLEMENTATION
                              
EOF
}

check_prerequisites() {
    log "Checking prerequisites..."
    
    local missing=()
    
    # Check required tools
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v kubectl >/dev/null 2>&1 || missing+=("kubectl")
    command -v python3 >/dev/null 2>&1 || missing+=("python3")
    command -v npm >/dev/null 2>&1 || missing+=("npm")
    command -v az >/dev/null 2>&1 || missing+=("az")
    command -v terraform >/dev/null 2>&1 || missing+=("terraform")
    command -v code >/dev/null 2>&1 || missing+=("vscode")
    
    if [ ${#missing[@]} -ne 0 ]; then
        error "Missing required tools: ${missing[*]}"
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if (( $(echo "$python_version < 3.11" | bc -l) )); then
        error "Python 3.11+ required (found $python_version)"
    fi
    
    # Check Docker daemon
    if ! docker info >/dev/null 2>&1; then
        error "Docker daemon is not running"
    fi
    
    # Check Azure login
    if ! az account show >/dev/null 2>&1; then
        warning "Not logged into Azure. Run 'az login' to deploy to cloud"
    else
        success "Azure CLI authenticated"
        AZURE_SUBSCRIPTION=$(az account show --query name -o tsv)
        log "Using subscription: $AZURE_SUBSCRIPTION"
    fi
    
    # Check GitHub Copilot
    if code --list-extensions | grep -q "GitHub.copilot"; then
        success "GitHub Copilot extension found"
    else
        warning "GitHub Copilot extension not found in VS Code"
    fi
    
    success "All prerequisites satisfied"
}

setup_workspace() {
    log "Setting up challenge workspace..."
    
    # Create directory structure
    mkdir -p {src,tests,infrastructure,docs,scripts,legacy-code,sample-data}
    mkdir -p src/{transaction-service,fraud-service,analytics-service,dashboard,shared}
    mkdir -p infrastructure/{terraform,k8s,docker,scripts}
    mkdir -p tests/{unit,integration,e2e,performance,security}
    mkdir -p docs/{api,architecture,deployment}
    
    # Create Python package structure
    touch src/__init__.py
    touch src/transaction-service/__init__.py
    touch src/fraud-service/__init__.py
    touch src/analytics-service/__init__.py
    touch src/shared/__init__.py
    
    success "Workspace created"
}

generate_starter_code() {
    log "Generating starter code..."
    
    # Shared models and schemas
    cat > src/shared/models.py << 'EOF'
"""Shared data models for all services"""
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class TransactionType(str, Enum):
    DOMESTIC = "DM"
    INTERNATIONAL = "IN"
    WIRE_TRANSFER = "WT"
    
class AccountType(str, Enum):
    CHECKING = "C"
    SAVINGS = "S"
    BUSINESS = "B"
    INVESTMENT = "I"

class TransactionRequest(BaseModel):
    transaction_id: Optional[str] = Field(default_factory=lambda: f"TXN{datetime.utcnow().timestamp()}")
    from_account: str = Field(..., regex="^[0-9]{10}$")
    to_account: str = Field(..., regex="^[0-9]{10}$")
    amount: Decimal = Field(..., gt=0, le=1000000)
    currency: str = Field(default="USD", regex="^[A-Z]{3}$")
    transaction_type: TransactionType = Field(default=TransactionType.DOMESTIC)
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, any]] = None
    
    @validator('from_account', 'to_account')
    def validate_account_format(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Account number must be exactly 10 digits')
        return v
    
    @validator('from_account')
    def validate_different_accounts(cls, v, values):
        if 'to_account' in values and v == values['to_account']:
            raise ValueError('Cannot transfer to same account')
        return v

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    processing_time: Optional[float] = None
    risk_score: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FraudCheckRequest(BaseModel):
    transaction: TransactionRequest
    account_history: Optional[Dict] = None
    device_info: Optional[Dict] = None
    location: Optional[Dict] = None

class FraudCheckResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    risk_factors: List[str]
    recommendation: str
    confidence: float = Field(..., ge=0, le=1)
    explanation: Optional[str] = None
EOF

    # Transaction Service starter
    cat > src/transaction-service/main.py << 'EOF'
"""
Transaction Service - Modernized from TRANSACTION-PROCESSOR.cob
TODO: Complete the implementation following the business rules
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, List
import asyncio
import logging
import os

# Import shared models
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.models import TransactionRequest, TransactionResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Transaction Service",
    version="2.0.0",
    description="Modernized transaction processing system from COBOL"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Initialize database connection
# TODO: Initialize Redis cache
# TODO: Initialize event publisher
# TODO: Initialize fraud service client

@app.post("/api/v1/transactions", response_model=TransactionResponse)
async def process_transaction(
    transaction: TransactionRequest,
    background_tasks: BackgroundTasks
):
    """
    Process a financial transaction
    
    TODO: Implement the following steps:
    1. Validate transaction against business rules
    2. Check for duplicate (idempotency)
    3. Call fraud detection service
    4. Lock accounts and check balances
    5. Execute transaction atomically
    6. Update account balances
    7. Publish transaction event
    8. Update COBOL system (async)
    9. Return response
    
    Business Rules from COBOL:
    - Minimum amount: $0.01
    - Maximum single transaction: $1,000,000
    - Daily limit per account: $5,000,000
    - VIP customers have no fees
    - Business accounts can overdraft up to $100,000
    """
    logger.info(f"Processing transaction: {transaction.transaction_id}")
    
    # TODO: Your implementation here
    # Hint: Use GitHub Copilot to help implement each step
    # Start by typing: "# Step 1: Validate transaction against business rules"
    
    # Placeholder response
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        status="pending",
        message="Transaction received - TODO: Complete implementation",
        processing_time=0.0,
        risk_score=0
    )

@app.get("/api/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    """Get transaction status by ID"""
    # TODO: Implement transaction lookup
    return {"transaction_id": transaction_id, "status": "not_implemented"}

@app.get("/api/v1/accounts/{account_id}")
async def get_account(account_id: str):
    """Get account details"""
    # TODO: Implement account lookup
    return {
        "account_id": account_id,
        "balance": 0.0,
        "available_balance": 0.0,
        "account_type": "C",
        "status": "active"
    }

@app.post("/api/v1/accounts/{account_id}/balance")
async def update_balance(account_id: str, amount: Decimal, operation: str):
    """Update account balance (for testing)"""
    # TODO: Implement balance update
    return {"account_id": account_id, "new_balance": 0.0}

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
async def readiness_check():
    """Readiness check - verify all dependencies"""
    # TODO: Check database connection
    # TODO: Check cache connection
    # TODO: Check event publisher
    return {"status": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
EOF

    # Fraud Service starter
    cat > src/fraud-service/main.py << 'EOF'
"""
AI-Powered Fraud Detection Service
TODO: Implement multi-layer fraud detection with Azure OpenAI
"""
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import os

# Import shared models
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.models import TransactionRequest, FraudCheckResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fraud Detection Service",
    version="2.0.0",
    description="AI-powered fraud detection system using Azure OpenAI"
)

# TODO: Initialize Azure OpenAI client
# TODO: Initialize rule engine
# TODO: Initialize pattern analyzer
# TODO: Initialize ML model

@app.post("/api/v1/analyze", response_model=FraudCheckResponse)
async def analyze_transaction(transaction: TransactionRequest) -> FraudCheckResponse:
    """
    Analyze transaction for fraud using multiple layers:
    
    1. Rule-based checks (from COBOL logic)
    2. ML pattern detection
    3. AI deep analysis with Azure OpenAI
    4. Combine scores for final decision
    
    TODO: Implement each layer
    """
    logger.info(f"Analyzing transaction: {transaction.transaction_id}")
    
    # TODO: Layer 1 - Rule-based checks
    # Implement velocity check, amount anomaly, sanctions check, etc.
    
    # TODO: Layer 2 - ML pattern detection
    # Use pre-trained model or simple heuristics
    
    # TODO: Layer 3 - AI analysis with Azure OpenAI
    # Create prompt with transaction context
    # Call Azure OpenAI for intelligent analysis
    
    # TODO: Combine all scores
    # Weight each layer appropriately
    
    # Placeholder response
    return FraudCheckResponse(
        risk_score=10,
        risk_level="low",
        risk_factors=[],
        recommendation="allow",
        confidence=0.85,
        explanation="Placeholder - implement fraud detection logic"
    )

@app.get("/api/v1/rules")
async def get_active_rules():
    """Get list of active fraud detection rules"""
    # TODO: Return configured rules
    return {
        "rules": [
            {"name": "velocity_check", "enabled": True},
            {"name": "amount_anomaly", "enabled": True},
            {"name": "sanctions_check", "enabled": True}
        ]
    }

@app.post("/api/v1/train")
async def train_model(labeled_transactions: List[Dict]):
    """Train or update fraud detection model with labeled data"""
    # TODO: Implement model training/updating
    return {"status": "training_not_implemented", "message": "TODO"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fraud-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
EOF

    # Analytics Service starter
    cat > src/analytics-service/main.py << 'EOF'
"""
Real-time Analytics Service
TODO: Implement stream processing and WebSocket updates
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import asyncio
import json
import logging
from datetime import datetime

app = FastAPI(
    title="Analytics Service",
    version="2.0.0",
    description="Real-time transaction analytics with WebSocket support"
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# TODO: Initialize Event Hub consumer
# TODO: Initialize Cosmos DB client
# TODO: Initialize metrics storage

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics"""
    await manager.connect(websocket)
    
    try:
        # Send initial metrics
        initial_metrics = {
            "type": "initial",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "totalTransactions": 0,
                "totalVolume": 0,
                "fraudBlocked": 0,
                "avgResponseTime": 0
            }
        }
        await websocket.send_text(json.dumps(initial_metrics))
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/v1/metrics/summary")
async def get_metrics_summary():
    """Get current metrics summary"""
    # TODO: Implement metrics aggregation
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "totalTransactions": 0,
            "totalVolume": 0.0,
            "fraudBlocked": 0,
            "avgResponseTime": 0.0
        }
    }

@app.get("/api/v1/metrics/historical")
async def get_historical_metrics(start_date: str, end_date: str):
    """Get historical metrics from Cosmos DB"""
    # TODO: Query Cosmos DB for historical data
    return {
        "period": f"{start_date} to {end_date}",
        "data": []
    }

# TODO: Implement event processing
# async def process_events():
#     """Process events from Event Hub"""
#     pass

@app.on_event("startup")
async def startup_event():
    """Start event processing on startup"""
    # TODO: Start consuming from Event Hub
    # asyncio.create_task(process_events())
    pass

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "analytics-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
EOF

    # Dashboard starter (package.json)
    cat > src/dashboard/package.json << 'EOF'
{
  "name": "transaction-dashboard",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.3",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.15.10",
    "@mui/material": "^5.15.10",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.4",
    "typescript": "^5.3.3",
    "web-vitals": "^3.5.2"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "react-scripts": "5.0.1"
  }
}
EOF

    # Create requirements.txt
    cat > requirements.txt << 'EOF'
# Core Framework
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.3
python-multipart==0.0.6

# AI/ML
openai==1.10.0
langchain==0.1.0
langchain-community==0.0.10
tiktoken==0.5.2

# Database
sqlalchemy==2.0.25
asyncpg==0.29.0
psycopg2-binary==2.9.9
redis==5.0.1
motor==3.3.2

# Azure SDKs
azure-identity==1.15.0
azure-keyvault-secrets==4.7.0
azure-eventhub==5.11.5
azure-cosmos==4.5.1
azure-storage-blob==12.19.0
azure-monitor-opentelemetry==1.2.0

# Event Streaming
aiokafka==0.10.0
confluent-kafka==2.3.0

# API & Integration
httpx==0.26.0
aiohttp==3.9.1
websockets==12.0

# Data Processing
pandas==2.1.4
numpy==1.26.3

# Monitoring & Logging
prometheus-client==0.19.0
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
structlog==24.1.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.2
pytest-cov==4.1.0
locust==2.20.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==41.0.7

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
click==8.1.7
rich==13.7.0

# Development
black==23.12.1
ruff==0.1.9
mypy==1.8.0
EOF

    success "Starter code generated"
}

create_infrastructure_templates() {
    log "Creating infrastructure templates..."
    
    # Docker Compose for local development
    cat > docker-compose.yml << 'EOF'
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: transactions
      POSTGRES_USER: challenge
      POSTGRES_PASSWORD: challenge123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U challenge"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  azurite:
    image: mcr.microsoft.com/azure-storage/azurite
    ports:
      - "10000:10000"  # Blob
      - "10001:10001"  # Queue
      - "10002:10002"  # Table
    volumes:
      - azurite_data:/data
  
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - kafka_data:/var/lib/kafka/data
      
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data
      - zookeeper_logs:/var/lib/zookeeper/log

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: challenge
      MONGO_INITDB_ROOT_PASSWORD: challenge123
      MONGO_INITDB_DATABASE: analytics
    volumes:
      - mongo_data:/data/db

volumes:
  postgres_data:
  redis_data:
  azurite_data:
  kafka_data:
  zookeeper_data:
  zookeeper_logs:
  mongo_data:
EOF

    # Terraform main configuration
    cat > infrastructure/terraform/main.tf << 'EOF'
# Azure Provider Configuration
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.47.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "challenge"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus2"
}

variable "unique_suffix" {
  description = "Unique suffix for globally unique resources"
  type        = string
  default     = ""
}

# Local variables
locals {
  resource_prefix = "sc-${var.environment}"
  unique_suffix   = var.unique_suffix != "" ? var.unique_suffix : random_string.unique.result
  tags = {
    Environment = var.environment
    Project     = "SuperChallenge"
    Module      = "22"
    ManagedBy   = "Terraform"
  }
}

# Random suffix for unique names
resource "random_string" "unique" {
  length  = 6
  special = false
  upper   = false
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${local.resource_prefix}"
  location = var.location
  tags     = local.tags
}

# TODO: Add the following resources:
# 1. Azure Kubernetes Service (AKS)
# 2. Azure Container Registry (ACR)
# 3. Azure OpenAI Service
# 4. Azure Event Hubs
# 5. Azure Cosmos DB
# 6. Azure Key Vault
# 7. Azure Application Insights
# 8. Virtual Network and Subnets
# 9. Network Security Groups
# 10. Managed Identities

# Example AKS cluster (starter)
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${local.resource_prefix}-${local.unique_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks-${local.resource_prefix}"
  
  default_node_pool {
    name                = "default"
    node_count          = 3
    vm_size             = "Standard_D4s_v5"
    enable_auto_scaling = true
    min_count           = 3
    max_count           = 10
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  tags = local.tags
}

# Output values
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive = true
}
EOF

    # Kubernetes deployment template
    cat > infrastructure/k8s/namespace.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: super-challenge
  labels:
    name: super-challenge
    module: "22"
EOF

    success "Infrastructure templates created"
}

create_legacy_cobol() {
    log "Creating legacy COBOL files..."
    
    # Main transaction processor
    cat > legacy-code/TRANSACTION-PROCESSOR.cob << 'EOF'
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TRANSACTION-PROCESSOR.
       AUTHOR. LEGACYFINANCE-TEAM.
       DATE-WRITTEN. 1985-03-15.
      *****************************************************************
      * TRANSACTION PROCESSING SYSTEM                                 *
      * HANDLES FINANCIAL TRANSACTIONS WITH FRAUD DETECTION           *
      *****************************************************************
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-370.
       OBJECT-COMPUTER. IBM-370.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-TRANSACTION-RECORD.
           05  TR-ID               PIC X(20).
           05  TR-DATE             PIC 9(8).
           05  TR-TIME             PIC 9(6).
           05  TR-FROM-ACCT        PIC 9(10).
           05  TR-TO-ACCT          PIC 9(10).
           05  TR-AMOUNT           PIC 9(13)V99.
           05  TR-CURRENCY         PIC X(3).
           05  TR-TYPE             PIC X(2).
               88  DOMESTIC        VALUE 'DM'.
               88  INTERNATIONAL   VALUE 'IN'.
               88  WIRE-TRANSFER   VALUE 'WT'.
           05  TR-STATUS           PIC X.
               88  PENDING         VALUE 'P'.
               88  COMPLETED       VALUE 'C'.
               88  FAILED          VALUE 'F'.
               88  BLOCKED         VALUE 'B'.
               
       01  WS-ACCOUNT-RECORD.
           05  ACCT-NUMBER         PIC 9(10).
           05  ACCT-TYPE           PIC X.
               88  CHECKING        VALUE 'C'.
               88  SAVINGS         VALUE 'S'.
               88  BUSINESS        VALUE 'B'.
               88  INVESTMENT      VALUE 'I'.
           05  ACCT-BALANCE        PIC S9(13)V99 COMP-3.
           05  ACCT-DAILY-LIMIT    PIC 9(13)V99.
           05  ACCT-STATUS         PIC X.
               88  ACTIVE          VALUE 'A'.
               88  SUSPENDED       VALUE 'S'.
               88  CLOSED          VALUE 'C'.
               
       01  WS-BUSINESS-RULES.
           05  MIN-AMOUNT          PIC 9(13)V99 VALUE 0.01.
           05  MAX-SINGLE-TXN      PIC 9(13)V99 VALUE 1000000.00.
           05  DAILY-LIMIT         PIC 9(13)V99 VALUE 5000000.00.
           05  OVERDRAFT-LIMIT     PIC 9(13)V99 VALUE 100000.00.
           
       01  WS-FEES.
           05  DOM-FEE            PIC 9(5)V99 VALUE 2.50.
           05  INTL-FEE           PIC 9(5)V99 VALUE 25.00.
           05  WIRE-FEE           PIC 9(5)V99 VALUE 35.00.
           
       PROCEDURE DIVISION.
       0000-MAIN-CONTROL.
           PERFORM 1000-VALIDATE-TRANSACTION
           PERFORM 2000-CHECK-FRAUD
           PERFORM 3000-PROCESS-TRANSACTION
           PERFORM 4000-UPDATE-ACCOUNTS
           STOP RUN.
EOF

    # Business rules documentation
    cat > docs/business-rules.md << 'EOF'
# Business Rules - LegacyFinance Inc.

## Transaction Processing Rules

### 1. Transaction Validation
- **Minimum Amount**: $0.01
- **Maximum Single Transaction**: $1,000,000
- **Daily Limit per Account**: $5,000,000
- **Required Fields**: account_from, account_to, amount, currency

### 2. Account Rules
- **Account Format**: 10 digits (XXXXXXXXXX)
- **Account Types**: 
  - Checking (C): Standard consumer account
  - Savings (S): Interest-bearing account
  - Business (B): Commercial account with overdraft
  - Investment (I): Trading account
- **Overdraft Protection**: Only Business accounts up to $100,000
- **Minimum Balance**: 
  - Checking: $0
  - Savings: $100
  - Business: $1,000
  - Investment: $10,000

### 3. Fee Structure
- Domestic Transfer (DM): $2.50
- International Transfer (IN): $25.00
- Wire Transfer (WT): $35.00
- VIP Customers: No fees
- Volume Discounts:
  - 100+ transactions/month: 10% discount
  - 500+ transactions/month: 20% discount
  - 1000+ transactions/month: 30% discount

### 4. Fraud Detection Thresholds
- Velocity: Max 50 transactions per hour
- Amount Anomaly: 300% above average triggers review
- Geographic: Multiple countries in 1 hour = high risk
- Time-based: 2 AM - 5 AM local = +15 risk points
- Risk Score Actions:
  - 0-30: Auto-approve
  - 31-60: Additional verification
  - 61-80: Manual review required
  - 81+: Block and investigate

### 5. Performance Requirements
- Transaction Processing: < 100ms (p99)
- Fraud Check: < 500ms
- End-to-end: < 200ms average
- Throughput: 10,000 TPS minimum
- Availability: 99.99% uptime
EOF

    success "Legacy COBOL files created"
}

create_sample_data() {
    log "Creating sample data..."
    
    # Test transactions
    cat > sample-data/test-transactions.json << 'EOF'
[
  {
    "from_account": "1234567890",
    "to_account": "0987654321",
    "amount": 100.00,
    "currency": "USD",
    "transaction_type": "DM",
    "metadata": {
      "description": "Normal domestic transfer",
      "expected_result": "success"
    }
  },
  {
    "from_account": "1111111111",
    "to_account": "2222222222",
    "amount": 50000.00,
    "currency": "USD",
    "transaction_type": "WT",
    "metadata": {
      "description": "Large wire transfer",
      "expected_result": "review_required"
    }
  },
  {
    "from_account": "3333333333",
    "to_account": "4444444444",
    "amount": 999999.00,
    "currency": "EUR",
    "transaction_type": "IN",
    "metadata": {
      "description": "Suspicious international transfer",
      "expected_result": "blocked"
    }
  },
  {
    "from_account": "5555555555",
    "to_account": "6666666666",
    "amount": 0.005,
    "currency": "USD",
    "transaction_type": "DM",
    "metadata": {
      "description": "Below minimum amount",
      "expected_result": "validation_error"
    }
  },
  {
    "from_account": "7777777777",
    "to_account": "7777777777",
    "amount": 100.00,
    "currency": "USD",
    "transaction_type": "DM",
    "metadata": {
      "description": "Same account transfer",
      "expected_result": "validation_error"
    }
  }
]
EOF

    # Test accounts
    cat > sample-data/test-accounts.json << 'EOF'
[
  {
    "account_number": "1234567890",
    "account_type": "C",
    "balance": 10000.00,
    "available_balance": 10000.00,
    "daily_limit": 5000000.00,
    "daily_used": 0.00,
    "customer_id": "CUST000001",
    "is_vip": false,
    "risk_score": 10
  },
  {
    "account_number": "0987654321",
    "account_type": "S",
    "balance": 50000.00,
    "available_balance": 50000.00,
    "daily_limit": 5000000.00,
    "daily_used": 0.00,
    "customer_id": "CUST000002",
    "is_vip": true,
    "risk_score": 5
  },
  {
    "account_number": "1111111111",
    "account_type": "B",
    "balance": 100000.00,
    "available_balance": 200000.00,
    "daily_limit": 5000000.00,
    "daily_used": 0.00,
    "customer_id": "BUSI000001",
    "is_vip": true,
    "risk_score": 15,
    "overdraft_limit": 100000.00
  }
]
EOF

    success "Sample data created"
}

create_helper_scripts() {
    log "Creating helper scripts..."
    
    # Timer script
    cat > scripts/start-challenge.sh << 'EOF'
#!/bin/bash
# Start the challenge timer

START_TIME=$(date +%s)
END_TIME=$((START_TIME + 10800))  # 3 hours

echo "🚀 SUPER CHALLENGE STARTED!"
echo "Start time: $(date)"
echo "End time: $(date -d @$END_TIME)"
echo ""
echo "Timer running..."

while true; do
    CURRENT_TIME=$(date +%s)
    REMAINING=$((END_TIME - CURRENT_TIME))
    
    if [ $REMAINING -le 0 ]; then
        echo -e "\n\n⏰ TIME'S UP! Challenge completed."
        echo "Please submit your solution now."
        break
    fi
    
    HOURS=$((REMAINING / 3600))
    MINUTES=$(((REMAINING % 3600) / 60))
    SECONDS=$((REMAINING % 60))
    
    printf "\rTime remaining: %02d:%02d:%02d" $HOURS $MINUTES $SECONDS
    sleep 1
done
EOF
    chmod +x scripts/start-challenge.sh
    
    # Environment setup script
    cat > scripts/setup-env.sh << 'EOF'
#!/bin/bash
# Set up environment variables

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env with your Azure credentials"
fi

# Source environment variables
set -a
source .env
set +a

# Export for child processes
export AZURE_SUBSCRIPTION_ID
export AZURE_TENANT_ID
export AZURE_OPENAI_ENDPOINT
export AZURE_OPENAI_KEY

echo "Environment variables loaded"
EOF
    chmod +x scripts/setup-env.sh
    
    # Quick test script
    cat > scripts/test-services.sh << 'EOF'
#!/bin/bash
# Test all services are running

echo "Testing services..."

# Transaction Service
echo -n "Transaction Service: "
curl -s http://localhost:8001/health >/dev/null 2>&1 && echo "✓" || echo "✗"

# Fraud Service
echo -n "Fraud Service: "
curl -s http://localhost:8002/health >/dev/null 2>&1 && echo "✓" || echo "✗"

# Analytics Service
echo -n "Analytics Service: "
curl -s http://localhost:8003/health >/dev/null 2>&1 && echo "✓" || echo "✗"

# Dashboard
echo -n "Dashboard: "
curl -s http://localhost:3000 >/dev/null 2>&1 && echo "✓" || echo "✗"

# Databases
echo -n "PostgreSQL: "
docker exec $(docker ps -qf "name=postgres") pg_isready >/dev/null 2>&1 && echo "✓" || echo "✗"

echo -n "Redis: "
docker exec $(docker ps -qf "name=redis") redis-cli ping >/dev/null 2>&1 && echo "✓" || echo "✗"

echo -n "MongoDB: "
docker exec $(docker ps -qf "name=mongodb") mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1 && echo "✓" || echo "✗"
EOF
    chmod +x scripts/test-services.sh
    
    success "Helper scripts created"
}

create_env_template() {
    log "Creating environment template..."
    
    cat > .env.example << 'EOF'
# Challenge Environment Variables
CHALLENGE_ID=super-challenge
ENVIRONMENT=development

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_RESOURCE_GROUP=rg-super-challenge

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Database
DATABASE_URL=postgresql://challenge:challenge123@localhost:5432/transactions
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://challenge:challenge123@localhost:27017/analytics

# Event Hub
EVENT_HUB_CONNECTION_STRING=Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=your-key
EVENT_HUB_NAME=transactions

# Cosmos DB
COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_KEY=your-cosmos-key
COSMOS_DATABASE=analytics

# Application Insights
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=your-key;IngestionEndpoint=https://your-region.in.applicationinsights.azure.com/

# Feature Flags
ENABLE_FRAUD_CHECK=true
ENABLE_REAL_TIME_ANALYTICS=true
ENABLE_AI_ENHANCEMENT=true

# Performance Settings
MAX_CONCURRENT_TRANSACTIONS=1000
CACHE_TTL_SECONDS=300
CONNECTION_POOL_SIZE=20
EOF

    success "Environment template created"
}

setup_vscode() {
    log "Setting up VS Code workspace..."
    
    # VS Code workspace settings
    mkdir -p .vscode
    
    cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".coverage": true,
        "htmlcov": true
    },
    "github.copilot.enable": {
        "*": true,
        "yaml": true,
        "plaintext": true,
        "markdown": true,
        "python": true,
        "typescript": true,
        "typescriptreact": true
    }
}
EOF

    # VS Code launch configuration
    cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Transaction Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.transaction-service.main:app",
                "--reload",
                "--port", "8001"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Fraud Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.fraud-service.main:app",
                "--reload",
                "--port", "8002"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Analytics Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.analytics-service.main:app",
                "--reload",
                "--port", "8003"
            ],
            "jinja": true,
            "justMyCode": false
        }
    ]
}
EOF

    # VS Code recommended extensions
    cat > .vscode/extensions.json << 'EOF'
{
    "recommendations": [
        "github.copilot",
        "github.copilot-chat",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "hashicorp.terraform",
        "ms-vscode.azure-account",
        "ms-azuretools.vscode-azurefunctions",
        "ms-toolsai.jupyter",
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint"
    ]
}
EOF

    success "VS Code workspace configured"
}

final_setup() {
    log "Finalizing setup..."
    
    # Create Python virtual environment
    python3 -m venv venv
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.env

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/
.hypothesis/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
*.log
docker-compose.override.yml

# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build outputs
dist/
build/
*.egg-info/
.cache/

# Azure
.azure/
*.pfx

# Secrets
*.pem
*.key
secrets/
EOF

    # Create README for the challenge
    cat > README.md << 'EOF'
# Super Challenge - AI-Powered Enterprise Transformation

## 🚀 Quick Start

1. **Verify Prerequisites**
   ```bash
   ./scripts/validate-prerequisites.sh
   ```

2. **Set Up Environment**
   ```bash
   # Copy and edit environment variables
   cp .env.example .env
   # Edit .env with your Azure credentials
   
   # Install Python dependencies
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Start Local Services**
   ```bash
   docker-compose up -d
   ./scripts/test-services.sh
   ```

4. **Start the Challenge**
   ```bash
   ./scripts/start-challenge.sh
   ```

## 📁 Project Structure

```
.
├── src/                    # Service implementations
│   ├── transaction-service/
│   ├── fraud-service/
│   ├── analytics-service/
│   └── dashboard/
├── infrastructure/         # IaC and deployment
│   ├── terraform/
│   ├── k8s/
│   └── docker/
├── tests/                  # Test suites
├── legacy-code/           # COBOL programs
├── sample-data/           # Test data
├── scripts/               # Helper scripts
└── docs/                  # Documentation
```

## 🎯 Your Mission

Transform LegacyFinance's COBOL system into a modern cloud-native solution with:
- Microservices architecture
- AI-powered fraud detection
- Real-time analytics
- 99.99% uptime
- < 100ms transaction processing

## ⏰ Time Limit: 3 Hours

Good luck! 🚀
EOF

    success "Setup complete!"
}

# Main execution
main() {
    print_banner
    
    echo -e "${BOLD}Setting up Module 22 - Super Challenge Environment...${NC}\n"
    
    check_prerequisites
    setup_workspace
    generate_starter_code
    create_infrastructure_templates
    create_legacy_cobol
    create_sample_data
    create_helper_scripts
    create_env_template
    setup_vscode
    final_setup
    
    echo -e "\n${GREEN}${BOLD}✨ CHALLENGE ENVIRONMENT READY! ✨${NC}\n"
    
    cat << EOF
${BOLD}Next Steps:${NC}
1. Review the business rules: ${BLUE}docs/business-rules.md${NC}
2. Analyze the COBOL code: ${BLUE}legacy-code/TRANSACTION-PROCESSOR.cob${NC}
3. Update your Azure credentials: ${BLUE}.env${NC}
4. Start local services: ${BLUE}docker-compose up -d${NC}
5. Activate Python environment: ${BLUE}source venv/bin/activate${NC}
6. Start the timer: ${BLUE}./scripts/start-challenge.sh${NC}

${BOLD}Key Resources:${NC}
- Starter code in ${BLUE}src/${NC}
- Infrastructure templates in ${BLUE}infrastructure/${NC}
- Test data in ${BLUE}sample-data/${NC}
- Helper scripts in ${BLUE}scripts/${NC}

${YELLOW}${BOLD}Remember:${NC}
- You have exactly 3 hours from when you start the timer
- Focus on working solution first, optimize later
- Use GitHub Copilot extensively
- Test as you go
- Prepare your demo

${GREEN}${BOLD}Good luck! May your code be bug-free and your AI helpful! 🚀${NC}
EOF
}

# Run main function
main "$@"
