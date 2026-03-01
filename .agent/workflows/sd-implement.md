---
description: Feature implementation from specification to PR
---

# Senior Developer Implementation Workflow

## Trigger
- Issue assigned with clear spec
- Feature ready for implementation

## Steps

### 1. Understand Requirements
- Read issue description and acceptance criteria
- Check linked specifications
- Clarify any ambiguity with Product Owner

### 2. Plan Implementation
- Break down into sub-tasks
- Identify test cases needed
- Estimate complexity

### 3. Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/{issue-number}-{short-description}
```

### 4. Implement with Tests
Follow TDD/BDD approach:
1. Write failing test
2. Implement minimum to pass
3. Refactor for quality
### 4. Implementation

1. Create feature branch.
2. Implement code.

3. Test locally:

   ```bash
   uv run pytest
   ```

4. Create Pull Request.
```
mcp_github-mcp-server_create_pull_request
- Link to issue
- Describe changes
- Tag reviewer (SSE)
```

### 5. Self-Review Checklist
- [ ] All acceptance criteria met
- [ ] Tests pass locally
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Commit messages clear


### 7. Address Feedback
- Respond to review comments
- Push fixes promptly
- Ask questions if unclear

## Escalation
- Blocked → Delivery Lead
- Scope unclear → Product Owner
- Technical uncertainty → Senior Software Engineer
