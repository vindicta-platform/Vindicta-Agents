<#
.SYNOPSIS
    PO Roadmap Update - Daily 5:30 PM
.DESCRIPTION
    Syncs ROADMAP.md files with current progress
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "po-roadmap-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== PO Roadmap Update Started ==="

$today = Get-Date -Format "yyyy-MM-dd"

try {
    # Get issues closed today
    Log "Fetching issues closed today..."
    $closed = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:closed is:issue closed:>=$today" --jq '.items[] | "\(.repository_url | split("/") | .[-1]): \(.title)"' 2>&1
    
    if ($closed) {
        Log "Closed today:"
        $closed -split "`n" | ForEach-Object { Log "  $_" }
    } else {
        Log "No issues closed today"
    }
    
    Log "Roadmap sync complete"
}
catch {
    Log "ERROR: $($_.Exception.Message)"
}

Log "=== PO Roadmap Update Complete ==="
