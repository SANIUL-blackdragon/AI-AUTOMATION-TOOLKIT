---
# AGENTS.md v1.1 - The Operational Rulebook
# This metadata block enables automated parsing of agent configuration.
agent_name: "{{INSERT_AGENT_NAME}}"  # e.g., "Frontend-Architect" or "Repo-Guardian"
version: "1.0.0"
role: "{{INSERT_ROLE}}"              # e.g., "Senior React Engineer" or "QA Specialist"
permissions:
  terminal: true                     # Can the agent execute shell commands?
  filesystem: true                   # Can the agent read/write files?
  internet: false                    # Can the agent access external URLs?
skills:                              # List of associated SKILL.md files to load
  - "{{INSERT_SKILL_NAME}}"          # e.g., "frontend-design"
  - "{{INSERT_SKILL_NAME}}"
---

<!-- 
    TEMPLATE INSTRUCTIONS:
    This file serves as the "Executive Chef" for your AI agent. 
    It defines the strategy, rules, and final verification steps.
    Replace all {{PLACEHOLDERS}} with project-specific details.
    Remove these comment blocks after filling out the template.
-->

# 1. Project Overview & Role
<!-- 
    Clearly state the project's high-level goal and the AI's specific persona.
    Define the tech stack with specific versions to prevent hallucinations.
-->

**Objective**: {{INSERT_PROJECT_OBJECTIVE}}
**Persona**: You are a {{INSERT_PERSONA_DESCRIPTION}}.
**Tech Stack**:
- **Language**: {{INSERT_LANGUAGE_AND_VERSION}} (e.g., Python 3.11, TypeScript 5.4)
- **Framework**: {{INSERT_FRAMEWORK_AND_VERSION}} (e.g., Next.js 14, Django 5.0)
- **Database**: {{INSERT_DATABASE}} (e.g., PostgreSQL, MongoDB)
- **Key Libraries**: {{INSERT_KEY_LIBRARIES}}

---

# 2. Core Directives (Rules of Engagement)
<!-- 
    High-level behavioral "orders" that apply to every session.
    Categorize them for clarity.
-->

### ✅ Always Do
- {{INSERT_MANDATORY_ACTION}} (e.g., "Run verification commands after every file change")
- {{INSERT_MANDATORY_ACTION}} (e.g., "Add type hints to all new functions")

### ✋ Ask First
- {{INSERT_CONSULTATION_TRIGGER}} (e.g., "Deleting files outside the temp directory")
- {{INSERT_CONSULTATION_TRIGGER}} (e.g., "Changing database schemas or migration files")

### ❌ Never Do
- {{INSERT_FORBIDDEN_ACTION}} (e.g., "Commit secrets or API keys")
- {{INSERT_FORBIDDEN_ACTION}} (e.g., "Use `any` type in TypeScript")

---

# 3. Architecture & Structure
<!-- 
    A "machine-readable map" to prevent the agent from guessing file locations.
    Explain the data flow or specific design patterns (MVC, Clean Arch, etc.).
-->

**Pattern**: {{INSERT_ARCHITECTURAL_PATTERN}} (e.g., "Feature-based folder structure", "Microservices")

**Key Directories**:
- `{{INSERT_DIR_PATH}}`: {{INSERT_DIR_DESCRIPTION}} (e.g., `src/core`: Business logic)
- `{{INSERT_DIR_PATH}}`: {{INSERT_DIR_DESCRIPTION}} (e.g., `src/ui`: Reusable components)
- `{{INSERT_DIR_PATH}}`: {{INSERT_DIR_DESCRIPTION}} (e.g., `tests/`: Integration tests)

**Data Flow**:
{{INSERT_DATA_FLOW_DESCRIPTION}} (e.g., "Controllers -> Services -> Repositories -> DB")

---

# 4. Build & Development Commands
<!-- 
    CRITICAL SECTION: The exact commands for autonomous verification.
    Ensure these are copy-pasteable and work in the root directory.
-->

The agent **must** use these commands to verify its work:

| Action | Command | Description |
| :--- | :--- | :--- |
| **Start Dev** | `{{INSERT_START_COMMAND}}` | Starts local development server |
| **Build** | `{{INSERT_BUILD_COMMAND}}` | Compiles the project for production |
| **Lint** | `{{INSERT_LINT_COMMAND}}` | Checks for style and syntax errors |
| **Format** | `{{INSERT_FORMAT_COMMAND}}` | Auto-formats code (e.g., Prettier/Black) |

---

# 5. Testing Guidelines
<!-- 
    Ensures the agent maintains code quality standards.
    Define the framework and expected coverage.
-->

**Framework**: {{INSERT_TEST_FRAMEWORK}} (e.g., Jest, Pytest)
**Coverage Goal**: {{INSERT_COVERAGE_PERCENTAGE}}% for new features.

**Test Location Strategy**:
- {{INSERT_TEST_LOCATION_RULE}} (e.g., "Co-located with source files" or "In `tests/` folder")

**Mandatory Test Command**:
```bash
{{INSERT_TEST_COMMAND}}
```

---

# 6. Coding Conventions & Style
<!-- 
    Aligns AI code with the team's patterns.
    Provide a "Gold Standard" example snippet.
-->

**Style Rules**:
- {{INSERT_STYLE_RULE}} (e.g., "Use functional components with hooks, not classes")
- {{INSERT_STYLE_RULE}} (e.g., "Naming convention: camelCase for vars, PascalCase for components")

**Gold Standard Example**:
<!-- Ideally, provide a small, perfect snippet of code that represents 'Good' code in this repo -->
```{{INSERT_LANGUAGE_EXT}}
{{INSERT_CODE_EXAMPLE}}
```

---

# 7. Security & Boundaries
<!-- 
    Safety guardrails for the agent.
    List sensitive areas and mandatory practices.
-->

**Restricted Zones**:
- 🚫 `{{INSERT_SENSITIVE_DIR}}` (e.g., `.env`, `/config/secrets`) - **DO NOT MODIFY** without explicit permission.

**Mandatory Practices**:
1. {{INSERT_SECURITY_RULE}} (e.g., "Sanitize all SQL inputs")
2. {{INSERT_SECURITY_RULE}} (e.g., "No hardcoded credentials")

---

# 8. Git Workflow & Communication
<!-- 
    Automates the administrative side of development.
-->

**Branching Strategy**:
- Pattern: `{{INSERT_BRANCH_PATTERN}}` (e.g., `feat/<ticket-id>-<description>`)

**Commit Messages**:
- Format: `{{INSERT_COMMIT_FORMAT}}` (e.g., Conventional Commits: `type(scope): subject`)

**PR Checklist**:
- [ ] {{INSERT_CHECKLIST_ITEM}}
- [ ] {{INSERT_CHECKLIST_ITEM}}
