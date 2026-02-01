#!/usr/bin/env python3
"""
Demo script to test the AI Employee system
"""

import os
import time
from AI_Employee_Watcher import FileWatcher
from AI_Employee_Reasoning import ReasoningEngine

def demo():
    print("AI Employee System Demo")
    print("=" * 50)

    # Define vault path
    vault_path = "./AI_Employee_Vault"
    watch_dir = "./test_watch_dir"

    print(f"Vault path: {vault_path}")
    print(f"Watch directory: {watch_dir}")
    print()

    # Create instances
    watcher = FileWatcher(vault_path, watch_dir)
    reasoning_engine = ReasoningEngine(vault_path)

    print("Created FileWatcher and ReasoningEngine instances")

    # Scan and process any new files
    print("Scanning for new files...")
    watcher.scan_and_process()

    print("Processing items in Needs_Action...")
    reasoning_engine.process_needs_action_items()

    print()
    print("Vault Directory Contents:")
    for dir_name in ["Inbox", "Needs_Action", "Done", "Plans", "Pending_Approval"]:
        dir_path = os.path.join(vault_path, dir_name)
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            print(f"  {dir_name}: {len(files)} files")

    print()
    print("Done directory contents:")
    done_dir = os.path.join(vault_path, "Done")
    if os.path.exists(done_dir):
        done_files = os.listdir(done_dir)
        for f in done_files[-5:]:  # Show last 5 files
            print(f"  {f}")

    print()
    print("Recent Dashboard Activity:")
    dashboard_path = os.path.join(vault_path, "Dashboard.md")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Show recent activity section
            lines = content.split('\n')
            in_recent_activity = False
            for line in lines:
                if "## Recent Activity" in line:
                    in_recent_activity = True
                    print("  Recent Activity Section:")
                elif in_recent_activity and line.strip().startswith('- [') and '] ' in line:
                    print(f"    {line.strip()}")
                elif in_recent_activity and line.strip().startswith('## ') and 'Recent Activity' not in line:
                    break  # End of recent activity section

    print()
    print("Demo completed successfully!")

if __name__ == "__main__":
    demo()