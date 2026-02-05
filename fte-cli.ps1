<#
.SYNOPSIS
FTE Bronze Tier Project CLI Tool

.DESCRIPTION
Provides easy access to project management commands

.USAGE
    .\fte-cli.ps1 tasks list
    .\fte-cli.ps1 tasks done T022
    .\fte-cli.ps1 tasks approve T030
    .\fte-cli.ps1 run
    .\fte-cli.ps1 help
#>

param(
    [Parameter(Position=0)]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$SubCommand,

    [Parameter(Position=2)]
    [string]$TaskId
)

if (-not $Command) {
    Write-Host "FTE Bronze Tier Project CLI" -ForegroundColor Green
    Write-Host "===========================" -ForegroundColor Green
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\fte-cli.ps1 tasks list              - List all project tasks" -ForegroundColor White
    Write-Host "  .\fte-cli.ps1 tasks done <task_id>    - Mark task as done" -ForegroundColor White
    Write-Host "  .\fte-cli.ps1 tasks approve <task_id> - Approve task" -ForegroundColor White
    Write-Host "  .\fte-cli.ps1 run                     - Start the AI Employee system" -ForegroundColor White
    Write-Host "  .\fte-cli.ps1 help                    - Show this help" -ForegroundColor White
    return
}

switch ($Command) {
    "tasks" {
        switch ($SubCommand) {
            "list" {
                & python task_manager.py --list
            }
            "done" {
                if (-not $TaskId) {
                    Write-Host "ERROR: Please provide a task ID" -ForegroundColor Red
                    Write-Host "Usage: .\fte-cli.ps1 tasks done <task_id>" -ForegroundColor Red
                    exit 1
                }
                & python task_manager.py --mark-done $TaskId
            }
            "approve" {
                if (-not $TaskId) {
                    Write-Host "ERROR: Please provide a task ID" -ForegroundColor Red
                    Write-Host "Usage: .\fte-cli.ps1 tasks approve <task_id>" -ForegroundColor Red
                    exit 1
                }
                & python task_manager.py --approve $TaskId
            }
            default {
                Write-Host "Unknown tasks command: $SubCommand" -ForegroundColor Red
                Write-Host "Available: list, done, approve" -ForegroundColor Yellow
                exit 1
            }
        }
    }
    "approvals" {
        switch ($SubCommand) {
            "list" {
                & python approval_manager.py --list
            }
            "approve" {
                if (-not $TaskId) {
                    Write-Host "ERROR: Please provide a filename" -ForegroundColor Red
                    Write-Host "Usage: .\fte-cli.ps1 approvals approve <filename>" -ForegroundColor Red
                    exit 1
                }
                & python approval_manager.py --approve $TaskId
            }
            "reject" {
                if (-not $TaskId) {
                    Write-Host "ERROR: Please provide a filename" -ForegroundColor Red
                    Write-Host "Usage: .\fte-cli.ps1 approvals reject <filename>" -ForegroundColor Red
                    exit 1
                }
                & python approval_manager.py --reject $TaskId
            }
            default {
                Write-Host "Unknown approvals command: $SubCommand" -ForegroundColor Red
                Write-Host "Available: list, approve, reject" -ForegroundColor Yellow
                exit 1
            }
        }
    }
    "run" {
        & python AI_Employee.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder
    }
    "help" {
        Write-Host "FTE Bronze Tier Project CLI" -ForegroundColor Green
        Write-Host "===========================" -ForegroundColor Green
        Write-Host ""
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "  .\fte-cli.ps1 tasks list              - List all project tasks" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 tasks done <task_id>    - Mark task as done" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 tasks approve <task_id> - Approve task" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 approvals list          - List pending approvals" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 approvals approve <filename> - Approve pending item" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 approvals reject <filename> - Reject pending item" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 run                     - Start the AI Employee system" -ForegroundColor White
        Write-Host "  .\fte-cli.ps1 help                    - Show this help" -ForegroundColor White
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Use '.\fte-cli.ps1 help' for available commands" -ForegroundColor Yellow
    }
}