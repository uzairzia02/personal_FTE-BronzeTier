# Task Manager Agent Skill

## Description
Manages and executes tasks within the AI Employee system. Provides tools for creating, organizing, and tracking tasks.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required)
- `--list`: List all tasks in the system
- `--create`: Create a new task with specified parameters
- `--execute`: Execute a specific task

## Usage Examples
```
/task-manager --vault-path "./AI_Employee_Vault" --list
/task-manager --vault-path "./AI_Employee_Vault" --create "New task description"
/task-manager --vault-path "./AI_Employee_Vault" --execute "task_id"
```

## Implementation
This skill wraps the task management functionality from task_manager.py, enabling systematic handling of tasks within the AI Employee system.

## Capabilities
- Create new tasks with proper metadata
- List and organize existing tasks
- Execute tasks with appropriate handling
- Track task status and completion
- Integrate with other AI Employee components