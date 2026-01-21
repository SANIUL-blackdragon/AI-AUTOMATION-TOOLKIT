# AGENTS.md Anatomy

An `AGENTS.md` file acts as an operating contract and specific instruction set for AI agents. It generally consists of two main parts: the **Operating Contract** (behavioral rules) and the **Contextual Instructions** (project specifics).

## Part 1: Operating Contract (Behavioral)

These sections define *how* the agent should behave, making it reliable and safe.

### 1. Authority & Permissions
- **Purpose**: Explicitly define what the agent is allowed to do (read, write, delete) and what requires user confirmation.
- **Key Rules**:
  - "Agent is not read-only."
  - "Must alert user before destructive actions."
  - "Zero assumptions allowed."

### 2. Operating Mode
- **Purpose**: Define the autonomy level.
- **Modes**:
  - **Execute**: Just do it.
  - **Plan**: Always plan before doing.
  - **Hybrid**: Act on clear instructions, ask on ambiguity.

### 3. Safety & Hard Stops
- **Purpose**: Define conditions where the agent MUST stop immediately.
- **Examples**:
  - Missing API keys.
  - Conflicting files.
  - Ambiguous user intent.

### 4. Communication Style
- **Purpose**: How the agent should talk to the user.
- **Examples**:
  - "Be concise."
  - "Explain reasoning only for complex tasks."
  - "Format output in Markdown."

## Part 2: Contextual Instructions (Technical)

These sections define *what* the agent needs to know to work on this specific project.

### 1. Persona/Role
- **Purpose**: Anchors the agent's behavior.
- **Example**: "You are a Senior React Engineer specializing in performance."

### 2. Project Knowledge & Tech Stack
- **Purpose**: Lists libraries, versions, and architectural decisions.
- **Content**:
  - Tech stack (e.g., "React 18", "Python 3.10").
  - File structure map.
  - Key architectural patterns (e.g., "Feature-based folders").

### 3. Operational Commands
- **Purpose**: Pre-defined commands for building, testing, and linting.
- **Example**:
  - Build: `npm run build`
  - Test: `npm test`
  - Lint: `npm run lint`

### 4. Code Style & Standards
- **Purpose**: Specific coding conventions.
- **Content**:
  - Naming conventions (camelCase vs snake_case).
  - Preference for functional vs object-oriented.
  - Error handling patterns.

### 5. Boundaries (Dos and Don'ts)
- **Purpose**: Hard rules for the agent.
- **Dos**: "Always write tests first."
- **Don'ts**: "Never modify `config/` files directly." "Never commit secrets."
