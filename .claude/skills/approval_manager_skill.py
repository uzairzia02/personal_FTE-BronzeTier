#!/usr/bin/env python3
"""
Approval Manager Agent Skill Implementation
Wraps the approval management functionality as an agent skill.
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the approval manager functionality
import approval_manager


def main():
    parser = argparse.ArgumentParser(description='Approval Manager Agent Skill - Manages approval workflow for sensitive tasks')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--list', '-l', action='store_true', help='List all pending approval items')
    parser.add_argument('--approve', '-a', help='Approve a specific file from Pending_Approval')
    parser.add_argument('--reject', '-r', help='Reject a specific file from Pending_Approval')

    args = parser.parse_args()

    # Set up arguments for the approval manager
    sys.argv = ['approval_manager.py']

    if args.list:
        sys.argv.extend(['--list'])
    elif args.approve:
        sys.argv.extend(['--approve', args.approve])
    elif args.reject:
        sys.argv.extend(['--reject', args.reject])

    # Set vault path as needed
    if '--list' in sys.argv:
        sys.argv.extend(['--vault-path', args.vault_path])
    elif args.approve or args.reject:
        sys.argv.extend(['--vault-path', args.vault_path])

    # Call the original approval manager main function
    approval_manager.main()


if __name__ == "__main__":
    main()