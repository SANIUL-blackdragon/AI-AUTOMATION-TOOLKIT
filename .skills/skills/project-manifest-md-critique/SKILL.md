---
name: project-manifest-md-critique
description: >
  Use this skill whenever a user provides a project manifest, README, build guide, setup doc, 
  or any markdown file that describes how to build, install, or run a software project — and 
  wants to know if it's complete, correct, or production-ready. Trigger this skill when the user 
  says things like "review my README", "check if my build docs are complete", "can someone 
  follow this to set up my project", "critique my manifest", "does this have any gaps", or 
  "will this build automatically". Also trigger when the user pastes a markdown document 
  describing project setup and asks any evaluative question about it. This skill applies deep, 
  multi-dimensional analysis to determine whether a project manifest could be followed by an 
  automated system or a new developer with zero context — and produces a structured critique 
  with severity ratings and concrete fixes for every gap found.
---

# ProjectManifestMD-critique

## The Core Question

The purpose of this skill is to answer one question with precision: **Could a completely context-free agent — human or machine — follow this document and produce a running, testable, deployable build with zero intervention, zero tribal knowledge, and zero tolerance for ambiguity?**

That standard is intentionally extreme. "Mostly complete" is not good enough. A missing environment variable, an assumed tool version, a build step that is silently destructive on re-run, a contradiction between section 2 and section 7, an example that embeds PII, a license that conflicts with a dependency — any of these can cause a build to fail, a deployment to corrupt data, a team to accumulate hours of invisible debugging debt, or a company to face legal exposure. Your job is to find every one of them.

Buildability is not the only axis. A manifest can be executable but logically incoherent, accurate today but drift-prone tomorrow, runnable on one platform but silently broken on another, technically complete but legally dangerous. All of these failure modes are in scope.

---

## Phase 1: Document Ingestion and Orientation

Read the entire document before writing a single finding. Understand what type of document this is and what it is trying to enable.

Ask yourself: What is the intended build target — local dev, CI/CD pipeline, production deployment, Docker container, cloud function, embedded system? Who is the assumed reader — a new hire with no context, an experienced ops engineer, an automated agent? What is the project's architecture — monolith, microservices, monorepo, library, CLI tool?

If the document doesn't make any of these explicit, that is itself a finding. A manifest that doesn't know its own audience is already failing.

Note the document's implied scope: does it claim to cover only local development, or the full lifecycle? Hold it to the scope it claims, but flag if the claimed scope is narrower than what a reader would reasonably need.

**Deferral Pre-Scan.** Before running any cluster analysis, do one full pass through the document to identify and catalog every deferral — every place where the document knowingly delegates, postpones, or hands off a responsibility rather than fulfilling it inline. Build a deferral map before you evaluate anything, because the clusters will encounter these items and need to classify them correctly rather than treating them as silent gaps.

A deferral is any signal that the author is aware a topic exists but has chosen not to cover it here. Recognize it in these forms: explicit cross-references ("see `DEPLOYMENT.md`", "refer to the ops runbook", "consult the wiki"), scope declarations ("this guide covers local development only"), delegation language ("your ops team will provision the database", "handled by the CI pipeline"), markers (`TODO`, `WIP`, `coming soon`, `TBD`), conditional branching ("if using Kubernetes, follow the separate Kubernetes guide"), and version gating ("available in v2.0"). Each of these is a deferral, not a gap — but each one must be independently validated in Cluster H.

The key mental distinction to hold through the entire analysis: **a gap is something the author forgot or didn't know was needed; a deferral is something the author acknowledged but chose not to cover here.** The critique treats them differently. A gap gets a finding in the relevant cluster. A deferral gets an entry in Cluster H. This distinction matters because the fix for a gap is to add content, while the fix for a broken deferral is to repair the reference or re-scope the document. Conflating them produces noise — flagging intentional design decisions as omissions, or missing broken references because they look intentional.

---

## Phase 2: The Seven Analysis Clusters

Work through each cluster in order. For every item, extract the specific claims the document makes, then evaluate whether those claims are complete, internally consistent, accurate to reality, safe, and unambiguous. Do not skip clusters because they seem unlikely to apply — the most dangerous gaps are the ones that seem unlikely until they aren't.

---

### Cluster A — Build Execution Correctness

*Can a context-free agent actually execute this and get a running system?*

