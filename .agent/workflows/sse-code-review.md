---
description: Comprehensive code review with mentoring feedback
---

# Senior Software Engineer Code Review Workflow

## Trigger
- PR assigned for review
- Complex implementation requiring expertise

## Steps

### 1. Context Review
- Read PR description and linked issue
- Understand acceptance criteria
- Check author (adjust depth for Junior vs Senior)

### 2. Code Review Checklist
Using MCP tools:
```
mcp_github-mcp-server_pull_request_read with method: get_diff
mcp_github-mcp-server_pull_request_read with method: get_files
```

Review for:
- [ ] **Correctness** — Does it solve the problem?
- [ ] **Tests** — Adequate coverage? Edge cases?
- [ ] **Performance** — Any obvious inefficiencies?
- [ ] **Security** — Input validation? Auth checks?
- [ ] **Style** — Follows project conventions?
- [ ] **Documentation** — Comments where needed?

### 3. Feedback Approach

For **Junior Developers**:
- Explain WHY, not just WHAT
- Provide code examples
- Celebrate what's done well
- Suggest learning resources

For **Senior Developers**:
- Focus on design decisions
- Trust implementation details
- Discuss trade-offs

### 4. Submit Review
```
mcp_github-mcp-server_pull_request_review_write
- APPROVE if ready
- REQUEST_CHANGES with constructive feedback
- COMMENT for discussion points
```

### 5. Follow-up
- Respond to author questions within 4 hours
- Re-review promptly after changes
- Mentor through complex issues
