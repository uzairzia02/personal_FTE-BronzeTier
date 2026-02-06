#!/usr/bin/env python3
"""
Reasoning Engine Agent Skill Implementation
Wraps the ReasoningEngine functionality as an agent skill.
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_Employee_Reasoning import ReasoningEngine
from AI_Employee_Logger import Logger


def main():
    parser = argparse.ArgumentParser(description='Reasoning Engine Agent Skill - Processes items in Needs_Action')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--scan-once', action='store_true', help='Process all Needs_Action items once and exit')

    args = parser.parse_args()

    # Initialize the reasoning engine
    engine = ReasoningEngine(args.vault_path)

    if args.scan_once:
        # Process all items in Needs_Action once
        engine.process_needs_action_items()
        print(f"[SKILL] Reasoning engine completed processing Needs_Action items")
    else:
        # Process all items in Needs_Action once (default behavior for agent skill)
        engine.process_needs_action_items()
        print(f"[SKILL] Reasoning engine processed Needs_Action items")


if __name__ == "__main__":
    main()