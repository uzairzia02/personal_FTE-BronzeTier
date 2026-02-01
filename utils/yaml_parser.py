"""
Utility functions for parsing YAML frontmatter in markdown files.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Tuple, Any, Optional


def parse_yaml_frontmatter(file_path: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse a markdown file and extract YAML frontmatter and content.

    Args:
        file_path: Path to the markdown file

    Returns:
        Tuple of (frontmatter_dict, content_str)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for YAML frontmatter
    if content.startswith('---'):
        # Find the end of the YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_str = parts[1]
            markdown_content = parts[2]
            frontmatter = yaml.safe_load(yaml_str) or {}
            return frontmatter, markdown_content

    # If no frontmatter found, return empty frontmatter and full content
    return {}, content


def add_or_update_frontmatter(file_path: str, updates: Dict[str, Any]) -> bool:
    """
    Add or update YAML frontmatter in a markdown file.

    Args:
        file_path: Path to the markdown file
        updates: Dictionary of key-value pairs to add/update in frontmatter

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the file already has frontmatter
        if content.startswith('---'):
            # Split existing frontmatter from content
            parts = content.split('---', 2)
            if len(parts) >= 3:
                existing_frontmatter = yaml.safe_load(parts[1]) or {}
                markdown_content = parts[2]

                # Update the frontmatter
                existing_frontmatter.update(updates)

                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("---\n")
                    yaml.dump(existing_frontmatter, f, default_flow_style=False)
                    f.write("---\n")
                    f.write(markdown_content)

                return True
            else:
                # Malformed frontmatter, treat as no frontmatter
                frontmatter_exists = False
        else:
            frontmatter_exists = False

        # If no frontmatter existed, create new one
        if not frontmatter_exists:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                yaml.dump(updates, f, default_flow_style=False)
                f.write("---\n")
                f.write(markdown_content)

        return True
    except Exception as e:
        print(f"Error updating frontmatter in {file_path}: {str(e)}")
        return False


def validate_frontmatter(frontmatter: Dict[str, Any], required_fields: Optional[list] = None) -> Tuple[bool, list]:
    """
    Validate that required fields exist in the frontmatter.

    Args:
        frontmatter: The frontmatter dictionary
        required_fields: List of required field names (optional)

    Returns:
        Tuple of (is_valid, list_of_missing_fields)
    """
    if required_fields is None:
        required_fields = ['title', 'created', 'status', 'priority', 'sensitivity', 'assigned_to']

    missing_fields = []
    for field in required_fields:
        if field not in frontmatter:
            missing_fields.append(field)

    return len(missing_fields) == 0, missing_fields


def create_default_frontmatter(title: str = "", status: str = "pending",
                             priority: str = "medium", sensitivity: str = "routine") -> Dict[str, Any]:
    """
    Create a default frontmatter dictionary.

    Args:
        title: Title for the item
        status: Current status
        priority: Priority level
        sensitivity: Sensitivity level

    Returns:
        Dictionary with default frontmatter values
    """
    from datetime import datetime

    return {
        'title': title,
        'created': datetime.now().isoformat(),
        'status': status,
        'priority': priority,
        'sensitivity': sensitivity,
        'assigned_to': 'AI_Employee'
    }