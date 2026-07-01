# 🏦 Context Engineering Banking Starter

A hands-on starter project for learning **context engineering** with AI coding assistants.
Build a PSD2-compliant payment API while exploring Steering Files, MCP Servers, Powers, Agent Skills, and Custom Agents.

## What's Inside

```
.kiro/
├── steering/           ← Always-on project context
│   ├── product.md        Product overview
│   ├── tech.md           Technology stack
│   ├── structure.md      Project structure
│   ├── api-standards.md  PSD2/PCI-DSS API conventions (Always)
│   └── security.md       Security deep-dive (Manual)
├── hooks/
│   └── lint-secrets.json ← Block commits with hardcoded keys
├── agents/
│   ├── api-developer.md  ← Developer persona
│   └── compliance-reviewer.md ← Read-only auditor
└── skills/
    └── security-assessment/  ← IAM + data protection review

src/                    ← FastAPI application
├── main.py               App entry point
├── models.py             Pydantic models (PSD2 types)
├── routes/
│   └── payments.py       Payment initiation endpoint
└── middleware/
    └── audit.py          Audit logging middleware

tests/                  ← Pytest test suite
powers/                 ← Instructions for installing Powers
CHALLENGES.md           ← 5 guided exercises
```

## Quick Start

### Prerequisites
- [Kiro IDE](https://kiro.dev) installed
- Python 3.11+
- `uv` or `pip` for dependency management

### Setup

```bash
# Clone the repo
git clone <this-repo-url>
cd context-engineering-banking-starter

# Create virtual environment and install dependencies
uv venv && uv pip install -r requirements.txt

# Run the app locally
uvicorn src.main:app --reload --port 8000

# Open in Kiro
kiro .
```

### Verify Context Engineering is Working

1. Open the project in Kiro
2. Check the Steering panel — you should see 5 steering files loaded
3. Ask Kiro: *"Create a new endpoint for listing transactions"*
4. Observe: the generated code automatically includes audit fields, PSD2 naming, and error formats

## Challenges

See [CHALLENGES.md](CHALLENGES.md) for 5 guided exercises that walk you through each context engineering method.

## Tech Stack

- **Python 3.11+** with FastAPI
- **AWS Lambda** via Mangum adapter
- **Pydantic v2** for request/response validation
- **Pytest** for testing
- Designed for deployment on AWS (Lambda + API Gateway)

## License

MIT — fork it, break it, make it yours.
