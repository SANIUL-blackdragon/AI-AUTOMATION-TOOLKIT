---
name: project-manifest-md-refiner
description: >
  Use this skill whenever a user provides a project manifest, README, build guide, setup doc, or
  any markdown file describing how to build, install, or run a software project — and wants the
  best possible version of that document produced directly. Trigger this skill when the user says
  things like "refine my manifest", "improve my README", "make this production-ready", "rewrite
  my build docs", "clean up my project manifest", "make this complete", or simply pastes a
  manifest and asks Claude to make it better. Also trigger when a user provides a manifest
  alongside critique output and says "now fix it" or "apply all fixes and give me the full
  document." This skill performs the critique and solver passes internally and outputs a single,
  complete, final manifest — no templates, no placeholders, no generic advice. Everything written
  is derived from the project's own context, and every output is fully executable by an autonomous
  agent with zero human intervention during the automated run.
---

# ProjectManifestMD-refiner

## What This Skill Does

This skill takes any project manifest — polished or rough, minimal or verbose — and returns the **single best version of that document**, written from scratch in the author's voice, calibrated to the project's actual stack and audience, and complete enough to be executed by an autonomous agent on a clean machine with zero mid-run intervention.

It is not a patcher. It is not a section generator. It does not output a critique, a list of fixes, or annotated suggestions. It outputs **one document** — the manifest that should exist for this project.

The critique skill finds gaps. The solver skill writes fixes. The refiner **authors the whole thing**, using everything both prior passes would have produced, without surfacing any of that intermediate work to the user. All cognition happens internally during Phases 1 and 2. Only the final document emerges.

---

## The Refiner's Standard

Before beginning, internalize this bar — in strict order of priority:

> **Primary test (agent buildability):** An autonomous agent — a CI/CD pipeline, an AI coding assistant, a build bot — executing this manifest on a clean machine, character by character, with no ability to ask questions, infer intent, recover from ambiguity, click a UI, or deviate from what is literally written, should reach a fully running, tested, deployable build without a single point of failure.

> **Secondary test (human readability):** A senior engineer who has never seen this project should be able to read this document and understand not just what to do, but why each step exists and how to verify it succeeded.

The primary test is the harder one and the one that matters most. A document that satisfies a human reader but fails an agent is not a complete manifest — it is documentation with hidden manual steps. Human readers compensate with judgment. Agents cannot. Every compensation a human would make silently is a gap that must be closed explicitly in the text.

Additionally, the document should feel **written**, not assembled. Every line should reflect the specific project's nature — its stack, its deployment target, its audience, and its author's choices. No reader should be able to point to any section and say "that could have been written for any project."

---

## Phase 1: Deep Project Archaeology

Before writing a single word of output, perform a thorough silent analysis of the manifest. This phase exists entirely in your reasoning — it produces no output. Go deep.

### 1.1 Extract the Project's Identity

Determine what this project *actually is*. Not just the tech stack — the purpose, the shape, the intended lifecycle. What does this software do, and for whom? Is it a library, a CLI tool, a web service, a daemon, a data pipeline, a monorepo, a microservice mesh, an SDK? What is its expected operating environment — a developer's laptop, a CI runner, a Docker container, a Kubernetes cluster, a serverless function, a bare VM? Is it meant to be run once or continuously? By the author, by a team, by end users?

Exhaust the manifest for signals before making any inferences. Filenames, command names, referenced services, environment variable patterns, directory structures mentioned in passing — all of these are identity signals.

### 1.2 Reconstruct the Full Dependency Graph

Map out every dependency the project has, including ones the manifest doesn't mention. Infer from context. If the manifest references `psycopg2`, PostgreSQL is a dependency even if never named. If it references `s3://` URIs, AWS credentials and an S3 bucket exist. If it runs `prisma migrate`, a database schema and migration toolchain are in play.

Every inferred dependency that isn't documented is a gap to close.

### 1.3 Hunt for Agent-Hostile Patterns

This sub-phase has one job: find every place in the manifest where an autonomous agent would stall, fail silently, or produce incorrect output. These patterns are often invisible to human readers because humans compensate for them automatically. Agents cannot. Each one is a hard blocker.

