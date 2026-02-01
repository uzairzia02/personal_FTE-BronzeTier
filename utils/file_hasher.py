"""
Utility functions for calculating file hashes to prevent duplicates.
"""

import hashlib
import os
from typing import Optional


def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path: Path to the file to hash
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        Hex digest of the hash, or None if an error occurs
    """
    try:
        hash_func = getattr(hashlib, algorithm)()

        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {str(e)}")
        return None


def compare_files_by_hash(file1_path: str, file2_path: str, algorithm: str = 'sha256') -> bool:
    """
    Compare two files by their hash values.

    Args:
        file1_path: Path to the first file
        file2_path: Path to the second file
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        True if files have the same hash, False otherwise
    """
    hash1 = calculate_file_hash(file1_path, algorithm)
    hash2 = calculate_file_hash(file2_path, algorithm)

    if hash1 is None or hash2 is None:
        return False

    return hash1 == hash2


def hash_content(content: str, algorithm: str = 'sha256') -> str:
    """
    Calculate the hash of a string content.

    Args:
        content: String content to hash
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        Hex digest of the hash
    """
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(content.encode('utf-8'))
    return hash_func.hexdigest()


def is_duplicate_content(file_path: str, content: str, algorithm: str = 'sha256') -> bool:
    """
    Check if the given content is a duplicate of the file content.

    Args:
        file_path: Path to the file to compare
        content: Content to compare against the file
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        True if content matches file content, False otherwise
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        return hash_content(file_content, algorithm) == hash_content(content, algorithm)
    except Exception:
        # If there's an error reading the file, assume it's not a duplicate
        return False