@echo off
REM FTE Project CLI Tool
REM Provides easy access to project management commands

setlocal enabledelayedexpansion

if "%1"=="" (
    echo FTE Bronze Tier Project CLI
    echo ===========================
    echo.
    echo USAGE:
    echo   fte-cli tasks list           - List all project tasks
    echo   fte-cli tasks done ^<task_id^> - Mark task as done
    echo   fte-cli tasks approve ^<task_id^> - Approve task
    echo   fte-cli run                  - Start the AI Employee system
    echo   fte-cli help                 - Show this help
    goto :eof
)

if "%1"=="tasks" (
    if "%2"=="list" (
        python task_manager.py --list
        goto :eof
    )
    if "%2"=="done" (
        if "%3"=="" (
            echo ERROR: Please provide a task ID
            echo Usage: fte-cli tasks done ^<task_id^>
            exit /b 1
        )
        python task_manager.py --mark-done %3
        goto :eof
    )
    if "%2"=="approve" (
        if "%3"=="" (
            echo ERROR: Please provide a task ID
            echo Usage: fte-cli tasks approve ^<task_id^>
            exit /b 1
        )
        python task_manager.py --approve %3
        goto :eof
    )
    echo Unknown tasks command: %2
    echo Available: list, done, approve
    exit /b 1
)

if "%1"=="approvals" (
    if "%2"=="list" (
        python approval_manager.py --list
        goto :eof
    )
    if "%2"=="approve" (
        if "%3"=="" (
            echo ERROR: Please provide a filename
            echo Usage: fte-cli approvals approve ^<filename^>
            exit /b 1
        )
        python approval_manager.py --approve %3
        goto :eof
    )
    if "%2"=="reject" (
        if "%3"=="" (
            echo ERROR: Please provide a filename
            echo Usage: fte-cli approvals reject ^<filename^>
            exit /b 1
        )
        python approval_manager.py --reject %3
        goto :eof
    )
    echo Unknown approvals command: %2
    echo Available: list, approve, reject
    exit /b 1
)

if "%1"=="run" (
    python AI_Employee.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder
    goto :eof
)

if "%1"=="help" (
    echo FTE Bronze Tier Project CLI
    echo ===========================
    echo.
    echo USAGE:
    echo   fte-cli tasks list           - List all project tasks
    echo   fte-cli tasks done ^<task_id^> - Mark task as done
    echo   fte-cli tasks approve ^<task_id^> - Approve task
    echo   fte-cli run                  - Start the AI Employee system
    echo   fte-cli help                 - Show this help
    goto :eof
)

echo Unknown command: %1
echo Use "fte-cli help" for available commands