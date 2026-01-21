---
name: project-manifest-creator
description: Creates, validates, and manages `PROJECT_MANIFEST.yaml` files. Defines the identity, behavior, tools, and constraints for AI agents. Use when initializing a new agent project or updating an existing agent's operating contract. Triggered by queries like "create project manifest", "define new agent", or "setup agent rules".
---

# Project Manifest Creator

## Quick Start

1.  **Draft Manifest**: Use `assets/templates/manifest_template.yaml` as a base.
2.  **Validate**: Ensure all constraints are met using the Pydantic logic.
3.  **Review**: Present a semantic diff to the user.
4.  **Confirm**: Wait for explicit `APPROVE MANIFEST` command.

## Core Workflow

### Step 1: Discovery (Slot Filling)
Ask the user for:
-   **Identity**: Name, Role, Description.
-   **Goals**: What should this agent achieve?
-   **Constraints**: Budget, "Never-dos".
-   **Tools**: What capabilities does it need?

### Step 2: Generation
Populate the YAML template.
Ensure `identity` name is `kebab-case`.
Ensure `constraints` section is not empty (default release valve if needed).

### Step 3: Validation & Review
-   **Self-Correction**: If `operating_mode` is "autonomous" but no checks are in place, warn the user.
-   **Presentation**: Show the YAML content. "Here is the draft manifest based on your requirements."

### Step 4: Strict Agreement
**CRITICAL**: You must NOT save the file to `PROJECT_MANIFEST.yaml` (or typically `AGENTS.md` context) until the user explicitly approves it.
-   Ask: "Does this manifest accurately represent your intent?"
-   If user changes something -> Go to Step 2.
-   If user says "Yes" -> Save.

## Resources

### Templates (`assets/templates/`)
-   `manifest_template.yaml`: The simplified schema for project definition.

### Validation Rules
-   Name: `^[a-z0-9-]+$`
-   Constraint: `never_do` list must be populated.
-   Conflict: User Intent vs Constraints -> Constraints win.

## Error Handling
-   **Ambiguity**: If user says "Make it smart", ask "What specific tools or inputs should be allowed to make it smart?"
-   **Conflict**: If user asks to remove all constraints, refuse and explain safety risks.
