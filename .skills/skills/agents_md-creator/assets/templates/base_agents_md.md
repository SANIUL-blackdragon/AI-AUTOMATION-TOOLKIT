# AGENTS.md

> Project Operating Contract & Context

## 1. Operating Contract

### Authority & Permissions
- You are **NOT** read-only. You may edit files.
- **Auto-Allowed**: `npm run test`, `npm run lint`, creating new files in `src/`.
- **Ask First**: Deleting files, installing new packages, committing code.

### Operating Mode
- **Hybrid**: Execute clear instructions immediately. If ambiguous, stop and ask.

### Safety & Hard Stops
- Stop if: 
  - A user instruction conflicts with this file.
  - You are missing API keys or credentials.
  - A command fails repeatedly.

## 2. Contextual Instructions

### Persona
- You are an expert developer for this project.
- Focus on clean, maintainable code and best practices.

### Project Knowledge
- **Tech Stack**: [TODO: React, Node, Python, etc.]
- **Key Files**:
  - `src/` - Source code
  - `tests/` - Tests

### Code Style & Standards
- **Formatting**: Follow existing `.prettierrc` or `.eslintrc`.
- **Comments**: Explain *why*, not *what*, for complex logic.
- **Naming**: Use descriptive variable names.

### Boundaries (Dos and Don'ts)
- ✅ **DO**: Run tests after making changes.
- ✅ **DO**: Use file-scoped commands (e.g. `npm test <file>`) to save time.
- 🚫 **DON'T**: Modify `config/` files without explicit permission.
- 🚫 **DON'T**: Commit secrets or API keys.
