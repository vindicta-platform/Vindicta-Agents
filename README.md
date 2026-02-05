# Vindicta-Agents

> AI Agent Team for Vindicta Platform Delivery

## Structure

```
.specify/memory/
└── constitution.md       # Unified rules for all agents

.agent/workflows/
├── adl-standup.md        # Daily standup (9:00 AM)
├── adl-pr-review.md      # PR review sweep (5:00 PM)
├── adl-weekly-report.md  # Friday velocity report
├── po-sprint-planning.md # Monday sprint planning
├── po-roadmap-update.md  # Daily roadmap sync
├── po-release-management.md # Milestone releases
├── sm-check-in.md        # Daily check-in (8:30 AM)
├── sm-start-work.md      # Work initialization
└── sm-end-day.md         # End-of-day status (6:00 PM)

agents/
├── agile-delivery-lead/
│   └── AGENT.md          # Role identity only
├── product-owner/
│   └── AGENT.md          # Role identity only
└── senior-manager/
    └── AGENT.md          # Role identity only
```

## Agent Team

| Agent | Role | Workflows |
|-------|------|-----------|
| **Senior Manager** | Orchestration & Health | `/sm-check-in`, `/sm-start-work`, `/sm-end-day` |
| **Agile Delivery Lead** | Execution & Process | `/adl-standup`, `/adl-pr-review`, `/adl-weekly-report` |
| **Product Owner** | Vision & Priority | `/po-sprint-planning`, `/po-roadmap-update`, `/po-release-management` |

## Usage

Workflows are Antigravity-compatible. Invoke with slash commands:

```
/sm-check-in      # Execute morning check-in (orchestrates sub-agents)
/sm-start-work    # Trigger implementation phase
/sm-end-day       # Execute end-of-day status
/adl-standup      # Execute morning standup
/adl-pr-review    # Execute PR review sweep
/po-sprint-planning  # Execute Monday planning
```

## Constitution

All agents follow `.specify/memory/constitution.md` which defines:
- Role boundaries
- Escalation matrix
- MCP-First tooling policy
- Success metrics
- Forbidden actions

---

*Vindicta Platform Agent Team — Established 2026-02-04*
