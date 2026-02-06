#!/usr/bin/env python3
"""
AI Employee Agent Skill Implementation
Wraps the main AI Employee orchestrator functionality as an agent skill.
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the AI Employee functionality
from AI_Employee import main as ai_employee_main


def main():
    parser = argparse.ArgumentParser(description='AI Employee Agent Skill - Main orchestrator for the AI Employee system')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--watch-dir', help='Directory to monitor for new files')
    parser.add_argument('--single-cycle', action='store_true',
                       help='Run a single processing cycle instead of persistent operation')

    args = parser.parse_args()

    # Since the AI Employee module expects sys.argv to contain the arguments,
    # we need to temporarily modify sys.argv
    original_argv = sys.argv.copy()

    # Prepare the arguments for the AI Employee module
    sys.argv = ['AI_Employee.py', '--vault-path', args.vault_path]

    if args.watch_dir:
        sys.argv.extend(['--watch-dir', args.watch_dir])

    if args.single_cycle:
        sys.argv.append('--single-cycle')

    # Call the original AI Employee main function
    try:
        ai_employee_main()
    finally:
        # Restore the original sys.argv
        sys.argv = original_argv


if __name__ == "__main__":
    main()