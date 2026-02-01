# AI Employee (Bronze Tier) Data Model

## Task Entity

### Attributes
- **id**: string (derived from filename)
- **type**: string (email, file_drop, or custom types)
- **from**: string (sender or source of the item)
- **subject/original_name**: string (original subject or filename)
- **received**: datetime (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)
- **status**: enum (pending, in_progress, completed, approval_needed)
- **priority**: enum (high, medium, low)
- **content**: string (markdown body content)
- **created_at**: datetime (when the task was created in the system)

### Relationships
- Related to Plan entities (one-to-many when complex tasks require detailed plans)
- Related to Log entries (many-to-many through system activity)

### Validation Rules
- id must be unique within the system
- received and created_at must be valid ISO 8601 datetime strings
- status must be one of the defined enum values
- priority must be one of the defined enum values
- content must not exceed 1MB in size

## Log Entry Entity

### Attributes
- **timestamp**: datetime (ISO 8601 format: YYYY-MM-DD HH:MM:SS.mmm)
- **severity**: enum (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **event_type**: string (task_processing, approval_needed, error, system_status, batch_processing)
- **description**: string (brief description of the event)
- **details**: object (optional structured data about the event)

### Validation Rules
- timestamp must be current or past time
- severity must be one of the defined enum values
- event_type must be from the predefined list
- description must be non-empty

## Plan Entity

### Attributes
- **id**: string (derived from related task filename)
- **related_item**: string (original task filename)
- **created**: datetime (ISO 8601 format)
- **status**: enum (not_started, in_progress, completed)
- **steps**: array of objects
  - completed: boolean
  - description: string
  - completed_at: datetime (nullable, ISO 8601 format)
- **timeline**: string (estimated completion timeframe)
- **success_criteria**: array of objects
  - met: boolean
  - description: string

### Relationships
- Related to Task entity (many-to-one)
- Related to Log entries (many-to-many through system activity)

### Validation Rules
- id must be unique within the system
- related_item must reference an existing task
- steps array must contain at least one element
- all date fields must be valid ISO 8601 datetime strings

## Approval Request Entity

### Attributes
- **id**: string (derived from original filename)
- **original_file**: string (name of the original file requiring approval)
- **request_created**: datetime (ISO 8601 format)
- **status**: enum (pending_approval, approved, rejected)
- **urgency**: enum (high, medium, low)
- **reason**: string (why approval is needed)
- **decision_notes**: string (optional notes from approver)

### Validation Rules
- id must be unique within the system
- request_created must be valid ISO 8601 datetime string
- status must be one of the defined enum values
- urgency must be one of the defined enum values

## State Transitions

### Task States
```
pending → in_progress → completed
           ↓
       approval_needed → pending_approval → approved/completed
                                          ↓
                                        rejected
```

### Approval Request States
```
pending_approval → approved → completed
                 ↓
               rejected
```

### Validation Rules for State Transitions
- Tasks can only move forward in state (no reverting to previous states)
- Tasks requiring approval must transition through approval_needed state
- Approval requests must be resolved (approved/rejected) before related tasks can proceed