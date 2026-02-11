---
description: Senior Manager work initialization workflow
---

# SM Start Work Workflow

Trigger implementation phase across sub-agents.

## Trigger
- Monday morning after sprint planning
- When new high-priority work arrives
- When blockers are cleared and work can resume

## Steps

// turbo-all
1. Execute Sprint Planning (if Monday):
   ```
   /po-sprint-planning
   ```
   - Get current sprint items
   - Capture sprint goals
   - Note priority order

2. Check for Architecture Review Needs:
   - Scan new issues for labels: `needs-arch-review`
   - Check issue descriptions for keywords: "breaking change", "new integration", "API design"
   - If needed, execute:
     ```
     /arch-review
     ```

3. Assign Work to Developers:
   - Group issues by complexity:
     - Junior Developer: `complexity:low`
     - Senior Developer: `complexity:medium`
     - Senior Software Engineer: `complexity:high` or `needs-mentoring`
   - For each assigned issue:
     ```
     mcp_github-mcp-server_add_issue_comment
     body: "🚀 **Work Started**\n\nAssigned to: [agent role]\nStarted: [timestamp]\nExpected completion: [estimate]"
     ```

4. Trigger Implementation Workflows:
   - For ready issues:
     ```
     /sd-implement
     ```
   - For learning opportunities:
     ```
     /jd-bugfix
     ```

5. Setup Tracking:
   - Add PRs to **Project #3** (PR Review Board) for review tracking
   - Add issues to **Project #4** (Platform Roadmap) for sprint tracking
   - Update status label to `status:in-progress`
   - Set milestone based on sprint week

   **MCP Tools for Project Updates:**
   ```
   # Add issue to project (requires project and issue node IDs)
   mcp_github-mcp-server_add_issue_comment
   body: "📋 Added to Project #3 (Roadmap) and #4 (Sprint)"

   # Update issue labels for tracking
   mcp_github-mcp-server_issue_write
   method: "update"
   labels: ["status:in-progress"]
   ```

6. Generate Kickoff Summary:
   ```markdown
   # Work Session Started - [Date]

   ## Sprint Goals
   - [Goal 1]
   - [Goal 2]

   ## Work Assigned
   - Junior Developer: [count] items
   - Senior Developer: [count] items
   - Senior Software Engineer: [count] items

   ## Architecture Reviews Pending
   - [Issue #X]: [title]

   ## Expected Deliverables Today
   - [Deliverable 1]
   - [Deliverable 2]
   ```

## Success Criteria
- All sprint items have clear assignees
- No work starts without passing architecture review
- Tracking updated within 5 minutes of work start
