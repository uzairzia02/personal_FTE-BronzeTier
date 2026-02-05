#!/usr/bin/env python3
"""
Approval Manager for FTE Bronze Tier Project

This script allows you to approve tasks from the Pending_Approval folder from the command line.
Usage:
    python approval_manager.py --list
    python approval_manager.py --approve <filename>
    python approval_manager.py --reject <filename>
    python approval_manager.py --help
"""

import sys
import os
import argparse
import re
from pathlib import Path
from datetime import datetime
import shutil

def find_vault_path():
    """Find the vault path - look for common vault directory names"""
    # Look for vault directory in common locations
    possible_paths = [
        "AI_Employee_Vault",
        "./AI_Employee_Vault",
        "../AI_Employee_Vault",
        "vault",
        "./vault"
    ]

    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            return path

    # If not found, look for directories containing the expected subdirectories
    for item in os.listdir('.'):
        if os.path.isdir(item):
            vault_path = os.path.join('.', item)
            required_dirs = ['Needs_Action', 'Done', 'Pending_Approval']
            if all(os.path.exists(os.path.join(vault_path, d)) for d in required_dirs):
                return vault_path

    # Default to a reasonable path
    return "AI_Employee_Vault"

def list_pending_approvals(vault_path):
    """List all pending approval items"""
    pending_dir = os.path.join(vault_path, "Pending_Approval")

    if not os.path.exists(pending_dir):
        print(f"[ERROR] Pending_Approval directory does not exist: {pending_dir}")
        return

    print(f"\n[APPROVALS] Pending Approval Items in {pending_dir}:")
    print("="*70)

    items = []
    for filename in os.listdir(pending_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(pending_dir, filename)
            stat = os.stat(filepath)
            mtime = datetime.fromtimestamp(stat.st_mtime)

            # Read the content to extract description
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract content after YAML frontmatter if present
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2][:100]  # First 100 chars of content
                    else:
                        content = content[:100]
                else:
                    content = content[:100]

                # Clean up content for display
                content = content.replace('\n', ' ').strip()

                items.append((filename, mtime.strftime("%Y-%m-%d %H:%M:%S"), content))
            except Exception as e:
                items.append((filename, mtime.strftime("%Y-%m-%d %H:%M:%S"), f"[Could not read: {str(e)}]"))

    if not items:
        print("[INFO] No pending approval items found.")
    else:
        for filename, timestamp, content in items:
            print(f"[{timestamp}] {filename}")
            print(f"  Content preview: {content}...")
            print()

