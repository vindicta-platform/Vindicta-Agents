---
description: Agile Delivery Lead afternoon PR review sweep
---

# ADL PR Review Workflow

Execute daily at 5:00 PM by Agile Delivery Lead agent.

### 1. Identify PRs to Review

// turbo
1. Search all open PRs:
   ```yaml
   mcp_github-mcp-server_search_pull_requests
   query: "org:vindicta-platform is:open"
   ```

2. For each PR, gather:

   ```yaml
   mcp_github-mcp-server_pull_request_read (method: get)
   mcp_github-mcp-server_pull_request_read (method: get_reviews)
   mcp_github-mcp-server_pull_request_read (method: get_comments)
   ```

3. Check Constitution compliance (Rule 17, GCP/GitHub isolation)

4. Suggest Copilot review if needed:
   - No reviews AND (foundation PR OR >5 files)

   ```yaml
   mcp_github-mcp-server_request_copilot_review
   ```

5. Merge ready PRs:

   ```yaml
   mcp_github-mcp-server_merge_pull_request
   merge_method: "squash"
   ```

6. Comment on blocked PRs

## Copilot Suggestion Criteria

| Scenario            | Suggest? |
| ------------------- | -------- |
| Foundation scaffold | ✅        |
| >5 files            | ✅        |
| Has human approval  | ❌        |
| Docs-only           | ❌        |
