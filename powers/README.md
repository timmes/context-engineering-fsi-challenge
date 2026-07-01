# Powers — On-Demand Context Activation

## Installing Powers

Powers can be installed from the Kiro Powers panel or from kiro.dev/powers.

### Recommended Powers for This Project

1. **Stripe Power** (for payment processing)
   - Open Kiro → Powers panel → Search "Stripe" → Install
   - Activates when you mention: "payment", "checkout", "stripe", "subscription"
   - Provides: Stripe API tools + idempotency patterns + webhook best practices

2. **AWS Power** (for Lambda/DynamoDB)
   - Open Kiro → Powers panel → Search "AWS" → Install
   - Activates when you mention: "lambda", "dynamodb", "cloudwatch", "deploy"
   - Provides: AWS SDK patterns + IAM best practices + CloudFormation guidance

## Building a Private Power

For your organization, you can create a private "Open Banking Power" that bundles:
- PSD2 API patterns and naming conventions
- PCI-DSS secure coding guidelines
- Your internal compliance MCP server
- Hooks for regulatory checks

Structure:
```
my-open-banking-power/
├── POWER.md           ← Instructions + activation keywords
├── steering/
│   └── psd2-patterns.md
├── mcp.json           ← Compliance tracker MCP config
└── hooks/
    └── pci-check.json
```

See: https://kiro.dev/docs/powers/create/ for the full guide.
