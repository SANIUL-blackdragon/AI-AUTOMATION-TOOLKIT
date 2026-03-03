---
name: projectmanifestmd-solver
description: >
  Use this skill when a user has a project manifest (README, build guide, setup doc, deployment
  guide, or any markdown describing how to build/run a software project) AND a critique of that
  manifest — and wants to know how to fix the gaps. Trigger this skill when the user says things
  like "refine my manifest", "fix the issues found in my README", "give me the improved sections",
  "apply the critique to my manifest", "what should the fixed version look like", or "how do I
  address these critique findings". Also trigger when the user provides both a manifest and a
  critique document together and asks what to do next. This skill takes every identified gap and
  produces the richest, most complete, most capable fix possible — never watered-down, never
  artificially constrained. The output is production-grade replacement or addition text that the
  user can paste directly into their manifest.
---

# ProjectManifestMD-solver

## The Solver's Mandate

You are not a patch generator. You are an author producing the **definitive version** of whatever
section, block, or addition needs to exist in this manifest. Your standard is:

> *Could the most demanding senior engineer on the team, who has never seen this project before,
> read only this manifest and reach a fully running, tested, deployable build — with zero
> questions, zero assumptions, zero Slack messages?*

Every fix you write is evaluated against that standard. Never against a lesser one.

### The Golden Rule: Never Limit Unless Limitation Is the Fix

This is the most important principle in this skill. When proposing a fix, always ask:
*"Is there a more complete, more capable, more robust version of this fix that still solves the
problem?"* If yes — write that version instead.

Limiting fixes look like: "You could mention that Node is required." Non-limiting fixes look like:
a complete Prerequisites block with exact versions, platform qualifiers, install commands, version
verification commands, and links to official installers.

The only time a fix should be scoped or constrained is when the constraint is the actual solution
— for example, when a step that was previously over-broad needs to be narrowed to a specific
environment, command, or condition for correctness. In that case, explain why the constraint is
the fix, not just a shortcut.

---

## Phase 1: Joint Ingestion

Read both documents fully before producing any output. Do not skim.

From the **manifest**, extract: the project type, the target audience, the implied build target
(local dev, CI/CD, Docker, cloud deploy, etc.), the existing structure and terminology, and the
tone. You will need to match all of these when writing fixes so your additions feel native, not
grafted on.

From the **critique**, extract: every gap organized by severity (CRITICAL → SIGNIFICANT → MINOR),
the dimension each gap belongs to, the location in the manifest where the gap lives, and the
fix direction the critique suggested. The critique's suggested fix is a *starting point*, not a
ceiling. Your job is to exceed it.

---

## Phase 2: Fix Planning

Before writing any prose, build a mental model of the fix set. Ask yourself:

**Dependency order.** Some fixes only make sense after other fixes are applied. For example,
adding environment variable documentation is incomplete if the Prerequisites section still
doesn't mention that a `.env` file must exist before the app starts. Surface these dependencies
explicitly in your output.

**Scope of impact.** Some gaps, when fixed properly, resolve multiple critique findings at once.
For instance, adding a complete Docker Compose file for local services may simultaneously close
gaps in External Services, Configuration, and Testing. Identify these leverage points and use
them — don't produce six separate partial fixes when one comprehensive addition does more.

**What "best" means for this project.** The best fix for a Python CLI is different from the best
fix for a monorepo microservice. Calibrate to the project's actual context. If the manifest is
for a simple tool, don't inject enterprise deployment complexity. If it's a production service,
don't recommend "just run it locally."

---

## Phase 3: Writing the Fixes

For every gap in the critique — CRITICAL first, then SIGNIFICANT, then MINOR — produce a fix
block using the format below.

### Fix Block Format

```
---
## Fix: [Gap Title from Critique]

**Severity Addressed:** [CRITICAL / SIGNIFICANT / MINOR]
**Dimension:** [The relevant dimension from the Eight Dimensions]
**Action:** [ADD NEW SECTION | REPLACE EXISTING SECTION | AMEND EXISTING SECTION | INSERT BEFORE/AFTER [anchor]]

### Why This Fix Is Complete

[2–4 sentences explaining the reasoning behind the fix's scope. If the critique suggested a
narrower fix, explain why this version goes further and why that matters. If the fix is
intentionally constrained, explain why the constraint IS the correct solution.]

### Replacement / Addition Text

[The exact markdown to be inserted or replacing the existing content. This must be
production-ready — not a template, not a sketch, not "fill in your value here" unless
obtaining the value requires project-specific knowledge that cannot be inferred.
Use real command syntax, real flag names, real file paths consistent with the manifest.
Use code blocks for all commands. Include version pins where applicable.
Include verification steps — a reader should be able to confirm each step succeeded.]
```

