"""
Utility functions for file operations like moving, copying, and validating files.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional


def move_file(source_path: str, destination_path: str) -> bool:
    """
    Move a file from source to destination.

    Args:
        source_path: Path to the source file
        destination_path: Path to the destination

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination_path)
        os.makedirs(dest_dir, exist_ok=True)

        # Move the file
        shutil.move(source_path, destination_path)
        return True
    except Exception as e:
        print(f"Error moving file from {source_path} to {destination_path}: {str(e)}")
        return False


def copy_file(source_path: str, destination_path: str) -> bool:
    """
    Copy a file from source to destination.

    Args:
        source_path: Path to the source file
        destination_path: Path to the destination

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination_path)
        os.makedirs(dest_dir, exist_ok=True)

        # Copy the file
        shutil.copy2(source_path, destination_path)
        return True
    except Exception as e:
        print(f"Error copying file from {source_path} to {destination_path}: {str(e)}")
        return False


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory

    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {str(e)}")
        return False


def get_files_in_directory(directory_path: str, extensions: Optional[List[str]] = None) -> List[str]:
    """
    Get a list of files in a directory, optionally filtered by extension.

    Args:
        directory_path: Path to the directory
        extensions: List of file extensions to filter by (e.g., ['.txt', '.md'])

    Returns:
        List of file paths
    """
    if not os.path.exists(directory_path):
        return []

    files = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            if extensions is None:
                files.append(item_path)
            else:
                _, ext = os.path.splitext(item_path)
                if ext.lower() in [ext.lower() for ext in extensions]:
                    files.append(item_path)

    return files


def is_safe_path(base_path: str, target_path: str) -> bool:
    """
    Check if a target path is safe (doesn't escape the base path).

    Args:
        base_path: Base directory that paths should be contained within
        target_path: Target path to check

    Returns:
        True if path is safe, False otherwise
    """
    try:
        base_path = os.path.abspath(base_path)
        target_path = os.path.abspath(target_path)
        return os.path.commonpath([base_path]) == os.path.commonpath([base_path, target_path])
    except Exception:
        return False


def validate_file_path(file_path: str, allowed_base_paths: List[str]) -> bool:
    """
    Validate that a file path is within allowed base paths.

    Args:
        file_path: Path to validate
        allowed_base_paths: List of allowed base paths

    Returns:
        True if path is valid, False otherwise
    """
    for base_path in allowed_base_paths:
        if is_safe_path(base_path, file_path):
            return True
    return False


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        Size in bytes, or -1 if an error occurs
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return -1


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to the file

    Returns:
        True if file exists, False otherwise
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)


def delete_file(file_path: str) -> bool:
    """
    Delete a file.

    Args:
        file_path: Path to the file

    Returns:
        True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")
        return False