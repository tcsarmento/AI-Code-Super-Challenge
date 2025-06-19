#!/usr/bin/env python3
"""
Performance Testing Script for Super Challenge
Validates that the solution meets performance requirements
"""

import asyncio
import httpx
import time
import statistics
import json
import argparse
from datetime import datetime
from typing import List, Dict, Tuple
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live

# Initialize Rich console for beautiful output
console = Console()

# Test configuration
DEFAULT_BASE_URL = "http://localhost:8001"
DEFAULT_DURATION = 60  # seconds
DEFAULT_TARGET_TPS = 100
LATENCY_REQUIREMENT_MS = 100  # p99 must be under 100ms

# Test accounts for performance testing
PERF_TEST_ACCOUNTS = [
    ("5555555555", "6666666666"),
    ("6666666666", "7777777777"),
    ("7777777777", "8888888888"),
    ("8888888888", "9999999999"),
    ("9999999999", "5555555555"),
]

class PerformanceTest:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = {
            "successful": 0,
            "failed": 0,
            "latencies": [],
            "errors": {},
            "start_time": None,
            "end_time": None
        }
        
    async def submit_transaction(self, session: httpx.AsyncClient, from_account: str, to_account: str) -> Tuple[bool, float, str]:
        """Submit a single transaction and return success, latency, error"""
        transaction = {
            "from_account": from_account,
            "to_account": to_account,
            "amount": 10.00,  # Small amount for testing
            "currency": "USD",
            "transaction_type": "DM"
        }
        
        start_time = time.time()
        try:
            response = await session.post(
                f"{self.base_url}/api/v1/transactions",
                json=transaction,
                timeout=5.0
            )
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                return True, latency, None
            else:
                return False, latency, f"HTTP {response.status_code}: {response.text}"
                
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return False, latency, str(e)
    
    async def run_load_test(self, duration: int, target_tps: int, progress: Progress) -> Dict:
        """Run load test for specified duration"""
        self.results["start_time"] = datetime.now()
        
        async with httpx.AsyncClient() as session:
            tasks = []
            account_index = 0
            
            # Create progress task
            task_id = progress.add_task(
                "[cyan]Running load test...", 
                total=duration
            )
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                batch_start = time.time()
                
                # Submit batch of requests
                batch_tasks = []
                for _ in range(target_tps):
                    from_acc, to_acc = PERF_TEST_ACCOUNTS[account_index % len(PERF_TEST_ACCOUNTS)]
                    account_index += 1
                    
                    task = self.submit_transaction(session, from_acc, to_acc)
                    batch_tasks.append(task)
                
                # Wait for batch to complete
                batch_results = await asyncio.gather(*batch_tasks)
                
                # Process results
                for success, latency, error in batch_results:
                    if success:
                        self.results["successful"] += 1
                        self.results["latencies"].append(latency)
                    else:
                        self.results["failed"] += 1
                        if error:
                            self.results["errors"][error] = self.results["errors"].get(error, 0) + 1
                    
                # Update progress
                elapsed = time.time() - start_time
                progress.update(task_id, completed=min(elapsed, duration))
                
                # Wait to maintain target TPS
                batch_duration = time.time() - batch_start
                if batch_duration < 1.0:
                    await asyncio.sleep(1.0 - batch_duration)
        
        self.results["end_time"] = datetime.now()
        progress.update(task_id, completed=duration)
        return self.results
    
    def calculate_metrics(self) -> Dict:
        """Calculate performance metrics from results"""
        if not self.results["latencies"]:
            return {"error": "No successful requests"}
        
        latencies = sorted(self.results["latencies"])
        total_requests = self.results["successful"] + self.results["failed"]
        duration = (self.results["end_time"] - self.results["start_time"]).total_seconds()
        
        metrics = {
            "total_requests": total_requests,
            "successful_requests": self.results["successful"],
            "failed_requests": self.results["failed"],
            "success_rate": (self.results["successful"] / total_requests * 100) if total_requests > 0 else 0,
            "actual_tps": total_requests / duration if duration > 0 else 0,
            "latency_min": latencies[0],
            "latency_max": latencies[-1],
            "latency_mean": statistics.mean(latencies),
            "latency_median": statistics.median(latencies),
            "latency_p50": latencies[int(len(latencies) * 0.50)],
            "latency_p90": latencies[int(len(latencies) * 0.90)],
            "latency_p95": latencies[int(len(latencies) * 0.95)],
            "latency_p99": latencies[int(len(latencies) * 0.99)],
            "latency_p999": latencies[int(len(latencies) * 0.999)] if len(latencies) > 1000 else latencies[-1],
            "errors": self.results["errors"]
        }
        
        return metrics

