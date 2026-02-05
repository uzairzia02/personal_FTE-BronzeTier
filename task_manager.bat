@echo off
REM Task Manager Batch Script for FTE Bronze Tier Project
REM Usage:
REM task_manager.bat list          - List all tasks
REM task_manager.bat done T022     - Mark task T022 as done
REM task_manager.bat approve T030  - Approve task T030

setlocal enabledelayedexpansion

if "%1"=="" (
    echo USAGE:
    echo   task_manager.bat list          - List all tasks
    echo   task_manager.bat done ^<task_id^>  - Mark task as done
    echo   task_manager.bat approve ^<task_id^> - Approve task
    goto :eof
)

if "%1"=="list" (
    python task_manager.py --list
    goto :eof
)

if "%1"=="done" (
    if "%2"=="" (
        echo ERROR: Please provide a task ID
        echo Usage: task_manager.bat done ^<task_id^>
        exit /b 1
    )
    python task_manager.py --mark-done %2
    goto :eof
)

if "%1"=="approve" (
    if "%2"=="" (
        echo ERROR: Please provide a task ID
        echo Usage: task_manager.bat approve ^<task_id^>
        exit /b 1
    )
    python task_manager.py --approve %2
    goto :eof
)

echo Unknown command: %1
echo Available commands: list, done, approve