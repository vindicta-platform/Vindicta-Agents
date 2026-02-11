---
description: Senior Manager end-of-day status workflow
---

# SM End Day Workflow

Execute daily at 6:00 PM by Senior Manager agent.

## Steps

// turbo-all
1. Execute PR Review:
   ```
   /adl-pr-review
   ```
   - Get PR status summary
   - Capture merge statistics
   - Note pending reviews

2. Calculate Daily Velocity:
   - Count issues moved to `status:done` today
   - Count PRs merged today
   - Compare to sprint average
   - Trend: ↑ (above average), → (on track), ↓ (below average)

3. Execute Weekly Report (if Friday):
   ```
   /adl-weekly-report
   ```
   - Capture full week summary
   - Include velocity charts
   - Note sprint completion percentage

4. Preview Tomorrow's Work:
   - List issues in `status:in-progress`
   - List issues in `status:ready` queue
   - Identify potential blockers
   - Check for scheduled reviews

5. Generate End-of-Day Handoff:
   ```markdown
   # End of Day Report - [Date]

   ## Today's Accomplishments
   - Issues Completed: [count]
   - PRs Merged: [count]
   - Velocity: [↑/→/↓]

   ## PR Status
   - Pending Review: [count]
   - Approved (awaiting merge): [count]
   - Changes Requested: [count]

   ## Active Blockers
   - [Blocker 1] - Age: [hours]
   - [Blocker 2] - Age: [hours]

   ## Tomorrow's Focus
   - In Progress: [count] items
   - Ready to Start: [count] items
   - Potential Blockers: [list]

   ## Weekly Summary (Fridays only)
   [Include full weekly report from /adl-weekly-report]
   ```

6. Flag Critical Items for Human Review:
   - Blockers >8h old
   - PRs with >3 change requests
   - Sprint items at risk of missing deadline
   - Cross-repo conflicts unresolved

## Report Distribution

| Recipient | When | Content |
|-----------|------|---------|
| Human Oversight | Daily | Critical items only |
| Project Archive | Daily | Full report |
| Weekly Stakeholders | Friday | Weekly summary |

## Cleanup Tasks

- Archive completed issues
- Update Project #4 board
- Close stale notifications
