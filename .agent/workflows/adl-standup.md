---
description: Agile Delivery Lead morning standup routine
---

# ADL Standup Workflow

Execute daily at 9:00 AM by Agile Delivery Lead agent.

## Steps

// turbo
1. Get today's context:
   - Current week in 6-week roadmap (Feb 4 - Mar 17, 2026)
   - Calculate: `week = ceil((today - Feb4) / 7)`

2. Search open issues:
   ```
   mcp_github-mcp-server_search_issues
   query: "org:vindicta-platform is:open label:status:in-progress"
   ```

3. Identify slipped items (should have been done yesterday)

4. Flag blockers:
   ```
   mcp_github-mcp-server_add_issue_comment
   body: "⚠️ **Blocker Identified**\n\n[Description]\n\nTime: [timestamp]"
   ```

5. Output standup summary:
   - ✅ Completed yesterday
   - 🎯 Focus today
   - 🚨 Blockers (with age)

## Blocker Thresholds

| Age | Action |
|-----|--------|
| 0-4h | Log and monitor |
| 4-24h | Add escalation comment |
| >24h | Escalate to Product Owner |
