---
description: Senior Manager morning check-in routine
---

# SM Check-In Workflow

Execute daily at 8:30 AM by Senior Manager agent.

## Steps

// turbo-all
1. Get current context:
   - Current week in 6-week roadmap (Feb 4 - Mar 17, 2026)
   - Today's date: `week = ceil((today - Feb4) / 7)`

2. Execute ADL Standup:
   ```
   /adl-standup
   ```
   - Capture sprint execution status
   - Note any blockers identified

3. Execute PO Roadmap Update:
   ```
   /po-roadmap-update
   ```
   - Capture roadmap alignment status
   - Note any scope changes

4. Platform Health Check:
   - Count open issues by status across all repos
   - Check PR merge rate (target: 80%+ within 24h)
   - Identify stale PRs (>48h old)

5. Blocker Summary:
   - Aggregate all blockers from ADL standup
   - Categorize by severity and age
   - Assign escalation priority

6. Generate Platform Status Report:
   ```markdown
   # Platform Status - [Date]

   ## Sprint Execution (from ADL)
   - ✅ Completed: [count]
   - 🎯 In Progress: [count]
   - 🚨 Blockers: [count]

   ## Roadmap Alignment (from PO)
   - On Track: [%]
   - At Risk: [%]
   - Scope Changes: [summary]

   ## Platform Health
   - PR Merge Rate: [%]
   - Open Issues: [count]
   - Velocity Trend: [↑/→/↓]

   ## Critical Actions Required
   - [Action 1]
   - [Action 2]
   ```

## Escalation Criteria

| Issue | Escalation |
|-------|------------|
| Blocker >4h unresolved | Immediate human alert |
| Velocity drop >20% | Daily report highlight |
| Cross-repo dependency conflict | Architect review |
