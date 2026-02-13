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

3. Get closed issues this week:

   ```yaml
   is:issue is:closed closed:>2026-02-01
   ```

4. Get open blockers:

   ```yaml
   is:issue is:open label:blocked
   ```

### 2. Generate Report

1. Create `automation/reports/Velocity_Report_Week_X.md`
2. Run `velocity-report` script (if available) or fill manually:

   ```markdown
   # Velocity Report: Week X

   | Metric            | Value | Target | Status |
   | ----------------- | ----- | ------ | ------ |
   | Sprint Completion | X%    | ≥85%   | ✅/❌    |
   | PR Cycle Time     | Xh    | <24h   | ✅/❌    |
   | Blockers Resolved | X     | -      | -      |
   ```
