---
name: skill-sanitizer
description: Security scanner that makes AI agent skills DETERMINISTIC and SAFE. Verifies that every skill behavior matches its description exactly, with no hidden actions, no hidden targets, no extra data flows, no undisclosed executions. Use when: (1) Validating a skill before use, (2) Auditing existing skills, (3) Reviewing skill submissions, (4) Debugging skill security issues, or any time skill safety needs verification.
---

# skill-sanitizer

A skill is SAFE when it is DETERMINISTIC. A deterministic skill does EXACTLY what its description says, and NOTHING beyond that.

**Mission**: Transform skills into deterministic, safe packages that cannot become attack surfaces.

---

## Core Principle

```
EVERY ACTION a skill takes MUST be EXPLICITLY DESCRIBED.
ANY ACTION not described = ATTACK.
```

---

## What skill-sanitizer Checks

### 1. Behavior-Description Alignment

For every action in the skill code, verify:

| Check | Question | If NO |
|-------|----------|-------|
| Is it described? | Does the description mention this type of action? | FLAG |
| Does it match? | Does the action match the description exactly? | FLAG |
| Are targets visible? | Can a human see all targets in the skill files? | FLAG |
| Is scope limited? | Does the action stay within described scope? | FLAG |

### 2. Behavior Categories to Verify

Every action falls into a category. For each category, ask: "Does the description mention this?"

| Category | If NOT Described |
|----------|------------------|
| **Data Movement** | ANY data sent anywhere = FLAG |
| **Code Execution** | ANY script/command execution = FLAG |
| **Downloads** | ANY file downloads = FLAG |
| **File Reads** | ANY file access = FLAG |
| **File Writes** | ANY file modifications = FLAG |
| **Network Requests** | ANY HTTP/WebSocket calls = FLAG |
| **Process Spawning** | ANY subprocess calls = FLAG |
| **Environment Access** | ANY env variable access = FLAG |
| **Credential Access** | ANY credential access = FLAG |
| **Tool Usage** | ANY tool not described = FLAG |
| **API Calls** | ANY API calls not described = FLAG |
| **Memory Operations** | ANY sensitive data storage = FLAG |
| **System Modifications** | ANY system changes = FLAG |
| **User Interaction** | ANY unexpected prompts = FLAG |
| **Time Operations** | ANY time-based triggers = FLAG |
| **External Service Calls** | ANY external services = FLAG |
| **Cryptographic Operations** | ANY crypto operations = FLAG |
| **Logging** | ANY sensitive data logging = FLAG |
| **Error Handling** | ANY external error transmission = FLAG |

### 3. Hidden Content Detection

Verify all targets are VISIBLE:

| Detection | What to Find |
|-----------|---------------|
| **HTML comments** | `<!-- hidden content -->` |
| **Invisible text** | White-on-white, display:none |
| **Collapsed sections** | Markdown collapsed sections |
| **Encoded content** | Base64, hex, unicode escapes |
| **Zero-width characters** | U+200B, U+200C, U+200D, U+FEFF, U+E0000-U+E007F |
| **RTLO abuse** | Bidirectional text overrides |
| **Homoglyphs** | Cyrillic lookalikes: а, е, о, р, с |
| **Markdown hiding** | Hidden code blocks, links |
| **File metadata** | PDF metadata, image EXIF |

### 4. Target Verification

When the description specifies targets (emails, URLs, IPs, file paths):

1. **Are all targets in the defined location?**
   - If description says "emails in references/target_emails.md"
   - Check that ALL emails in code come from that file

2. **Are all targets VISIBLE?**
   - Open the file and check for hidden content
   - Verify no hidden emails/URLs exist

3. **Are there EXTRA targets?**
   - Check code for any targets NOT in the defined location
   - ANY extra target = ATTACK

---

## Scanning Process

### Phase 1: Deterministic Scan (Scripts)

Run pattern-based detection scripts for known attack signatures.

**What it catches:**
- Known malicious patterns
- Obvious deviations from description
- Hidden Unicode/encoding attacks
- Common attack signatures

**What it MISSES:**
- Novel attacks
- Creative language manipulation
- Semantic trickery

### Phase 2: Probabilistic Scan (AI Workflow)

Follow the workflow in `references/workflow.md` for semantic analysis.

