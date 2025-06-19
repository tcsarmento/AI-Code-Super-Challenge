# 📋 Business Rules Quick Reference Card

## 💰 Transaction Limits

| Rule | Value | Notes |
|------|-------|-------|
| **Minimum Amount** | $0.01 | Reject if less |
| **Maximum Single Transaction** | $1,000,000 | Reject if more |
| **Daily Limit per Account** | $5,000,000 | Cumulative limit |
| **Overdraft (Business only)** | $100,000 | Only account type 'B' |

## 💳 Account Types

| Code | Type | Min Balance | Special Rules |
|------|------|-------------|---------------|
| **C** | Checking | $0 | Standard consumer account |
| **S** | Savings | $100 | Interest-bearing |
| **B** | Business | $1,000 | Can overdraft up to $100k |
| **I** | Investment | $10,000 | Trading account |

## 💵 Fee Structure

### Base Fees
| Transaction Type | Code | Fee | VIP Fee |
|-----------------|------|-----|---------|
| **Domestic** | DM | $2.50 | $0 |
| **International** | IN | $25.00 | $0 |
| **Wire Transfer** | WT | $35.00 | $0 |

### Volume Discounts
| Monthly Volume | Discount |
|----------------|----------|
| 100+ transactions | 10% off fees |
| 500+ transactions | 20% off fees |
| 1000+ transactions | 30% off fees |

## 🚨 Fraud Detection Rules

### Risk Score Calculation
```
Base Score: 0
+ New Account (<30 days): +20 points
+ High Amount (>$50k): +15 points
+ International: +10 points
+ Unusual Time (2-5 AM): +10 points
+ New Payee: +15 points
+ Multiple Red Flags: +30 points
```

### Risk Thresholds
| Score | Action | Response |
|-------|--------|----------|
| 0-30 | Auto-approve | Process immediately |
| 31-60 | Review | Additional verification |
| 61-80 | Manual review | Hold for investigation |
| 81+ | Block | Reject transaction |

### Velocity Limits
- **Max per hour**: 50 transactions
- **Max per day**: 500 transactions
- **Concurrent limit**: 5 transactions

## 🏦 Account Validation

### Account Number Format
- **Length**: Exactly 10 digits
- **Format**: Numeric only (0-9)
- **Example**: `1234567890`

### Required Fields
1. `from_account` - Source account
2. `to_account` - Destination account
3. `amount` - Transaction amount
4. `currency` - 3-letter code (default: USD)

## ⚡ Performance Requirements

| Metric | Requirement | Target |
|--------|-------------|--------|
| **Response Time** | < 100ms (p99) | 50ms |
| **Throughput** | 100 TPS minimum | 1000 TPS |
| **Success Rate** | > 95% | 99.9% |
| **Availability** | 99.9% | 99.99% |

## 🔄 Transaction Status Codes

| Status | Code | Meaning |
|--------|------|---------|
| **Pending** | P | Processing started |
| **Completed** | C | Successfully processed |
| **Failed** | F | Processing failed |
| **Blocked** | B | Fraud detection blocked |

## 📊 Quick Calculations

### Fee Calculation
```python
def calculate_fee(transaction_type, is_vip, monthly_volume):
    if is_vip:
        return 0.00
    
    base_fees = {
        "DM": 2.50,
        "IN": 25.00,
        "WT": 35.00
    }
    
    fee = base_fees.get(transaction_type, 0)
    
    # Apply volume discount
    if monthly_volume >= 1000:
        fee *= 0.70  # 30% off
    elif monthly_volume >= 500:
        fee *= 0.80  # 20% off
    elif monthly_volume >= 100:
        fee *= 0.90  # 10% off
    
    return fee
```

### Daily Limit Check
```python
def check_daily_limit(account, amount):
    remaining = account.daily_limit - account.daily_used
    return amount <= remaining
```

### Overdraft Check
```python
def can_overdraft(account, amount):
    if account.type != 'B':
        return False
    
    total_available = account.balance + account.overdraft_limit
    return amount <= total_available
```

## 🎯 COBOL Business Logic Mapping

| COBOL Paragraph | Modern Implementation |
|-----------------|----------------------|
| `2200-VALIDATE-TRANSACTION` | Transaction validation service |
| `2300-FRAUD-CHECK` | Fraud detection service |
| `2400-EXECUTE-TRANSACTION` | Transaction processing |
| `3100-CHECK-VELOCITY` | Rate limiting middleware |
| `4000-CALCULATE-FEES` | Fee calculation function |

## ⚠️ Critical Business Rules

1. **Never** allow same-account transfers
2. **Always** check balance before processing
3. **VIP customers** pay no fees regardless of volume
4. **Business accounts** are the only ones with overdraft
5. **International transfers** require additional validation
6. **Sanctions list** must be checked for all transactions

## 🔍 Validation Checklist

Before processing any transaction:
- [ ] Valid account number format (10 digits)
- [ ] Different from/to accounts
- [ ] Amount within limits ($0.01 - $1M)
- [ ] Daily limit not exceeded
- [ ] Sufficient balance (or overdraft)
- [ ] Fraud score < 80
- [ ] Account status is active

---

**Keep this card visible during the challenge for quick reference!**