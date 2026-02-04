# Product Owner — Daily Workflow

## Morning Routine (Start of Day)

### 1. Review Delivery Lead Standup

Check standup summary from Agile Delivery Lead:
- Completed items → Update roadmap if milestone complete
- Blocked items → Prioritization decision needed
- Velocity concerns → Scope adjustment discussion

### 2. Backlog Grooming

Review backlog for today's priorities:
1. Check issues in "Ready" column of Project #4
2. Ensure next sprint's issues have clear acceptance criteria
3. Add missing details to any under-specified issues

**MCP Tools:**
```
mcp_github-mcp-server_list_issues (state: OPEN, orderBy: CREATED_AT)
mcp_github-mcp-server_issue_write (method: update) — to add details
```

---

## Afternoon Routine (End of Day)

### 3. Roadmap Sync
```
/roadmap-update
```

**Actions:**
1. Get closed issues from today
2. Update ROADMAP.md files with completed items
3. Mark slipped items for rescheduling
4. Push updates to repositories

### 4. Stakeholder Communication

Prepare end-of-day update:
- Major completions worth announcing
- Risks or blockers requiring escalation
- Any scope changes approved today

---

## Weekly Routines

### Monday: Sprint Planning
```
/sprint-planning
```

**Actions:**
1. Review upcoming week in 6-week roadmap
2. Create issues for scheduled tasks
3. Assign milestones and labels
4. Add issues to Project #4
5. Communicate sprint goals to Delivery Lead

### Friday: Weekly Review

**Actions:**
1. Review `/weekly-report` from Delivery Lead
2. Assess roadmap progress vs plan
3. Identify at-risk milestones
4. Plan adjustments for next week

### End of Sprint: Release Check
```
/release-management
```

Check if any milestones are ready for release:
- All issues closed
- Tests passing
- Documentation complete

---

## Collaboration Points

| Time | Sync With | Topic |
|------|-----------|-------|
| Morning | Delivery Lead | Standup review, blockers |
| Midday | (As needed) | Priority calls, scope decisions |
| EOD | Delivery Lead | Velocity update, concerns |
| Monday AM | Delivery Lead | Sprint planning capacity check |
| Friday PM | Delivery Lead | Weekly review, next week prep |
