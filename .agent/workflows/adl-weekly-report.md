---
description: Agile Delivery Lead Friday velocity report
---

# ADL Weekly Report Workflow

Execute Friday at 4:00 PM by Agile Delivery Lead agent.

## Steps

// turbo
1. Get closed issues this week:
   ```
   mcp_github-mcp-server_search_issues
   query: "org:vindicta-platform is:closed closed:>=YYYY-MM-DD"
   ```

2. Get merged PRs this week:
   ```
   mcp_github-mcp-server_search_pull_requests
   query: "org:vindicta-platform is:merged merged:>=YYYY-MM-DD"
   ```

3. Calculate metrics:
   - Sprint completion % = closed / committed
   - PR cycle time = avg(merge_date - create_date)
   - Blocker resolution time

4. Compare to previous week (velocity trend)

5. Generate report:
   ```markdown
   # Weekly Velocity Report - Week [X]
   
   | Metric | Value | Target | Status |
   |--------|-------|--------|--------|
   | Sprint Completion | X% | ≥85% | ✅/❌ |
   | PR Cycle Time | Xh | <24h | ✅/❌ |
   | Blockers Resolved | X | - | - |
   ```
