---
name: agents_md-creator
description: "Creates high-quality, scenario-agnostic AGENTS.md files that define agent operating contracts for any repository or task. Supports codebase analysis, iterative refinement, and universal customization patterns. Use when: (1) Creating a new AGENTS.md from scratch, (2) Improving an existing AGENTS.md, (3) Defining agent behavioral rules for any scenario. Triggered by: 'create AGENTS.md', 'improve agent configuration', 'define agent rules', or 'agent operating contract'."
---

# AGENTS.md Creator

## Quick Start

1. **Analyze Codebase**: `python scripts/analyze_codebase.py --path <repo-path> --output context.json`
2. **Generate AGENTS.md**: `python scripts/init_agents_md.py --template <base|strict|flexible> --output <path>`
3. **Validate**: `python scripts/validate_agents_md.py --file <path>`

## Core Workflow

### Step 1: Analyze Context
Before creating an AGENTS.md, understand the environment. Run `analyze_codebase.py` to extract:
- Project structure and key files
- Technology stack and versions
- Existing documentation patterns
- Complexity indicators

### Step 2: Select Template & Create
Choose the right starting point based on the task:
- **Base**: Minimal viable contract. Good for most standard projects.
- **Strict**: High-control. Use for financial, security, or enterprise tasks.
- **Flexible**: High-autonomy. Use for creative, exploratory, or greenfield tasks.

Run `init_agents_md.py` with the selected template.

### Step 3: Refine with Research
Consult the references to tailor the AGENTS.md:
- **Structure**: See [AGENTS_MD_ANATOMY.md](references/agents-md-anatomy.md)
- **Best Practices**: See [BEST_PRACTICES.md](references/best-practices.md)
- **Anti-Patterns**: See [ANTI_PATTERNS.md](references/anti-patterns.md)
- **Examples**: See [UNIVERSAL_EXAMPLES.md](references/universal-examples.md)

### Step 4: Validate
Ensure the generated file is valid and follows safety rules by running `validate_agents_md.py`.

## Resources

### Scripts
- `scripts/analyze_codebase.py`: Scans repo for context.
- `scripts/init_agents_md.py`: Scaffolds file with templates.
- `scripts/validate_agents_md.py`: Checks structure and safety rules.

### Templates (`assets/templates/`)
- `base_agents_md.md`: Standard operating contract.
- `strict_agents_md.md`: Zero-trust, high-logging contract.
- `flexible_agents_md.md`: Outcome-focused, high-autonomy contract.

### References (`references/`)
- `agents-md-anatomy.md`: Explains each section (Authority, Operating Mode, etc.).
- `best-practices.md`: "Do's" for writing effective agent rules.
- `anti-patterns.md`: "Don'ts" and common pitfalls.
- `universal-examples.md`: Reference implementations for various scenarios.

## Error Handling
If validation fails:
1. Check output for specific section errors.
2. Verify "Safety & Hard Stops" section is present.
3. Ensure no conflicting instructions exist.
