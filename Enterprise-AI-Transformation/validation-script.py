#!/usr/bin/env python3
"""
Solution Validation Script for Super Challenge
Validates that all requirements are met before submission
"""

import asyncio
import httpx
import json
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import yaml

# Initialize Rich console
console = Console()

# Validation configuration
REQUIRED_SERVICES = {
    "transaction-service": {
        "url": "http://localhost:8001",
        "health_endpoint": "/health",
        "required_endpoints": [
            ("/api/v1/transactions", "POST"),
            ("/api/v1/transactions/{id}", "GET"),
            ("/api/v1/accounts/{id}", "GET")
        ]
    },
    "fraud-service": {
        "url": "http://localhost:8002",
        "health_endpoint": "/health",
        "required_endpoints": [
            ("/api/v1/analyze", "POST")
        ]
    },
    "analytics-service": {
        "url": "http://localhost:8003",
        "health_endpoint": "/health",
        "required_endpoints": [
            ("/api/v1/metrics/summary", "GET"),
            ("/ws/metrics", "WEBSOCKET")
        ]
    }
}

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "docker-compose.yml",
    ".env.example",
    "src/transaction-service/main.py",
    "src/fraud-service/main.py",
    "src/analytics-service/main.py"
]

REQUIRED_INFRASTRUCTURE = [
    "infrastructure/terraform/main.tf",
    "infrastructure/k8s/namespace.yaml"
]

BUSINESS_RULES = {
    "min_amount": 0.01,
    "max_amount": 1000000.00,
    "daily_limit": 5000000.00,
    "domestic_fee": 2.50,
    "international_fee": 25.00,
    "wire_fee": 35.00
}

