---
id: 3
title: Plan AI Employee Bronze Tier
stage: plan
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-employee
branch: 1-ai-employee
user: user
command: /sp.plan
labels: [ai-employee, bronze-tier, planning, architecture]
links:
  spec: specs/1-ai-employee/spec.md
  plan: specs/1-ai-employee/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-employee/plan.md
  - specs/1-ai-employee/research.md
  - specs/1-ai-employee/data-model.md
  - specs/1-ai-employee/quickstart.md
tests:
  - none
---

## Prompt

You are Claude Code. You are tasked to generate detailed, actionable, step-by-step plans for the AI Employee system according to the Bronze Tier specifications and free setup constraints.

Context:
- The AI Employee system is designed to operate entirely locally, with no paid APIs or cloud dependencies.
- The system uses an Obsidian Vault structure with directories: /Inbox, /Needs_Action, /Done, /Plans, /Pending_Approval, /Logs.
- Sensitive actions must follow the human-in-the-loop approval workflow and be placed in /Pending_Approval.
- The system should monitor incoming tasks (using the File System Watcher) and convert them into structured markdown items.
- All tasks must include YAML frontmatter with metadata (title, created date, status, priority, sensitivity, assigned_to, etc.).
- Maintain comprehensive logging for auditability.

Task:
1. Review the input task from /Needs_Action or /Inbox.
2. Analyze its content and classify it as either:
   - Routine task (can be executed automatically)
   - Sensitive task (requires human approval)
3. If sensitive, move it to /Pending_Approval and provide a plan for human review.
4. If routine, generate a structured step-by-step plan in markdown format, ready to be executed by the AI Employee.
5. For every plan, include:
   - Objective: Clear description of the goal
   - Steps: Step-by-step actionable instructions
   - Dependencies: Any files, approvals, or references needed
   - Estimated Effort: Low/Medium/High
   - Next Action: What to do immediately
   - Completion Criteria: How to know task is done
6. Always follow Bronze Tier rules:
   - Local-first, free setup
   - Human-in-the-loop for sensitive tasks
   - Simple and modular steps
   - Avoid complex integrations (e.g., email watchers, cloud APIs)
7. Include a brief rationale for each step (why it is needed or what it achieves).

Output Format (Markdown):
---
title: "Task Title"
created: YYYY-MM-DD
status: pending
priority: high/medium/low
sensitivity: routine/sensitive
assigned_to: AI_Employee
---

# Objective
<Desc

## Response snapshot

Created comprehensive implementation plan for the AI Employee (Bronze Tier) system. The plan includes:
- Technical context defining the architecture and technology stack
- Constitution compliance verification ensuring all principles are followed
- Detailed research findings covering technology choices
- Complete data model specifying entities and relationships
- Implementation phases with specific objectives and steps
- Risk analysis and mitigation strategies
- Success criteria for completion validation

All components align with the local-first, human-in-the-loop requirements and constitutional principles.

## Outcome

- ✅ Impact: Complete implementation plan for AI Employee system
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: Generate tasks for implementation
- 🧠 Reflection: The plan provides a comprehensive roadmap for building a compliant AI employee system with proper governance.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all components planned
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A