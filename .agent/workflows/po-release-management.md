---
description: Product Owner release management
---

# PO Release Management Workflow

Execute as needed when milestones approach completion.

## Steps

// turbo
1. Check milestone status:
   ```
   mcp_github-mcp-server_list_issues
   state: OPEN, milestone: [milestone_number]
   ```
   Ready if open_issues = 0

2. Validate:
   - All issues closed
   - All PRs merged
   - Tests passing
   - Docs updated

3. Prepare release:
   - Update CHANGELOG.md
   - Create release tag:
   ```powershell
   gh release create v0.1.0 --title "v0.1.0 Foundation"
   ```

4. Close milestone, update ROADMAP.md

## Release Checklist

- [ ] All milestone issues closed
- [ ] All PRs merged
- [ ] ROADMAP.md updated
- [ ] Version tag created
