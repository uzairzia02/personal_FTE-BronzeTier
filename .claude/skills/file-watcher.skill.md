# File Watcher Agent Skill

## Description
Monitors a directory for new files and converts them to structured markdown items with YAML frontmatter in the Needs_Action directory.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required)
- `--watch-dir`: Directory to monitor for new files (required)
- `--scan-once`: Scan once and exit (optional, default: false)

## Usage Examples
```
/file-watcher --vault-path "./AI_Employee_Vault" --watch-dir "./watch_folder" --scan-once
```

## Implementation
This skill wraps the FileWatcher functionality from AI_Employee_Watcher.py, enabling monitoring of directories for new files and converting them to structured markdown items in the AI Employee system.

## Capabilities
- Monitors specified directory for new files
- Calculates file hashes to prevent duplicates
- Creates markdown files with YAML frontmatter in Needs_Action directory
- Handles both text and binary files appropriately
- Maintains processed files tracking to avoid reprocessing