async def test_single_transaction_latency(base_url: str) -> Dict:
    """Test single transaction latency without load"""
    console.print("\n[bold yellow]Testing single transaction latency...[/bold yellow]")
    
    latencies = []
    async with httpx.AsyncClient() as client:
        for i in range(10):
            transaction = {
                "from_account": "5555555555",
                "to_account": "6666666666",
                "amount": 1.00,
                "currency": "USD"
            }
            
            start_time = time.time()
            try:
                response = await client.post(
                    f"{base_url}/api/v1/transactions",
                    json=transaction,
                    timeout=5.0
                )
                latency = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    latencies.append(latency)
                    console.print(f"  Request {i+1}: [green]{latency:.2f}ms[/green]")
                else:
                    console.print(f"  Request {i+1}: [red]Failed - {response.status_code}[/red]")
            except Exception as e:
                console.print(f"  Request {i+1}: [red]Error - {str(e)}[/red]")
    
    if latencies:
        return {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "meets_requirement": max(latencies) < LATENCY_REQUIREMENT_MS
        }
    else:
        return {"error": "All requests failed"}

async def test_concurrent_requests(base_url: str, concurrent: int = 50) -> Dict:
    """Test system under concurrent load"""
    console.print(f"\n[bold yellow]Testing {concurrent} concurrent requests...[/bold yellow]")
    
    async def make_request(client: httpx.AsyncClient, index: int):
        transaction = {
            "from_account": PERF_TEST_ACCOUNTS[index % len(PERF_TEST_ACCOUNTS)][0],
            "to_account": PERF_TEST_ACCOUNTS[index % len(PERF_TEST_ACCOUNTS)][1],
            "amount": 1.00,
            "currency": "USD"
        }
        
        start_time = time.time()
        try:
            response = await client.post(
                f"{base_url}/api/v1/transactions",
                json=transaction,
                timeout=10.0
            )
            latency = (time.time() - start_time) * 1000
            return response.status_code == 200, latency
        except Exception:
            return False, (time.time() - start_time) * 1000
    
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, i) for i in range(concurrent)]
        results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    successful = sum(1 for success, _ in results if success)
    latencies = [latency for _, latency in results]
    
    return {
        "total_requests": concurrent,
        "successful": successful,
        "success_rate": successful / concurrent * 100,
        "total_time": total_time,
        "requests_per_second": concurrent / total_time,
        "avg_latency": statistics.mean(latencies),
        "max_latency": max(latencies)
    }

