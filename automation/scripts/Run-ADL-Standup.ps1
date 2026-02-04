<#
.SYNOPSIS
    ADL Morning Standup - Daily 9:00 AM
.DESCRIPTION
    Executes the Agile Delivery Lead standup workflow via Gemini CLI
#>

$ErrorActionPreference = "Stop"
$AgentRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "adl-standup-$(Get-Date -Format 'yyyy-MM-dd').log"

# Ensure log directory
if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== ADL Standup Started ==="

# Calculate week number
$startDate = [DateTime]"2026-02-04"
$weekNum = [math]::Ceiling((((Get-Date) - $startDate).Days + 1) / 7)
Log "Week $weekNum of 6"

# Execute via GitHub CLI (MCP operations)
try {
    Log "Fetching open issues..."
    $issues = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:open is:issue" --jq '.total_count' 2>&1
    Log "Open issues: $issues"

    Log "Fetching open PRs..."
    $prs = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:open is:pr" --jq '.total_count' 2>&1
    Log "Open PRs: $prs"

    Log "Fetching blocked issues..."
    $blocked = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:open label:blocked" --jq '.total_count' 2>&1
    Log "Blocked: $blocked"

    # Summary
    $summary = @"

# Daily Standup - $(Get-Date -Format 'dddd, MMMM dd')
Week $weekNum | Open Issues: $issues | Open PRs: $prs | Blocked: $blocked
"@
    Log $summary
}
catch {
    Log "ERROR: $($_.Exception.Message)"
}

Log "=== ADL Standup Complete ==="
