---
name: security-assessment
description: Run a security assessment against banking API code, checking for PCI-DSS compliance, authentication issues, and data protection gaps.
---

# Security Assessment

## Description
Run a security assessment against banking API code, checking for PCI-DSS compliance, authentication issues, and data protection gaps.

## When to Use
Invoke this skill when you need to perform a structured security review of the codebase, especially before deployments or during pull request reviews.

## Steps

### Step 1: Identify Scope
- List all Python files in `src/` that handle sensitive data
- Identify routes that accept user input
- Map data flows from request → processing → storage → response

### Step 2: Authentication & Authorization Review
- Verify OAuth2 token validation on all protected endpoints
- Check scope enforcement matches endpoint requirements
- Confirm no endpoint is accidentally unprotected
- Verify token expiry validation

### Step 3: Data Protection Review
- Search for any plaintext PAN or card data storage
- Verify all IBANs are masked in logs
- Check encryption is applied to data at rest
- Confirm no sensitive data in error responses

### Step 4: Input Validation Review
- Verify all request bodies use Pydantic models with constraints
- Check for SQL injection vectors (parameterized queries)
- Validate regex patterns for IBAN, currency codes
- Confirm amount fields use integer cents (not float)

### Step 5: Audit & Logging Review
- Verify all state-changing operations emit audit events
- Check logs don't contain sensitive data
- Confirm request_id and correlation_id propagation
- Validate structured logging format (JSON)

### Step 6: Generate Report
Output a structured findings report:
```
# Security Assessment Report
Date: [today]
Scope: [files reviewed]

## Critical Findings
[list]

## High Findings
[list]

## Recommendations
[prioritized action items]
```
