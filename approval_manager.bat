@echo off
REM Approval Manager Batch Script for FTE Bronze Tier Project
REM Usage:
REM approval_manager.bat list                    - List all pending approvals
REM approval_manager.bat approve filename.md     - Approve a specific file
REM approval_manager.bat reject filename.md      - Reject a specific file

setlocal enabledelayedexpansion

if "%1"=="" (
    echo USAGE:
    echo   approval_manager.bat list                    - List all pending approval items
    echo   approval_manager.bat approve ^<filename^>      - Approve a specific file
    echo   approval_manager.bat reject ^<filename^>       - Reject a specific file
    goto :eof
)

if "%1"=="list" (
    python approval_manager.py --list
    goto :eof
)

if "%1"=="approve" (
    if "%2"=="" (
        echo ERROR: Please provide a filename
        echo Usage: approval_manager.bat approve ^<filename^>
        exit /b 1
    )
    python approval_manager.py --approve %2
    goto :eof
)

if "%1"=="reject" (
    if "%2"=="" (
        echo ERROR: Please provide a filename
        echo Usage: approval_manager.bat reject ^<filename^>
        exit /b 1
    )
    python approval_manager.py --reject %2
    goto :eof
)

echo Unknown command: %1
echo Available commands: list, approve, reject