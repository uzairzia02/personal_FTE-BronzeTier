#!/usr/bin/env python3
"""
AI Employee - File Watcher Module
Monitors a directory for new files and converts them to structured markdown items.
"""

import os
import hashlib
import time
from pathlib import Path
from datetime import datetime
import yaml
from typing import Dict, List, Optional

from AI_Employee_Logger import Logger
from utils.constants import PROCESSED_FILES_PATH


class FileWatcher:
    """
    Monitors a directory for new files and converts them to structured markdown items
    with YAML frontmatter in the Needs_Action directory.
    """

    def __init__(self, vault_path: str, watch_dir: str):
        self.vault_path = vault_path
        self.watch_dir = watch_dir
        self.needs_action_dir = os.path.join(vault_path, "Needs_Action")
        self.processed_files_path = PROCESSED_FILES_PATH

        # Initialize logger
        self.logger = Logger(vault_path)

        # Create processed files tracking if it doesn't exist
        if not os.path.exists(self.processed_files_path):
            with open(self.processed_files_path, 'w') as f:
                yaml.dump({}, f)

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file to prevent duplicates."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def has_been_processed(self, file_path: str, file_hash: str) -> bool:
        """Check if a file has already been processed based on its hash."""
        try:
            with open(self.processed_files_path, 'r') as f:
                processed_files = yaml.safe_load(f) or {}

            # Check if this hash exists in the processed files
            return file_hash in processed_files.values()
        except Exception as e:
            self.logger.error("FileWatcher", f"Error checking processed files: {str(e)}")
            return False

    def mark_as_processed(self, original_filename: str, file_hash: str):
        """Mark a file as processed by storing its hash."""
        try:
            # Load existing processed files
            if os.path.exists(self.processed_files_path):
                with open(self.processed_files_path, 'r') as f:
                    processed_files = yaml.safe_load(f) or {}
            else:
                processed_files = {}

            # Add the new file hash with timestamp
            processed_files[original_filename] = {
                'hash': file_hash,
                'timestamp': datetime.now().isoformat()
            }

            # Save updated processed files
            with open(self.processed_files_path, 'w') as f:
                yaml.dump(processed_files, f)
        except Exception as e:
            self.logger.error("FileWatcher", f"Error marking file as processed: {str(e)}")

    def create_markdown_with_frontmatter(self, original_file_path: str, file_content: str, file_hash: str):
        """Create a markdown file with YAML frontmatter in the Needs_Action directory."""
        try:
            original_filename = os.path.basename(original_file_path)
            file_size = os.path.getsize(original_file_path)
            file_modified = datetime.fromtimestamp(os.path.getmtime(original_file_path)).isoformat()

            # Create a unique filename for the markdown file
            base_name = os.path.splitext(original_filename)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            markdown_filename = f"{base_name}_{timestamp}.md"
            markdown_path = os.path.join(self.needs_action_dir, markdown_filename)

            # Create YAML frontmatter
            frontmatter = {
                'title': base_name,
                'created': datetime.now().isoformat(),
                'status': 'pending',
                'priority': 'medium',
                'sensitivity': 'routine',  # Will be updated by reasoning engine if needed
                'assigned_to': 'AI_Employee',
                'original_filename': original_filename,
                'original_file_size': file_size,
                'original_file_modified': file_modified,
                'file_hash': file_hash
            }

            # Write the markdown file with frontmatter
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False)
                f.write("---\n\n")

                # Add the original content (for text files) or a placeholder
                if self.is_text_file(original_file_path):
                    f.write(file_content)
                else:
                    f.write(f"Binary file content from {original_filename}\n")
                    f.write(f"Size: {file_size} bytes\n")
                    f.write(f"MD5 Hash: {file_hash}\n")

            self.logger.info("FileWatcher", f"Created markdown file: {markdown_filename}")
            return markdown_path
        except Exception as e:
            self.logger.error("FileWatcher", f"Error creating markdown file: {str(e)}")
            return None

    def is_text_file(self, file_path: str) -> bool:
        """Check if a file is likely a text file by attempting to read it."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(512)  # Try to read first 512 bytes
            return True
        except UnicodeDecodeError:
            return False
        except Exception:
            return False

    def scan_and_process(self):
        """Scan the watch directory and process any new files."""
        if not os.path.exists(self.watch_dir):
            self.logger.warning("FileWatcher", f"Watch directory does not exist: {self.watch_dir}")
            return

        # Get all files in the watch directory
        for filename in os.listdir(self.watch_dir):
            file_path = os.path.join(self.watch_dir, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            # Calculate file hash
            file_hash = self.calculate_file_hash(file_path)

            # Check if file has already been processed
            if self.has_been_processed(file_path, file_hash):
                continue  # Skip already processed files

            try:
                # Read file content (try to read as text, fall back to binary info)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    # For binary files, just record the file info
                    file_content = ""

                # Create markdown file with frontmatter
                markdown_path = self.create_markdown_with_frontmatter(file_path, file_content, file_hash)

                if markdown_path:
                    # Mark file as processed
                    self.mark_as_processed(filename, file_hash)

                    # Optionally, move the original file to a processed directory
                    # or leave it as is depending on requirements
                    self.logger.info("FileWatcher", f"Processed file: {filename}")
                else:
                    self.logger.error("FileWatcher", f"Failed to process file: {filename}")

            except Exception as e:
                self.logger.error("FileWatcher", f"Error processing file {filename}: {str(e)}")


def main():
    """Command line interface for the file watcher."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee File Watcher')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--watch-dir', required=True, help='Directory to monitor for new files')
    parser.add_argument('--scan-once', action='store_true', help='Scan once and exit')
    parser.add_argument('--interval', type=int, default=10, help='Interval between scans in seconds (default: 10)')

    args = parser.parse_args()

    watcher = FileWatcher(args.vault_path, args.watch_dir)

    if args.scan_once:
        watcher.scan_and_process()
    else:
        print(f"Starting file watcher on {args.watch_dir}, checking every {args.interval} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                watcher.scan_and_process()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopping file watcher...")


if __name__ == "__main__":
    main()