**A1. Prerequisites and Environment.** Every tool, runtime, binary, or system capability the project depends on must be listed with an exact version or a justified minimum version range. "Install Node" and "Python 3+" are not prerequisites — they are placeholders. Check for: language runtimes, package managers, build tools (make, cmake, gradle, bazel), system libraries, OS platform constraints, CPU architecture requirements (x86 vs ARM vs Apple Silicon), and required environment wrappers (Docker, Kubernetes, cloud CLI tools, nvm, pyenv, rbenv). Flag any tool mentioned without a version, any version range that could silently break across minor releases, and any system library that is implied by the build steps but not listed.

**A2. Dependencies and Package Management.** The exact install command must be present and unambiguous — not "install the dependencies" but `npm ci` or `pip install -r requirements.txt`. Check whether a lock file exists, is committed, and is referenced. Check for private registry requirements, auth token configuration (`.npmrc`, `.pypirc`, Artifactory credentials), git submodule initialization, vendor directory expectations, and any dependency that must be installed globally rather than locally. Flag any dependency that requires out-of-band setup: downloading a binary manually, cloning a separate repo, or running a generator script not mentioned elsewhere.

**A3. Configuration and Environment Variables.** This is where manifests fail most often. Every configuration value the application reads must be documented by name, with its purpose, its expected format or type, whether it is required or optional, a safe default if one exists, and how to obtain it. Check for: a complete env var listing, a `.env.example` file that is committed and current, secrets sourcing instructions (vault path, CI/CD secret name, service portal URL), and any config files that must be created or populated before the build can proceed. Flag any env var referenced in code or infra that is absent from the manifest, any "fill in your value" instruction without sourcing guidance, and any variable with undocumented format constraints (must be a URL, must be base64, must be a specific date format).

**A4. Build Steps — Completeness, Order, and Executability.** Each build step must be an unambiguous, literal, executable command. Steps requiring human judgment or interpretation are not build steps — they are gaps. Check: are all steps literal shell commands in code blocks? Are they in the correct dependency order (you cannot migrate before the DB is running; you cannot start the frontend before the API is up)? Does every step have its preconditions guaranteed by previous steps? Are steps idempotent, or does re-running them break state? Does any step produce an artifact that a later step consumes, and is that artifact's expected location and format documented? Flag vague imperative verbs: "configure," "set up," "update," "ensure," "make sure." These are the hallmarks of gaps disguised as instructions.

**A5. External Services and Infrastructure.** Any service the application connects to must be fully accounted for: what it is, how to provision it locally (Docker Compose service, emulator, mock), what credentials it requires, how to verify the connection is healthy before proceeding, and whether a local substitute is acceptable or production credentials are required even for local dev. Check for: databases (with schema migration and seed instructions), message queues, object storage, third-party APIs, internal microservices, CDN configuration, DNS requirements, SMTP services, authentication providers, feature flag services, and observability backends. Flag any external service that is assumed to already exist without documentation of how to create it.

**A6. Testing and Validation.** A manifest without a verification step cannot distinguish a successful build from a silent failure. Check for: the exact command to run the test suite, a smoke test or health check command and its expected output, any environment setup required before tests can run (a test database, specific env vars, fixture data), and the expected exit code and output of a passing run. Flag if tests are documented but require undocumented setup, if expected output is not described, or if there is no way to distinguish a passing build from a hung process.

**A7. Deployment and Runtime.** If the manifest covers deployment (not just local dev), every step of producing and delivering the artifact must be literal and executable. Check for: build artifact creation commands (Docker build, compile, bundle), registry push steps with the expected image tag format, infrastructure provisioning commands (Terraform, CDK, Pulumi), deployment commands (kubectl, helm, serverless, fly deploy), environment-specific configuration differences between staging and production, and rollout verification steps. Flag any deployment step that requires clicking through a UI, any step that assumes pre-existing infrastructure without documentation of how to create it, and any production secret management described vaguely.

**A8. Hardware and Physical Resource Requirements.** The build and runtime resource envelope must be specified. A developer on a 2-core laptop attempting a build that requires 16GB RAM will encounter confusing failures with no explanation. Check for: minimum RAM for build and runtime, minimum disk space (builds downloading large Docker layers or compiling large codebases need this), CPU architecture requirements, GPU requirements for ML workloads, network bandwidth minimums for dependency-heavy builds, and IOPS requirements for database-intensive operations. Flag any project that could plausibly hit resource constraints on a standard developer machine without warning.

