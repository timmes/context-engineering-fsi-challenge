# 🎯 Challenges

Five guided exercises to master context engineering. Each takes 10-15 minutes.

---

## Challenge 1: Steering Files — "Add a Transactions Endpoint"

**Goal**: See how steering files shape AI-generated code automatically.

**Steps**:
1. Open the project in Kiro and verify steering files are loaded (check the Steering panel)
2. Ask Kiro: *"Add a GET /v1/transactions endpoint that returns paginated transaction history"*
3. **Observe** what the AI generates — look for:
   - PSD2-compliant field names (`transaction_id`, `debtor_account`, `creditor_account`)
   - Mandatory audit fields (`x-request-id`, `x-idempotency-key`)
   - Error response format matching `api-standards.md`

**Experiment**: Delete `.kiro/steering/api-standards.md`, regenerate the endpoint, and compare. Put it back when done.

**What you learned**: Steering files provide persistent, zero-effort conventions to every AI interaction.

---

## Challenge 2: MCP Servers — "Connect External Tools"

**Goal**: Give your AI assistant access to external systems.

**Steps**:
1. Install the GitHub MCP server:
   ```json
   // .kiro/settings/mcp.json
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
         }
       }
     }
   }
   ```
2. Set your `GITHUB_TOKEN` environment variable
3. Ask Kiro: *"What are the open issues in this repository?"*
4. Ask: *"Create a new issue titled 'Add rate limiting to payments endpoint'"*

**Experiment**: Try connecting the Filesystem MCP server to give Kiro read access to a docs folder outside the project.

**What you learned**: MCP servers let your AI agent interact with external systems in real-time.

---

## Challenge 3: Powers — "Install the Stripe Power"

**Goal**: Experience on-demand context activation.

**Steps**:
1. Install the Stripe Power from the Kiro Powers panel (or from kiro.dev/powers)
2. Start a conversation about something unrelated (e.g., *"Refactor the audit middleware"*)
3. Now mention payments: *"Add Stripe payment processing to the payment initiation endpoint"*
4. **Observe**: The Stripe Power activates — loading Stripe API tools and best practices
5. The AI now knows about idempotency keys, webhook verification, and Stripe error handling

**Experiment**: Check your context usage before and after Power activation. Note how it only loads when relevant.

**What you learned**: Powers provide specialist knowledge on-demand without permanent context cost.

---

## Challenge 4: Custom Agents — "Create a Security Auditor"

**Goal**: Build a task-specific persona with restricted permissions.

**Steps**:
1. Read the existing `.kiro/agents/compliance-reviewer.md`
2. Create a new agent: `.kiro/agents/security-auditor.md`:
   ```markdown
   ---
   description: Security auditor for banking APIs — finds vulnerabilities
   model: claude-sonnet-4
   tools: [read, context]
   permissions:
     - capability: filesystem
       effect: deny
       match: [".env", "secrets/**", "*.key", "*.pem"]
     - capability: shell
       effect: deny
   ---
   You are a security auditor specializing in banking applications.
   
   Review code for:
   - SQL injection vulnerabilities
   - Hardcoded credentials or API keys
   - Missing input validation
   - Insecure cryptographic practices
   - PCI-DSS compliance gaps
   
   Report findings in severity order (Critical > High > Medium > Low).
   For each finding, provide: location, risk, and remediation.
   ```
3. Switch to the security-auditor agent in the agent selector
4. Ask: *"Audit the payments route for security vulnerabilities"*

**Experiment**: Try giving the auditor `write` permissions and asking it to fix the issues it finds. What changes?

**What you learned**: Custom agents create specialist personas with appropriate tool access and guardrails.

---

## Challenge 5: Hooks — "Auto-Generate Tests on Save"

**Goal**: Automate repetitive tasks with event-driven triggers.

**Steps**:
1. Create a new hook file `.kiro/hooks/auto-test.json`:
   ```json
   {
     "version": "v1",
     "hooks": [
       {
         "name": "generate-tests-on-save",
         "trigger": "PostFileSave",
         "matcher": "src/routes/.*\\.py$",
         "action": {
           "type": "agent",
           "prompt": "A route file was just saved. Check if there's a corresponding test file in tests/. If not, generate one with pytest tests covering the happy path and common error cases. Follow the patterns in existing test files."
         },
         "timeout": 60,
         "enabled": true
       }
     ]
   }
   ```
2. Edit `src/routes/payments.py` (add a comment or modify a docstring) and save
3. **Observe**: Kiro automatically generates/updates the test file

**Experiment**: Create a hook that runs `pytest` after test files are saved and reports failures inline.

**What you learned**: Hooks automate quality checks without manual intervention.

---

## 🏆 Bonus Challenge: Full Feature with Specs

**Goal**: Use Kiro Specs to plan and build a complete feature.

**Steps**:
1. Open the Kiro pane → Specs → click `+`
2. Choose "Feature" and describe: *"Add transaction categorization — users can assign categories (food, transport, salary, etc.) to transactions and filter by category"*
3. Walk through the three phases:
   - **Requirements**: Review user stories and acceptance criteria
   - **Design**: Check the architecture (does it respect your steering file patterns?)
   - **Tasks**: Run tasks and watch steering + agents shape every generated file
4. When complete, switch to the compliance-reviewer agent and ask it to review the full feature

**What you learned**: Specs + context engineering = structured development with automated guardrails at every step.

---

## Share Your Work! 🎉

Completed a challenge? Share your approach or interesting findings in the discussion channel.
We'll feature creative solutions and unexpected discoveries.
