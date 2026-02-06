# Reasoning Engine Agent Skill

## Description
Processes items in Needs_Action, determines if they require human approval, and routes them appropriately. Updates the dashboard with processing results.

## Parameters
- `--vault-path`: Path to the AI Employee Vault (required)
- `--scan-once`: Process all Needs_Action items once and exit (optional, default: false)

## Usage Examples
```
/reasoning-engine --vault-path "./AI_Employee_Vault" --scan-once
```

## Implementation
This skill wraps the ReasoningEngine functionality from AI_Employee_Reasoning.py, enabling intelligent processing of tasks and routing them to appropriate directories based on content analysis.

## Capabilities
- Identifies sensitive content that requires human approval
- Routes sensitive content to Pending_Approval directory
- Creates detailed plans for complex tasks in Plans directory
- Moves routine tasks to Done directory
- Updates dashboard with processing results
- Maintains YAML frontmatter with status information