**Interactive prompts.** Does any step invoke a command that pauses for user input — a `y/n` confirmation, a passphrase, a first-run wizard, a license acceptance? Common offenders: `apt install` without `-y`, `npm init` without `--yes`, `ssh-keygen` without pre-specified flags, database seeders with confirmation gates. Every such command must be replaced with its non-interactive equivalent.

**UI-dependent steps.** Does any step require clicking through a web console, a desktop app, or a GUI wizard? These are absolute blockers for agents. Every such step must either be replaced with a CLI or API equivalent — or, if truly no programmatic path exists, explicitly pulled out and flagged in the Refiner's Note as a manual prerequisite that must be completed before the automated run begins. It must never remain as an inline step that an agent will silently fail on.

**Implicit working directory assumptions.** Does any step assume the shell is in a specific directory without a preceding `cd` to establish it? Agents don't carry working directory context between steps the way a human does when glancing at a terminal prompt. Every step that requires a specific location must establish it explicitly via `cd` or use absolute paths throughout.

**Missing output-to-input chains.** Does any step depend on a file, credential, service, or state that a prior step was supposed to produce — but that prior step is absent or incomplete? Map every step's required inputs against the outputs of all prior steps. Close every gap in that chain.

**Exit code ambiguity.** Does any step produce a non-zero exit code on success, or a zero exit code on failure, in a way that would cause an agent running with `set -e` to abort incorrectly? Identify these and write the correct exit code handling explicitly into the step.

**Race conditions and timing dependencies.** Does the manifest instruct an agent to connect to a service immediately after starting it, without waiting for that service to become ready? A human watches the logs and retries. An agent executes the next line immediately and fails. Any step that starts a service and is followed by a step that depends on it must include a readiness gate — a health poll, a `wait-for-it` loop, or a retry strategy — before proceeding.

**Credentials assumed to already exist.** Does the manifest reference credentials, tokens, or secrets as though they're already present in the environment? Agents run in clean environments with no pre-loaded secrets. Every credential must either be fully documented (how to obtain it, which variable or file it goes in, what format it must take) or the manifest must include the provisioning step that creates it. A credential the manifest assumes but doesn't document is a silent build failure waiting to happen.

**Ordering violations invisible in prose.** Sometimes a manifest documents steps in a logical grouping that doesn't match the correct execution order. A human reads ahead and mentally reorders. An agent executes linearly. Verify that the written order is the correct execution order, even if that means splitting apart sections the original manifest grouped for conceptual clarity.

### 1.4 Identify the Audience

Who is the intended reader of this manifest? A new open-source contributor, a DevOps engineer provisioning infrastructure, and a client receiving a deployable artifact all have different needs. The audience determines: how much background to assume, how much to explain versus command, and what tone to adopt.

If the manifest mixes audience assumptions inconsistently, calibrate to the most demanding expected reader and be consistent. Note, however, that agent buildability is always required regardless of audience. It is not a function of how expert the human reader is assumed to be.

### 1.5 Evaluate Against the Eight Dimensions

Internally run the critique skill's Eight Dimensions analysis in full. You are not writing a critique report — you are populating your understanding of what the final document must contain.

**Prerequisites and Environment.** Every runtime, tool, binary, package manager, build tool, OS constraint, and architecture requirement — each with an exact or minimum version. Any tool mentioned without a version, or any OS-specific step without a platform qualifier, is a gap.

**Dependencies and Package Management.** The exact install command, lock file strategy, private registry needs, git submodule handling, and any dependency requiring out-of-band setup.

**Configuration and Environment Variables.** A complete inventory of every variable the application reads, its purpose, its format, whether it's required or optional, how to obtain it, and what files must exist before the build starts.

**Build Steps — Completeness and Order.** Every step as an unambiguous executable command, in correct dependency order, with no vague verbs like "configure" or "set up" left unexplained. Every step's preconditions guaranteed by prior steps.

**External Services and Infrastructure.** Every service the application talks to, how to provision it or provide a local substitute, what credentials it requires, and how to verify the connection.

