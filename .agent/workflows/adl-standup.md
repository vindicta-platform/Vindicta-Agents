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

   ```yaml
   mcp_github-mcp-server_search_issues
   query: "org:vindicta-platform is:open label:status:in-progress"
   ```

3. Identify slipped items (should have been done yesterday)

4. Flag blockers:

   ```yaml
   mcp_github-mcp-server_add_issue_comment
   body: "⚠️ **Blocker Identified**\n\n[Description]\n\nTime: [timestamp]"
   ```

5. Sync with GitHub Projects:

   - **Project #3** (PR Review Board): Ensure open PRs are tracked
   - **Project #4** (Platform Roadmap): Update issue statuses

   ```yaml
   mcp_github-mcp-server_issue_write
   method: "update"
   labels: ["status:in-progress"] or ["status:done"]
   ```

6. Output standup summary:
   - ✅ Completed yesterday
   - 🎯 Focus today
   - 🚨 Blockers (with age)
   - 📋 Project board sync status

## Blocker Thresholds

| Age   | Action                    |
| ----- | ------------------------- |
| 0-4h  | Log and monitor           |
| 4-24h | Add escalation comment    |
| >24h  | Escalate to Product Owner |
