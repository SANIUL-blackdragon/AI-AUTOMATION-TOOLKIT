# AGENTS.md Best Practices

Synthesized from analysis of 2,500+ repositories and official documentation.

## Core Principles

1. **Be Explicit and Concise**
   - AI thrives on clear, unambiguous instructions.
   - Avoid vague descriptions like "Try to..." or "Preferably...".
   - Use imperative language: "Use TypeScript", "Run tests", "Stop if...".

2. **Focus on AI-Specific Context**
   - Do NOT duplicate the human `README.md`.
   - Focus on "implementation details" the AI needs but humans might know implicitly.
   - Example: Directory structures, specific build flags, linting rules.

3. **Examples Beat Explanations**
   - A single code snippet showing a pattern is worth 1000 words of description.
   - Point to existing files in the repo that are "Gold Standard" examples.

## Structural Best Practices

4. **Put Commands First**
   - List executable commands early (Build, Test, Lint).
   - Include specific flags (e.g., `npm run test -- --watch`).
   - Define "File-Scoped" commands for faster feedback (e.g., linting just the changed file).

5. **Define Clear Boundaries**
   - Use a **"Never-Do List"**.
   - Explicitly list forbidden actions (e.g., "Never commit secrets", "Never edit vendor files").
   - Define what requires permission vs. what is auto-allowed.

6. **Progressive Disclosure**
   - For massive repos, nest `AGENTS.md` files in subdirectories.
   - The root `AGENTS.md` handles global rules; `src/components/AGENTS.md` handles specific component rules.

## Maintenance

7. **Treat it as Live Code**
   - Update `AGENTS.md` when stack versions change.
   - If the agent makes a mistake, add a rule to prevent it next time.
   - Iterate based on real failures.

8. **Keep it Token-Efficient**
   - Aim for 150-300 lines for the main file.
   - Don't overload the context window with irrelevant history or generic definitions.