**A9. Network and Connectivity Assumptions.** The manifest assumes unrestricted internet access during the build. In corporate environments with outbound proxies, firewall rules, or air-gapped networks, every `npm install`, `docker pull`, and `git clone` will fail silently or with an opaque error. Check for: `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` documentation, private registry override configuration, VPN requirements (especially for credential-bearing steps), offline or air-gapped build instructions, and any step that pulls from a domain that may be blocked on corporate networks. Flag if none of this is addressed for a project that is likely to be built in enterprise environments.

**A10. Privilege and Permission Requirements.** Document which steps require elevated permissions and which should not be run as root. Check for: steps requiring `sudo` or administrator access (and whether they are scoped correctly), file and directory permission requirements (writable log dirs, executable scripts, setuid binaries), OS user and group membership requirements (the `docker` group, a specific service account), and any step that mutates system-level configuration (`/etc/hosts`, `/etc/ld.so.conf`, systemd service installation). Flag any step that silently requires root without stating it, and any step that documents `sudo` unnecessarily, creating a security concern.

**A11. Timing and Performance Expectations.** The manifest must communicate which steps are slow so a developer doesn't abort a correct-but-long operation. A build that downloads 2GB of Docker layers will appear hung without context. Check for: time estimates on slow steps (initial `npm install`, Docker builds, database migrations on large datasets, ML model downloads), progress indicators or verbose flags available during long operations, timeout values for CI/CD steps, and expected output frequency during long-running commands. Flag any step that is likely to exceed 60 seconds without any progress signal.

---

### Cluster B — Logical and Structural Defects

*Is the document internally coherent? Can a valid execution order even exist?*

**B1. Internal Contradictions.** The document makes two or more claims that cannot both be true simultaneously. These are not ambiguities — they are direct factual conflicts within the same document. Check for: the same tool version cited differently in different sections, the same environment variable named differently in prerequisites vs. configuration sections, the same port number or URL specified inconsistently, the same file named differently in instructions vs. code examples, and architectural claims in one section that conflict with technical details in another. Flag every contradiction regardless of how minor it appears — a discrepancy that seems trivial to the author is a genuine decision point for the reader.

**B2. Ambiguity — Instructions with Multiple Valid Interpretations.** Unlike contradictions, these are instructions that aren't wrong but can be reasonably interpreted in more than one way. "Configure your database" could mean create it, migrate it, seed it, grant permissions, or all four. "Build the application" could mean compile TypeScript, bundle the frontend, build a Docker image, or run a Gradle task. File paths that are ambiguously relative or absolute. Commands that could apply to local or production contexts without being labeled. Flag every instruction where two reasonable readers could take meaningfully different actions.

**B3. Logical Errors in Build Sequence.** Steps that are individually correct but placed in an incorrect order, creating a logical defect. Mentally simulate the execution as a state machine: can every step be executed given only the outputs of all prior steps? Are services started before the steps that depend on them? Are migrations run after the database is initialized and before the application starts? Are environment variables sourced before the commands that read them? Is the frontend built before the server that serves it is started? Flag any step whose preconditions are not guaranteed by the accumulated state of all prior steps.

**B4. Circular and Bootstrapping Paradoxes.** These are not ordering errors — they are genuine logical impossibilities where no valid linear execution order exists. The document requires tool X to install tool X. Credential setup is documented after the step that requires those credentials. The application must run once to generate its own configuration file before it can run. The test suite requires a seeded database that only the running application can populate, but the application requires a passing test suite before deployment. Identify any step A whose precondition is the output of step B, where step B requires the completion of step A.

**B5. Non-Idempotency and Silent State Mutation.** Some documented steps are destructive or non-idempotent and the manifest doesn't say so. Running a migration twice may corrupt data. Running a seed script twice may duplicate records. Running an `init` command twice may overwrite a manually edited config. Running a `chmod -R 777` for "convenience" permanently weakens security. Check every step: what happens if it is run a second time? A third time? After a failed partial run? Flag any step that is non-idempotent without labeling itself as such, and any step that is silent about its state mutations.

**B6. Environment Tier Conflation.** Instructions for local development, CI/CD, staging, and production are interleaved or undifferentiated. A developer reading a "deployment" section doesn't know if those steps apply to their local Docker environment, the staging pipeline, or the production cluster. This causes production-specific steps to be applied in development contexts, and development shortcuts (debug flags, relaxed security, mock credentials) to leak into production. Check that every instruction is clearly labeled with its intended environment, and flag any section where multiple tiers are addressed without explicit labeling.

