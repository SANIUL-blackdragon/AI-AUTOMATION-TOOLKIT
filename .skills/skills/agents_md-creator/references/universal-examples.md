# Universal AGENTS.md Examples

These examples demonstrate the *structure* and *pattern* of effective AGENTS.md files without being tied to a specific domain.

## Example 1: The "Strict Contract" (High-Stakes / regulated)

Use this pattern when correctness and safety are paramount.

```markdown
# AGENTS.md

## 1. Operating Contract
- **Authority**: You DO NOT have permission to commit code without review.
- **Safety**: You MUST NOT delete any file outside of `tmp/`.
- **Privacy**: You MUST NOT output any real customer data (PII) in logs.

## 2. Validation Constraints
- All code must include unit tests.
- Code coverage must remain above 90%.
- No new external dependencies allowed without explicit permission.

## 3. Communication
- **Plan First**: Before writing code, output a 5-step plan.
- **Log Actions**: Append all major decisions to `work_log.md`.
```

## Example 2: The "Creative Partner" (Exploration / Greenfields)

Use this pattern when you want the agent to brainstorm and iterate quickly.

```markdown
# AGENTS.md

## 1. Persona
- You are a creative product engineer.
- Your goal is to find the most user-friendly solution, not just the easiest code.

## 2. Operating Mode
- **Autonomy**: High. You may create new files and refactor provided structure if it improves UX.
- **Experimentation**: If multiple solutions exist, present the top 2 options with pros/cons.

## 3. Style Goals
- Code should be clean and readable.
- Prioritize "working prototypes" over "perfect architecture" for this phase.
```

## Example 3: The "Maintenance Worker" (legacy / large repo)

Use this pattern for navigating established, complex codebases.

```markdown
# AGENTS.md

## 1. Context
- This is a legacy codebase (5+ years old).
- We are migrating from [Old Framework] to [New Framework].

## 2. Map
- `legacy/`: Do not touch unless fixing critical bugs.
- `modern/`: All new features go here.
- `shared/`: Shared utilities.

## 3. Rules of Engagement
- **Do No Harm**: Do not reformat entire files (diff noise). Format only changed lines.
- **Match Style**: Mimic the coding style of the file you are editing, even if it's outdated.
- **Incrementalism**: Break large refactors into small, distinct PRs.
```