**Testing and Validation.** A command to run the test suite, a smoke test or health check, expected output, and — if relevant — coverage thresholds or quality gates.

**Deployment and Runtime.** If deployment is in scope: artifact creation, container registry steps, infrastructure provisioning, deployment commands, and environment-specific config differences.

**Documentation Quality and Navigability.** Linear flow, consistent terminology, code blocks for all commands, no dead links, no placeholder text, no TODO sections in critical paths.

### 1.6 Identify What to Preserve vs. Reconstruct

Distinguish between what the original manifest got right — preserve the substance, potentially improve the form — and what must be reconstructed because it's incomplete, vague, or missing.

Also note the author's stylistic choices — heading levels, section ordering, use of notes or warnings, level of explanatory prose between commands — and carry these forward in the output. A refiner that changes the document's voice is a failure even if the content improves. Agent buildability must be achieved without requiring a change of voice.

---

## Phase 2: Document Architecture

Before writing, plan the document's structure. This phase is also silent — it shapes the output, not the output itself.

Determine the right section order for *this project*. Most manifests benefit from a flow that mirrors both the reader's comprehension journey and the agent's execution journey: understand → set up environment → install dependencies → configure → build → verify → run → deploy. But some projects need different orderings. Derive the order from the project.

Critically: the section order must also be a valid execution order. An agent runs sections top to bottom. If a section assumes state that an earlier section hasn't yet produced, that is an architectural failure, not a style choice.

Identify sections that can be collapsed because they serve the same moment in the execution journey. Identify sections the original manifest merged that should be split — for example, a combined "Setup and Configuration" section that mixes environment setup with application config.

Plan the granularity of each section: some steps deserve their own heading because they're complex enough that an agent needs a clean boundary for error recovery; others belong as a numbered list item inside a larger step.

---

## Phase 3: Writing the Refined Manifest

Now write the document. The output is the complete manifest — every section, every command, every explanation — ready to be used as-is by an autonomous agent or a human reader.

### The Zero-Template Rule

This is the most important writing rule in this skill. **No section of the output may be written in a way that could apply to any other project.** Every sentence must earn its place by reflecting something specific about this project.

Violations look like: "Replace `your-project-name` with your actual project name." Or: "Set `DATABASE_URL` to your database connection string." Or: a Prerequisites section that lists generic tools without versions specific to this stack.

Non-violations look like: "Set `DATABASE_URL` to a PostgreSQL connection string in the form `postgresql://user:pass@host:5432/dbname`. For local development, the default Compose setup provides `postgresql://app:secret@localhost:5432/app_dev`." Or: "This project requires Node.js 20.x (LTS). Verify with `node --version`. The project uses ESM modules and will fail on versions below 18."

If a value is genuinely project-specific and cannot be inferred from context — a third-party API key, a cloud account ID — document exactly how to obtain it, where to put it, and what format it must take. The placeholder is the last resort, never the default.

### Writing for Agent Execution

When writing any command or step, apply these rules without exception.

**Non-interactive by default.** Every command that could prompt for input must include the flag or configuration that suppresses that prompt. Write the flags explicitly even when they feel redundant. An agent that encounters an interactive prompt halts indefinitely.

**Explicit working directory.** If a step must be run from a specific directory, the step begins with `cd /path/to/dir &&` or states clearly that all subsequent commands run from a defined root. Never rely on the agent inferring its location in the filesystem.

**Readiness gates before connection steps.** Whenever a step starts a service and the next step connects to it, write the actual readiness check command between them — not a suggestion to add one. For example:

```bash
# Start the database
docker-compose up -d postgres

# Wait until it accepts connections before proceeding
until pg_isready -h localhost -p 5432 -U app; do
  echo "Waiting for postgres..."; sleep 1
done
```

**Documented success conditions on each step.** After every non-trivial step, write what a successful execution produces: a specific log line, a file that now exists, an HTTP response code, a process ID. An agent with no expected output cannot distinguish a silent success from a silent failure.

**Known failure modes documented inline.** If a step is known to fail in specific circumstances — a port conflict, a missing system library, a timing window — document the failure symptom and the resolution command. An agent that hits an undocumented failure has no recovery path.