---

### Cluster C — Accuracy and Drift

*Does the document accurately describe the codebase as it exists today?*

**C1. Staleness and Documentation Rot.** The document was once correct, then the code changed and the docs didn't. It now contains instructions referencing files that were renamed, API endpoints that no longer exist, command names that changed in a dependency upgrade, architecture descriptions of a system that was refactored, and expected outputs that no longer match runtime reality. Check for: commands that reference scripts not present in `package.json` or `Makefile`, config keys the application no longer reads, service names that don't match the Docker Compose or Kubernetes manifests, and build steps that would fail against the current codebase. The dangerous characteristic of stale documentation is that it looks authoritative.

**C2. External Inconsistency — Document vs. Repository Reality.** The manifest describes a reality that doesn't match the actual codebase. This is distinct from staleness — it may have always been inaccurate, written aspirationally or carelessly from the start. Check: do the documented `package.json` scripts actually exist? Do the referenced configuration files actually exist at the stated paths? Does the described port match what the application actually binds to? Does the described data flow match the actual code? Does the architecture diagram reflect the actual system topology? Validate claims against the repository structure rather than taking them on faith.

**C3. Aspirational Scope — Claiming Things That Don't Exist Yet.** The document presents planned, in-progress, or wishful features alongside current reality, without distinguishing them. A feature is documented as available but marked TODO in the code. An architecture diagram includes services that haven't been built. A configuration key is documented but the application silently ignores it. Check for: TODOs in code that contradict documented behavior, configuration options that have no effect, and sections that describe future state without labeling them as such.

**C4. Misleading Architecture and Design Descriptions.** The system diagram or prose description is directionally wrong in a way that causes new contributors to build an incorrect mental model of the system. The diagram shows microservices but the code is a monolith. The described data flow shows A calling B but in reality B calls A. The README says the app uses a message queue but the queue was replaced by synchronous calls in the last refactor. These are more dangerous than mere staleness because they actively corrupt the reader's understanding of how the system works, contaminating every subsequent decision they make.

**C5. Deprecated Approach Persistence.** The document describes a way of doing something that was correct two years ago but is now deprecated, replaced, or actively harmful in newer versions of the toolchain. The old approach may still technically work (which is why nobody updated the docs), but it misses security fixes, uses APIs scheduled for removal, bypasses a recommended mitigation, or produces a less reliable result. Check for: deprecated package names, old authentication patterns, legacy configuration formats, and build commands that have safer modern equivalents.

**C6. False Confidence in Tests.** Documented tests that will pass even when the system is broken. Tests written against mocks that return canned success responses regardless of system state. A smoke test that checks the process started rather than that it responded correctly. A health check endpoint that always returns 200. This is distinct from missing tests — these are present-but-misleading tests that create an illusion of verification. Flag any test step where passing doesn't actually imply correctness of the underlying system.

**C7. Multi-Contributor Authorship Drift.** Different sections were written by different people at different times with different levels of accuracy, terminology, and assumptions about the reader. The reliability of the document is not uniform, but the document gives no signal about this. Section 2 may be battle-tested; section 6 may have been written hastily by someone who left the team and has never been reviewed. Check for: sections with inconsistent voice or precision level, sections that contradict each other on specifics, and sections with hedged or vague language scattered among otherwise precise sections.

---

### Cluster D — Safety and Risk

*Does the document introduce danger, exposure, or legal liability?*

**D1. Security Vulnerabilities Introduced by the Documentation.** The manifest actively teaches or enables insecure practices. Hardcoded secrets in example commands — even "fake" credentials get copied, committed, and forgotten. A `.env.example` with real-looking default values that developers leave unchanged. Instructions to disable SSL verification "for development" with no production warning. Steps that require running services as root. Credentials that appear in log output examples. The document itself becomes an attack surface. Flag any example that could be committed to a repository and used as a credential, and any instruction that disables a security control without an explicit warning.

**D2. Legal and Licensing Deficits.** The manifest introduces a dependency whose license is incompatible with the project's declared license — GPL code in a proprietary product, SSPL-licensed infrastructure in a SaaS product. It uses data assets, API outputs, or third-party models whose licenses impose redistribution restrictions the reader isn't warned about. Or it simply has no license statement, which in most jurisdictions means the project is legally "all rights reserved" even if it appears open. Check for: the presence of a license declaration, known license incompatibilities among documented dependencies, and any dependency on data or model outputs with usage restrictions.