class SolutionValidator:
    def __init__(self):
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }
        self.score = 0
        self.max_score = 100
        
    async def validate_all(self) -> Dict:
        """Run all validation checks"""
        console.print(Panel.fit(
            "[bold cyan]Super Challenge Solution Validator[/bold cyan]\n" +
            "Checking all requirements...",
            border_style="cyan"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # File structure validation
            task = progress.add_task("[yellow]Validating file structure...", total=1)
            self.validate_file_structure()
            progress.update(task, completed=1)
            
            # Docker services validation
            task = progress.add_task("[yellow]Checking Docker services...", total=1)
            self.validate_docker_services()
            progress.update(task, completed=1)
            
            # API endpoints validation
            task = progress.add_task("[yellow]Testing API endpoints...", total=1)
            await self.validate_api_endpoints()
            progress.update(task, completed=1)
            
            # Business rules validation
            task = progress.add_task("[yellow]Testing business rules...", total=1)
            await self.validate_business_rules()
            progress.update(task, completed=1)
            
            # Fraud detection validation
            task = progress.add_task("[yellow]Testing fraud detection...", total=1)
            await self.validate_fraud_detection()
            progress.update(task, completed=1)
            
            # Analytics validation
            task = progress.add_task("[yellow]Testing analytics...", total=1)
            await self.validate_analytics()
            progress.update(task, completed=1)
            
            # Performance validation
            task = progress.add_task("[yellow]Testing performance...", total=1)
            await self.validate_performance()
            progress.update(task, completed=1)
            
            # Infrastructure validation
            task = progress.add_task("[yellow]Checking infrastructure...", total=1)
            self.validate_infrastructure()
            progress.update(task, completed=1)
        
        return self.generate_report()
    
    def validate_file_structure(self):
        """Check if all required files exist"""
        console.print("\n[bold]1. File Structure Validation[/bold]")
        
        for file_path in REQUIRED_FILES:
            if Path(file_path).exists():
                self.results["passed"].append(f"File exists: {file_path}")
                self.score += 1
            else:
                self.results["failed"].append(f"Missing file: {file_path}")
        
        # Check for test files
        if Path("tests").exists() and any(Path("tests").rglob("test_*.py")):
            self.results["passed"].append("Test files found")
            self.score += 5
        else:
            self.results["warnings"].append("No test files found")
    
    def validate_docker_services(self):
        """Check if Docker services are running"""
        console.print("\n[bold]2. Docker Services Validation[/bold]")
        
        try:
            # Check docker-compose services
            result = subprocess.run(
                ["docker-compose", "ps", "--format", "json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                services = json.loads(result.stdout)
                running_services = [s for s in services if "running" in s.get("State", "").lower()]
                
                if len(running_services) >= 3:
                    self.results["passed"].append(f"Docker services running: {len(running_services)}")
                    self.score += 5
                else:
                    self.results["failed"].append(f"Insufficient Docker services: {len(running_services)}")
            else:
                self.results["failed"].append("Docker services not running")
                
        except Exception as e:
            self.results["failed"].append(f"Docker check failed: {str(e)}")
    
    async def validate_api_endpoints(self):
        """Test all required API endpoints"""
        console.print("\n[bold]3. API Endpoints Validation[/bold]")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            for service_name, config in REQUIRED_SERVICES.items():
                # Check health endpoint
                try:
                    response = await client.get(f"{config['url']}{config['health_endpoint']}")
                    if response.status_code == 200:
                        self.results["passed"].append(f"{service_name} health check passed")
                        self.score += 2
                    else:
                        self.results["failed"].append(f"{service_name} health check failed: {response.status_code}")
                except Exception as e:
                    self.results["failed"].append(f"{service_name} unreachable: {str(e)}")
                
                # Check required endpoints
                for endpoint, method in config.get("required_endpoints", []):
                    if "WEBSOCKET" in method:
                        # Skip WebSocket validation here
                        continue
                    
                    # Test endpoint exists (OPTIONS request)
                    try:
                        test_url = f"{config['url']}{endpoint.replace('{id}', '1234567890')}"
                        response = await client.request("OPTIONS", test_url)
                        if response.status_code < 500:
                            self.results["passed"].append(f"{service_name} {endpoint} exists")
                            self.score += 1
                        else:
                            self.results["failed"].append(f"{service_name} {endpoint} error: {response.status_code}")
                    except Exception:
                        self.results["warnings"].append(f"Could not verify {service_name} {endpoint}")
    
    async def validate_business_rules(self):
        """Test business rules implementation"""
        console.print("\n[bold]4. Business Rules Validation[/bold]")
        
        test_cases = [
            {
                "name": "Valid transaction",
                "transaction": {
                    "from_account": "1111111111",
                    "to_account": "2222222222",
                    "amount": 100.00,
                    "currency": "USD",
                    "transaction_type": "DM"
                },
                "expected_status": 200
            },
            {
                "name": "Amount too low",
                "transaction": {
                    "from_account": "1111111111",
                    "to_account": "2222222222",
                    "amount": 0.001,
                    "currency": "USD"
                },
                "expected_status": 422
            },
            {
                "name": "Amount too high",
                "transaction": {
                    "from_account": "1111111111",
                    "to_account": "2222222222",
                    "amount": 2000000.00,
                    "currency": "USD"
                },
                "expected_status": 422
            },
            {
                "name": "Same account transfer",
                "transaction": {
                    "from_account": "1111111111",
                    "to_account": "1111111111",
                    "amount": 100.00,
                    "currency": "USD"
                },
                "expected_status": 422
            }
        ]
        
        async with httpx.AsyncClient() as client:
            for test_case in test_cases:
                try:
                    response = await client.post(
                        f"{REQUIRED_SERVICES['transaction-service']['url']}/api/v1/transactions",
                        json=test_case["transaction"]
                    )
                    
                    if response.status_code == test_case["expected_status"]:
                        self.results["passed"].append(f"Business rule test passed: {test_case['name']}")
                        self.score += 3
                    else:
                        self.results["failed"].append(
                            f"Business rule test failed: {test_case['name']} "
                            f"(expected {test_case['expected_status']}, got {response.status_code})"
                        )
                except Exception as e:
                    self.results["failed"].append(f"Business rule test error: {test_case['name']} - {str(e)}")
    
    async def validate_fraud_detection(self):
        """Test fraud detection functionality"""
        console.print("\n[bold]5. Fraud Detection Validation[/bold]")
        
        # Test high-risk transaction
        high_risk_transaction = {
            "from_account": "9999999999",
            "to_account": "1111111111",
            "amount": 999999.00,
            "currency": "USD",
            "transaction_type": "WT"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                # Test fraud service directly
                response = await client.post(
                    f"{REQUIRED_SERVICES['fraud-service']['url']}/api/v1/analyze",
                    json=high_risk_transaction
                )
                
                if response.status_code == 200:
                    fraud_result = response.json()
                    if fraud_result.get("risk_score", 0) > 60:
                        self.results["passed"].append("Fraud detection identifies high-risk transactions")
                        self.score += 10
                    else:
                        self.results["warnings"].append("Fraud detection may not be properly calibrated")
                        self.score += 5
                else:
                    self.results["failed"].append("Fraud service not working properly")
                    
        except Exception as e:
            self.results["failed"].append(f"Fraud detection test failed: {str(e)}")
    
    async def validate_analytics(self):
        """Test analytics functionality"""
        console.print("\n[bold]6. Analytics Validation[/bold]")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test metrics endpoint
                response = await client.get(
                    f"{REQUIRED_SERVICES['analytics-service']['url']}/api/v1/metrics/summary"
                )
                
                if response.status_code == 200:
                    metrics = response.json()
                    if "metrics" in metrics:
                        self.results["passed"].append("Analytics metrics endpoint working")
                        self.score += 5
                    else:
                        self.results["warnings"].append("Analytics metrics format incorrect")
                        self.score += 2
                else:
                    self.results["failed"].append("Analytics metrics endpoint not working")
                    
        except Exception as e:
            self.results["failed"].append(f"Analytics test failed: {str(e)}")
    
    async def validate_performance(self):
        """Basic performance validation"""
        console.print("\n[bold]7. Performance Validation[/bold]")
        
        # Simple latency test
        latencies = []
        
        async with httpx.AsyncClient() as client:
            for _ in range(10):
                start_time = asyncio.get_event_loop().time()
                try:
                    response = await client.get(
                        f"{REQUIRED_SERVICES['transaction-service']['url']}/health"
                    )
                    if response.status_code == 200:
                        latency = (asyncio.get_event_loop().time() - start_time) * 1000
                        latencies.append(latency)
                except Exception:
                    pass
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            if avg_latency < 100:
                self.results["passed"].append(f"Average latency: {avg_latency:.2f}ms")
                self.score += 10
            else:
                self.results["warnings"].append(f"High latency: {avg_latency:.2f}ms")
                self.score += 5
        else:
            self.results["failed"].append("Could not test performance")
    
    def validate_infrastructure(self):
        """Check infrastructure configuration"""
        console.print("\n[bold]8. Infrastructure Validation[/bold]")
        
        # Check Terraform files
        if Path("infrastructure/terraform/main.tf").exists():
            self.results["passed"].append("Terraform configuration found")
            self.score += 5
            
            # Basic Terraform validation
            try:
                result = subprocess.run(
                    ["terraform", "validate"],
                    cwd="infrastructure/terraform",
                    capture_output=True
                )
                if result.returncode == 0:
                    self.results["passed"].append("Terraform configuration valid")
                    self.score += 5
                else:
                    self.results["warnings"].append("Terraform configuration has issues")
            except Exception:
                self.results["warnings"].append("Terraform not installed - cannot validate")
        
        # Check Kubernetes manifests
        k8s_files = list(Path("infrastructure/k8s").rglob("*.yaml")) if Path("infrastructure/k8s").exists() else []
        if k8s_files:
            self.results["passed"].append(f"Kubernetes manifests found: {len(k8s_files)}")
            self.score += 5
        else:
            self.results["warnings"].append("No Kubernetes manifests found")
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        # Calculate final score
        self.score = min(self.score, self.max_score)  # Cap at 100
        
        # Create summary table
        table = Table(title="Validation Results", show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Status", style="yellow")
        table.add_column("Points", style="green")
        
        # Add summary rows
        table.add_row("Passed Checks", str(len(self.results["passed"])), f"+{len(self.results['passed']) * 2}")
        table.add_row("Failed Checks", str(len(self.results["failed"])), f"-{len(self.results['failed']) * 5}")
        table.add_row("Warnings", str(len(self.results["warnings"])), "0")
        table.add_section()
        table.add_row("Final Score", f"{self.score}/100", "")
        
        console.print("\n")
        console.print(table)
        
        # Show details if there are failures
        if self.results["failed"]:
            console.print("\n[bold red]Failed Checks:[/bold red]")
            for failure in self.results["failed"]:
                console.print(f"  ❌ {failure}")
        
        if self.results["warnings"]:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in self.results["warnings"]:
                console.print(f"  ⚠️  {warning}")
        
        # Final verdict
        if self.score >= 80:
            console.print(Panel.fit(
                f"[bold green]✅ VALIDATION PASSED![/bold green]\n" +
                f"Score: {self.score}/100\n" +
                "Your solution meets the requirements!",
                border_style="green"
            ))
            status = "PASSED"
        elif self.score >= 60:
            console.print(Panel.fit(
                f"[bold yellow]⚠️  VALIDATION PARTIALLY PASSED[/bold yellow]\n" +
                f"Score: {self.score}/100\n" +
                "Your solution needs some improvements.",
                border_style="yellow"
            ))
            status = "PARTIAL"
        else:
            console.print(Panel.fit(
                f"[bold red]❌ VALIDATION FAILED[/bold red]\n" +
                f"Score: {self.score}/100\n" +
                "Your solution needs significant work.",
                border_style="red"
            ))
            status = "FAILED"
        
        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "score": self.score,
            "status": status,
            "summary": {
                "passed": len(self.results["passed"]),
                "failed": len(self.results["failed"]),
                "warnings": len(self.results["warnings"])
            },
            "details": self.results
        }
        
        with open("validation-report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        console.print("\n[dim]Full report saved to validation-report.json[/dim]")
        
        return report

async def main():
    """Main validation function"""
    validator = SolutionValidator()
    
    try:
        # Check if we're in the right directory
        if not Path("src").exists():
            console.print("[bold red]Error:[/bold red] Please run this script from the project root directory")
            return 1
        
        # Run validation
        report = await validator.validate_all()
        
        # Return appropriate exit code
        if report["status"] == "PASSED":
            return 0
        elif report["status"] == "PARTIAL":
            return 1
        else:
            return 2
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Validation interrupted by user[/yellow]")
        return 3
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
        return 4

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