**No prose-only steps.** Every step must contain at least one literal, executable command in a code block. "Make sure your environment variables are configured" is not a step. `cp .env.example .env` followed by documentation of each variable is a step.

### Voice Fidelity

Match the author's voice. If the original manifest is terse and command-forward, the refined version should not add paragraphs of explanation the author wouldn't have written. If it's narrative and explains its reasoning, preserve that quality. The goal is the best version of *their* manifest. Agent buildability must be achieved without changing the document's character.

### Handling Genuine Ambiguity

When the manifest contains a gap that cannot be resolved from context — the project could deploy to AWS Lambda or a bare VM, and there is no signal either way — write a clearly labeled decision branch and write both paths fully. Note that the author must choose one and remove the other before handing the manifest to an agent, because an agent encountering an ambiguous fork will execute one path arbitrarily. Never leave a fork as a placeholder.

### On Inferred Content

When you write content that wasn't in the original manifest but is inferred from context, write it with the same confidence as documented content. Don't hedge. A manifest that says "you may also need to run migrations" is worse than one that places `npm run db:migrate` in the correct position in the build sequence. If an inference could be wrong, add one brief inline note explaining how to verify it. Keep the note short.

One calibration matters here: state what you inferred, but don't invent a *specific technical reason* to justify it if you don't actually know that reason. For example, if the manifest says "Python 3" with no version, it's correct to write "Python 3.11.x (LTS)" and flag it in the Refiner's Note. It is not correct to additionally write "the project uses match statements introduced in 3.10 and will fail on 3.9" unless the manifest or codebase actually contains that evidence. Specific technical rationales for inferred constraints carry authority — if they're wrong, they mislead. When in doubt, state the inferred value and flag it; don't reach for a justification you cannot substantiate.

---

## Phase 4: Post-Write Quality Gate

Before producing the final output, run every section through this checklist. Fix failures before outputting.

**Agent execution checks.** Would every command execute without pausing for user input? Does every step that requires a specific working directory establish it explicitly? Does every step that starts a service include a readiness gate before the next dependent step? Does every step have a documented success condition? Is every credential fully documented or provisioned by an earlier step? Are all steps in correct execution order, not just logical grouping order? Are known failure modes documented with their recovery commands?

**Completeness checks.** Is every command in a code block? Are all version numbers pinned or explained? Is every external service either fully documented or given a local substitute? Is every environment variable documented with its purpose, format, required/optional status, and acquisition path? Does any step contain the words "configure," "set up," or "update" without an immediately following command or file content?

**Agent simulation pass (final and mandatory).** Mentally simulate running this manifest as an agent, top to bottom, on a machine that has only the tools listed in the Prerequisites section and nothing else. At each step, ask: "Do I have everything I need to execute this command right now, without reading ahead or making any assumption?" If the answer is ever "no," that step has a gap. Find it and close it before outputting.

If any check fails, revise. Do not output until all checks pass.

---

## Output Format

Output the refined manifest as a single, complete markdown document. Begin directly with the document — no preamble and no postamble. The output *is* the manifest.

If the original manifest had a title, preserve it. If it didn't, add one derived from the project's identity.

After the document, on a new line separated by `---`, write a brief **Refiner's Note** of 3–6 sentences maximum. This note surfaces: any step that requires human intervention before an automated run can begin and what that intervention is; any significant content added from inference rather than the source document, so the author can verify it; and any decision branch that requires the author to choose a path and remove the other before handing the manifest to an agent. This note is for the author's awareness before automation — not for the document's reader.

---

## Mindset: Authorship for Automation

Editors improve documents. Authors write them. The refiner's posture is authorship — imagining that this project deserves a manifest written by someone who deeply understands it *and* who knows it will be executed by a machine.

This means writing the verification steps the original author forgot, the version pins they assumed were obvious, the readiness gates they didn't think to add, and the error conditions they didn't anticipate. It means not stopping at "technically complete" when "reliably automatable" is achievable.

The refined manifest should feel like it was written in one sitting by the person who knows this project best and who has run its build pipeline enough times to know exactly where it fails. That person is you, after Phase 1.
