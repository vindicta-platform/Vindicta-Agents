# Vindicta Agent Automation

Windows Task Scheduler automation for AI agent workflows.

## Schedule

| Time | Agent | Workflow | Task Name |
|------|-------|----------|-----------|
| 9:00 AM | ADL | `/adl-standup` | VindictaAgents\ADL-Standup |
| 5:00 PM | ADL | `/adl-pr-review` | VindictaAgents\ADL-PRReview |
| 5:30 PM | PO | `/po-roadmap-update` | VindictaAgents\PO-RoadmapUpdate |
| Monday 9:30 AM | PO | `/po-sprint-planning` | VindictaAgents\PO-SprintPlanning |
| Friday 4:00 PM | ADL | `/adl-weekly-report` | VindictaAgents\ADL-WeeklyReport |

## Setup

```powershell
# Run as Administrator
.\Register-AgentTasks.ps1
```

## Scripts

- `Run-ADL-Standup.ps1` — Morning standup
- `Run-ADL-PRReview.ps1` — Afternoon PR sweep
- `Run-ADL-WeeklyReport.ps1` — Friday velocity report
- `Run-PO-SprintPlanning.ps1` — Monday planning
- `Run-PO-RoadmapUpdate.ps1` — Daily roadmap sync

## Logs

Logs are written to `automation/logs/` with daily rotation.

## Manual Execution

```powershell
# Run a task immediately
Start-ScheduledTask -TaskPath "\VindictaAgents\" -TaskName "ADL-Standup"

# Or run script directly
.\scripts\Run-ADL-Standup.ps1
```
