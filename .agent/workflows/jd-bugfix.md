---
description: Bug fix workflow for learning developers
---

# Junior Developer Bug Fix Workflow

## Trigger
- Bug issue assigned with `good-first-issue` or `junior-friendly` label

## Steps

### 1. Understand the Bug
- Read issue description carefully
- Reproduce the bug locally
- Ask questions if anything unclear

### 2. Find the Root Cause
- Use debugger or logging
- Check related test files
- Look at recent changes in area

### 3. Plan the Fix
Before writing code:
- Describe your fix plan in a comment
- Wait for Senior Dev confirmation if unsure
- Consider edge cases

### 4. Implement Fix
```bash
git checkout main
git pull origin main
git checkout -b fix/{issue-number}-{short-description}
```

Write fix with test:
1. Add failing test that reproduces bug
2. Implement fix
3. Verify test passes
4. Run full test suite

### 5. Self-Check
- [ ] Bug is fixed
- [ ] New test covers the fix
- [ ] No other tests broken
- [ ] Code follows existing patterns

### 6. Request Review
```
mcp_github-mcp-server_create_pull_request
- Describe the bug and fix
- Link to issue
- Request review from Senior Dev
```

### 7. Learn from Feedback
- Read all review comments carefully
- Ask questions to understand
- Apply changes promptly
- Thank reviewer

## Important Rules
- **ALWAYS** get code review before merge
- **ASK** before trying unfamiliar approaches
- **NEVER** push directly to main

## When Stuck
1. Re-read the issue
2. Search existing code for patterns
3. Ask Senior Developer for help
4. Document what you tried
