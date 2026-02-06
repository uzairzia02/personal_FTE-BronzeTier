# Approval Manager Agent Skill

## Description
Manages the approval workflow for tasks that require human review. Allows listing, approving, and rejecting tasks from the Pending_Approval directory.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required if not specifying pending-dir)
- `--list`: List all pending approval items
- `--approve`: Approve a specific file from Pending_Approval
- `--reject`: Reject a specific file from Pending_Approval

## Usage Examples
```
/approval-manager --vault-path "./AI_Employee_Vault" --list
/approval-manager --vault-path "./AI_Employee_Vault" --approve "approval_filename.md"
/approval-manager --vault-path "./AI_Employee_Vault" --reject "approval_filename.md"
```

## Implementation
This skill wraps the approval management functionality from approval_manager.py, enabling human oversight of sensitive tasks in the AI Employee system.

## Capabilities
- List pending approval items with content previews
- Approve specific items to move them to Done directory
- Reject specific items to keep them in Pending_Approval with rejection status
- Update dashboard with approval/rejection activities
- Maintain YAML frontmatter with approval/rejection metadata