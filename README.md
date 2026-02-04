# Vindicta-Agents

> AI Agent Team for Vindicta Platform Delivery

This repository contains the configuration and instructions for the AI agents that collaboratively manage the Vindicta Platform.

## Agent Team

| Agent | Role | Primary Focus |
|-------|------|---------------|
| **Agile Delivery Lead** | Process & Delivery | Sprint execution, blockers, velocity |
| **Product Owner** | Vision & Priority | Backlog, roadmap, stakeholder value |

## Agent Files

```
agents/
├── agile-delivery-lead/
│   ├── AGENT.md          # Agent identity and instructions
│   ├── DAILY_WORKFLOW.md # Daily standup routine
│   └── COLLABORATION.md  # How to work with other agents
├── product-owner/
│   ├── AGENT.md          # Agent identity and instructions
│   ├── DAILY_WORKFLOW.md # Daily planning routine
│   └── COLLABORATION.md  # How to work with other agents
└── shared/
    └── TEAM_CHARTER.md   # Shared principles and escalation
```

## Workflows Reference

Agents use workflows from `vindicta-platform/.agent/workflows/`:

| Workflow | Primary User | Purpose |
|----------|--------------|--------|
| `/daily-standup` | Delivery Lead | Daily progress review |
| `/pr-review` | Delivery Lead | PR review and merge |
| `/sprint-planning` | Product Owner | Create sprint issues |
| `/roadmap-update` | Product Owner | Sync ROADMAPs with progress |
| `/weekly-report` | Both | Weekly metrics report |
| `/release-management` | Both | Milestone releases |

## Getting Started

Agents are invoked by referencing their AGENT.md file and providing context.

---

*Vindicta Platform Agent Team — Established 2026-02-04*
