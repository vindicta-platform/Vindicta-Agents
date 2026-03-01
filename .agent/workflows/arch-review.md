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

## When to Trigger

- New product integration
- Changing core data models
- Adding new infrastructure dependency

## Steps

### 1. Gather Context

- Read the proposed change (PR, Issue, or RFC)
- Check `docs/architecture.md` for alignment

### 2. Impact Assessment

Run dependency check:

```bash
uv graph
```

Identify affected domains.

### 3. Review Criteria

- [ ] Aligns with Platform Constitution?
- [ ] Maintains domain isolation?
- [ ] Scalable?

### 4. Decision & Documentation

- Add approval comment to PR/issue
- OR request changes:
  - Link to specific architecture violation
  - Suggest alternative pattern

- Comment specific concerns

### 5. Success Criteria

- Decision documented within 24h
- No architectural debt introduced
- Follow-up actions identified
```
