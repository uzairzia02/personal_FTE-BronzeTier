# FTE CLI Agent Skill

## Description
Front-end command-line interface for the FTE Bronze Tier project. Provides unified access to all AI Employee system functionalities.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required for most operations)
- `--mode`: Operation mode (watch, reason, approve, task, etc.)
- `--config`: Configuration file path (optional)

## Usage Examples
```
/fte-cli --vault-path "./AI_Employee_Vault" --mode watch
/fte-cli --vault-path "./AI_Employee_Vault" --mode reason
/fte-cli --vault-path "./AI_Employee_Vault" --mode approve --action list
```

## Implementation
This skill wraps the FTE CLI functionality from fte-cli.py, providing a unified command-line interface to the entire AI Employee system.

## Capabilities
- Unified access to all AI Employee system components
- Configurable operation modes
- Parameter validation and error handling
- Integration with vault and file management
- Support for batch operations