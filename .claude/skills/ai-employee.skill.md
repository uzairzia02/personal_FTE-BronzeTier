# AI Employee Agent Skill

## Description
Main orchestrator for the AI Employee system. Coordinates the file watcher and reasoning engine in a persistent loop or single cycle mode.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required)
- `--watch-dir`: Directory to monitor for new files (optional)
- `--single-cycle`: Run a single processing cycle instead of persistent operation (optional)

## Usage Examples
```
/ai-employee --vault-path "./AI_Employee_Vault" --watch-dir "./watch_folder" --single-cycle
/ai-employee --vault-path "./AI_Employee_Vault" --watch-dir "./watch_folder"
```

## Implementation
This skill wraps the main AI Employee functionality from AI_Employee.py, enabling coordinated operation of file watching and reasoning components.

## Capabilities
- Coordinate file watcher and reasoning engine components
- Support both persistent and single-cycle operation modes
- Handle graceful shutdown on interrupt signals
- Monitor specified directory for new files and process them
- Apply intelligent reasoning to determine task routing
- Maintain system logging and status tracking