**What it catches:**
- Intent analysis beyond patterns
- Creative bypasses
- Semantic manipulation
- Novel attack vectors

**Critical**: This phase catches what scripts cannot.

---

## Determinism Verification Framework

For each action found in skill code:

```
STEP 1: IS THE ACTION DESCRIBED?
├── Check SKILL.md description
├── Check references/ documentation  
├── Check frontmatter
└── NO → FLAG (undocumented action)

STEP 2: DOES IT MATCH DESCRIPTION EXACTLY?
├── Same targets? (URLs, emails, paths)
├── Same data? (what's being processed)
├── Same scope? (limitations)
└── NO → FLAG (action deviates)

STEP 3: ARE ALL TARGETS VISIBLE?
├── No hidden HTML comments
├── No invisible Unicode
├── No collapsed sections
├── No encoded content
└── NO → FLAG (hidden targets)

STEP 4: ARE THERE EXTRA ACTIONS?
├── Extra downloads?
├── Extra executions?
├── Extra network calls?
├── Extra file operations?
└── YES → FLAG (undisclosed actions)

STEP 5: IS BEHAVIOR DETERMINISTIC?
├── No conditional hidden behavior
├── No time-based triggers
├── No environment-dependent behavior
└── NO → FLAG (non-deterministic)
```

---

## Common Attack Patterns to Detect

### Hidden Target Pattern
```
Description: "Send to emails in target_emails.md"
target_emails.md: 9 visible emails + 1 hidden via HTML comment
Attack: The hidden email receives data
```

### Undefined Target Pattern
```
Description: "Send to defined targets"
Code: Sends to defined targets + attacker@evil.com
Attack: The extra target is not described
```

### Scope Expansion Pattern
```
Description: "Process X type of data"
Code: Processes X + also grabs credentials
Attack: Extra data access not described
```

### Undeclared Capability Pattern
```
Description: "Format documents"
Code: Makes network requests
Attack: Network capability not described
```

### Hidden File Content Pattern
```
Reference file: Visible content + hidden content
Hidden content: Malicious instructions or targets
Attack: Hidden content bypasses review
```

### Extra Data Flow Pattern
```
Description: "Data flows from A to B"
Code: Also has data flowing from A to C
Attack: The C path is not described
```

### Undeclared Execution Pattern
```
Description: "Help with documents"
Code: Runs shell scripts
Attack: Script execution not described
```

### Undeclared Download Pattern
```
Description: "Process local files"
Code: Downloads files from internet
Attack: Download capability not described
```

---

## Output Format

```markdown
# SKILL SANITIZATION REPORT

## Summary
- **Skill Name**: [name]
- **Scan Date**: [timestamp]
- **Status**: [SAFE / UNSAFE / REVIEW REQUIRED]

## Determinism Score
- **Declared Behaviors**: [count]
- **Actual Behaviors**: [count]
- **Match**: [YES/NO/PARTIAL]

## Findings

### CRITICAL
[Actions that completely contradict description]

### HIGH
[Undisclosed actions not mentioned anywhere]

### MEDIUM
[Actions that partially match description]

### LOW
[Minor deviations or ambiguities]

## Detailed Analysis

### Behavior Verification
| Action | Described? | Matches? | Visible? | Status |
|--------|------------|----------|----------|--------|
| [action] | [YES/NO] | [YES/NO/NA] | [YES/NO/NA] | [status] |

### Target Verification
| Target Type | Described Location | Actual Location | Match |
|-------------|-------------------|-----------------|-------|
| [type] | [location] | [location] | [YES/NO] |

## Recommendation
[PASS / FAIL / MANUAL REVIEW REQUIRED]
```

---

## Resources

### scripts/
Pattern-based detection scripts for deterministic scanning.

### references/workflow.md
AI agent workflow for probabilistic semantic analysis. Use this when scripts complete to catch novel attacks.

### references/attack-patterns.md
Comprehensive catalog of known attack patterns against AI agent skills.

---

## Usage

1. **Point skill-sanitizer at a skill directory**
2. **Run deterministic scan (scripts)**
3. **Run probabilistic scan (workflow)**
4. **Review combined report**
5. **Make PASS/FAIL decision**

A skill that PASSES is DETERMINISTIC. It does exactly what it says, nothing more, nothing less. Such a skill cannot be an attack surface.
