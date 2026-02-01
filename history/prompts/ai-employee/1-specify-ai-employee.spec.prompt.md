---
id: 1
title: Specify AI Employee Bronze Tier
stage: spec
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-employee
branch: 1-ai-employee
user: user
command: /sp.specify
labels: [ai-employee, bronze-tier, specification, local-first]
links:
  spec: specs/1-ai-employee/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-employee/spec.md
  - specs/1-ai-employee/checklists/requirements.md
tests:
  - none
---

## Prompt

You are building my Personal AI Employee (Bronze Tier) using Claude Code.
Follow my constitution.md instructions carefully. Your task is to setup a minimum viable AI employee with the following specifications:

1. **Obsidian Vault Setup**
   - Vault name: "AI_Employee_Vault"
   - Create folders:
     /Inbox
     /Needs_Action
     /Done
     /Plans (for task plans)
     /Pending_Approval (optional placeholder for HITL)
   - Create Markdown files with initial content:
     - Dashboard.md: basic recent activity section
     - Company_Handbook.md: basic rules of engagement
     - Business_Goals.md: placeholder weekly goals

2. **Watcher (Pick 1, Gmail or FileSystem)**
   - Watcher must detect new items (emails or file drops)
   - Convert them into actionable Markdown files in `/Needs_Action`
   - Suggested fields in each file:
     ---
     type: email/file_drop
     from: ...
     subject/original_name: ...
     received: datetime
     status: pending
     priority: high
     ---
     ## Suggested Actions
     - [ ] Process task
     - [ ] Mark as done
   - Must track already processed items to avoid duplication

3. **Claude Code Reasoning (Agent Skills)**
   - Read all files in `/Needs_Action`
   - Decide next steps (basic plan) and write a Plan.md file for each task
   - Update Dashboard.md with recent activity
   - Move processed tasks to `/Done` after completion
   - Use **Ralph Wiggum Loop** to retry until task is moved to `/Done`

4. **Human-in-the-Loop Placeholder**
   - Create `/Pending_Approval` folder
   - Any action that is sensitive (like sending email or file upload) should create a placeholder Markdown approval request file
   - For Bronze Tier, actual approval workflow not required; just placeholders

5. **Local-First and Free Setup**
   - Everything must be local (Obsidian Vault + Claude Code + Python Watcher)
   - Do NOT use paid APIs or cloud services
   - Ensure all file paths and processing works on a free local setup

6. **Logging**
   - Keep a simple log inside `/Vault/Logs/`
   - Log format:

## Response snapshot

Created a comprehensive specification for the AI Employee (Bronze Tier) with all required sections. The specification includes functional requirements for Obsidian vault setup, watcher service, reasoning engine, human-in-the-loop processing, logging, and Ralph Wiggum loop implementation. The document defines success criteria with both quantitative and qualitative measures, identifies key entities, and establishes clear scope boundaries. A quality checklist was also created to validate the specification completeness.

## Outcome

- ✅ Impact: Created complete specification for AI Employee Bronze Tier
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Plan the implementation of the AI Employee
- 🧠 Reflection: The specification provides a solid foundation for building a local-first AI employee system with appropriate governance and safety measures.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all required sections included
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A