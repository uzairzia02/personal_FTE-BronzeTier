<#
.SYNOPSIS
Task Manager Script for FTE Bronze Tier Project

.DESCRIPTION
This script allows you to easily mark tasks as done from the PowerShell command line.
Usage:
    .\task_manager.ps1 -MarkDone "T022"
    .\task_manager.ps1 -Approve "T030"
    .\task_manager.ps1 -List
    .\task_manager.ps1 -Help

.PARAMETER MarkDone
Marks a specific task as done (e.g., T022)

.PARAMETER Approve
Approves a specific task (e.g., T030)

.PARAMETER List
Lists all tasks with their status

.PARAMETER TasksFile
Specifies the path to the tasks.md file
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$MarkDone,

    [Parameter(Mandatory=$false)]
    [string]$Approve,

    [Parameter(Mandatory=$false)]
    [switch]$List,

    [Parameter(Mandatory=$false)]
    [string]$TasksFile
)

function Find-TasksFile {
    # Look for tasks.md in common locations
    $possiblePaths = @(
        "specs/1-ai-employee/tasks.md",
        "tasks.md"
    )

    foreach ($pattern in $possiblePaths) {
        $path = Join-Path $PSScriptRoot $pattern
        if (Test-Path $path) {
            return $path
        }
    }

    # Search recursively for tasks.md in specs directory
    $searchPath = Join-Path $PSScriptRoot "specs"
    if (Test-Path $searchPath) {
        $foundFiles = Get-ChildItem -Path $searchPath -Recurse -Name "tasks.md" -File
        if ($foundFiles.Count -gt 0) {
            return Join-Path $searchPath $foundFiles[0].FullName
        }
    }

    throw "Could not find tasks.md file"
}

function Show-Tasks {
    param([string]$TasksFilePath)

    Write-Host "`n📋 Current Tasks in $TasksFilePath:" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Yellow

    $content = Get-Content $TasksFilePath -Raw
    $lines = $content -split "`n"

    foreach ($line in $lines) {
        if ($line -match '^(\s*-\s*\[([ X])\]\s+(T\d+)\s+(.*?))$') {
            $fullMatch = $matches[1]
            $status = $matches[2]
            $taskId = $matches[3]
            $description = $matches[4]

            $statusSymbol = if ($status -eq "X") { "✓" } else { "○" }
            $color = if ($status -eq "X") { "Green" } else { "White" }

            Write-Host "$statusSymbol [$taskId] $description" -ForegroundColor $color
        }
    }
}

function Update-TaskStatus {
    param(
        [string]$TasksFilePath,
        [string]$TaskId,
        [string]$Action = "done"
    )

    Write-Host "Marking task $TaskId as $Action..." -ForegroundColor Yellow

    $content = Get-Content $TasksFilePath -Raw

    # Create pattern to match the specific task
    $pattern = "^(\\s*-\s*\[([ X])\]\s+$([regex]::Escape($TaskId))\s+.*)$"

    $updatedContent = $content -replace $pattern, {
        param($match)
        $lineContent = $match.Value
        # Replace [ ] with [X] to mark as done
        $updatedLine = $lineContent -replace '\[ \]', '[X]'
        return $updatedLine
    }

    if ($content -ne $updatedContent) {
        Set-Content -Path $TasksFilePath -Value $updatedContent -Encoding UTF8
        Write-Host "✅ Successfully marked task $TaskId as done!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Task $TaskId not found in the tasks file." -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    # Find tasks file
    if ($TasksFile) {
        $tasksFilePath = $TasksFile
    } else {
        $tasksFilePath = Find-TasksFile
    }

    if ($List) {
        Show-Tasks -TasksFilePath $tasksFilePath
        return
    }

    if ($MarkDone) {
        $success = Update-TaskStatus -TasksFilePath $tasksFilePath -TaskId $MarkDone.ToUpper() -Action "done"
        if ($success) {
            Write-Host ""
            Write-Host "📝 Don't forget to commit your changes:" -ForegroundColor Cyan
            Write-Host "git add $tasksFilePath"
            Write-Host "git commit -m `"Mark task $MarkDone as completed`""
        }
        exit $(if ($success) { 0 } else { 1 })
    }

    if ($Approve) {
        $success = Update-TaskStatus -TasksFilePath $tasksFilePath -TaskId $Approve.ToUpper() -Action "approved"
        if ($success) {
            Write-Host ""
            Write-Host "📝 Don't forget to commit your changes:" -ForegroundColor Cyan
            Write-Host "git add $tasksFilePath"
            Write-Host "git commit -m `"Approve task $Approve`""
        }
        exit $(if ($success) { 0 } else { 1 })
    }

    # If no parameters provided, show help
    if (!$MarkDone -and !$Approve -and !$List) {
        Write-Host "Task Manager for FTE Bronze Tier Project" -ForegroundColor Green
        Write-Host ""
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "    .\task_manager.ps1 -MarkDone `"T022`"" -ForegroundColor White
        Write-Host "    .\task_manager.ps1 -Approve `"T030`"" -ForegroundColor White
        Write-Host "    .\task_manager.ps1 -List" -ForegroundColor White
        Write-Host ""
        Write-Host "EXAMPLES:" -ForegroundColor Yellow
        Write-Host "  .\task_manager.ps1 -List" -ForegroundColor White
        Write-Host "  .\task_manager.ps1 -MarkDone T022" -ForegroundColor White
        Write-Host "  .\task_manager.ps1 -Approve T030" -ForegroundColor White
    }

} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}