**D3. Data Privacy Contamination in Examples.** The manifest uses real-looking PII in example commands, sample API calls, test data snippets, or expected output blocks — names that look like real people, email addresses that look deliverable, credit card numbers that pass Luhn check, OAuth tokens that look like real JWTs. Developers copy these into local environments, test databases, error logs, and Slack messages. Some of these "example" values may be real data that was anonymized improperly. Check every example for PII patterns and flag anything that could be mistaken for or misused as real personal data.

**D4. Absence of Negative Instructions — What Not To Do.** The manifest only tells you what to do, never what not to do. It doesn't warn you not to run the seed script in production. It doesn't note that running the migration twice will corrupt the join table. It doesn't flag that the `reset` command drops all data without confirmation. These omissions are often more dangerous than missing positive instructions, because developers make reasonable-seeming choices that the author knew were wrong but never documented. Check for any irreversible operations, destructive commands, or dangerous configurations that have no warning attached.

**D5. Environment Contamination and Unscoped Side Effects.** The documented setup performs global mutations as side effects without documenting them. Installing npm packages globally. Modifying system-wide shell profiles. Writing to `/etc/hosts`. Installing system-level services. These changes persist after the build, affect other projects on the same machine, and interfere with re-running the setup. Flag any step whose side effects extend beyond the project directory, and note whether cleanup or reversal instructions are provided.

**D6. Reproducibility and Determinism Gaps.** The manifest gives no indication of whether the build is expected to be reproducible — whether running it twice should produce identical output. For signed artifacts, reproducible builds are a security requirement. For ML projects, random seeds and hardware-dependent floating-point behavior mean "works on my machine" is a class of reproducibility failure. Check for: random seeds that are undocumented, floating-point non-determinism that could affect test thresholds, and build timestamps embedded in artifact hashes. Flag the absence of a reproducibility contract for any project where reproducibility would matter.

---

### Cluster E — Operational Completeness

*Can a team operate this system beyond the first successful build?*

**E1. Rollback, Recovery, and Teardown.** The manifest tells you how to build forward but gives no instructions for what happens when something goes wrong mid-process, or when you need to reset and start over. If the database migration at step 8 fails, how do you roll it back? If a Docker build leaves dangling intermediate layers, how do you clean them up? If you need to fully reset to a clean slate, what does that command sequence look like? Check for: rollback commands for each stateful operation, cleanup commands for failed builds, reset-to-clean-state instructions, and any partial-run recovery procedure. Flag any step that creates persistent state without a documented reversal.

**E2. Observability and Debugging Information.** The manifest tells you what to run but never tells you how to debug it when it goes wrong. It doesn't say where log files are written. It doesn't mention that `DEBUG=*` or `--verbose` will produce diagnostic output. It doesn't describe what a healthy startup sequence looks like versus an unhealthy one. Check for: log file locations, debug flag documentation, expected healthy startup output patterns, and known failure modes with their diagnostic messages. Flag any project where a failure would produce no actionable output without this information.

**E3. Missing Error Signposting and Validation Checkpoints.** Steps with no expected output leave the reader unable to distinguish successful silent completion from silent failure. No intermediate checkpoints in long sequences. No indication of which steps are slow. No way to verify that a service is actually ready before proceeding to a step that depends on it. Check for: expected output or exit codes for every non-trivial step, readiness checks before steps that depend on external services, and clear indicators of build completion versus in-progress states.

**E4. Dependency Conflict and Pinning Rationale.** The manifest lists pinned versions but never explains why. When a maintainer encounters a pin six months later, they cannot know if it exists because of a security patch, a known incompatibility, a transitive conflict, or neglect — and therefore can't make an informed decision about upgrading. Check for: pins with no explanatory comment, known incompatibilities between documented dependencies, and transitive dependency conflicts that may silently break on re-resolution. Flag pins that look arbitrary without rationale.

**E5. Output Format and Encoding Contract.** The build produces artifacts — binaries, bundles, Docker images, packages, config files — but the manifest never specifies their expected format, encoding, naming convention, hash, checksum, or size range. A downstream consumer of these artifacts has no contract to verify against. Check for: expected artifact naming conventions, checksum or signature verification steps, encoding declarations, and size or content validation steps for critical artifacts.

---

### Cluster F — Accessibility and Reader Usability

*Can people across different contexts, platforms, and experience levels actually follow this?*