def display_results(metrics: Dict):
    """Display test results in a beautiful table"""
    # Create results table
    table = Table(title="Performance Test Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")
    table.add_column("Status", style="green")
    
    # Add rows
    table.add_row("Total Requests", f"{metrics['total_requests']:,}", "")
    table.add_row("Successful", f"{metrics['successful_requests']:,}", "✓" if metrics['success_rate'] > 95 else "✗")
    table.add_row("Failed", f"{metrics['failed_requests']:,}", "")
    table.add_row("Success Rate", f"{metrics['success_rate']:.2f}%", "✓" if metrics['success_rate'] > 95 else "✗")
    table.add_row("Actual TPS", f"{metrics['actual_tps']:.2f}", "")
    
    table.add_section()
    table.add_row("Min Latency", f"{metrics['latency_min']:.2f}ms", "")
    table.add_row("Mean Latency", f"{metrics['latency_mean']:.2f}ms", "")
    table.add_row("P50 Latency", f"{metrics['latency_p50']:.2f}ms", "")
    table.add_row("P90 Latency", f"{metrics['latency_p90']:.2f}ms", "")
    table.add_row("P95 Latency", f"{metrics['latency_p95']:.2f}ms", "")
    table.add_row("P99 Latency", f"{metrics['latency_p99']:.2f}ms", "✓" if metrics['latency_p99'] < LATENCY_REQUIREMENT_MS else "✗")
    table.add_row("Max Latency", f"{metrics['latency_max']:.2f}ms", "")
    
    console.print(table)
    
    # Show errors if any
    if metrics.get('errors'):
        error_table = Table(title="Errors", show_header=True, header_style="bold red")
        error_table.add_column("Error", style="red")
        error_table.add_column("Count", style="yellow")
        
        for error, count in sorted(metrics['errors'].items(), key=lambda x: x[1], reverse=True)[:5]:
            error_table.add_row(error[:80] + "..." if len(error) > 80 else error, str(count))
        
        console.print(error_table)
    
    # Final verdict
    passed = (
        metrics['success_rate'] > 95 and
        metrics['latency_p99'] < LATENCY_REQUIREMENT_MS and
        metrics['actual_tps'] > 50
    )
    
    if passed:
        console.print(Panel.fit(
            "[bold green]✅ PERFORMANCE TEST PASSED![/bold green]\n" +
            "Your solution meets all performance requirements!",
            border_style="green"
        ))
    else:
        failures = []
        if metrics['success_rate'] <= 95:
            failures.append(f"Success rate {metrics['success_rate']:.1f}% is below 95%")
        if metrics['latency_p99'] >= LATENCY_REQUIREMENT_MS:
            failures.append(f"P99 latency {metrics['latency_p99']:.0f}ms exceeds {LATENCY_REQUIREMENT_MS}ms")
        if metrics['actual_tps'] <= 50:
            failures.append(f"Throughput {metrics['actual_tps']:.1f} TPS is below 50 TPS")
        
        console.print(Panel.fit(
            "[bold red]❌ PERFORMANCE TEST FAILED![/bold red]\n" +
            "\n".join(f"• {failure}" for failure in failures),
            border_style="red"
        ))

async def main():
    parser = argparse.ArgumentParser(description="Performance test for Super Challenge")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="Base URL of the API")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="Test duration in seconds")
    parser.add_argument("--tps", type=int, default=DEFAULT_TARGET_TPS, help="Target transactions per second")
    parser.add_argument("--quick", action="store_true", help="Run quick test (10 seconds)")
    
    args = parser.parse_args()
    
    if args.quick:
        args.duration = 10
    
    console.print(Panel.fit(
        "[bold cyan]Super Challenge Performance Test[/bold cyan]\n" +
        f"URL: {args.url}\n" +
        f"Duration: {args.duration}s\n" +
        f"Target TPS: {args.tps}",
        border_style="cyan"
    ))
    
    try:
        # Test 1: Single transaction latency
        single_result = await test_single_transaction_latency(args.url)
        if "error" not in single_result:
            console.print(f"Single transaction latency: [green]{single_result['avg']:.2f}ms[/green] average")
        
        # Test 2: Concurrent requests
        concurrent_result = await test_concurrent_requests(args.url)
        console.print(f"Concurrent test: [green]{concurrent_result['success_rate']:.1f}%[/green] success rate")
        
        # Test 3: Sustained load test
        console.print(f"\n[bold yellow]Starting {args.duration} second load test at {args.tps} TPS...[/bold yellow]")
        
        tester = PerformanceTest(args.url)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            results = await tester.run_load_test(args.duration, args.tps, progress)
        
        # Calculate and display metrics
        metrics = tester.calculate_metrics()
        display_results(metrics)
        
        # Save results to file
        with open("performance-test-results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "configuration": {
                    "url": args.url,
                    "duration": args.duration,
                    "target_tps": args.tps
                },
                "results": metrics
            }, f, indent=2)
        
        console.print("\n[dim]Results saved to performance-test-results.json[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
