---
description: Product Owner Monday sprint planning
---

# PO Sprint Planning Workflow

Execute Monday at 9:30 AM by Product Owner agent.

## Steps

// turbo
1. Identify current week (1-6 in roadmap)

2### 1. Define Goal

1. Read `ROADMAP.md`.
2. Select next prioritized features.

3. Draft Sprint Goal:

   ```markdown
   # Sprint Goal: [Goal]
   - Focus: [Theme]
   - Key Deliverable: [Deliverable]
   ```

### 2. Create Issues

1. Create GitHub issues for selected features.
2. Add to Project Board.

3. Assign to specialized roles:

   ```yaml
   assignees: [senior-dev, junior-dev]
   ```method: "create"
   title: "[Week X] Task Name"
   body: "## Task\n...\n## Acceptance Criteria\n- [ ] ..."
   labels: ["priority:p1-high", "status:ready"]
   ```

   ```powershell
   gh project item-add 4 --owner vindicta-platform --url [issue_url]
   ```

5. Communicate sprint goal to Delivery Lead

## Priority Framework

| P0 | Critical - blocks others |
| P1 | Current sprint commitment |
| P2 | Can wait one sprint |
| P3 | Future consideration |
