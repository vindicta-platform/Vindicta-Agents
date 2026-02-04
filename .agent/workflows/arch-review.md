---
description: Architecture review for significant changes affecting platform structure
---

# Architecture Review Workflow

## When to Trigger
- New product integration
- Cross-product dependency changes
- Technology stack additions
- Database schema changes
- API contract modifications

## Steps

### 1. Gather Context
- Read the proposed change (PR, spec, or issue)
- Identify affected products/components
- Check Constitution compliance

### 2. Impact Assessment
Using MCP tools:
```
# Check for related patterns
mcp_github-mcp-server_search_code for similar implementations

# Review existing architecture
Check relevant ADRs in .specify/decisions/
```

### 3. Review Criteria
- [ ] Aligns with Platform Constitution
- [ ] Follows established patterns
- [ ] No circular dependencies
- [ ] API contracts are backward compatible
- [ ] Test coverage requirements met
- [ ] Documentation updated

### 4. Decision & Documentation
If approved:
- Add approval comment to PR/issue
- Create ADR if significant decision

If changes needed:
- Comment specific concerns
- Suggest alternative approaches
- Offer to pair on solution

### 5. Success Criteria
- Decision documented within 24 hours
- Clear rationale provided
- Follow-up actions identified
