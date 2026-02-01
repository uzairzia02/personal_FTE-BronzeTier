"""
Utility functions for validating the vault directory structure and integrity.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple


def validate_vault_structure(vault_path: str) -> Tuple[bool, List[str]]:
    """
    Validate that the vault has the required directory structure.

    Args:
        vault_path: Path to the vault

    Returns:
        Tuple of (is_valid, list_of_missing_directories)
    """
    required_dirs = [
        "Inbox",
        "Needs_Action",
        "Done",
        "Plans",
        "Pending_Approval",
        "Logs"
    ]

    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = os.path.join(vault_path, dir_name)
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)

    return len(missing_dirs) == 0, missing_dirs


def create_vault_structure(vault_path: str) -> bool:
    """
    Create the required vault directory structure if it doesn't exist.

    Args:
        vault_path: Path to the vault

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create the main vault directory if it doesn't exist
        os.makedirs(vault_path, exist_ok=True)

        # Create required subdirectories
        required_dirs = [
            "Inbox",
            "Needs_Action",
            "Done",
            "Plans",
            "Pending_Approval",
            "Logs"
        ]

        for dir_name in required_dirs:
            dir_path = os.path.join(vault_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)

        return True
    except Exception as e:
        print(f"Error creating vault structure: {str(e)}")
        return False


def validate_vault_integrity(vault_path: str) -> Tuple[bool, Dict[str, List[str]]]:
    """
    Validate the integrity of the vault by checking for critical files and permissions.

    Args:
        vault_path: Path to the vault

    Returns:
        Tuple of (is_valid, dict_of_issues)
    """
    issues = {}

    # Check if vault directory exists
    if not os.path.exists(vault_path):
        issues['vault_exists'] = ['Vault directory does not exist']
        return False, issues

    # Check if vault directory is writable
    if not os.access(vault_path, os.W_OK):
        issues['permissions'] = ['Vault directory is not writable']

    # Validate structure
    is_valid_structure, missing_dirs = validate_vault_structure(vault_path)
    if not is_valid_structure:
        issues['structure'] = [f'Missing directory: {dir_name}' for dir_name in missing_dirs]

    # Check for critical files
    critical_files = [
        "Dashboard.md",
        "Company_Handbook.md",
        "Business_Goals.md"
    ]

    missing_critical_files = []
    for file_name in critical_files:
        file_path = os.path.join(vault_path, file_name)
        if not os.path.exists(file_path):
            missing_critical_files.append(file_name)

    if missing_critical_files:
        issues['critical_files'] = [f'Missing critical file: {file_name}' for file_name in missing_critical_files]

    return len(issues) == 0, issues


def get_vault_statistics(vault_path: str) -> Dict[str, int]:
    """
    Get statistics about the vault contents.

    Args:
        vault_path: Path to the vault

    Returns:
        Dictionary with statistics
    """
    stats = {
        'inbox_count': 0,
        'needs_action_count': 0,
        'done_count': 0,
        'plans_count': 0,
        'pending_approval_count': 0,
        'logs_count': 0,
        'total_files': 0
    }

    for key, dir_name in [
        ('inbox_count', 'Inbox'),
        ('needs_action_count', 'Needs_Action'),
        ('done_count', 'Done'),
        ('plans_count', 'Plans'),
        ('pending_approval_count', 'Pending_Approval'),
        ('logs_count', 'Logs')
    ]:
        dir_path = os.path.join(vault_path, dir_name)
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            stats[key] = count
            stats['total_files'] += count

    return stats


def repair_vault_structure(vault_path: str) -> Tuple[bool, List[str]]:
    """
    Attempt to repair the vault structure by creating missing directories.

    Args:
        vault_path: Path to the vault

    Returns:
        Tuple of (is_repaired, list_of_repaired_items)
    """
    repaired_items = []

    # Create vault directory if needed
    if not os.path.exists(vault_path):
        os.makedirs(vault_path, exist_ok=True)
        repaired_items.append(f"Created vault directory: {vault_path}")

    # Validate structure and create missing directories
    is_valid, missing_dirs = validate_vault_structure(vault_path)

    for dir_name in missing_dirs:
        dir_path = os.path.join(vault_path, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        repaired_items.append(f"Created directory: {dir_name}")

    # Create critical files if they don't exist
    critical_files = [
        "Dashboard.md",
        "Company_Handbook.md",
        "Business_Goals.md"
    ]

    for file_name in critical_files:
        file_path = os.path.join(vault_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                if file_name == "Dashboard.md":
                    f.write("# AI Employee Dashboard\n\n## Recent Activity\n\n")
                elif file_name == "Company_Handbook.md":
                    f.write("# Company Handbook\n\nRules of engagement for AI Employee.\n")
                elif file_name == "Business_Goals.md":
                    f.write("# Business Goals\n\nWeekly objectives for AI Employee.\n")
            repaired_items.append(f"Created file: {file_name}")

    return len(repaired_items) > 0, repaired_items