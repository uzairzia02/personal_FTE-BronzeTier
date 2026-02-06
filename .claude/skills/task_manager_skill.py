#!/usr/bin/env python3
"""
Task Manager Agent Skill Implementation
Wraps the task management functionality as an agent skill.
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the task manager functionality
import task_manager


def main():
    parser = argparse.ArgumentParser(description='Task Manager Agent Skill - Manages and tracks tasks')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--list', action='store_true', help='List all tasks with their status')
    parser.add_argument('--mark-done', help='Mark a specific task as done (e.g., T022)')
    parser.add_argument('--approve', help='Approve a specific task (e.g., T022)')
    parser.add_argument('--tasks-file', help='Specify the path to the tasks.md file')

    args = parser.parse_args()

    # Set up arguments for the task manager
    sys.argv = ['task_manager.py']

    if args.list:
        sys.argv.extend(['--list'])
    elif args.mark_done:
        sys.argv.extend(['--mark-done', args.mark_done.upper()])
    elif args.approve:
        sys.argv.extend(['--approve', args.approve.upper()])

    if args.tasks_file:
        sys.argv.extend(['--tasks-file', args.tasks_file])

    # Call the original task manager main function
    task_manager.main()


if __name__ == "__main__":
    main()