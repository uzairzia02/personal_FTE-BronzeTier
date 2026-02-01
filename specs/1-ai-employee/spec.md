# AI Employee (Bronze Tier) Specification

## Overview

Build a minimum viable Personal AI Employee using Claude Code that follows a local-first, agent-based architecture. The system will operate 24/7 using an Obsidian vault as its memory system, with automated watchers, reasoning capabilities, and human-in-the-loop approval mechanisms.

## User Scenarios & Testing

### Primary User Scenario
As a busy professional, I want an AI employee that can monitor my inbox and file system, process routine tasks automatically, and escalate important decisions to me for approval, so that I can focus on high-value activities while maintaining control over critical decisions.

### Secondary User Scenarios
1. As a user, I want the AI employee to organize and prioritize incoming tasks so I can focus on important items.
2. As a user, I want the AI employee to maintain detailed logs of all activities for audit and review purposes.
3. As a user, I want the AI employee to follow company handbook rules and business goals to maintain consistency in operations.

### Testing Approach
- Verify that new items in monitored locations create corresponding files in `/Needs_Action`
- Confirm that the AI employee processes items from `/Needs_Action` and moves them to `/Done`
- Test that sensitive actions are escalated to `/Pending_Approval` as required
- Validate that the dashboard updates with recent activity
- Ensure the system handles errors gracefully and continues operation

## Functional Requirements

### FR1: Obsidian Vault Setup
- The system shall create an Obsidian vault named "AI_Employee_Vault"
- The system shall create the following directories: `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`, `/Pending_Approval`, `/Logs`
- The system shall create initial files: `Dashboard.md`, `Company_Handbook.md`, `Business_Goals.md`
- The system shall initialize these files with appropriate baseline content

### FR2: Watcher Service
- The system shall monitor either Gmail inbox or file system for new items
- When new items are detected, the system shall create markdown files in `/Needs_Action` with standardized frontmatter
- The system shall prevent duplicate processing of the same items
- The system shall include appropriate metadata in the frontmatter (type, source, timestamp, status, priority)

### FR3: Reasoning Engine
- The system shall read all files in `/Needs_Action` periodically
- For each item, the system shall determine appropriate next steps
- The system shall create plan files in `/Plans` when complex tasks are identified
- The system shall update `Dashboard.md` with recent activity
- The system shall move processed items to `/Done` after completion

### FR4: Human-in-the-Loop Processing
- When sensitive actions are required, the system shall create approval request files in `/Pending_Approval`
- The system shall pause processing until approval is received (for Bronze Tier, this is a placeholder)
- The system shall document approval requirements in accordance with the constitution

### FR5: Logging and Monitoring
- The system shall maintain logs of all activities in `/Logs`
- The system shall record timestamps, actions taken, and outcomes
- The system shall support basic audit trail requirements

### FR6: Ralph Wiggum Loop Implementation
- The system shall implement retry logic to ensure task completion
- The system shall continue processing until items are moved from `/Needs_Action` to `/Done`
- The system shall have appropriate safety limits to prevent infinite loops

## Non-Functional Requirements

### NFR1: Local-First Operation
- All data must remain on the local system
- No cloud storage of sensitive information
- All processing must occur locally

### NFR2: Free Tier Compatibility
- The system must operate without requiring paid APIs
- All components must be compatible with free-tier tools
- No external dependencies on commercial services

### NFR3: Reliability
- The system shall handle errors gracefully
- The system shall maintain operation despite individual component failures
- The system shall preserve data integrity during failures

## Success Criteria

### Quantitative Measures
- 100% of new items detected are processed into actionable files
- 95% of routine tasks are completed without human intervention
- 100% of sensitive actions are escalated for approval when required
- Dashboard updates occur within 30 seconds of activity
- Log entries are created for all major system actions

### Qualitative Measures
- Users report increased productivity after implementing the AI employee
- Users feel confident that sensitive decisions are appropriately escalated
- The system demonstrates reliable operation over extended periods
- The system follows established business rules consistently

## Key Entities

### AI Employee
The core system that performs automated tasks and decision-making within defined boundaries.

### Obsidian Vault
The centralized knowledge base and memory system for the AI employee.

### Watcher
Component that monitors external inputs (email/file system) and creates actionable items.

### Reasoning Engine
Component that processes tasks and determines appropriate actions.

### Human-in-the-Loop (HITL)
Mechanism for escalating sensitive decisions to human operators.

## Scope

### In Scope
- Obsidian vault setup and initialization
- File system watcher implementation
- Task processing and routing logic
- Dashboard and logging systems
- Human approval workflow placeholders

### Out of Scope
- Advanced machine learning models
- Complex natural language understanding
- Third-party API integrations beyond essential functions
- Real-time communication channels beyond file-based interaction

## Assumptions

- The user has Claude Code installed and configured
- The user has access to Obsidian for the vault interface
- Basic file system access is available for the watcher
- The user will provide appropriate credentials for email access if chosen
- The system will run on a local machine with sufficient resources

## Constraints

- Must operate within free tier limitations of all tools
- All sensitive data must remain local
- Must comply with the AI Employee Constitution
- System must be auditable and transparent in its operations
- All actions must be reversible or recoverable

## Clarifications

### Session 2026-01-30

- Q: Which type of watcher should be the primary implementation? → A: File System Watcher
- Q: What criteria should determine if an action requires human approval? → A: Content-based classification using keywords and patterns
- Q: What should be the system's approach when encountering processing errors? → A: Retry with limits and escalation
- Q: How frequently should the system check for and process tasks? → A: Configurable intervals
- Q: How often should the dashboard be updated with new activity? → A: Near real-time updates