---
description: Product Owner Monday sprint planning
---

# PO Sprint Planning Workflow

Execute Monday at 9:30 AM by Product Owner agent.

## Steps

// turbo
1. Identify current week (1-6 in roadmap)

2. Read each product's ROADMAP.md:
   ```
   mcp_github-mcp-server_get_file_contents
   owner: vindicta-platform, repo: [each], path: ROADMAP.md
   ```

3. Create issues for scheduled tasks:
   ```
   mcp_github-mcp-server_issue_write
   method: "create"
   title: "[Week X] Task Name"
   body: "## Task\n...\n## Acceptance Criteria\n- [ ] ..."
   labels: ["priority:p1-high", "status:ready"]
   ```

4. Add to Project #4:
   ```powershell
   gh project item-add 4 --owner vindicta-platform --url [issue_url]
   ```

5. Communicate sprint goal to Delivery Lead

## Priority Framework

| P0 | Critical - blocks others |
| P1 | Current sprint commitment |
| P2 | Can wait one sprint |
| P3 | Future consideration |