**F1. Implicit Assumptions — Undocumented Prerequisites.** The document assumes the reader has knowledge, context, tools, or environment state it never establishes. The reader is assumed to be on macOS. They're assumed to be using bash. They're assumed to have admin access. They're assumed to have a running database from a previous project. They're assumed to have gone through onboarding that no longer reflects the current setup. These gaps feel obvious to the author and catastrophic to the reader. Check: does the document create everything it needs, or does it assume a context that a brand-new reader on a fresh machine would not have?

**F2. Platform and Environment Specificity Without Labeling.** Instructions that work only on a specific platform or shell, presented without labeling them as such. macOS-only commands (`brew`, `open`, `pbcopy`). Bash-only syntax in a world of zsh and fish users. x86-specific steps that fail on Apple Silicon or ARM servers. Windows backslash paths in cross-platform projects. Check every command for platform or shell specificity and flag any that would behave differently or fail on any mainstream platform without a label indicating so.

**F3. Internationalization and Locale Assumptions.** Commands that parse output from system tools like `date`, `ls -l`, `ps`, or `sort` will produce different output depending on locale and language settings. Shell scripts that rely on English error message text for control flow will fail on non-English systems. UTF-8 encoding is not universal — Windows defaults to CP-1252, causing build corruption in codebases that rely on consistent encoding. Check for any command whose output is parsed programmatically, and any encoding assumption that is not explicitly declared.

**F4. Inconsistent Terminology.** The same concept is referred to by different names in different sections. The database is called "Postgres," "PostgreSQL," "the DB," "postgres:latest," and "the primary datastore" in five different sections. This is not just a readability problem — it makes the document non-parseable by automated systems, makes cross-referencing error-prone, and makes it genuinely unclear whether two mentions of seemingly different things refer to the same entity. Check that a consistent term is used for every concept throughout the entire document.

**F5. Cognitive Overload and Structural Navigation Failure.** This specifically concerns the manifest imposing excessive working memory demands on the reader — requiring them to hold many context variables in mind before any action can be taken, distributing prerequisite knowledge across non-contiguous sections, burying critical warnings in large prose paragraphs, presenting everything with equal visual weight regardless of importance. Research in documentation usability demonstrates that cognitive overload directly increases error rates: a developer under high cognitive load will make more mistakes executing correct instructions. Check: can the document be followed linearly without backtracking? Are warnings visually distinct from instructions? Are optional steps labeled as optional?

**F6. Monorepo and Multi-Package Structural Opacity.** The project is a monorepo with multiple packages, services, or modules, but the manifest describes it as if it were a single-package project. Check for: the build order of interdependent packages, how packages are linked during development (symlinks, workspace protocols, local registry), which packages share a build step and which require independent steps, and how to run a subset of the project for faster iteration. Flag if the repo structure implies a monorepo but the manifest treats it as a single package.

---

### Cluster G — Governance and Longevity

*Will this document remain reliable, legally sound, and maintainable over time?*

**G1. Governance and Maintainability Deficits.** The document provides no signal about its own reliability or currency. No "last verified" date or manifest version number, making it impossible to know whether it predates a major refactor. No owner or point of contact for when the instructions fail. No changelog for the manifest itself. No indication of the project's maintenance status (actively developed, in maintenance mode, archived, deprecated). These don't prevent the first build but compound every failure that follows — without governance metadata, a broken manifest has no owner and no history.

**G2. Unreachable or Broken References.** The document points to things that don't exist or no longer exist: dead hyperlinks, references to deprecated packages, internal cross-references pointing to the wrong section, references to files in the repo that have been deleted or renamed, code examples calling functions that no longer exist, Docker image tags never pushed to the referenced registry, and configuration keys pointing to values the application no longer reads. Each broken reference is a dead end that transforms a confident reader into a stuck one.

**G3. Concurrency and Setup Race Conditions.** Multi-step setups that start services and then immediately run against them assume the service is ready at the moment the next command runs. This is a non-deterministic failure — it works sometimes and fails sometimes based on machine speed. The `wait-for-postgres.sh` pattern exists because this failure mode is universal. Similarly, parallel CI/CD jobs that both write to the same artifact directory, the same database, or the same registry tag without serialization constraints introduce instruction-level race conditions. Check for: any step that starts a service and immediately connects to it without a readiness check, and any parallel step configuration that shares mutable state.

---

### Cluster H — Deferral Integrity

