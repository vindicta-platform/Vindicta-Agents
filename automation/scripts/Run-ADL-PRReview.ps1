<#
.SYNOPSIS
    ADL PR Review - Daily 5:00 PM
.DESCRIPTION
    Executes the Agile Delivery Lead PR review workflow
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "adl-pr-review-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== ADL PR Review Started ==="

try {
    # Get open PRs across organization
    Log "Searching open PRs..."
    $prs = gh pr list --state open --json number,title,repository,createdAt,author --limit 50 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $prList = $prs | ConvertFrom-Json
        Log "Found $($prList.Count) open PRs"
        
        foreach ($pr in $prList) {
            $age = ((Get-Date) - [DateTime]$pr.createdAt).TotalHours
            $status = if ($age -gt 48) { "⚠️ AGING" } elseif ($age -gt 24) { "⏰ >24h" } else { "✅ OK" }
            Log "  PR #$($pr.number): $($pr.title) - $status ($([math]::Round($age))h)"
        }
    }
    
    # Check for PRs needing Copilot review
    Log "Checking for PRs without reviews..."
    # This would integrate with MCP tools in full implementation
}
catch {
    Log "ERROR: $($_.Exception.Message)"
}

Log "=== ADL PR Review Complete ==="
