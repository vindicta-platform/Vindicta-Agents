---
description: Product Owner daily roadmap sync
---

# PO Roadmap Update Workflow

Execute daily at 5:30 PM by Product Owner agent.

## Steps

// turbo
1. Get closed issues today:

   ```yaml
   mcp_github-mcp-server_search_issues
   query: "org:vindicta-platform is:closed closed:>=YYYY-MM-DD"
   ```

2. For each repo with closed issues:

   a. Read ROADMAP.md:

   ```yaml
   mcp_github-mcp-server_get_file_contents
   ```

   b. Update checklists:

   - `[ ]` → `[x]` for completed
   - `[ ]` → `[/]` for in-progress
   - Add ⚠️ for slipped items

   c. Push update:

   ```yaml
   mcp_github-mcp-server_create_or_update_file
   message: "docs: Update ROADMAP.md with current progress"
   ```

## Review (5 min)

1. Check `ROADMAP.md` against current progress:

   - Are we on track for the 6-week goal?
   - Any new risks?

## Checklist Syntax

| `[ ]` | Not started |
| `[/]` | In progress |
| `[x]` | Completed |
| ⚠️ | Slipped |
```
