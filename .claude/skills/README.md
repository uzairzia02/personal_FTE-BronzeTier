# AI Employee Agent Skills

This project implements AI functionality as modular agent skills that can be invoked individually or in combination.

## Available Agent Skills

### 1. File Watcher Skill (`/file-watcher`)
Monitors a directory for new files and converts them to structured markdown items with YAML frontmatter in the Needs_Action directory.

**Usage:**
```
/file-watcher --vault-path "./AI_Employee_Vault" --watch-dir "./watch_folder" --scan-once
```

### 2. Reasoning Engine Skill (`/reasoning-engine`)
Processes items in Needs_Action, determines if they require human approval, and routes them appropriately. Updates the dashboard with processing results.

**Usage:**
```
/reasoning-engine --vault-path "./AI_Employee_Vault" --scan-once
```

### 3. Approval Manager Skill (`/approval-manager`)
Manages the approval workflow for tasks that require human review. Allows listing, approving, and rejecting tasks from the Pending_Approval directory.

**Usage:**
```
/approval-manager --vault-path "./AI_Employee_Vault" --list
/approval-manager --vault-path "./AI_Employee_Vault" --approve "filename.md"
/approval-manager --vault-path "./AI_Employee_Vault" --reject "filename.md"
```

### 4. AI Employee Skill (`/ai-employee`)
Main orchestrator for the AI Employee system. Coordinates the file watcher and reasoning engine in a persistent loop or single cycle mode.

**Usage:**
```
/ai-employee --vault-path "./AI_Employee_Vault" --watch-dir "./watch_folder" --single-cycle
```

### 5. Task Manager Skill (`/task-manager`)
Manages and executes tasks within the AI Employee system. Provides tools for creating, organizing, and tracking tasks.

**Usage:**
```
/task-manager --vault-path "./AI_Employee_Vault" --list
```

### 6. FTE CLI Skill (`/fte-cli`)
Front-end command-line interface for the FTE Bronze Tier project. Provides unified access to all AI Employee system functionalities.

**Usage:**
```
/fte-cli --vault-path "./AI_Employee_Vault" --mode watch
```

## Implementation Details

Each skill is implemented as:
- A Markdown specification file (`.skill.md`) defining the skill's interface
- A Python implementation file (`.py`) that wraps the existing functionality

## Benefits of Agent Skills Architecture

1. **Modularity**: Each component can be invoked independently
2. **Flexibility**: Skills can be combined in various workflows
3. **Maintainability**: Clear separation of concerns
4. **Extensibility**: New skills can be added easily
5. **Traceability**: Each skill maintains its own logs and status

## Running Skills

Skills can be invoked through the Claude Code interface using the `/skill-name` syntax, or directly via Python if needed for advanced use cases.