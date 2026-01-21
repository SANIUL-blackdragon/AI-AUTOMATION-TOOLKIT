# AGENTS.md Anti-Patterns

Common mistakes that lead to agent hallucination, context bloat, or poor performance.

## 1. The "Human README" Clone
**Mistake:** Copy-pasting the entire project README into AGENTS.md.
**Why it fails:** Wastes context window. Agents usually have access to the README anyway.
**Fix:** Only include *behavioral* rules and *operational* context not found in the high-level README.

## 2. Vague "Polite" Instructions
**Mistake:** "Please try to make the code look nice if you can."
**Why it fails:** Interpretable in too many ways. "Nice" is subjective.
**Fix:** "Enforce Prettier formatting. Max line length 80 chars. Use functional components."

## 3. The "Wall of Text"
**Mistake:** Long paragraphs explaining the philosophy of the project.
**Why it fails:** Agents struggle to extract actionable constraints from prose.
**Fix:** Use bullet points, checklists, and code snippets.

## 4. Conflicting Directives
**Mistake:** Rule A: "Always use Python." ... (200 lines later) ... Rule B: "Use Node.js for scripts."
**Why it fails:** Causes agent confusion and unpredictable behavior.
**Fix:** Keep rules categorized and review for consistency.

## 5. Over-Specification of Standard Libraries
**Mistake:** Explaining how `React.useState` works in the AGENTS.md.
**Why it fails:** The model already knows standard libraries.
**Fix:** Only duplicate documentation if you are using a proprietary internal library or a very weird pattern.

## 6. Micromanaging "Thinking"
**Mistake:** "First think about A, then B, then C, then..." for every single trivial task.
**Why it fails:** Slows down simple tasks and consumes tokens.
**Fix:** Use an "Operating Mode" (e.g., Plan vs. Execute) to toggle this behavior based on task complexity.

## 7. Leaving "Never-Dos" Implicit
**Mistake:** Assuming the agent knows not to delete the database.
**Why it fails:** Agents have no common sense or fear.
**Fix:** Explicitly list "Destructive Actions" that require user approval.
