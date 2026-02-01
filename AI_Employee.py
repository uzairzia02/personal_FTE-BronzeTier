#!/usr/bin/env python3
"""
AI Employee - Main Orchestrator
Coordinates the file watcher and reasoning engine in a persistent loop.
"""

import os
import sys
import time
import signal
import threading
import argparse
from datetime import datetime
import logging

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AI_Employee_Watcher import FileWatcher
from AI_Employee_Reasoning import ReasoningEngine
from AI_Employee_Logger import Logger
from utils.constants import DEFAULT_WATCH_INTERVAL, DEFAULT_REASONING_INTERVAL

class AIEmployee:
    """
    Main orchestrator for the AI Employee system.
    Manages the file watcher and reasoning engine in a persistent loop.
    """

    def __init__(self, vault_path, watch_dir=None, single_cycle=False):
        self.vault_path = vault_path
        self.watch_dir = watch_dir
        self.single_cycle = single_cycle
        self.running = True

        # Initialize components
        self.logger = Logger(vault_path)
        self.file_watcher = FileWatcher(vault_path, watch_dir) if watch_dir else None
        self.reasoning_engine = ReasoningEngine(vault_path)

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.logger.info("AI_Employee", "System initialized", {"vault_path": vault_path, "watch_dir": watch_dir})

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info("AI_Employee", f"Received signal {signum}, shutting down...")
        self.running = False

    def run_single_cycle(self):
        """Run one complete cycle of monitoring and processing."""
        self.logger.info("AI_Employee", "Starting single processing cycle")

        # Run watcher if configured
        if self.file_watcher:
            self.file_watcher.scan_and_process()

        # Run reasoning engine
        self.reasoning_engine.process_needs_action_items()

        self.logger.info("AI_Employee", "Completed single processing cycle")

    def run_persistent(self):
        """Run the system in persistent mode with concurrent components."""
        self.logger.info("AI_Employee", "Starting persistent operation mode")

        # Create threads for concurrent operation
        threads = []

        # Thread for file watcher if configured
        if self.file_watcher:
            def watcher_loop():
                while self.running:
                    try:
                        self.file_watcher.scan_and_process()
                        time.sleep(DEFAULT_WATCH_INTERVAL)
                    except Exception as e:
                        self.logger.error("AI_Employee", f"Error in watcher thread: {str(e)}")
                        time.sleep(DEFAULT_WATCH_INTERVAL)

            watcher_thread = threading.Thread(target=watcher_loop, daemon=True)
            threads.append(watcher_thread)
            watcher_thread.start()

        # Thread for reasoning engine
        def reasoning_loop():
            while self.running:
                try:
                    self.reasoning_engine.process_needs_action_items()
                    time.sleep(DEFAULT_REASONING_INTERVAL)
                except Exception as e:
                    self.logger.error("AI_Employee", f"Error in reasoning thread: {str(e)}")
                    time.sleep(DEFAULT_REASONING_INTERVAL)

        reasoning_thread = threading.Thread(target=reasoning_loop, daemon=True)
        threads.append(reasoning_thread)
        reasoning_thread.start()

        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("AI_Employee", "Keyboard interrupt received, shutting down...")
            self.running = False

        # Wait for threads to finish (they're daemon threads, so this is mostly for cleanup)
        for thread in threads:
            thread.join(timeout=1)

        self.logger.info("AI_Employee", "System shutdown complete")

    def run(self):
        """Main run method - starts the appropriate mode."""
        if self.single_cycle:
            self.run_single_cycle()
        else:
            self.run_persistent()


def main():
    parser = argparse.ArgumentParser(description='AI Employee - Automated Task Processor')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--watch-dir', help='Directory to monitor for new files')
    parser.add_argument('--single-cycle', action='store_true',
                       help='Run a single processing cycle instead of persistent operation')

    args = parser.parse_args()

    # Validate vault path exists
    if not os.path.isdir(args.vault_path):
        print(f"Error: Vault path '{args.vault_path}' does not exist")
        sys.exit(1)

    # If watch directory is specified, validate it exists
    if args.watch_dir and not os.path.isdir(args.watch_dir):
        print(f"Error: Watch directory '{args.watch_dir}' does not exist")
        sys.exit(1)

    # Create AI Employee instance and run
    ai_employee = AIEmployee(
        vault_path=args.vault_path,
        watch_dir=args.watch_dir,
        single_cycle=args.single_cycle
    )

    ai_employee.run()


if __name__ == "__main__":
    main()