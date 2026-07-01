---
inclusion: always
---

# Product Overview

## What We're Building
An Open Banking API platform that provides PSD2-compliant payment services.
This is a reference implementation for learning context engineering patterns.

## Target Users
- Third-Party Payment Providers (TPPs)
- Account Information Service Providers (AISPs)
- Payment Initiation Service Providers (PISPs)

## Business Context
- Regulated under PSD2 (EU Payment Services Directive 2)
- Must comply with PCI-DSS for card data handling
- All endpoints require Strong Customer Authentication (SCA) awareness
- Audit trail is mandatory for all state-changing operations

## Key Constraints
- All APIs must be versioned (v1, v2)
- Maximum response time: 500ms for payment initiation
- 99.9% availability SLA
- Data residency: EU only