*For everything the document intentionally delegates, postpones, or hands off: is the deferral safe, reachable, and complete enough to be honoured?*

This cluster operates on the deferral map you built in Phase 1. Every identified deferral gets evaluated here. Do not re-evaluate deferrals in the other clusters — but do note in those clusters when a topic is absent because it has been deferred rather than simply missing.

**H1. Explicit Cross-Reference Validity.** Every "see X" or "refer to Y" must point to something that actually exists and actually covers what it promises to cover. Check for: referenced files that don't exist in the repository (`DEPLOYMENT.md`, `ops/runbook.md`, a wiki page URL that 404s), referenced sections that don't exist within the same document ("see the Configuration section" when there is no Configuration section), and references that exist but are themselves incomplete or outdated — a "see X" that resolves to another broken document is a deferred gap, not a fulfilled one. A broken cross-reference is often worse than a silent gap because it creates a false sense that the information exists somewhere.

**H2. Scope Declaration Adequacy.** When the document declares its own scope ("this guide covers local development only"), evaluate whether that scope declaration is sufficient for the document's stated purpose, whether it appears early enough for the reader to know before they start following instructions, and whether everything outside the declared scope has a documented path to resolution. A scope declaration without a pointer to where the out-of-scope information lives is not a valid deferral — it is an unresolved delegation.

**H3. Delegation Language — Is the Delegatee Identified and Reachable?** When the document says "your ops team will handle this" or "handled by CI," the reader must be able to identify who or what that means and how to reach them. Check for: delegations to unnamed or unteachable parties ("the DevOps team" with no contact or link), delegations to automated processes with no documentation of what those processes do or where they're configured, and delegations that would block a solo developer or contractor who has no access to the delegatee. A delegation to a person or team that a reader might not have access to is a SIGNIFICANT finding unless the document acknowledges and provides an alternative.

**H4. TODO and WIP Markers — Intent vs. Impact.** A `TODO` or `WIP` marker in a non-critical section is a minor cosmetic concern. A `TODO` inside a build step, a security section, or a deployment procedure is a CRITICAL finding — the reader cannot skip it just because the author didn't finish it. Evaluate each marker on its location and impact: is the unfinished section on the critical path? Does the surrounding content still make sense without the missing piece? Does the marker indicate "I'll add this later" or "this whole section needs to be written"? A document with a `TODO: add deployment instructions` in the Deployment section is functionally equivalent to having no Deployment section at all.

**H5. Conditional Deferrals and Branch Completeness.** When the document says "if using Kubernetes, follow the Kubernetes guide" or "if on Windows, see the Windows setup doc," both branches must be valid and reachable. Check for: branches where one path is fully documented and another is deferred to a reference that doesn't exist, conditional branches with no fallback for cases that don't match any documented path, and branching logic that is ambiguous — "if using Docker" when Docker is optional but the document doesn't say so, leaving the reader to guess whether they should use Docker. Every conditional must have a complete resolution for every case the reader might fall into.

**H6. Deferred Chains — Cascading Delegation.** A deferral that points to a document that itself defers to another document that itself defers further creates a resolution chain that may never terminate. Check whether following all the cross-references and delegations in the document eventually resolves to complete, actionable instructions or leads to a chain of dead ends. A manifest that defers to a runbook that defers to a wiki that defers to a Confluence page that requires an account the reader doesn't have is a deferred chain failure. The document is responsible for the resolvability of every chain it initiates.

**H7. Implicit Deferrals — Gaps Disguised as Choices.** These are the most dangerous category. An implicit deferral is when the document omits something without any signal that the omission was intentional — no cross-reference, no scope declaration, no TODO marker. It just isn't there. The reader cannot distinguish this from a simple oversight. Use context to assess: is this topic absent because the author made a deliberate scoping decision that they simply failed to communicate, or is it a pure gap? If there's evidence of intent (the document is clearly scoped to local dev, or a later section assumes the thing was handled), classify it as an implicit deferral and flag in H7 that the deferral needs to be made explicit. If there's no evidence of intent, classify it as a gap in the relevant cluster. When in doubt, classify as a gap — the cost of over-flagging is lower than the cost of letting a true gap pass as an intentional deferral.

---

## Phase 3: Producing the Critique

Structure the output exactly as follows. Every finding must have a home, a specific location, a precise problem statement, and an actionable fix. Vague findings are not findings — they are noise.

