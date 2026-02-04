# Agile Delivery Lead — Daily Workflow

## Morning Routine (Start of Day)

### 1. Daily Standup Review
```
/daily-standup
```

**Actions:**
1. Check current week in 6-week roadmap (Feb 4 - Mar 17, 2026)
2. List issues scheduled for today from Project #4
3. Identify any issues that slipped from yesterday
4. Flag blockers requiring immediate attention

**Output:** Standup summary with:
- Yesterday's completed items
- Today's focus items
- Blockers requiring escalation

### 2. Blocker Triage

For each identified blocker:
1. Check if blocker is technical or dependency-based
2. If technical: Add troubleshooting comment to issue
3. If dependency: Notify Product Owner for prioritization
4. Set reminder for 4-hour follow-up

---

## Afternoon Routine (End of Day)

### 3. PR Review Sweep
```
/pr-review
```

**Actions:**
1. Search all open PRs across organization
2. For each PR:
   - Check if Copilot review exists (suggest if needed)
   - Review Constitution compliance
   - Merge if ready, comment if blocked
3. Flag any PRs approaching 48-hour threshold

### 4. Progress Update

1. Update issue status on Project #4 board
2. Move completed items to "Done"
3. Move blocked items with blocker label
4. Calculate daily velocity

---

## Friday Additions

### 5. Weekly Report
```
/weekly-report
```

Generate metrics:
- Issues closed this week
- PRs merged
- Sprint completion percentage
- Velocity trend (vs last week)

### 6. Release Check
```
/release-management
```

Check milestones approaching due date.

---

## Handoff to Product Owner

At end of day, notify Product Owner of:
- Completed items (for backlog grooming)
- Blocked items (for prioritization)
- Velocity concerns (for scope adjustment)
