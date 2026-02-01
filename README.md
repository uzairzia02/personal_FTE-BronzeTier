# AI Employee (Bronze Tier)

A local-first AI employee system that operates 24/7 using an Obsidian vault as its memory system, with human-in-the-loop approval for sensitive actions.

## Overview

The AI Employee system is designed to operate entirely locally with no cloud dependencies. It uses an Obsidian vault structure to manage tasks and maintain memory of its operations.

### Architecture

The system consists of four main components:

1. **File System Watcher**: Monitors a designated directory for new files and converts them into structured markdown items in the `/Needs_Action` folder
2. **Reasoning Engine**: Processes items in `/Needs_Action`, determines if they require human approval, and routes them appropriately
3. **Logging System**: Maintains comprehensive logs of all activities for auditability
4. **Orchestrator**: Coordinates all components and implements the Ralph Wiggum Loop for persistent operation

### Vault Structure

The system uses the following directory structure:

```
AI_Employee_Vault/
├── Inbox/              # Incoming files
├── Needs_Action/       # Items requiring processing
├── Done/               # Completed items
├── Plans/              # Detailed plans for complex tasks
├── Pending_Approval/   # Items requiring human approval
├── Logs/               # System logs (dated files)
├── Dashboard.md        # System status dashboard
├── Company_Handbook.md # Rules of engagement
└── Business_Goals.md   # Weekly objectives
```

## Setup

### Prerequisites

- Python 3.7 or higher
- Pip package manager

### Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install pyyaml
```

3. Create the vault structure (if not already created):

```bash
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Done,Plans,Pending_Approval,Logs}
```

4. Ensure the initial files exist:

```bash
# The system will create these automatically if they don't exist, but you can create them manually:
touch AI_Employee_Vault/{Dashboard.md,Company_Handbook.md,Business_Goals.md}
```

## Usage

### Running the Complete System

```bash
python AI_Employee.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder
```

This starts both the file watcher and reasoning engine in a coordinated manner with persistent operation.

### Running a Single Processing Cycle

```bash
python AI_Employee.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder --single-cycle
```

This processes any pending items once and then exits.

### Running Without Watching Directory (Reasoning Engine Only)

```bash
python AI_Employee.py --vault-path ./AI_Employee_Vault --single-cycle
```

This runs only the reasoning engine to process items already in the Needs_Action folder.

### Running Individual Components

#### File Watcher Only

```bash
python AI_Employee_Watcher.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder --scan-once
```

Or for continuous monitoring:

```bash
python AI_Employee_Watcher.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder
```

#### Reasoning Engine Only

```bash
python AI_Employee_Reasoning.py --vault-path ./AI_Employee_Vault --scan-once
```

#### Logging Utility

```bash
python AI_Employee_Logger.py --vault-path ./AI_Employee_Vault --event-type system_status --description "Manual log entry" --severity INFO
```

## Configuration

### Environment Variables

The system supports the following environment variables:

- `VAULT_PATH`: Path to the AI Employee Vault (default: `./AI_Employee_Vault`)
- `WATCH_DIR`: Directory to monitor for new files (default: `./watch_folder`)
- `WATCH_INTERVAL`: Time between scans in seconds (default: 10)
- `REASONING_INTERVAL`: Time between processing cycles in seconds (default: 15)
- `LOG_LEVEL`: Logging level (default: INFO)
- `SINGLE_CYCLE`: Run a single processing cycle and exit (default: False)

### Sensitive Content Detection

The system automatically detects sensitive content based on predefined keywords. When sensitive content is detected, the item is moved to the `Pending_Approval` folder for human review.

Sensitive keywords include:
- Password, credential, secret
- Credit card, SSN, financial, bank account
- Personal information, confidential
- Contract, legal, salary, medical information

## Workflow

### 1. File Monitoring
- The file watcher monitors a designated directory for new files
- New files are converted to markdown with YAML frontmatter in `/Needs_Action`

### 2. Task Processing
- The reasoning engine processes items in `/Needs_Action`
- Content is analyzed for sensitive keywords
- Complex tasks are identified for detailed planning

### 3. Routing Logic
- **Routine tasks**: Automatically processed and moved to `/Done`
- **Sensitive tasks**: Moved to `/Pending_Approval` for human review
- **Complex tasks**: Generate detailed plans in `/Plans`

### 4. Dashboard Updates
- System activity is recorded in `Dashboard.md`
- Status metrics are maintained

### 5. Logging
- All activities are logged in JSON format in dated files in `/Logs`

## Constitutional Compliance

The system adheres to the following principles:

- **Local-First Philosophy**: All data remains on local infrastructure, no cloud sync
- **Human-in-the-Loop Supremacy**: Sensitive actions are escalated to human approval
- **Safety > Speed > Convenience**: Error handling with safety brakes
- **Auditability by Default**: Comprehensive logging of all actions
- **Least-Privilege Access**: Only accesses required vault directories
- **Human Authority**: Critical decisions require approval

## Troubleshooting

### Common Issues

**"Vault path does not exist"**
- Verify the path is correct
- Ensure all required subdirectories exist

**"Permission denied"**
- Check that the system has read/write permissions to the vault directory
- Ensure the watched directory is accessible

**"Module not found: yaml"**
- Run `pip install pyyaml` to install the required dependency

### Checking System Health

1. Verify all required directories exist in the vault
2. Check that the dashboard is being updated
3. Review recent log files for any error messages
4. Ensure the system processes files from `/Needs_Action`

## Extending the System

The system is designed to be modular and extensible:

- Add new sensitive keywords to `utils/constants.py`
- Extend the reasoning engine with additional processing rules
- Modify the vault structure as needed for your use case
- Add new components following the established patterns
