# Super Challenge - Prerequisites

## 📋 Required Before Starting


#### 2. Software Installation Checklist

##### Core Development Tools
```bash
# Verify installations
git --version                    # 2.40+
python --version                 # 3.11+
node --version                   # 20.0+
dotnet --version                 # 8.0+
docker --version                 # 24.0+
kubectl version --client         # 1.28+
terraform --version              # 1.6+
az --version                     # 2.55+
```

##### IDE and Extensions
- **Visual Studio Code** (latest)
  - GitHub Copilot
  - GitHub Copilot Chat
  - Python
  - Pylance
  - Docker
  - Kubernetes
  - Azure Tools
  - Terraform
  - Remote - SSH
  - Live Share

##### Python Environment
```bash
# Create virtual environment
python -m venv challenge-env

# Activate (Linux/Mac)
source challenge-env/bin/activate

# Activate (Windows)
challenge-env\Scripts\activate

# Install base packages
pip install --upgrade pip
pip install fastapi uvicorn httpx pytest pytest-asyncio
pip install azure-identity azure-keyvault-secrets
pip install langchain openai redis asyncpg
pip install pandas numpy matplotlib
```

##### Node.js Environment
```bash
# Install global packages
npm install -g typescript
npm install -g @azure/static-web-apps-cli
npm install -g create-react-app
```

#### 3. Cloud Accounts and Access

##### Azure Subscription
- **Required Services:**
  - Azure Kubernetes Service (AKS)
  - Azure Container Registry (ACR)
  - Azure OpenAI Service
  - Azure Event Hubs
  - Azure Cosmos DB
  - Azure Key Vault
  - Azure Monitor
  - Application Insights

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "Your-Subscription-Name"

# Verify access
az account show

# Create resource group for challenge
az group create --name rg-super-challenge --location eastus2
```

##### GitHub Account
- GitHub Copilot subscription (Individual or Business)
- Personal Access Token with scopes:
  - repo
  - workflow
  - packages
  - admin:org (if using GitHub Packages)

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set up GitHub CLI (optional but recommended)
gh auth login
```

#### 4. Local Development Services

##### Docker Desktop Configuration
```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "features": {
    "buildkit": true
  },
  "kubernetes": {
    "enabled": true
  }
}
```

##### Local Kubernetes Setup
```bash
# Enable Kubernetes in Docker Desktop
# OR use minikube
minikube start --cpus=4 --memory=8192

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

#### 5. Pre-Challenge Validation

Run this script to validate your environment:

```bash
#!/bin/bash
# save as validate-prerequisites.sh

echo "🔍 Validating Module 22 Prerequisites..."

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check command
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 found: $(command -v $1)"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        return 1
    fi
}

# Function to check version
check_version() {
    local cmd=$1
    local flag=$2
    local required=$3
    local version=$($cmd $flag 2>&1 | head -n 1)
    echo -e "${GREEN}✓${NC} $cmd version: $version (required: $required+)"
}

echo -e "\n📦 Checking Core Tools..."
check_command git && check_version git --version "2.40"
check_command python && check_version python --version "3.11"
check_command node && check_version node --version "20.0"
check_command docker && check_version docker --version "24.0"
check_command kubectl && check_version kubectl "version --client --short" "1.28"
check_command terraform && check_version terraform --version "1.6"
check_command az && check_version az --version "2.55"

echo -e "\n☁️ Checking Azure Access..."
if az account show &> /dev/null; then
    echo -e "${GREEN}✓${NC} Azure CLI authenticated"
    echo "  Subscription: $(az account show --query name -o tsv)"
else
    echo -e "${RED}✗${NC} Not logged into Azure"
fi

echo -e "\n🐙 Checking GitHub..."
if gh auth status &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub CLI authenticated"
else
    echo -e "${RED}✗${NC} GitHub CLI not authenticated (optional)"
fi

echo -e "\n🐳 Checking Docker..."
if docker info &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker daemon running"
    echo "  Containers: $(docker ps -q | wc -l) running"
else
    echo -e "${RED}✗${NC} Docker daemon not running"
fi

echo -e "\n☸️ Checking Kubernetes..."
if kubectl cluster-info &> /dev/null; then
    echo -e "${GREEN}✓${NC} Kubernetes cluster accessible"
    echo "  Context: $(kubectl config current-context)"
else
    echo -e "${RED}✗${NC} No Kubernetes cluster found"
fi

echo -e "\n🔧 Checking VS Code Extensions..."
code --list-extensions | grep -q "GitHub.copilot" && \
    echo -e "${GREEN}✓${NC} GitHub Copilot installed" || \
    echo -e "${RED}✗${NC} GitHub Copilot not installed"

echo -e "\n✅ Prerequisite check complete!"
```

### 🚀 Quick Start Commands

Once prerequisites are met, use these commands to begin:

```bash
# 1. Clone the challenge repository
git clone https://github.com/workshop/module-22-super-challenge.git
cd module-22-super-challenge

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your values

# 4. Start local services
docker-compose up -d

# 5. Verify setup
./scripts/verify-setup.sh

# 6. Start the challenge timer
./scripts/start-challenge.sh
```

### 📝 Pre-Challenge Checklist

Before starting the 3-hour challenge:

- [ ] All prerequisite software installed and verified
- [ ] Azure subscription with required services enabled
- [ ] GitHub Copilot working in VS Code
- [ ] Local Docker and Kubernetes running
- [ ] Sample COBOL files downloaded
- [ ] Business rules document reviewed
- [ ] Architecture patterns familiar
- [ ] Backup internet connection available
- [ ] Quiet environment for 3 hours
- [ ] Caffeine and snacks ready 😊

### 🆘 Troubleshooting Common Issues

#### Issue: Docker Desktop won't start
```bash
# Windows WSL2
wsl --update
wsl --set-default-version 2

# Reset Docker Desktop
# Settings > Troubleshoot > Reset to factory defaults
```

#### Issue: Kubernetes context not found
```bash
# Docker Desktop
# Settings > Kubernetes > Enable Kubernetes

# Minikube
minikube delete
minikube start --driver=docker
```

#### Issue: Azure CLI authentication fails
```bash
# Clear cached credentials
az account clear
az login --use-device-code
```

#### Issue: Python package conflicts
```bash
# Use fresh virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**Important**: Ensure all prerequisites are met BEFORE starting the challenge. The 4-hour timer is strict, and technical issues won't extend your time.
