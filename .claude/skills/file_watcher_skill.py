#!/usr/bin/env python3
"""
File Watcher Agent Skill Implementation
Wraps the FileWatcher functionality as an agent skill.
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_Employee_Watcher import FileWatcher
from AI_Employee_Logger import Logger


def main():
    parser = argparse.ArgumentParser(description='File Watcher Agent Skill - Monitors a directory for new files')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--watch-dir', required=True, help='Directory to monitor for new files')
    parser.add_argument('--scan-once', action='store_true', help='Scan once and exit')

    args = parser.parse_args()

    # Initialize the file watcher
    watcher = FileWatcher(args.vault_path, args.watch_dir)

    if args.scan_once:
        # Perform a single scan
        watcher.scan_and_process()
        print(f"[SKILL] File watcher completed single scan of {args.watch_dir}")
    else:
        # This would typically run continuously, but for an agent skill
        # we'll just do a single scan to avoid blocking
        watcher.scan_and_process()
        print(f"[SKILL] File watcher processed {args.watch_dir}")


if __name__ == "__main__":
    main()