```
# Manifest Critique: [Document Title or "Untitled Manifest"]

## Overall Verdict
[One of: FULLY BUILDABLE | BUILDABLE WITH CAVEATS | NOT BUILDABLE]
[One of: SAFE | SAFE WITH WARNINGS | CONTAINS RISKS]
[One of: ACCURATE | PARTIALLY ACCURATE | MATERIALLY INACCURATE]

Two to three sentences explaining the verdict across all three dimensions.
What are the biggest blockers or risks? What makes it pass if it passes?

---

## Critical Findings (Build-Breaking, Safety-Critical, or Legally Significant)

**[Finding Title]**
Cluster: [Letter and number, e.g. "A4 — Build Steps"]
Severity: CRITICAL
Location: [Section name, line number, or "Missing — no section covers this"]
Problem: [What is wrong or absent, stated precisely enough that the author
immediately understands the specific gap]
Fix: [The exact change required — specific enough to implement without further
clarification. Include example commands, configuration, or text where applicable]

---

## Significant Findings (Likely to Cause Failure in Common Conditions)

[Same format, Severity: SIGNIFICANT]

---

## Minor Findings (Fragility, Polish, and Long-Term Reliability)

[Same format, Severity: MINOR]

---

## Deferred Items

List every deferral identified in the Cluster H analysis, classified by 
its integrity status. Use exactly three sub-sections:

**Valid Deferrals** — intentional, clearly signaled, and pointing to a
reachable, complete target. These are not findings. Acknowledge them 
briefly so the author knows the skill recognized the intent.

**Broken Deferrals** — intentional but pointing to a missing, unreachable,
or incomplete target. These are findings. For each: what the deferral 
promises, why the target fails to deliver it, and what the fix is 
(repair the reference, inline the content, or declare it out of scope 
with an acknowledgment).

**Implicit Deferrals** — omissions that appear to have been intentionally
scoped out, but were never communicated as such. For each: the evidence 
of intent, why the omission is still a risk, and the recommended fix 
(make the deferral explicit with a cross-reference or scope note, or 
promote it to a gap finding in the relevant cluster).

If there are no deferrals of a given type, write "None identified" rather 
than omitting the sub-section — absence is itself informative.

---

## Passed Checks

Briefly acknowledge what the manifest gets right, organized by cluster.
This is not a courtesy — it tells the author which sections are trustworthy
and confirms the critique is balanced rather than adversarial.

---

## Recommended Fix Priority

List the top five fixes in the order they must be applied, because some
fixes depend on others. For each: the finding title, and one sentence on
why it must precede the next item.
```

---

## Mindset Notes

**You are simulating a context-free automated agent.** Pretend you are a CI/CD pipeline executing these steps character by character, with no ability to infer intent, no tribal knowledge, no tolerance for ambiguity, and no way to ask a clarifying question. If a step says "configure your database," you cannot do it. Flag it every time.

**Distinguish between absent, incomplete, and deferred.** Three different states, three different fixes. Absent means the author didn't know it was needed. Incomplete means the author started but didn't finish. Deferred means the author knowingly chose not to cover it here. The first two are gaps in the relevant cluster. The third belongs in Cluster H. Misclassifying a deferral as a gap produces noise that erodes trust in the critique; misclassifying a gap as a deferral lets a real problem hide behind false intent.

**A broken deferral is worse than a silent gap.** If the document says nothing about deployment, the reader knows there's a gap. If the document says "see `DEPLOYMENT.md`" and that file doesn't exist, the reader confidently walks into a dead end. Broken references create false confidence, which is more dangerous than acknowledged ignorance.

**Never let diplomatic softening obscure a real gap.** A manifest that would cause a two-hour debugging session for a new developer has a real problem worth naming clearly. Use precise language: not "the configuration section could be expanded" but "the `REDIS_URL` environment variable is read in `src/queue/connection.ts` but is not documented anywhere in this manifest."

**The most dangerous gaps are the ones that look complete.** A step that is present but wrong, a test that passes but doesn't validate, an architecture diagram that is confidently incorrect — these are worse than missing sections because they don't trigger suspicion.

**Every cluster applies to every manifest.** Do not skip Cluster D because the project looks like a toy project. Do not skip Cluster G because the document looks recent. Do not skip Cluster B because the steps look correct individually. The categories that seem least likely to apply are the ones most likely to be genuinely absent.

**When in doubt, file it as MINOR.** Surface it and let the author downgrade it. A consciously omitted section is fine; an unconsciously missing one costs someone hours.
