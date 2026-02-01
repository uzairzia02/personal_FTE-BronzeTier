#!/usr/bin/env python3
"""
AI Employee - Logger Module
Provides JSON-formatted logging with timestamp and severity support.
"""

import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
import threading


class Severity(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """
    JSON logger that creates properly formatted log entries in dated files.
    """

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.logs_dir = os.path.join(vault_path, "Logs")

        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)

        # Thread lock for safe logging
        self._lock = threading.Lock()

    def _get_log_file_path(self) -> str:
        """Get the path for today's log file."""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.logs_dir, f"log_{today}.jsonl")

    def _write_log_entry(self, severity: Severity, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Write a log entry to the appropriate log file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity.value,
            "component": component,
            "description": description,
            "details": details or {}
        }

        with self._lock:
            log_file_path = self._get_log_file_path()
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')

    def debug(self, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log a debug message."""
        self._write_log_entry(Severity.DEBUG, component, description, details)

    def info(self, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log an info message."""
        self._write_log_entry(Severity.INFO, component, description, details)

    def warning(self, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        self._write_log_entry(Severity.WARNING, component, description, details)

    def error(self, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log an error message."""
        self._write_log_entry(Severity.ERROR, component, description, details)

    def critical(self, component: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log a critical message."""
        self._write_log_entry(Severity.CRITICAL, component, description, details)


def main():
    """Command line interface for testing the logger."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Logger')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--event-type', required=True, help='Type of event to log')
    parser.add_argument('--description', required=True, help='Description of the event')
    parser.add_argument('--severity', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       default='INFO', help='Severity level (default: INFO)')
    parser.add_argument('--details', help='Additional details as JSON string')

    args = parser.parse_args()

    logger = Logger(args.vault_path)

    # Parse details if provided
    details = None
    if args.details:
        try:
            details = json.loads(args.details)
        except json.JSONDecodeError:
            print("Invalid JSON for details, skipping...")
            details = None

    # Log the event based on severity
    severity_enum = Severity(args.severity)

    if severity_enum == Severity.DEBUG:
        logger.debug(args.event_type, args.description, details)
    elif severity_enum == Severity.INFO:
        logger.info(args.event_type, args.description, details)
    elif severity_enum == Severity.WARNING:
        logger.warning(args.event_type, args.description, details)
    elif severity_enum == Severity.ERROR:
        logger.error(args.event_type, args.description, details)
    elif severity_enum == Severity.CRITICAL:
        logger.critical(args.event_type, args.description, details)

    print(f"Logged event: {args.description}")


if __name__ == "__main__":
    main()
