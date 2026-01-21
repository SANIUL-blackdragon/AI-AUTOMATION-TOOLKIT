# Project Manifest Guidelines (Golden Standard)

## Overview
These guidelines define the structure, validation, and interaction protocols for creating "Project Manifests" for AI Agents. A Project Manifest is the single source of truth for an agent's identity, behavior, and boundaries.

## 1. Manifest Structure (`PROJECT_MANIFEST.yaml`)

The manifest MUST follow this strict YAML schema:

```yaml
identity:
  name: "agent-name" # lower-kebab-case
  role: "concise-role-description"
  description: "Detailed description of purpose and capabilities."

behavior:
  operating_mode: "semi-autonomous" # or "autonomous", "manual"
  communication_style: "concise" # or "verbose", "formal"
  input_rules:
    - "Rule 1"
  output_rules:
    - "Rule 1"

tools:
  definitions:
    - name: "tool-name"
      description: "what it does"
      parameters: { ... }

constraints:
  never_do:
    - "delete-production-db"
  budget:
    max_tokens: 100000
    max_cost: 5.00
  permissions:
    - "read-files"
    - "execute-safe-commands"

human_interaction:
  confirmation_triggers:
    - "file-deletion"
    - "deployment"
  review_workflow: "diff-based"
```

## 2. Validation Logic (Pydantic Rules)

Validation must be enforced programmatically:
- **Conditionals**: If `operating_mode` is "autonomous", then `constraints.budget` is REQUIRED.
- **Identity**: `name` must match regex `^[a-z0-9-]+$`.
- **Safety**: `constraints.never_do` must not be empty.

## 3. Human Agreement Protocol (Strict)

The creation process must follow this **irreversible sequence**:

1.  **Discovery (Slot Filling)**:
    -   Agent asks targeted questions to fill missing schema fields (e.g., "What is the budget limit?").
    -   *User UX*: Progressive profiling, not a giant form.

2.  **Drafting**:
    -   Agent synthesizes collected data into a valid YAML draft.

3.  **Review (Visual Diff)**:
    -   Agent presents the draft.
    -   If updating, Agent presents a **Semantic Diff** (e.g., "Changed `budget` from $5 to $10").
    -   *Constraint*: Agent must explicitly ask "Do you approve this manifest?".

4.  **Critique Loop**:
    -   User provides feedback.
    -   Agent refines and **repeats Step 3**.

5.  **Final Approval**:
    -   User issues explicit command: `APPROVE MANIFEST` (or clicks button).
    -   **HARD STOP**: Agent cannot save/finalize the file without this specific signal.

## 4. Conflict Resolution

-   **Scenario**: User asks for "full autonomy" but sets "zero budget".
-   **Action**: Agent **HALTS**. It does not auto-correct. It explains: "Conflict detected: Autonomy requires a budget. Please adjust one."