def approve_item(vault_path, filename):
    """Approve a specific item from Pending_Approval"""
    pending_dir = os.path.join(vault_path, "Pending_Approval")
    done_dir = os.path.join(vault_path, "Done")
    dashboard_path = os.path.join(vault_path, "Dashboard.md")
    needs_action_dir = os.path.join(vault_path, "Needs_Action")

    pending_file = os.path.join(pending_dir, filename)

    if not os.path.exists(pending_file):
        print(f"[ERROR] File does not exist in Pending_Approval: {filename}")
        return False

    try:
        # Read the file to update its status
        with open(pending_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # If there's YAML frontmatter, update the status
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                yaml_str = parts[1]
                body = parts[2]

                # Parse and update the YAML frontmatter
                import yaml
                try:
                    frontmatter = yaml.safe_load(yaml_str) or {}

                    # Update approval status
                    frontmatter['status'] = 'approved'
                    frontmatter['approved_at'] = datetime.now().isoformat()
                    frontmatter['approved_by'] = 'command_line_user'

                    # Reconstruct the file with updated frontmatter
                    updated_content = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n" + body
                except:
                    # If YAML parsing fails, just add approval info to frontmatter
                    updated_content = content
            else:
                updated_content = content
        else:
            updated_content = content

        # Move to Done directory
        done_file = os.path.join(done_dir, filename)

        # Write the updated content back to the file temporarily
        with open(pending_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Move the file to Done
        shutil.move(pending_file, done_file)

        # Update the dashboard to record the approval
        update_dashboard_after_approval(dashboard_path, filename)

        print(f"[SUCCESS] Approved and moved to Done: {filename}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to approve {filename}: {str(e)}")
        return False

def reject_item(vault_path, filename):
    """Reject a specific item from Pending_Approval"""
    pending_dir = os.path.join(vault_path, "Pending_Approval")
    dashboard_path = os.path.join(vault_path, "Dashboard.md")

    pending_file = os.path.join(pending_dir, filename)

    if not os.path.exists(pending_file):
        print(f"[ERROR] File does not exist in Pending_Approval: {filename}")
        return False

    try:
        # Read the file to update its status
        with open(pending_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # If there's YAML frontmatter, update the status
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                yaml_str = parts[1]
                body = parts[2]

                # Parse and update the YAML frontmatter
                import yaml
                try:
                    frontmatter = yaml.safe_load(yaml_str) or {}

                    # Update rejection status
                    frontmatter['status'] = 'rejected'
                    frontmatter['rejected_at'] = datetime.now().isoformat()
                    frontmatter['rejected_by'] = 'command_line_user'
                    frontmatter['reason'] = 'Rejected via command line'

                    # Reconstruct the file with updated frontmatter
                    updated_content = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n" + body
                except:
                    # If YAML parsing fails, just add rejection info to frontmatter
                    updated_content = content
            else:
                updated_content = content
        else:
            updated_content = content

        # Update the file with rejection status
        with open(pending_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Update the dashboard to record the rejection
        update_dashboard_after_rejection(dashboard_path, filename)

        print(f"[SUCCESS] Rejected item: {filename}")
        print(f"[INFO] File remains in Pending_Approval with rejection status.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to reject {filename}: {str(e)}")
        return False


def update_dashboard_after_approval(dashboard_path, filename):
    """
    Update the dashboard with the approval completion.
    """
    try:
        # Create dashboard if it doesn't exist
        if not os.path.exists(dashboard_path):
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write("# 🤖 AI Employee Dashboard\n\n")
                f.write("## 📊 Status Overview\n")
                f.write("- 🟡 **Pending Approval:** Files requiring human review\n")
                f.write("- ✅ **Approved:** Files approved and moved to Done\n")
                f.write("- ❌ **Rejected:** Files rejected and remaining in Pending_Approval\n")
                f.write("- 📋 **Completed:** Files processed automatically\n\n")
                f.write("## 🔄 Recent Activity\n\n")

        # Read current dashboard content
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Add new activity entry for approval
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"- ✅ [{timestamp}] Manual Approval Completed: {filename}\n"

        # Insert new entry after the "Recent Activity" header
        lines = current_content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == "## 🔄 Recent Activity" or line.strip() == "## Recent Activity":
                lines.insert(i + 1, new_entry)
                break
        else:
            # If header not found, add it
            lines.extend(["", "## 🔄 Recent Activity", new_entry])

        # Write updated content back to dashboard
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # Update the categorized summary
        update_categorized_summary_from_approval_manager(dashboard_path)

    except Exception as e:
        print(f"[ERROR] Failed to update dashboard: {str(e)}")


def update_dashboard_after_rejection(dashboard_path, filename):
    """
    Update the dashboard with the rejection.
    """
    try:
        # Create dashboard if it doesn't exist
        if not os.path.exists(dashboard_path):
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write("# 🤖 AI Employee Dashboard\n\n")
                f.write("## 📊 Status Overview\n")
                f.write("- 🟡 **Pending Approval:** Files requiring human review\n")
                f.write("- ✅ **Approved:** Files approved and moved to Done\n")
                f.write("- ❌ **Rejected:** Files rejected and remaining in Pending_Approval\n")
                f.write("- 📋 **Completed:** Files processed automatically\n\n")
                f.write("## 🔄 Recent Activity\n\n")

        # Read current dashboard content
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Add new activity entry for rejection
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"- ❌ [{timestamp}] Manual Rejection: {filename}\n"

        # Insert new entry after the "Recent Activity" header
        lines = current_content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == "## 🔄 Recent Activity" or line.strip() == "## Recent Activity":
                lines.insert(i + 1, new_entry)
                break
        else:
            # If header not found, add it
            lines.extend(["", "## 🔄 Recent Activity", new_entry])

        # Write updated content back to dashboard
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # Update the categorized summary
        update_categorized_summary_from_approval_manager(dashboard_path)

    except Exception as e:
        print(f"[ERROR] Failed to update dashboard: {str(e)}")


def update_categorized_summary_from_approval_manager(dashboard_path):
    """
    Update the dashboard with categorized summary of files in each directory.
    """
    try:
        # Get vault path from dashboard path
        vault_path = os.path.dirname(dashboard_path)

        # Define directory paths
        pending_approval_dir = os.path.join(vault_path, "Pending_Approval")
        done_dir = os.path.join(vault_path, "Done")
        needs_action_dir = os.path.join(vault_path, "Needs_Action")
        plans_dir = os.path.join(vault_path, "Plans")

        # Count files in each directory
        pending_approval_count = len(os.listdir(pending_approval_dir)) if os.path.exists(pending_approval_dir) else 0
        done_count = len(os.listdir(done_dir)) if os.path.exists(done_dir) else 0
        needs_action_count = len(os.listdir(needs_action_dir)) if os.path.exists(needs_action_dir) else 0
        plans_count = len(os.listdir(plans_dir)) if os.path.exists(plans_dir) else 0

        # Read current content
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create the categorized summary
        summary_section = f"## 📈 Current Status Summary\n"
        summary_section += f"- 🟡 **Pending Approval:** {pending_approval_count} files\n"
        summary_section += f"- ✅ **Needs Action:** {needs_action_count} files\n"
        summary_section += f"- 📋 **Completed (Done):** {done_count} files\n"
        summary_section += f"- 📝 **In Planning:** {plans_count} files\n\n"

        # Replace the entire summary section using regex
        import re
        # Pattern to match the entire summary section
        pattern = r'## 📈 Current Status Summary.*?(?=## |\n-\s*\w|\Z)'
        updated_content = re.sub(pattern, summary_section.rstrip(), content, flags=re.DOTALL)

        # Ensure the status overview section is clean
        status_overview_section = "## 📊 Status Overview\n"
        status_overview_section += "- 🟡 **Pending Approval:** Files requiring human review\n"
        status_overview_section += "- ✅ **Approved:** Files approved and moved to Done\n"
        status_overview_section += "- ❌ **Rejected:** Files rejected and remaining in Pending_Approval\n"
        status_overview_section += "- 📋 **Completed:** Files processed automatically\n\n"

        # Replace the status overview section
        pattern_status = r'## 📊 Status Overview.*?(?=## 📈|## 🔄|\n\n|\Z)'
        updated_content = re.sub(pattern_status, status_overview_section.rstrip(), updated_content, flags=re.DOTALL)

        # Write updated content back to dashboard
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

    except Exception as e:
        print(f"[ERROR] Failed to update categorized summary: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Approval Manager for AI Employee System')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all pending approval items')
    parser.add_argument('--approve', '-a',
                       help='Approve a specific file from Pending_Approval')
    parser.add_argument('--reject', '-r',
                       help='Reject a specific file from Pending_Approval')
    parser.add_argument('--vault-path', '-v',
                       help='Path to the AI Employee Vault')
    parser.add_argument('--pending-dir',
                       help='Specific path to Pending_Approval directory')

    args = parser.parse_args()

    # Determine vault path
    if args.vault_path:
        vault_path = args.vault_path
    elif args.pending_dir:
        # If pending dir is specified, derive vault path from it
        pending_path = Path(args.pending_dir)
        vault_path = str(pending_path.parent)
    else:
        vault_path = find_vault_path()

    if args.list:
        list_pending_approvals(vault_path)
        return

    if args.approve:
        success = approve_item(vault_path, args.approve)
        sys.exit(0 if success else 1)

    if args.reject:
        success = reject_item(vault_path, args.reject)
        sys.exit(0 if success else 1)

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nExamples:")
        print("  python approval_manager.py --list")
        print("  python approval_manager.py --approve approval_20231201_123456_sometask.md")
        print("  python approval_manager.py --reject approval_20231201_123456_sometask.md")
        sys.exit(0)

if __name__ == "__main__":
    main()