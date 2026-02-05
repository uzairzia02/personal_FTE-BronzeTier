#!/usr/bin/env python3
"""
Task Manager Script for FTE Bronze Tier Project

This script allows you to easily mark tasks as done from the command line.
Usage:
    python task_manager.py --mark-done <task_id>
    python task_manager.py --approve <task_id>
    python task_manager.py --list
    python task_manager.py --help
"""

import sys
import os
import argparse
import re
from pathlib import Path

def find_tasks_file():
    """Find the tasks.md file in the project"""
    # Look for tasks.md in common locations
    possible_paths = [
        "specs/1-ai-employee/tasks.md",
        "specs/*/tasks.md",
        "tasks.md",
        "./specs/**/tasks.md"
    ]

    for pattern in possible_paths:
        path = Path(pattern)
        if path.exists() and path.is_file():
            return str(path)

        # Try glob pattern matching
        if "*" in pattern or "**" in pattern:
            import glob
            matches = glob.glob(pattern, recursive=True)
            if matches:
                return matches[0]

    # If not found in relative paths, try absolute paths
    project_root = Path(__file__).parent
    for file_path in project_root.rglob("tasks.md"):
        if "specs" in str(file_path):
            return str(file_path)

    raise FileNotFoundError("Could not find tasks.md file")

def list_tasks(tasks_file):
    """List all tasks in the tasks file"""
    print(f"\n[TASKS] Current Tasks in {tasks_file}:")
    print("="*60)

    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all task lines with regex
    task_pattern = r'^(\s*- \[([ X])\]\s+(T\d+)\s+(.*?))$'
    lines = content.split('\n')

    for i, line in enumerate(lines):
        match = re.match(task_pattern, line)
        if match:
            full_match, status, task_id, description = match.groups()
            status_symbol = "DONE" if status == "X" else "TODO"
            print(f"[{status_symbol}] [{task_id}] {description}")

def mark_task_done(tasks_file, task_id):
    """Mark a specific task as done in the tasks file"""
    print(f"Marking task {task_id} as done...")

    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create pattern to match the specific task
    # Match the line that starts with - [ ], contains the task ID, and has the checkbox
    pattern = rf'^(\s*- \[([ X])\]\s+{re.escape(task_id)}\s+.*)$'

    def replace_checkbox(match):
        line_content = match.group(1)
        # Replace [ ] with [X] to mark as done
        updated_line = re.sub(r'\[ \]', '[X]', line_content, count=1)
        return updated_line

    # Find and replace the task line
    updated_content, num_replacements = re.subn(
        pattern, replace_checkbox, content, flags=re.MULTILINE
    )

    if num_replacements > 0:
        with open(tasks_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"[SUCCESS] Successfully marked task {task_id} as done!")
        return True
    else:
        print(f"[ERROR] Task {task_id} not found in the tasks file.")
        return False

def approve_task(tasks_file, task_id):
    """Mark a specific task as approved (same as done in this context)"""
    print(f"Approving task {task_id}...")
    return mark_task_done(tasks_file, task_id)

def main():
    parser = argparse.ArgumentParser(description='Task Manager for FTE Bronze Tier Project')
    parser.add_argument('--mark-done', '-d', dest='mark_done',
                       help='Mark a specific task as done (e.g., T022)')
    parser.add_argument('--approve', '-a', dest='approve',
                       help='Approve a specific task (e.g., T022)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all tasks with their status')
    parser.add_argument('--tasks-file', '-f',
                       help='Specify the path to the tasks.md file')

    args = parser.parse_args()

    # Find tasks file
    if args.tasks_file:
        tasks_file = args.tasks_file
    else:
        try:
            tasks_file = find_tasks_file()
        except FileNotFoundError:
            print("❌ Could not find tasks.md file in the project.")
            print("Please specify the path manually with --tasks-file")
            sys.exit(1)

    if args.list:
        list_tasks(tasks_file)
        return

    if args.mark_done:
        success = mark_task_done(tasks_file, args.mark_done.upper())
        if success:
            print(f"\n[COMMIT] Don't forget to commit your changes:")
            print(f"git add {tasks_file}")
            print(f"git commit -m \"Mark task {args.mark_done} as completed\"")
        sys.exit(0 if success else 1)

    if args.approve:
        success = approve_task(tasks_file, args.approve.upper())
        if success:
            print(f"\n[COMMIT] Don't forget to commit your changes:")
            print(f"git add {tasks_file}")
            print(f"git commit -m \"Approve task {args.approve}\"")
        sys.exit(0 if success else 1)

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nExamples:")
        print("  python task_manager.py --list")
        print("  python task_manager.py --mark-done T022")
        print("  python task_manager.py --approve T030")
        sys.exit(0)

if __name__ == "__main__":
    main()