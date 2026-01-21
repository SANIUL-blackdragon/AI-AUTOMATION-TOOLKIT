# AGENTS.md Guidelines

> A Comprehensive, Model-Agnostic Guide to Writing High-Performance Agent Configuration Files

**Version**: 2.0  
**Last Updated**: 2026-01-21  
**Based on**: Deep research from AIHero, HumanLayer, 12-factor-agents, GitHub Blog analysis, Anthropic research, and arXiv studies

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Understanding Agent Configuration Files](#2-understanding-agent-configuration-files)
3. [The Science: Why Less Is More](#3-the-science-why-less-is-more)
4. [The WHAT-WHY-HOW Framework](#4-the-what-why-how-framework)
5. [Required Root Content](#5-required-root-content)
6. [Progressive Disclosure Strategy](#6-progressive-disclosure-strategy)
7. [Monorepo Patterns](#7-monorepo-patterns)
8. [Anti-Patterns to Avoid](#8-anti-patterns-to-avoid)
9. [Context Engineering Principles](#9-context-engineering-principles)
10. [Tool Compatibility & Portability](#10-tool-compatibility--portability)
11. [Maintenance & Governance](#11-maintenance--governance)
12. [Practical Examples](#12-practical-examples)
13. [Quick Reference Checklist](#13-quick-reference-checklist)
14. [Sources & Further Reading](#14-sources--further-reading)

---

## 1. Executive Summary

AGENTS.md is a repository-checked markdown file that configures how AI coding agents behave in your codebase. It sits at the top of every conversation, immediately below the system prompt, making it the **highest-leverage configuration point** in your AI-assisted development workflow.

### Key Principles at a Glance

| Principle | Why It Matters |
|-----------|----------------|
| **Minimal by Design** | LLMs can reliably follow only ~150-200 instructions. Every unnecessary line degrades ALL instruction-following. |
| **Universally Applicable** | Content loads on EVERY request. Include only what's relevant to every single task. |
| **Progressive Disclosure** | Point to detailed docs instead of embedding everything. Agents navigate documentation hierarchies efficiently. |
| **Describe Capabilities, Not Paths** | File paths change constantly. Domain concepts and capabilities are more stable. |
| **Model-Agnostic** | Write for the behavior you want, not for a specific tool or model. |

### The Bottom Line

> **The ideal AGENTS.md is small, focused, and points elsewhere.** It gives the agent just enough context to start working, with breadcrumbs to more detailed guidance.  
> — *AIHero, "A Complete Guide To AGENTS.md"*

---

## 2. Understanding Agent Configuration Files

### 2.1 What Is AGENTS.md?

AGENTS.md is a markdown file you commit to version control that customizes how AI coding agents behave in your repository. Think of it as a **configuration layer between the agent's base instructions and your actual codebase**—a "project constitution" that defines the agent's role, directives, and limitations.

### 2.2 The Statelessness Problem

**LLMs are stateless functions.** Their weights are frozen at inference time—they don't learn over time, and they don't remember previous sessions. Every single time you start a new conversation with an AI coding agent:

1. **The agent knows absolutely nothing** about your codebase
2. **Critical information must be provided each time** you start a session
3. **AGENTS.md is the preferred mechanism** for delivering this context

This statelessness has a profound implication: AGENTS.md is the **only file that goes into every single conversation by default**. This makes it both incredibly powerful and incredibly dangerous—every line you add affects every task the agent performs.

### 2.3 Scope: Personal vs. Project

AGENTS.md can contain two types of guidance:

| Scope | Description | Examples |
|-------|-------------|----------|
| **Personal Scope** | Your individual preferences and patterns | Commit message style, preferred coding patterns, personal workflow |
| **Project Scope** | Team-wide project configuration | Project purpose, package manager, architecture decisions, build commands |

> **Tip**: Use `.local` variants (e.g., `CLAUDE.local.md`) for personal preferences that shouldn't be committed to version control. Add these to `.gitignore`.

### 2.4 The AGENTS.md Naming Convention

Different tools use different file names for the same purpose:

| Tool | File Name | Notes |
|------|-----------|-------|
| Most AI agents | `AGENTS.md` | Open standard, widely supported |
| Claude Code | `CLAUDE.md` | Anthropic's equivalent |
| Cursor | `.cursorrules` | Cursor-specific rules file |
| GitHub Copilot | `.github/copilot-instructions.md` | GitHub's standard |

For cross-tool compatibility, you can symlink files:

```bash
# Create symlink from AGENTS.md to CLAUDE.md
ln -s AGENTS.md CLAUDE.md
```

---

## 3. The Science: Why Less Is More

### 3.1 The Instruction Budget

Research on LLM instruction-following reveals critical constraints that should guide your AGENTS.md design:

| Model Type | Instruction Capacity | Degradation Pattern |
|------------|---------------------|---------------------|
| **Frontier Thinking Models** (GPT-4, Claude 3.5, Gemini) | ~150-200 instructions | Linear decay |
| **Smaller/Non-Thinking Models** | Significantly fewer | Exponential decay |

This research comes from academic studies on instruction-following, cited in HumanLayer's analysis:

> *"Frontier thinking LLMs can follow ~150-200 instructions with reasonable consistency. Smaller models can attend to fewer instructions than larger models, and non-thinking models can attend to fewer instructions than thinking models."*  
> — *HumanLayer, "Writing a good CLAUDE.md"*

### 3.2 The Math Problem

Consider this: Claude Code's system prompt alone contains approximately **~50 individual instructions**. That's nearly a **third of your instruction budget consumed before any user content is even loaded**.

When you add rules, plugins, skills, and user messages on top of that, your carefully-crafted AGENTS.md instructions are competing for attention in an increasingly crowded context window.

### 3.3 Uniform Degradation

A counterintuitive but critical finding: as instruction count increases, instruction-following quality decreases **uniformly across ALL instructions**. The model doesn't simply ignore newer or "further down in the file" instructions—it begins to ignore ALL of them uniformly.

This means adding "just one more rule" doesn't only risk that rule being ignored—it degrades the reliability of **every other rule** in the file.

### 3.4 Attention Position Effects

LLMs exhibit a bias towards instructions at the **peripheries** of the prompt:

- **Strong attention**: Very beginning (system prompt, AGENTS.md)
- **Strong attention**: Very end (most recent user messages)
- **Weak attention**: Middle sections

Additionally, research shows models tend to prioritize instructions appearing **earlier** in the prompt (primacy effects). This is why placement within AGENTS.md matters—put your most critical instructions first.

### 3.5 The "Lost in the Middle" Phenomenon

LLMs struggle to focus on relevant information buried within very long contexts. This phenomenon, documented in academic research, explains why bloated AGENTS.md files perform poorly—the agent literally loses track of important instructions in the middle of the noise.

### 3.6 Recommended File Size

Based on consensus from multiple sources:

| Metric | Recommendation | Source |
|--------|----------------|--------|
| **Maximum Lines** | <300 lines | General consensus, HumanLayer |
| **Optimal Target** | <60 lines | HumanLayer practice |
| **Ideal State** | As short as possible | Both AIHero and HumanLayer |

> *"At HumanLayer, our root CLAUDE.md file is less than sixty lines."*  
> — *HumanLayer, "Writing a good CLAUDE.md"*

---

## 4. The WHAT-WHY-HOW Framework

When structuring your AGENTS.md content, use the **WHAT-WHY-HOW framework** to ensure comprehensive but focused coverage:

### 4.1 WHAT: The Technical Landscape

Tell the agent about the technical environment it's working in:

| Element | Description | Example |
|---------|-------------|---------|
| **Tech Stack** | Languages, frameworks, libraries with versions | "This is a Next.js 14 application using TypeScript 5.4" |
| **Project Structure** | High-level map of the codebase | "The `src/` folder contains app code, `packages/` contains shared libraries" |
| **Key Components** | What the major parts of the system do | "The `api/` package handles GraphQL, `web/` is the Next.js frontend" |

> **Critical Warning**: Do NOT include specific file paths. File paths change constantly, and stale paths actively poison the agent's context. Instead, describe capabilities and let the agent discover the current structure.

### 4.2 WHY: Purpose and Function

Explain the reasoning behind the project and its architecture:

| Element | Description | Example |
|---------|-------------|---------|
| **Project Purpose** | One-sentence description of what this project does | "This is a React component library for accessible data visualization." |
| **Domain Concepts** | Important terminology and their meanings | "An 'organization' contains multiple 'workspaces', each with its own 'members'" |
| **Architectural Rationale** | Why the codebase is structured this way | "We use feature-based folders to keep related code co-located" |

### 4.3 HOW: Operational Instructions

Provide actionable instructions for working on the project:

| Element | Description | Example |
|---------|-------------|---------|
| **Package Manager** | Which package manager to use | "This project uses pnpm workspaces." |
| **Verification Commands** | How to run tests, typechecks, builds | `pnpm test`, `pnpm typecheck`, `pnpm build` |
| **Development Workflow** | How to start the dev server, run specific tasks | `pnpm dev` starts the development server |

---

## 5. Required Root Content

Based on research, these are the **absolute minimum** elements your root AGENTS.md should contain:

### 5.1 The Essential Three

1. **One-Sentence Project Description**  
   Acts like a role-based prompt, anchoring every decision the agent makes.
   ```markdown
   This is a React component library for accessible data visualization.
   ```

2. **Package Manager Specification** (if not npm)  
   Without this, agents may default to npm and generate incorrect commands.
   ```markdown
   This project uses pnpm workspaces.
   ```

3. **Non-Standard Build/Typecheck Commands**  
   If your commands differ from defaults, specify them.
   ```markdown
   ## Verification Commands
   - Build: `pnpm build`
   - Typecheck: `pnpm typecheck`
   - Test: `pnpm test --coverage`
   ```

### 5.2 Beyond the Essentials

If you have room in your instruction budget, consider adding:

| Element | When to Include | Placement |
|---------|-----------------|-----------|
| **Pointers to deep docs** | Always | In root AGENTS.md |
| **High-level architecture** | For complex projects | In root, keep brief |
| **Domain glossary** | When terminology is non-obvious | Consider separate doc |
| **Git workflow** | When non-standard | Consider separate doc |
| **Testing philosophy** | When important | Consider separate doc |

### 5.3 Sample Minimal AGENTS.md

```markdown
# Project Overview

This is a Next.js 14 e-commerce platform using TypeScript and Prisma ORM.

## Package Manager

This project uses pnpm. All commands should use `pnpm` instead of `npm`.

## Verification

After any code changes, run:
- `pnpm typecheck` - Type checking
- `pnpm test` - Unit tests
- `pnpm build` - Build verification

## Documentation

For detailed guidance, see:
- `/docs/ARCHITECTURE.md` - System design and patterns
- `/docs/CONVENTIONS.md` - Code style and conventions
- `/docs/TESTING.md` - Testing guidelines
```

---

## 6. Progressive Disclosure Strategy

Progressive disclosure is the technique of giving the agent only what it needs **right now**, and pointing to other resources when additional context is needed.

### 6.1 Why Progressive Disclosure Works

1. **Agents navigate documentation hierarchies efficiently**  
   AI agents are fast at finding and reading related documentation. They understand context well enough to navigate to what they need.

2. **Task-specific rules only load when relevant**  
   If an agent is debugging CSS, it doesn't need TypeScript conventions consuming attention.

3. **Keeps the file portable across models**  
   A focused root file works across different AI tools and model versions.

### 6.2 Implementing Progressive Disclosure

#### Step 1: Identify Detachable Content

Anything that isn't universally applicable to EVERY task should be a candidate for a separate file:

| Content Type | Should Go In... |
|--------------|-----------------|
| TypeScript conventions | `docs/TYPESCRIPT.md` |
| Testing patterns | `docs/TESTING.md` |
| API design guidelines | `docs/API_CONVENTIONS.md` |
| Database schema docs | `docs/DATABASE.md` |
| Git workflow details | `docs/GIT_WORKFLOW.md` |
| Security guidelines | `docs/SECURITY.md` |

#### Step 2: Create the Documentation Hierarchy

Organize supporting documentation in a discoverable structure:

```
docs/
├── ARCHITECTURE.md
│   └── references PATTERNS.md, DATABASE.md
├── CONVENTIONS.md
│   └── references TYPESCRIPT.md, TESTING.md
├── TYPESCRIPT.md
├── TESTING.md
├── API_CONVENTIONS.md
├── DATABASE.md
└── BUILD.md
    └── references esbuild configuration
```

Or use an agent-specific folder:

```
agent_docs/
├── building_the_project.md
├── running_tests.md
├── code_conventions.md
├── service_architecture.md
├── database_schema.md
└── service_communication_patterns.md
```

#### Step 3: Reference with a Light Touch

In your root AGENTS.md, use conversational references without forceful language:

```markdown
## Additional Context

For TypeScript conventions, see `docs/TYPESCRIPT.md`.
For testing guidelines, see `docs/TESTING.md`.
For API design patterns, consult `docs/API_CONVENTIONS.md`.
```

> **Do**: "For TypeScript conventions, see docs/TYPESCRIPT.md"  
> **Don't**: "ALWAYS read docs/TYPESCRIPT.md before writing ANY TypeScript"

#### Step 4: Nest Progressively

Your documentation files can reference each other:

```markdown
<!-- In docs/TYPESCRIPT.md -->
## Testing TypeScript Code

For testing conventions specific to TypeScript files, see `docs/TESTING.md`.
```

### 6.3 Prefer Pointers to Copies

A critical best practice: **prefer pointers to copies**.

| Do | Don't |
|----|-------|
| Reference file:line locations to authoritative context | Include code snippets in docs that will become stale |
| Link to external documentation (Prisma docs, Next.js docs) | Copy-paste external documentation that will drift |
| Point to actual source files as examples | Embed "ideal" code that diverges from reality |

```markdown
## Example: Good API Handler

See `src/api/users/create.ts` for our standard handler pattern.
```

### 6.4 Agent Skills as Progressive Disclosure

Many AI coding tools support "agent skills"—commands or workflows the agent can invoke to learn how to do something specific. These are another form of progressive disclosure: the agent pulls in knowledge only when needed.

---

## 7. Monorepo Patterns

In monorepos, you're not limited to a single AGENTS.md at the root. You can place AGENTS.md files in subdirectories, and they **merge with the root level**.

### 7.1 Hierarchical AGENTS.md

When an agent works in a subdirectory, it sees both the root AGENTS.md AND any local AGENTS.md files in its context.

```
my-monorepo/
├── AGENTS.md          # Root-level guidance
├── packages/
│   ├── api/
│   │   └── AGENTS.md  # API-specific guidance
│   ├── web/
│   │   └── AGENTS.md  # Web-specific guidance
│   └── shared/
│       └── AGENTS.md  # Shared package guidance
```

### 7.2 What Goes Where

| Level | Content | Example |
|-------|---------|---------|
| **Root AGENTS.md** | Cross-cutting concerns, workspace-level config | Package manager, overall architecture, links to package-specific files |
| **Package AGENTS.md** | Package-specific patterns and commands | Framework conventions, local build commands, package-specific testing |

### 7.3 Example: Root Level

```markdown
# Monorepo Overview

This is a monorepo containing web services and CLI tools. Use pnpm workspaces to manage dependencies.

See each package's AGENTS.md for specific guidelines:
- `packages/api/` - Node.js GraphQL API
- `packages/web/` - Next.js frontend
- `packages/cli/` - CLI tools
```

### 7.4 Example: Package Level

```markdown
# API Package

This package is a Node.js GraphQL API using Prisma.

## Commands
- `pnpm dev` - Start development server
- `pnpm test` - Run tests
- `pnpm db:migrate` - Run migrations

## Conventions
For API design patterns, follow `docs/API_CONVENTIONS.md`.
```

### 7.5 The Accumulation Problem

**Warning**: The agent sees ALL merged AGENTS.md files in its context. Don't overload any level. If your root file is 50 lines and three package files are 50 lines each, you've got 200 lines of instructions competing for attention.

Keep each level focused on what's relevant **at that scope**.

### 7.6 Real-World Example: OpenAI

According to analysis of public repositories, OpenAI's main repository utilizes **88 AGENTS.md files** within its subprojects. This demonstrates how large organizations use hierarchical AGENTS.md to provide tailored instructions for different components.

---

## 8. Anti-Patterns to Avoid

### 8.1 The "Ball of Mud" Anti-Pattern

There's a natural feedback loop that causes AGENTS.md files to grow dangerously large:

1. The agent does something you don't like
2. You add a rule to prevent it
3. Repeat hundreds of times over months
4. File becomes a "ball of mud"

Different developers add conflicting opinions. Nobody does a full style pass. The result? An unmaintainable mess that actually **hurts agent performance**.

> *"Generated files prioritize comprehensiveness over restraint."*  
> — *AIHero, "A Complete Guide To AGENTS.md"*

### 8.2 Auto-Generated AGENTS.md

**Never use initialization scripts to auto-generate your AGENTS.md.** They flood the file with things that are "useful for most scenarios" but would be better progressively disclosed. Auto-generated files suffer from:

- Generic content that isn't tailored to your project
- Excessive length that consumes instruction budget
- Stale information that becomes harmful over time
- One-size-fits-all patterns that don't fit your specific needs

### 8.3 Using the Agent as a Linter

> *"Never send an LLM to do a linter's job."*  
> — *HumanLayer, "Writing a good CLAUDE.md"*

LLMs are comparably expensive and incredibly slow compared to traditional linters and formatters. Code style guidelines in AGENTS.md:

- Add many instructions that consume your budget
- Include mostly-irrelevant code snippets
- Degrade overall instruction-following quality
- Are better enforced by deterministic tools

**Solution**: Use linters, formatters, and hooks. Consider a Claude Code Stop hook that runs your formatter & linter and presents errors for fixing.

### 8.4 Documenting File Paths

File paths change constantly. If your AGENTS.md says "authentication logic lives in `src/auth/handlers.ts`" and that file gets renamed or moved, the agent will confidently look in the wrong place.

| Don't | Do |
|-------|---|
| "The auth logic is in `src/auth/handlers.ts`" | "Authentication is handled in the auth module" |
| "Tests go in `__tests__/` folders" | "Tests are co-located with source files" |
| "Read `config/database.yml` for settings" | "Database configuration follows Rails conventions" |

### 8.5 Stale Documentation

For human developers, stale docs are annoying. For AI agents that read documentation on every request, stale information **actively poisons the context**. Regular maintenance is essential.

### 8.6 Task-Specific Instructions in Root

If your AGENTS.md contains instructions about how to structure a new database schema, that content will distract the model when working on completely unrelated tasks like CSS debugging or documentation updates.

### 8.7 Excessive Forcing Language

Avoid aggressive language that doesn't improve compliance and wastes tokens:

| Don't | Do |
|-------|---|
| "ALWAYS use const instead of let" | "Prefer const over let" |
| "NEVER use any type in TypeScript" | "Avoid any type" |
| "YOU MUST run tests before committing" | "Run tests before committing" |

### 8.8 The Relevance Filter Problem

Claude Code injects this system reminder with CLAUDE.md content:

```
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks. 
You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

The result: Claude will **ignore the contents** of your AGENTS.md if it decides they're not task-relevant. The more information you have that's not universally applicable, the more likely it is that Claude will ignore your instructions.

---

## 9. Context Engineering Principles

"Context engineering" is the emerging discipline of optimizing the informational context provided to LLMs. Understanding these principles helps you write better AGENTS.md files.

### 9.1 Everything Is Context

> *"LLMs are stateless functions that turn inputs into outputs. To get the best outputs, you need to give them the best inputs."*  
> — *12-factor-agents*

Great context includes:
- Prompts and instructions
- Retrieved documents (RAG)
- Past state, tool calls, and results
- Memory from related conversations
- Structured output instructions

Your AGENTS.md is the **permanent, always-present** portion of this context.

### 9.2 The High-Leverage Point

AGENTS.md affects **every phase** of your workflow and **every artifact** produced:

| Artifact | Impact of Bad AGENTS.md |
|----------|-------------------------|
| Research | Misunderstands system → bad research |
| Planning | Bad research → bad plan |
| Implementation | Bad plan → bad code |
| Review | Bad code → more cycles |

A bad line of code is a bad line of code. A bad line of implementation plan has the potential to create many bad lines of code. But a bad line in AGENTS.md affects **everything**.

### 9.3 Advanced Context Optimization Techniques

These techniques, documented in AI research, can inform your AGENTS.md design:

| Technique | Description | Application to AGENTS.md |
|-----------|-------------|--------------------------|
| **Selective Context Injection** | Load only relevant information | Progressive disclosure |
| **Structured Note-taking** | Agent writes notes outside context | Let agent generate its own documentation |
| **Summarization** | Compress older interactions | Keep AGENTS.md brief |
| **Semantic Chunking** | Break info into meaningful chunks | Organize by topic, not chronology |
| **Consistent Formatting** | Use bullet points, short paragraphs | Format for easy scanning |

### 9.4 In-Context Learning

LLMs are in-context learners. If your code follows a certain set of style guidelines or patterns, the agent will tend to follow existing code patterns and conventions **without being told to**.

This means you often don't need to document conventions that are already evident in the codebase. Focus AGENTS.md on:
- Things that AREN'T obvious from the code
- Exceptions to patterns the agent might infer incorrectly
- Critical safety boundaries

---

## 10. Tool Compatibility & Portability

### 10.1 The Open Standard

AGENTS.md is an open standard supported by many—though not all—AI coding tools. Writing tool-agnostic content maximizes portability.

### 10.2 File Naming by Tool

| Tool | Primary File | Notes |
|------|--------------|-------|
| General/Multi-tool | `AGENTS.md` | Most widely supported |
| Claude Code (Anthropic) | `CLAUDE.md` | Anthropic's variant |
| Cursor | `.cursorrules` | Also supports AGENTS.md |
| GitHub Copilot | `.github/copilot-instructions.md` | GitHub's standard |
| General AI assistants | `README.md` | Fallback for simple projects |

### 10.3 Symlinking for Compatibility

If you need to support multiple tools, use symlinks:

```bash
# Create CLAUDE.md as symlink to AGENTS.md
ln -s AGENTS.md CLAUDE.md

# Or vice versa
ln -s CLAUDE.md AGENTS.md
```

### 10.4 Local Overrides

Use `.local` variants for personal preferences that shouldn't be committed:

```
CLAUDE.local.md      # Personal Claude preferences (gitignored)
.cursorrules.local   # Personal Cursor rules (gitignored)
```

Add to `.gitignore`:
```gitignore
*.local.md
.cursorrules.local
```

### 10.5 Model-Agnostic Writing

Write for the behavior you want, not for a specific model's quirks:

| Model-Specific (Avoid) | Model-Agnostic (Prefer) |
|------------------------|------------------------|
| "Claude should use..." | "Use..." |
| "When GPT-4 encounters..." | "When encountering..." |
| "Gemini's function calling works by..." | "Function calls should..." |

---

## 11. Maintenance & Governance

### 11.1 Regular Review Cadence

AGENTS.md requires ongoing maintenance. Establish a review cadence:

| Frequency | Action |
|-----------|--------|
| **Weekly** | Quick scan for obvious staleness |
| **Monthly** | Full review against actual workflow |
| **Quarterly** | Comprehensive audit and pruning |
| **Per major change** | Update relevant sections |

### 11.2 Pruning Criteria

Regularly prune content that is:

- **Redundant**: The agent already knows this (e.g., common conventions)
- **Stale**: No longer accurate
- **Too vague**: Not actionable
- **Overly obvious**: "Write clean code"
- **Never triggered**: Rules for situations that never occur
- **Conflicting**: Contradicts other rules

### 11.3 Refactoring Prompt

If your AGENTS.md has grown unwieldy, use this prompt to refactor it:

```
I want you to refactor my AGENTS.md file to follow progressive disclosure principles. Follow these steps:

1. **Find contradictions**: Identify any instructions that conflict with each other. For each contradiction, ask me which version I want to keep.

2. **Identify the essentials**: Extract only what belongs in the root AGENTS.md:
   - One-sentence project description
   - Package manager (if not npm)
   - Non-standard build/typecheck commands
   - Anything truly relevant to every single task

3. **Group the rest**: Organize remaining instructions into logical categories (e.g., TypeScript conventions, testing patterns, API design, Git workflow). For each group, create a separate markdown file.

4. **Create the file structure**: Output:
   - A minimal root AGENTS.md with markdown links to the separate files
   - Each separate file with its relevant instructions
   - A suggested docs/ folder structure

5. **Flag for deletion**: Identify any instructions that are:
   - Redundant (the agent already knows this)
   - Too vague to be actionable
   - Overly obvious (like "write clean code")
```

### 11.4 Ownership Model

Assign clear ownership for AGENTS.md maintenance:

| Model | Description | Best For |
|-------|-------------|----------|
| **Rotational** | Different team members own it each sprint | Small teams, shared understanding |
| **Single owner** | One person is responsible | Consistency, larger teams |
| **Federated** | Package owners own their AGENTS.md | Monorepos |
| **Committee** | Changes require review | Enterprise, compliance-heavy |

### 11.5 Version Control Best Practices

- Commit AGENTS.md to version control
- Review changes in PRs like any other code
- Document the "why" in commit messages
- Consider CODEOWNERS for mandatory review

---

## 12. Practical Examples

### 12.1 Example: Minimal TypeScript Web Project

```markdown
# Project

This is a Next.js 14 SaaS application using TypeScript, Prisma, and Tailwind CSS.

## Package Manager

Use pnpm for all commands.

## Verification

Run before committing:
- `pnpm typecheck` - TypeScript checking
- `pnpm test` - Unit tests  
- `pnpm lint` - Linting

## Documentation

- Architecture: `/docs/ARCHITECTURE.md`
- Conventions: `/docs/CONVENTIONS.md`
- API patterns: `/docs/API.md`
```

### 12.2 Example: Python ML Project

```markdown
# Project

This is a PyTorch-based image classification training pipeline.

## Environment

Use Python 3.11 with pip. Virtual environment in `.venv/`.

## Commands

- `pip install -e .` - Install package
- `pytest` - Run tests
- `python train.py --config configs/base.yaml` - Training

## Documentation

See `docs/` for:
- `ARCHITECTURE.md` - Model architecture
- `DATA.md` - Data pipeline
- `EVAL.md` - Evaluation metrics
```

### 12.3 Example: Monorepo Root

```markdown
# Monorepo

E-commerce platform with web, mobile, and API.

## Workspace

pnpm workspaces. Run commands from root.

## Packages

- `packages/api/` - GraphQL API (Node.js)
- `packages/web/` - Next.js frontend
- `packages/mobile/` - React Native app
- `packages/shared/` - Shared types and utils

Each package has its own AGENTS.md with specific guidance.

## Global Commands

- `pnpm build` - Build all packages
- `pnpm test` - Test all packages
```

### 12.4 Example: Package-Level (API)

```markdown
# API Package

Node.js GraphQL API using Apollo Server and Prisma.

## Commands

- `pnpm dev` - Start with hot reload
- `pnpm test` - Run tests
- `pnpm db:migrate` - Run migrations
- `pnpm db:generate` - Generate Prisma client

## Conventions

See `/docs/API_CONVENTIONS.md` for resolver patterns.
```

---

## 13. Quick Reference Checklist

### ✅ AGENTS.md Health Check

Use this checklist to evaluate your AGENTS.md:

#### Content Quality
- [ ] Contains one-sentence project description
- [ ] Specifies package manager (if not npm)
- [ ] Lists verification commands
- [ ] Includes pointers to detailed documentation
- [ ] Each instruction is universally applicable

#### Size & Focus
- [ ] Under 300 lines (ideally under 60)
- [ ] No task-specific instructions in root
- [ ] No detailed file paths
- [ ] No code style rules (use linters instead)
- [ ] No redundant or obvious instructions

#### Structure
- [ ] Progressive disclosure implemented
- [ ] Documentation hierarchy exists
- [ ] Light touch references (not forceful language)
- [ ] Monorepo levels are appropriately scoped

#### Maintenance
- [ ] Committed to version control
- [ ] Regular review schedule established
- [ ] Clear ownership assigned
- [ ] No stale or conflicting content

---

## 14. Sources & Further Reading

### Primary Sources

1. **[A Complete Guide To AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md)** - AIHero  
   Comprehensive guide covering progressive disclosure, monorepo patterns, and anti-patterns.

2. **[Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)** - HumanLayer  
   Research-backed analysis of instruction budgets, file length, and best practices.

3. **[12-factor-agents: Own Your Context Window](https://github.com/humanlayer/12-factor-agents)** - HumanLayer  
   Context engineering principles for AI agent development.

### Research & Analysis

4. **[GitHub Blog: AGENTS.md Analysis](https://github.blog)** - GitHub  
   Analysis of 2,500+ AGENTS.md files identifying effective patterns.

5. **[arXiv: LLM Instruction Following Research](https://arxiv.org)** - Various authors  
   Academic research on instruction-following limits and degradation patterns.

6. **[Anthropic: Context Engineering](https://anthropic.com)** - Anthropic  
   Memory management and context optimization techniques.

### Standards & Examples

7. **[agents.md Official Website](https://agents.md)** - agentsmd  
   Open standard specification and community examples.

8. **[agentsmd.net Examples](https://agentsmd.net)** - agentsmd  
   Technology-specific AGENTS.md templates.

9. **[Cursor Documentation](https://cursor.com/docs)** - Cursor  
   Cursor-specific context and rules documentation.

### Tool Documentation

10. **[nodejs/corepack](https://github.com/nodejs/corepack)** - Node.js  
    Package manager version management for Node.js projects.

---

## Appendix: Template

Copy and customize this minimal template:

```markdown
# Project

[One sentence describing what this project does.]

## Environment

[Package manager and version information]

## Verification

[Essential commands to verify code changes]

## Documentation

[Pointers to detailed documentation files]
```

---

*This document was created through deep research following the [deep-research skill](.skills/skills/deep-research/SKILL.md) workflow, synthesizing findings from authoritative sources on AI agent configuration.*
