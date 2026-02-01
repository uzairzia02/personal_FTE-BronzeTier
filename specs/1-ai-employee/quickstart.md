# AI Employee (Bronze Tier) Quickstart Guide

## Prerequisites

- Python 3.7 or higher
- Pip package manager
- Basic command line familiarity

## Installation

### 1. Clone or download the AI Employee system
```bash
# If you have the files locally, navigate to the project directory
cd /path/to/ai-employee-system
```

### 2. Install required dependencies
```bash
pip install pyyaml
```

### 3. Verify the vault structure exists
The system should have the following directory structure:
```
AI_Employee_Vault/
├── Inbox/
├── Needs_Action/
├── Done/
├── Plans/
├── Pending_Approval/
├── Logs/
├── Dashboard.md
├── Company_Handbook.md
└── Business_Goals.md
```

If the structure doesn't exist, run the setup script or create it manually.

## Basic Usage

### Running the Complete System
```bash
python AI_Employee.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder
```

This starts both the file watcher and reasoning engine in a coordinated manner.

### Running a Single Processing Cycle
```bash
python AI_Employee.py --vault-path ./AI_Employee_Vault --single-cycle
```

This processes any pending items once and then exits.

### Running Individual Components

#### File Watcher Only
```bash
python AI_Employee_Watcher.py --vault-path ./AI_Employee_Vault --watch-dir ./watch_this_folder --interval 10
```

#### Reasoning Engine Only
```bash
python AI_Employee_Reasoning.py --vault-path ./AI_Employee_Vault --interval 15
```

#### Logging Utility
```bash
python AI_Employee_Logger.py --vault-path ./AI_Employee_Vault --event-type system_status --description "Manual log entry" --severity INFO
```

## Configuration

### File Watcher Settings
- `--watch-dir`: Directory to monitor for new files
- `--vault-path`: Path to the AI Employee Vault
- `--interval`: Time between scans in seconds (default: 10)

### Reasoning Engine Settings
- `--vault-path`: Path to the AI Employee Vault
- `--interval`: Time between processing cycles in seconds (default: 15)

## Example Workflow

### 1. Place a file in your watched directory
For example, create a file called `important_task.txt` in your watched directory.

### 2. Observe the system in action
- The file watcher detects the new file
- A markdown file with YAML frontmatter is created in `/Needs_Action`
- The reasoning engine processes the file
- Depending on content, it may be:
  - Automatically processed and moved to `/Done`
  - Flagged as sensitive and moved to `/Pending_Approval`
  - Identified as complex and get a plan in `/Plans`

### 3. Check the dashboard
Open `Dashboard.md` to see recent activity and system status.

### 4. Review logs
Check the appropriate log file in `/Logs` (named by date) to see detailed system activity.

## Troubleshooting

### Common Issues

#### "Vault path does not exist"
- Verify the path is correct
- Ensure all required subdirectories exist

#### "Permission denied"
- Check that the system has read/write permissions to the vault directory
- Ensure the watched directory is accessible

#### "Module not found: yaml"
- Run `pip install pyyaml` to install the required dependency

### Checking System Health
1. Verify all required directories exist in the vault
2. Check that the dashboard is being updated
3. Review recent log files for any error messages
4. Ensure the system processes files from `/Needs_Action`

## Next Steps

- Customize `Company_Handbook.md` with your specific rules of engagement
- Update `Business_Goals.md` with your weekly objectives
- Adjust the sensitivity detection keywords in the reasoning engine for your specific needs
- Set up automated startup of the AI Employee system if desired