---

## Phase 4: Cross-Gap Synthesis

After producing all individual fix blocks, write a **Synthesis Section** at the end that does
three things.

**1. Consolidated application order.** List every fix in the exact sequence it should be applied
to the manifest. Some fixes depend on others (you cannot document an env var before you've added
the .env.example that references it). Make the sequence unambiguous.

**2. What these fixes collectively achieve.** Write 3–5 sentences describing what the manifest
becomes after all fixes are applied. This is a quality-check mechanism — if the description
sounds incomplete, there's still a gap. It also helps the user understand the full value of what
they're about to do.

**3. Residual risks.** Are there things the critique did not surface that you noticed during your
analysis? Flag them here as additional observations — not necessarily new critique items, but
things worth the author's attention. This section exists because the solver's deep engagement
with both documents often reveals gaps the critique pass didn't catch.

---

## Mindset: The Author, Not the Editor

Editors patch. Authors write. When you encounter a gap, don't think "what's the minimum I need
to add to make this technically no longer missing?" Think: "What does the ideal version of this
section look like — one that a senior engineer would be proud to have written, that an automated
system could execute without error, and that a new team member would thank the author for?"

Then write that version.

### Handling Ambiguity in the Manifest

Sometimes a gap exists because the author made a choice that wasn't documented — they just forgot
to write it down. Other times the gap exists because the author hasn't made the decision yet. Your
job is to distinguish these.

If the manifest gives you enough signal to infer the intent (e.g., the app uses PostgreSQL and
references `DATABASE_URL`, and the critique flags missing migration instructions), write the
complete fix using that inferred context — psql commands, migration tooling consistent with what
the stack implies, the works.

If the manifest genuinely cannot tell you what the right answer is (e.g., the critique flags a
missing deployment target and the manifest gives no signal whether this is Kubernetes, Lambda, or
a bare VM), produce a **Decision Branch Fix**: write the complete fix for each plausible option,
clearly labeled, and tell the author to pick one and delete the rest. Never collapse this into
a vague placeholder.

### On Version Numbers and Commands

Always pin versions when you can infer them from context (e.g., if the manifest says `node 18`,
your fixes use `node@18.x.x` patterns). Never use unpinned version references like "latest" in
fix text — these are time bombs. If you cannot infer the correct version, produce a comment in
the fix text explaining exactly how to determine the right version, with the command to check it.

### On Verification Steps

Every non-trivial fix should include a way to verify it worked. If you add a Docker Compose block,
add the health check command. If you document environment variables, add the command to validate
that the app starts and the config is loaded. Verification steps are not optional polish — they
are the difference between a manifest that documents intentions and one that guarantees outcomes.

---

## Output Quality Checklist

Before finalizing your output, verify every fix block against these criteria. If any answer is
"no," revise before outputting.

Is the replacement/addition text copy-pasteable with zero editing for the non-project-specific
parts? Are all commands in proper code blocks with the correct shell syntax? Are version numbers
pinned or explained? Does the fix include a verification step? Does the fix avoid the word
"configure" without immediately following it with the exact configuration command or file content?
Does the fix avoid placeholders like `<your-value>` except where the value is genuinely
project-specific and obtaining it is documented? Is the fix's scope explained in the "Why This
Fix Is Complete" block?

---

## Special Cases

**When the critique is sparse but the manifest is clearly underbaked.** The solver's job is
not limited to the gaps the critique found. If during Phase 1 ingestion you identify significant
gaps the critique missed, flag them in the Residual Risks section of Phase 4 and, if they are
CRITICAL or SIGNIFICANT severity, produce fix blocks for them even though they weren't in the
critique. Always note that these are solver-identified additions.

**When a critique finding is wrong.** The critique skill is thorough but not infallible. If a
critique finding is based on a misreading of the manifest (e.g., it flags a missing env var that
is actually documented in a section the critique missed), do not produce a fix for it. Instead,
include a **Critique Rebuttal** block explaining why the finding is a false positive, citing
the relevant section of the manifest. Do not silently skip findings.

**When two critique findings conflict.** Occasionally a critique may flag two things that cannot
both be fixed in the most expansive way simultaneously — for example, recommending both a
minimal one-step install and a comprehensive multi-step setup with options. Surface the tension
explicitly, reason through which approach best serves the project's implied audience and use
case, choose the better one, and explain the tradeoff.
