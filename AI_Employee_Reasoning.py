#!/usr/bin/env python3
"""
AI Employee - Reasoning Engine Module
Processes items in Needs_Action, determines if they require human approval, and routes them appropriately.
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import shutil

from AI_Employee_Logger import Logger
from utils.constants import SENSITIVE_KEYWORDS


class ReasoningEngine:
    """
    Processes items in Needs_Action, determines if they require human approval, and routes them appropriately.
    Updates the dashboard with processing results.
    """

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.needs_action_dir = os.path.join(vault_path, "Needs_Action")
        self.done_dir = os.path.join(vault_path, "Done")
        self.pending_approval_dir = os.path.join(vault_path, "Pending_Approval")
        self.plans_dir = os.path.join(vault_path, "Plans")
        self.dashboard_path = os.path.join(vault_path, "Dashboard.md")

        # Initialize logger
        self.logger = Logger(vault_path)

    def parse_markdown_file(self, file_path: str) -> Tuple[Dict, str]:
        """
        Parse a markdown file with YAML frontmatter and return the frontmatter and content.
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

    def identify_sensitive_content(self, content: str) -> bool:
        """
        Identify if content contains sensitive keywords that require human approval.
        """
        content_lower = content.lower()

        for keyword in SENSITIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                self.logger.info("ReasoningEngine", f"Sensitive keyword '{keyword}' found in content")
                return True

        return False

    def identify_complex_task(self, content: str) -> bool:
        """
        Identify if the task is complex and requires detailed planning.
        """
        complex_indicators = [
            r'\bplan\b', r'\bstrategy\b', r'\bresearch\b', r'\banalysis\b',
            r'\breport\b', r'\bpresentation\b', r'\bproposal\b', r'\bdesign\b',
            r'\bdevelopment\b', r'\bimplementation\b', r'\bcreate.*detailed\b',
            r'\bneeds.*research\b', r'\brequires.*analysis\b'
        ]

        content_lower = content.lower()
        for indicator in complex_indicators:
            if re.search(indicator, content_lower):
                self.logger.info("ReasoningEngine", f"Complex task indicator '{indicator}' found in content")
                return True

        return False

    def create_approval_request(self, original_file_path: str, frontmatter: Dict, content: str):
        """
        Create an approval request for sensitive content.
        """
        try:
            original_filename = os.path.basename(original_file_path)

            # Extract a short description from the content for the filename
            # Take first 30 characters of content, strip whitespace and special chars
            short_desc = content.strip()[:30].replace('\n', ' ').replace('\r', ' ')
            # Remove special characters that might cause filesystem issues
            import re
            short_desc = re.sub(r'[^\w\s-]', '', short_desc)
            short_desc = re.sub(r'\s+', '_', short_desc).strip('_')

            # If short_desc is empty or just whitespace, use a generic term
            if not short_desc:
                short_desc = "task"

            # Create a new filename for the approval request with descriptive info
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            approval_filename = f"approval_{short_desc}_{timestamp}_{original_filename}"
            approval_path = os.path.join(self.pending_approval_dir, approval_filename)

            # Update frontmatter to indicate this needs approval
            frontmatter['status'] = 'approval_needed'
            frontmatter['approval_requested'] = datetime.now().isoformat()
            frontmatter['sensitivity'] = 'sensitive'
            frontmatter['reason_for_approval'] = 'Contains sensitive content'

            # Write the approval request file
            with open(approval_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False)
                f.write("---\n\n")
                f.write(content)

            self.logger.info("ReasoningEngine", f"Created approval request: {approval_filename}")

            # Remove the original file from Needs_Action
            os.remove(original_file_path)

            return approval_path
        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error creating approval request: {str(e)}")
            return None

    def create_plan(self, original_file_path: str, frontmatter: Dict, content: str):
        """
        Create a detailed plan for complex tasks.
        """
        try:
            original_filename = os.path.basename(original_file_path)

            # Extract a short description from the content for the filename
            # Take first 30 characters of content, strip whitespace and special chars
            import re
            short_desc = content.strip()[:30].replace('\n', ' ').replace('\r', ' ')
            # Remove special characters that might cause filesystem issues
            short_desc = re.sub(r'[^\w\s-]', '', short_desc)
            short_desc = re.sub(r'\s+', '_', short_desc).strip('_')

            # If short_desc is empty or just whitespace, use a generic term
            if not short_desc:
                short_desc = "task"

            # Create a new filename for the plan with descriptive info
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plan_filename = f"plan_{short_desc}_{timestamp}_{original_filename.replace('.md', '_plan.md')}"
            plan_path = os.path.join(self.plans_dir, plan_filename)

            # Update frontmatter for the plan
            frontmatter['status'] = 'planning'
            frontmatter['plan_created'] = datetime.now().isoformat()
            frontmatter['related_task'] = original_filename

            # Create a structured plan based on the content
            plan_content = self.generate_plan_content(content)

            # Write the plan file
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False)
                f.write("---\n\n")
                f.write("# Task Plan\n\n")
                f.write(plan_content)

            self.logger.info("ReasoningEngine", f"Created plan: {plan_filename}")

            # Move the original file to Done since a plan was created
            done_path = os.path.join(self.done_dir, original_filename)
            shutil.move(original_file_path, done_path)

            return plan_path
        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error creating plan: {str(e)}")
            return None

    def generate_plan_content(self, content: str) -> str:
        """
        Generate a structured plan based on the task content.
        """
        plan = f"""## Objective
{content[:100]}...

"""

        plan += "## Steps\n"
        plan += "1. Analyze the requirements\n"
        plan += "2. Research necessary information\n"
        plan += "3. Create detailed implementation\n"
        plan += "4. Test and validate results\n"
        plan += "5. Document and deliver\n\n"

        plan += "## Timeline\n"
        plan += "- Analysis: 1 day\n"
        plan += "- Implementation: 2-3 days\n"
        plan += "- Testing: 1 day\n"
        plan += "- Documentation: 0.5 days\n\n"

        plan += "## Success Criteria\n"
        plan += "- Requirements fulfilled\n"
        plan += "- Quality standards met\n"
        plan += "- Delivered on time\n\n"

        plan += "## Resources Needed\n"
        plan += "- Access to relevant information\n"
        plan += "- Appropriate tools\n"
        plan += "- Time allocation\n\n"

        plan += f"## Notes\nBased on original request: {content[:200]}..."

        return plan

    def update_dashboard(self, action_taken: str, filename: str, details: Dict = None):
        """
        Update the dashboard with recent activity.
        """
        try:
            # Create dashboard if it doesn't exist
            if not os.path.exists(self.dashboard_path):
                with open(self.dashboard_path, 'w', encoding='utf-8') as f:
                    f.write("# 🤖 AI Employee Dashboard\n\n")
                    f.write("## 📊 Status Overview\n")
                    f.write("- 🟡 **Pending Approval:** Files requiring human review\n")
                    f.write("- ✅ **Approved:** Files approved and moved to Done\n")
                    f.write("- ❌ **Rejected:** Files rejected and remaining in Pending_Approval\n")
                    f.write("- 📋 **Completed:** Files processed automatically\n\n")
                    f.write("## 📈 Current Status Summary\n")
                    f.write("- 🟡 **Pending Approval:** 0 files\n")
                    f.write("- ✅ **Needs Action:** 0 files\n")
                    f.write("- 📋 **Completed (Done):** 0 files\n")
                    f.write("- 📝 **In Planning:** 0 files\n\n")
                    f.write("## 🔄 Recent Activity\n\n")

            # Read current dashboard content
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                current_content = f.read()

            # Determine emoji and category based on action
            if "Approval Request" in action_taken:
                emoji = "🟡"
                category = "Pending Approval"
            elif "Approved" in action_taken:
                emoji = "✅"
                category = "Approved"
            elif "Rejected" in action_taken:
                emoji = "❌"
                category = "Rejected"
            elif "Completed" in action_taken:
                emoji = "📋"
                category = "Completed"
            else:
                emoji = "🔹"
                category = "Other"

            # Add new activity entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = f"- {emoji} [{timestamp}] {action_taken}: {filename}\n"

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
            with open(self.dashboard_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            # Now update the categorized summary
            self.update_categorized_summary()

            self.logger.info("ReasoningEngine", f"Updated dashboard with: {action_taken} for {filename}")
        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error updating dashboard: {str(e)}")

    def update_categorized_summary(self):
        """
        Update the dashboard with categorized summary of files in each directory.
        """
        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count files in each directory
            pending_approval_count = len(os.listdir(self.pending_approval_dir)) if os.path.exists(self.pending_approval_dir) else 0
            done_count = len(os.listdir(self.done_dir)) if os.path.exists(self.done_dir) else 0
            needs_action_count = len(os.listdir(self.needs_action_dir)) if os.path.exists(self.needs_action_dir) else 0
            plans_count = len(os.listdir(self.plans_dir)) if os.path.exists(self.plans_dir) else 0

            # Create the categorized summary
            summary_section = f"## 📈 Current Status Summary\n"
            summary_section += f"- 🟡 **Pending Approval:** {pending_approval_count} files\n"
            summary_section += f"- ✅ **Needs Action:** {needs_action_count} files\n"
            summary_section += f"- 📋 **Completed (Done):** {done_count} files\n"
            summary_section += f"- 📝 **In Planning:** {plans_count} files\n\n"

            # Replace the entire summary section using regex
            import re
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
            with open(self.dashboard_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error updating categorized summary: {str(e)}")

    def move_to_done(self, original_file_path: str):
        """
        Move a file to the Done directory.
        """
        try:
            original_filename = os.path.basename(original_file_path)

            # Extract a short description from the content for the filename (for consistency)
            frontmatter, content = self.parse_markdown_file(original_file_path)
            import re
            short_desc = content.strip()[:30].replace('\n', ' ').replace('\r', ' ')
            # Remove special characters that might cause filesystem issues
            short_desc = re.sub(r'[^\w\s-]', '', short_desc)
            short_desc = re.sub(r'\s+', '_', short_desc).strip('_')

            # If short_desc is empty or just whitespace, use the original filename
            if not short_desc:
                final_filename = original_filename
            else:
                # Create a more descriptive filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name_part, ext = os.path.splitext(original_filename)
                final_filename = f"done_{short_desc}_{timestamp}_{name_part}{ext}"

            done_path = os.path.join(self.done_dir, final_filename)

            # Update frontmatter to mark as done
            frontmatter['status'] = 'completed'
            frontmatter['completed_at'] = datetime.now().isoformat()

            # Write updated frontmatter back to file
            with open(original_file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # Replace frontmatter in content
            if file_content.startswith('---'):
                parts = file_content.split('---', 2)
                if len(parts) >= 3:
                    updated_content = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n" + parts[2]
                    with open(original_file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)

            # Move file to Done directory with new descriptive name
            shutil.move(original_file_path, done_path)

            self.logger.info("ReasoningEngine", f"Moved file to Done: {final_filename}")
            return done_path
        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error moving file to Done: {str(e)}")
            return None

    def process_file(self, file_path: str):
        """
        Process a single file from Needs_Action.
        """
        try:
            self.logger.info("ReasoningEngine", f"Processing file: {file_path}")

            # Parse the file
            frontmatter, content = self.parse_markdown_file(file_path)

            # Check for sensitive content
            if self.identify_sensitive_content(content):
                # Create approval request
                approval_path = self.create_approval_request(file_path, frontmatter, content)
                if approval_path:
                    self.update_dashboard("Created Approval Request", os.path.basename(approval_path))
                return "approval_created"

            # Check for complex tasks
            elif self.identify_complex_task(content):
                # Create a detailed plan
                plan_path = self.create_plan(file_path, frontmatter, content)
                if plan_path:
                    self.update_dashboard("Created Plan", os.path.basename(plan_path))
                return "plan_created"

            # For regular tasks, move to Done
            else:
                done_path = self.move_to_done(file_path)
                if done_path:
                    self.update_dashboard("Completed Task", os.path.basename(done_path))
                return "moved_to_done"

        except Exception as e:
            self.logger.error("ReasoningEngine", f"Error processing file {file_path}: {str(e)}")
            return "error"

    def process_needs_action_items(self):
        """
        Process all items in the Needs_Action directory.
        """
        if not os.path.exists(self.needs_action_dir):
            self.logger.warning("ReasoningEngine", f"Needs_Action directory does not exist: {self.needs_action_dir}")
            return

        # Get all markdown files in Needs_Action
        for filename in os.listdir(self.needs_action_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.needs_action_dir, filename)

                # Skip directories
                if os.path.isdir(file_path):
                    continue

                # Process the file
                result = self.process_file(file_path)
                self.logger.info("ReasoningEngine", f"File {filename} processing result: {result}")


def main():
    """Command line interface for the reasoning engine."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Reasoning Engine')
    parser.add_argument('--vault-path', required=True, help='Path to the AI Employee Vault')
    parser.add_argument('--process-single', help='Process a single file and exit')
    parser.add_argument('--scan-once', action='store_true', help='Process all Needs_Action items once and exit')

    args = parser.parse_args()

    engine = ReasoningEngine(args.vault_path)

    if args.process_single:
        # Process a single file
        if os.path.exists(args.process_single):
            result = engine.process_file(args.process_single)
            print(f"Processing result: {result}")
        else:
            print(f"File does not exist: {args.process_single}")
    elif args.scan_once or not args.process_single:
        # Process all Needs_Action items
        print("Processing all items in Needs_Action directory...")
        engine.process_needs_action_items()
        print("Processing complete.")


if __name__ == "__main__":
    main()