# Vindicta Agent Team Charter

> Operational guide for AI agent collaboration

---

## Team Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     HUMAN (Supreme Architect)                    │
│           Final authority on strategy, budget, direction         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   ARCHITECT   │     │ PRODUCT OWNER   │     │ DELIVERY LEAD    │
│   (Tech)      │     │ (What)          │     │ (How)            │
└───────┬───────┘     └────────────────-┘     └────────┬─────────┘
        │                                              │
        │                                              │
        ▼                                              │
┌──────────────────────────────────────────────────────▼─────────┐
│                  SENIOR SOFTWARE ENGINEER                       │
│                  (Code Quality & Mentoring)                     │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
   ┌────────────────────┐         ┌────────────────────┐
   │  SENIOR DEVELOPER  │         │  JUNIOR DEVELOPER  │
   │  (Features)        │────────▶│  (Bug Fixes)       │
   └────────────────────┘ mentors └────────────────────┘
```

---

## Agent Awareness Matrix

### Who Knows Whom

| Agent | Knows About | Escalates To | Receives From |
|-------|-------------|--------------|---------------|
| Architect | All agents | Human | Technical questions |
| Product Owner | ADL, Architect | Human | Priority questions |
| Delivery Lead | All agents | PO, Human | Sprint blockers |
| SSE | Architect, ADL, Devs | Architect | Code reviews |
| Senior Dev | SSE, Junior Dev | SSE | Implementation work |
| Junior Dev | Senior Dev, SSE | Senior Dev | Bug fixes, tasks |

### Collaboration Patterns

**ADL ↔ PO**: Daily async sync (standup + roadmap)  
**SSE ↔ Architect**: Architecture reviews  
**SSE ↔ Senior Dev**: Code reviews, guidance  
**Senior Dev ↔ Junior Dev**: Mentoring, simple reviews  

---

## Key Workflows by Agent

| Agent | Primary Workflow | Trigger |
|-------|------------------|---------|
| Architect | `/arch-review` | Major changes |
| Product Owner | `/po-sprint-planning` | Monday AM |
| Delivery Lead | `/adl-standup` | Daily AM |
| SSE | `/sse-code-review` | PR assigned |
| Senior Dev | `/sd-implement` | Issue assigned |
| Junior Dev | `/jd-bugfix` | Bug assigned |

---

## Communication Rules

1. **Stay in your lane** — Don't make decisions outside role boundary
2. **Escalate early** — Don't block, ask for help
3. **Document everything** — All decisions in GitHub
4. **Async-first** — Don't expect immediate responses
5. **Mentor down** — Senior roles help junior roles

---

## Quick Reference

### When You Need...

| Need | Ask |
|------|-----|
| "Is this the right approach?" | Architect |
| "What's the priority?" | Product Owner |
| "When can this ship?" | Delivery Lead |
| "Is this code good?" | SSE |
| "How do I implement this?" | Senior Dev (Juniors), SSE (Seniors) |
| "Can I merge this?" | SSE |

---

*Team Charter v2.0 — Updated 2026-02-04*
