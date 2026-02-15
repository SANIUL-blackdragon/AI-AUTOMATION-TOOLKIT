---
name: skill-creator
description: Complete guide for creating, updating, and maintaining skills that extend Agent's capabilities. Provides architectural patterns (SKILL.md, scripts, references, assets), progressive disclosure strategies, degrees of freedom framework, and packaging workflows. Use when users want to: (1) Create a new skill from scratch, (2) Update or fix an existing skill, (3) Understand skill architecture and file structure, (4) Debug triggering or context issues, or (5) Learn best practices for token efficiency and skill design.
---

# Skill Creator

This guide provides comprehensive instruction for creating effective skills that extend Agent's capabilities.

---

## Quick Reference Guide

**What is a Skill?** A modular package of specialized knowledge, workflows, and tools that transforms Agent into a specialized agent.

**Core Principles:**
1. ✂️ **Concise is Key** - Only add context Agent doesn't already have
2. 🎯 **Match Freedom to Task** - High/medium/low freedom based on fragility
3. 📦 **Progressive Disclosure** - Metadata → SKILL.md → Resources

**Resource Types:**
- `scripts/` - Executable code for repeated/fragile operations
- `references/` - Documentation loaded as needed
- `assets/` - Files used in output (templates, images)

**File Structure:**
```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
├── references/ (optional)
└── assets/ (optional)
└── requirements.txt (required even if empty) 
```

**Never Include:**
- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, or other auxiliary docs

---

## Phase 1: Understanding Skills

### What Skills Provide

Skills are modular, self-contained packages that extend Agent's capabilities by providing:

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

Think of skills as "onboarding guides" for specific domains or tasks—they transform Agent from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### When to Create a Skill

**Create a skill when:**
- Users repeatedly request similar workflows in a specific domain
- The task requires specialized domain knowledge not in Agent's training
- You need to integrate with specific APIs, file formats, or tools
- There's a need for consistent, repeatable execution of complex procedures
- The task requires bundled resources (templates, scripts, documentation)

**Don't create a skill when:**
- The task is simple and one-off
- The workflow is already straightforward for Agent
- You can solve it with a simple system prompt

### The Philosophy: Agent is Already Smart

**Default assumption: Agent is already very smart.** Only add context Agent doesn't already have. Challenge each piece of information: "Does Agent really need this explanation?" and "Does this paragraph justify its token cost?"

The context window is a public good. Skills share it with:
- System prompt
- Conversation history
- Other Skills' metadata
- The actual user request

---

## Phase 2: Planning Your Skill

### Step 1: Understand with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

**Gather concrete examples** by asking:
- "What functionality should the skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

**Example (image-editor skill):**
- "Remove the red-eye from this image"
- "Rotate this image 90 degrees clockwise"
- "Convert this image to black and white"
- "Resize this to 1920x1080"

**Conclude this step when:** You have a clear sense of the functionality the skill should support.

### Step 2: Plan Reusable Contents

Analyze each concrete example by:
1. Considering how to execute it from scratch
2. Identifying what scripts, references, and assets would be helpful

**Resource Decision Tree:**

```
Need to execute same code repeatedly?
├─ Yes → Use scripts/
└─ No
    Need to reference documentation/standards?
    ├─ Yes → Use references/
    └─ No
        Need files for output (templates, images)?
        ├─ Yes → Use assets/
        └─ No → Everything in SKILL.md
```

**Examples:**

| Task | Analysis | Resource to Include |
|------|----------|---------------------|
| "Rotate this PDF" | Rewriting rotation code each time | `scripts/rotate_pdf.py` |
| "Build me a todo app" | Same HTML/React boilerplate needed | `assets/frontend-template/` |
| "How many users logged in today?" | Need table schemas each query | `references/schema.md` |
| "Format this legal document" | Need style guidelines and examples | `references/legal-style-guide.md` |
| "Generate this report" | Need Word template | `assets/report-template.docx` |

### Step 3: Determine Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High Freedom (Text-based Instructions)**
- **When:** Multiple approaches are valid, decisions depend on context, heuristics guide approach
- **Example:** Creative writing, strategic planning, general consulting
- **SKILL.md format:** Descriptive guidelines, examples, principles

**Medium Freedom (Pseudocode or Scripts with Parameters)**
- **When:** Preferred pattern exists, some variation acceptable, configuration affects behavior
- **Example:** API integrations, data processing pipelines
- **SKILL.md format:** Workflow patterns, parameter explanations, conditional guidance

**Low Freedom (Specific Scripts, Few Parameters)**
- **When:** Operations are fragile/error-prone, consistency is critical, specific sequence required
- **Example:** Financial calculations, security operations, regulated workflows
- **SKILL.md format:** Step-by-step procedures, exact commands, validation checks

**Degrees of Freedom Implementation Examples:**

```markdown
## High Freedom: SEO Optimization

Analyze the content and suggest improvements focusing on:
- Keyword density and placement
- Meta tag optimization
- Content structure for readability
Use judgment based on content type and target audience.
```

```markdown
## Medium Freedom: Data Pipeline

Execute pipeline using this pattern:
1. Extract: [parameters for source]
2. Transform: [transform rules]
3. Load: [destination configuration]
Variations allowed for step 2 based on data type.
```

```markdown
## Low Freedom: Financial Reconciliation

Follow exact sequence:
1. Run reconciliation: `python scripts/reconcile.py --strict`
2. Verify output matches: `python scripts/verify.py output.csv`
3. Archive: `python scripts/archive.sh --date=today`
No variations permitted.
```

---

## Phase 3: Implementation

### Step 4: Initialize the Skill

When creating a new skill from scratch, always run the `init_skill.py` script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

**What this does:**
- Creates the skill directory
- Generates SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, `assets/`
- Adds example files in each directory

**Skip this step if:** The skill already exists and you're iterating.

### Step 5: Create or Update SKILL.md

#### Frontmatter (Required)

The YAML frontmatter contains the only fields Agent reads to determine when to use the skill. **This is critical.**

```yaml
---
name: your-skill-name
description: Clear, comprehensive description
---
```

**Writing Effective Descriptions**

The description is the primary triggering mechanism. It must answer:
1. What does the skill do?
2. When should it be used?
3. What are the key triggers/contexts?

**Poor Examples:**
```yaml
description: This skill helps with documents.
description: A tool for editing things.
description: PDF helper.
```

**Good Examples:**
```yaml
description: Professional document processing for .docx files including text extraction, tracked changes management, and content formatting. Use when working with corporate documents, legal contracts, or any .docx files requiring precise editing.

description: Comprehensive PDF manipulation toolkit supporting rotation, merging, splitting, text extraction, and form filling. Use when users need to modify PDF structure, extract content, or automate PDF workflows. Triggered by queries mentioning: "rotate PDF", "merge PDFs", "extract text from PDF", "PDF forms", "split PDF".

description: Financial data analysis with specialized knowledge of accounting standards, financial ratios, and reporting requirements. Use for financial statement analysis, budget review, variance analysis, or any task requiring domain-specific financial expertise.
```

**Description Best Practices:**
- Start with a clear 1-2 sentence summary of functionality
- List specific use cases in "Use when..." format
- Include trigger phrases when applicable
- Be comprehensive enough to catch all relevant queries
- Avoid being so specific it misses edge cases
- Avoid being so generic it triggers incorrectly

**Important:** Do not include any other fields in YAML frontmatter.

#### Body Structure

Organize the body with clear sections:

```markdown
# Skill Name

## Quick Start
[Immediate, actionable instructions]

## Core Workflow
[Main procedure]

## Advanced Features
[Links to references for complex topics]

## Error Handling
[What to do when things go wrong]

## Resources
[When to use scripts/references/assets]
```

**Writing Guidelines:**
- Always use imperative/infinitive form ("Extract text", not "Text extraction")
- Prefer concise examples over verbose explanations
- Link to references when content becomes detailed
- Keep core workflow visible in SKILL.md

### Step 6: Implement Bundled Resources

#### Scripts (`scripts/`)

Executable code for deterministic reliability or repeated execution.

**When to include:**
- Same code is being rewritten repeatedly
- Deterministic reliability is needed
- Complex logic that shouldn't be rewritten
- Performance-critical operations

**Example structure:**
```
scripts/
├── core_operation.py
├── validate.py
└── utils.py
```

**Best Practices:**
- Test all scripts before packaging
- Include clear error messages
- Handle edge cases gracefully
- Add comments for complex logic
- Use command-line arguments for flexibility

**Testing Scripts:**
- Run with expected inputs, verify output
- Test with edge cases
- Test error conditions
- For similar scripts, test representative sample

#### References (`references/`)

Documentation loaded as needed to inform Agent's process and thinking.

**When to include:**
- Documentation needed while working
- Domain knowledge not in general training
- Company-specific policies/schemas
- API documentation
- Detailed workflow guides

**Example structures:**

By domain:
```
references/
├── finance.md (revenue, billing metrics)
├── sales.md (opportunities, pipeline)
└── product.md (API usage, features)
```

By feature:
```
references/
├── advanced-forms.md
├── ooxml-specs.md
└── api-reference.md
```

**Best Practices:**
- For files >100 lines, include table of contents
- Avoid duplication with SKILL.md
- Reference from SKILL.md with clear "when to read"
- Keep content focused and actionable
- Use clear headings and structure

**Example reference structure:**
```markdown
# API Reference

## Quick Links
- Authentication: #authentication
- Endpoints: #endpoints
- Error Codes: #errors

## Authentication
[detailed auth instructions]

## Endpoints
[endpoint documentation]

## Errors
[error handling guide]
```

#### Assets (`assets/`)

Files used within Agent's output, not loaded into context.

**When to include:**
- Templates for output generation
- Brand assets (logos, fonts)
- Boilerplate code/projects
- Sample documents to copy/modify
- Configuration files

**Example structures:**
```
assets/
├── logo.png
├── report-template.docx
└── frontend-boilerplate/
    ├── package.json
    ├── src/
    └── public/
```

**Best Practices:**
- Document how assets should be used in SKILL.md
- Include usage examples
- Keep assets versioned with skill
- Test that assets work as expected

### Progressive Disclosure Patterns

Skills use a three-level loading system:
1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers
3. **Bundled resources** - As needed by Agent

**Pattern 1: High-level Guide with References**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

- **Form filling**: See [FORMS.md](references/FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](references/REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md) for common patterns
```

**Pattern 2: Domain-specific Organization**

SKILL.md:
```markdown
# BigQuery Analytics

## Overview

This skill provides domain-specific analytics for Finance, Sales, Product, and Marketing.

## Usage

Agent will load the relevant domain reference based on query context.

## Available Domains
- Finance: Revenue, billing metrics (see references/finance.md)
- Sales: Opportunities, pipeline (see references/sales.md)
- Product: API usage, features (see references/product.md)
- Marketing: Campaigns, attribution (see references/marketing.md)
```

Reference file structure:
```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

**Pattern 3: Conditional Details**

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](references/DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
**For OOXML details**: See [OOXML.md](references/OOXML.md)
```

**Pattern 4: Skill Lifecycle**

SKILL.md:
```markdown
# Data Engineering Pipeline

## Level 1: Basic Operations

Simple data movement and transformation.
(See [BASIC.md](references/BASIC.md) for fundamentals)

## Level 2: Advanced Processing

Complex transformations, joins, aggregations.
(See [ADVANCED.md](references/ADVANCED.md) for patterns)

## Level 3: Production Workflows

Scheduling, monitoring, error recovery.
(See [PRODUCTION.md](references/PRODUCTION.md) for ops)

## When to use each level:

- Level 1: One-off data tasks, quick prototypes
- Level 2: Regular reporting, data marts
- Level 3: Production pipelines, mission-critical data flows
```

### What to Not Include

A skill should only contain essential files that directly support its functionality.

**Do NOT create:**
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- TEST_RESULTS.md
- USER_MANUAL.md
- Any other auxiliary documentation

**Why:** These files add clutter and confusion. The skill is for an AI agent, not human users. All necessary information should be in SKILL.md or appropriately organized references.

---

## Phase 4: Testing & Validation

### Step 7: Validate Skill Functionality

**Testing Checklist:**

1. **Frontmatter Validation**
   - ✅ Description clearly describes when to use the skill
   - ✅ Description includes specific triggers/use cases
   - ✅ Name follows naming conventions (lowercase, hyphens)

2. **Structure Validation**
   - ✅ SKILL.md exists with proper frontmatter
   - ✅ All referenced files exist
   - ✅ Scripts, references, assets in correct directories
   - ✅ No auxiliary documentation files

3. **Content Validation**
   - ✅ SKILL.md body contains actionable instructions
   - ✅ References are linked and described with "when to read"
   - ✅ Scripts are tested and functional
   - ✅ Assets are documented

4. **Trigger Testing**
   - ✅ Test that description triggers on intended queries
   - ✅ Test that description doesn't trigger on unrelated queries
   - ✅ Test edge cases and ambiguous queries

### Step 8: Test Progressive Disclosure

**Validation Process:**

1. **Metadata Only**: Verify that name and description alone give enough context to know if the skill is relevant
2. **SKILL.md Loading**: Verify that loading SKILL.md provides complete workflow for basic tasks
3. **Reference Loading**: Test that references load at appropriate times and contain needed details

**Testing Scenarios:**
- Simple task: Should complete with just SKILL.md
- Complex task: Should load appropriate reference(s)
- Multi-domain task: Should load correct domain reference only

### Step 9: Error Handling Validation

**Test error conditions:**
- What happens if a script fails?
- What happens if a required file is missing?
- What happens if input is invalid?
- What happens if references contradict each other?

**Document error handling in SKILL.md:**
```markdown
## Error Handling

If script fails:
1. Check input format matches [specification]
2. Verify [prerequisite conditions]
3. Consult [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
```

### Common Pitfalls to Avoid

| Pitfall | Why it's bad | How to avoid |
|---------|--------------|--------------|
| Over-specific description | Misses edge cases, doesn't trigger when it should | Include broader context, multiple trigger examples |
| Over-abstract description | Triggers incorrectly, wastes context | Be specific about domain and use cases |
| Context bloat | Hits token limits, slow responses | Use progressive disclosure aggressively |
| Deeply nested references | Hard to find information | Keep references 1 level from SKILL.md |
| Duplication | Confusing, token waste | Info lives in SKILL.md OR references, never both |
| Untested scripts | Failures in production | Test all scripts before packaging |
| Missing "when to read" guidance | References never loaded | Explicitly state when each reference should be read |
| No error handling | Silent failures, user frustration | Document error handling and recovery |
| Ignoring token efficiency | Skills become unusable | Challenge every piece of content for necessity |
| Not updating frontmatter | Skill drifts from description | Review frontmatter when skill changes |

---

## Phase 5: Packaging & Deployment

### Step 10: Package the Skill

Once development is complete, package into a distributable .skill file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:
```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

**Packaging process:**
1. Validates skill structure and content
2. Creates .skill file (zip with .skill extension)
3. Maintains proper directory structure
4. Reports validation errors if any

**Validation checks:**
- YAML frontmatter format and required fields
- Skill naming conventions
- Directory structure
- Description completeness
- File organization and resource references
- No auxiliary documentation files

### Step 11: Deploy and Monitor

**Deployment considerations:**
- Document any environment requirements
- Specify any external dependencies (APIs, tools)
- Provide migration guide if updating existing skill
- Note any breaking changes

**Monitor for:**
- Trigger accuracy (is it activating when expected?)
- Token efficiency (staying within limits?)
- User satisfaction (solving the problem?)
- Common error patterns

### Step 12: Iterate Based on Usage

**Iteration workflow:**
1. Use skill on real tasks
2. Notice struggles or inefficiencies
3. Identify updates needed in SKILL.md or resources
4. Implement and test changes
5. Repackage

**Common iteration triggers:**
- Skill not triggering on expected queries → Improve description
- SKILL.md too long → Move content to references
- Reference files hard to navigate → Add TOC or reorganize
- Scripts failing → Debug and fix
- Users asking same questions repeatedly → Add to SKILL.md
- Edge cases not handled → Add error handling guidance

---

## Additional Considerations

### Skill Discoverability

Help users find and understand your skill:

**Naming Conventions:**
- Use lowercase with hyphens: `pdf-editor`, `financial-analysis`
- Be descriptive: `docx-legal-documents` not `word-helper`
- Avoid abbreviations: `financial-reports` not `fin-rpts`

**Categorization:**
If maintaining multiple skills, organize them logically:
- By domain: `finance/`, `engineering/`, `marketing/`
- By function: `data-processing/`, `document-creation/`, `api-integrations/`

### Skill Composition

**Can skills depend on other skills?**
Yes, but be cautious. Document dependencies clearly.

```markdown
## Dependencies

This skill builds on the `pdf-parser` skill. Ensure it is available for:
- Complex text extraction tasks
- PDF structure analysis
```

**Handling conflicts:**
- If two skills might trigger on similar queries, make descriptions more specific
- Document how skills interact
- Consider merging overlapping functionality

### Version Management

**When to version:**
- Breaking changes to functionality
- New major features
- Changes to triggering behavior
- Incompatible updates

**Version format:** Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

**Communication:**
- Document breaking changes clearly
- Provide migration path
- Note what changed in description

### Security Considerations

**For skills accessing external APIs:**
- Store credentials securely (never in skill files)
- Document required permissions
- Include error handling for auth failures
- Implement rate limiting if appropriate

**For skills handling sensitive data:**
- Document data handling practices
- Clear guidance on what should/shouldn't be logged
- Sanitize outputs appropriately

**For skills executing code:**
- Validate all inputs
- Use principle of least privilege
- Document security assumptions
- Test for injection vulnerabilities

### Success Criteria

A successful skill should demonstrate:

**Trigger Accuracy:**
- Activates on relevant queries
- Doesn't activate on irrelevant queries
- Handles edge cases appropriately

**Token Efficiency:**
- SKILL.md stays within reasonable length
- References load only when needed
- Scripts execute without loading into context

**User Satisfaction:**
- Solves the intended problem effectively
- Provides clear guidance
- Handles errors gracefully
- Maintains consistency

**Maintainability:**
- Clear structure
- Well-documented
- Easy to update
- Testable

---

## Worked Examples

### Example 1: Simple Skill (SKILL.md Only)

**Task:** Text normalization for data cleaning

**SKILL.md:**
```yaml
---
name: text-normalizer
description: Standardize and normalize text data including case conversion, whitespace handling, special character removal, and Unicode normalization. Use when cleaning data, preparing text for analysis, or standardizing user input.
---
```

```markdown
# Text Normalizer

## Quick Start

Apply this normalization pipeline:
1. Unicode normalization (NFKC form)
2. Trim leading/trailing whitespace
3. Replace multiple spaces with single space
4. Remove control characters (except newlines)
5. Convert to specified case (default: sentence case)

## Case Conversion

- `--case lower`: all lowercase
- `--case upper`: all uppercase
- `--case title`: Title Case
- `--case sentence`: Sentence case (default)

## Special Character Handling

By default, preserves most special characters. To remove specific characters:
- `--remove-punctuation`: Remove .,!?;:
- `--remove-symbols`: Remove @#$%^&* etc.
- `--keep`: Comma-separated list to preserve

## Example

Input: "  Hello\u00a0World!!!  "
Output: "Hello world!!!"

With `--case lower --remove-punctuation`: "helloworld"
```

---

### Example 2: Medium Complexity Skill (With References)

**Task:** Company policy lookup and application

**Directory Structure:**
```
company-policies/
├── SKILL.md
└── references/
    ├── hr-policies.md
    ├── it-policies.md
    ├── finance-policies.md
    └── travel-policies.md
```

**SKILL.md:**
```yaml
---
name: company-policies
description: Access and apply company policies across HR, IT, Finance, and Travel domains. Use when answering policy questions, reviewing compliance, or handling policy-related requests. Triggered by queries about: vacation policy, expense reimbursement, device usage, travel booking, or any "what's the policy on..." questions.
---
```

```markdown
# Company Policies

## How to Use

1. Identify the policy domain from the user query
2. Load the relevant reference file:
   - HR: references/hr-policies.md
   - IT: references/it-policies.md
   - Finance: references/finance-policies.md
   - Travel: references/travel-policies.md
3. Apply the policy to the specific situation
4. Cite the relevant policy section

## Policy Domains

### HR Policies
Employee conduct, benefits, leave, performance reviews
→ See [HR_POLICIES.md](references/hr-policies.md)

### IT Policies
Device usage, security, software installation, data access
→ See [IT_POLICIES.md](references/it-policies.md)

### Finance Policies
Expense reporting, reimbursements, budget approvals
→ See [FINANCE_POLICIES.md](references/finance-policies.md)

### Travel Policies
Booking, meal allowances, mileage, conference attendance
→ See [TRAVEL_POLICIES.md](references/travel-policies.md)

## Handling Exceptions

If policy doesn't address situation:
1. Check related domains
2. Look for general principles that apply
3. Recommend escalation to HR/manager
4. Document the gap for policy review

## Common Questions

**Can I expense lunch?**
→ Check FINANCE_POLICIES.md > Meals section

**What's the vacation carryover policy?**
→ Check HR_POLICIES.md > Leave section

**Can I use personal laptop for work?**
→ Check IT_POLICIES.md > Devices section
```

**references/hr-policies.md:**
```markdown
# HR Policies

## Table of Contents
- [Leave](#leave)
- [Benefits](#benefits)
- [Conduct](#conduct)
- [Performance](#performance)

## Leave

### Vacation
- Full-time: 20 days/year
- Part-time: Prorated
- Carryover: Maximum 5 days to next year
- Approval: Manager approval required for >3 consecutive days

### Sick Leave
- Full-time: 10 days/year
- Doctor's note: Required for >3 consecutive days
- Payout: Unused days do not carry over

### Personal Days
- 3 days/year for personal matters
- Requires 24-hour notice

## Benefits
[details...]

## Conduct
[details...]

## Performance
[details...]
```

---

### Example 3: Complex Skill (Scripts, References, Assets)

**Task:** Financial report generation

**Directory Structure:**
```
financial-reporter/
├── SKILL.md
├── scripts/
│   ├── calculate_metrics.py
│   ├── validate_data.py
│   └── generate_charts.py
├── references/
│   ├── metrics.md (financial metrics definitions)
│   ├── accounting-standards.md (GAAP/IFRS)
│   └── chart-specs.md (visualization standards)
└── assets/
    └── templates/
        ├── quarterly-report.docx
        └── executive-summary.pptx
```

**SKILL.md:**
```yaml
---
name: financial-reporter
description: Generate financial reports including income statements, balance sheets, and cash flow statements with supporting charts and executive summaries. Supports quarterly, annual, and ad-hoc reporting following GAAP standards. Use when: creating financial statements, analyzing financial performance, generating board reports, or preparing investor communications.
---
```

```markdown
# Financial Reporter

## Quick Start

1. Validate input data: `python scripts/validate_data.py <data.csv>`
2. Calculate metrics: `python scripts/calculate_metrics.py <data.csv> --period <quarter|year>`
3. Generate charts: `python scripts/generate_charts.py <metrics.json> --template standard`
4. Create report using template: Use assets/templates/quarterly-report.docx

## Core Workflow

### Step 1: Data Validation

Ensure data completeness and accuracy:
```bash
python scripts/validate_data.py input.csv
```

Common issues and fixes:
- Missing dates: Check date format (YYYY-MM-DD)
- Negative values where unexpected: Verify debits/credits
- Rounding errors: Ensure consistent decimal places

### Step 2: Metric Calculation

Calculate required financial metrics:
```bash
python scripts/calculate_metrics.py input.csv --period Q1-2024
```

**Key metrics calculated:**
- Revenue, COGS, Gross Margin
- Operating Expenses, EBITDA
- Net Income, EPS
- YoY growth, QoQ growth

See [METRICS.md](references/metrics.md) for definitions.

### Step 3: Visualization

Generate standard charts:
```bash
python scripts/generate_charts.py metrics.json --output charts/
```

**Standard charts:**
- Revenue trend (line chart)
- Expense breakdown (pie chart)
- Margin comparison (bar chart)
- YoY growth (combo chart)

See [CHART_SPECS.md](references/chart-specs.md) for standards.

### Step 4: Report Assembly

Use templates in assets/templates/:
- quarterly-report.docx: Standard quarterly format
- executive-summary.pptx: Board presentation format

Fill in calculated metrics and insert charts.

## Advanced Features

### Custom Metrics

For non-standard metrics, see [METRICS.md](references/metrics.md#custom) for calculation methods.

### Comparative Analysis

Generate period-over-period comparisons:
```bash
python scripts/calculate_metrics.py current.csv --compare previous.csv
```

### Forecasting

Basic forecasting available:
```bash
python scripts/calculate_metrics.py data.csv --forecast 4
```
Forecasts next 4 quarters based on historical trend.

## Accounting Standards

This skill follows:
- US GAAP for US entities
- IFRS for international entities

See [ACCOUNTING_STANDARDS.md](references/accounting-standards.md) for details.

## Error Handling

If validation fails:
1. Check error message for specific issue
2. Verify data format matches expected schema
3. Consult [TROUBLESHOOTING.md](references/troubleshooting.md)

If metrics calculation fails:
1. Ensure data validation passed
2. Check for required columns
3. Verify period format

## Quality Checklist

Before finalizing:
- [ ] All validations pass
- [ ] Metrics match expectations
- [ ] Charts follow brand standards
- [ ] References cited correctly
- [ ] Accounting standards applied
- [ ] Peer review completed
```

---

## Appendix A: Decision Trees

### Resource Selection Decision Tree

```
Need to repeat code multiple times?
├─ YES → Use scripts/
│         ├─ Is code complex/fragile?
│         │   ├─ YES → scripts/ with error handling
│         │   └─ NO → scripts/ (simple is fine)
│         └─ Need user configuration?
│             ├─ YES → Add CLI arguments
│             └─ NO → Hardcode parameters
└─ NO → Need documentation references?
          ├─ YES → Use references/
          │         ├─ Large documentation?
          │         │   ├─ YES → Split by topic/domain
          │         │   └─ NO → Single reference file
          │         └─ Need TOC?
          │             ├─ >100 lines → Add TOC
          │             └─ <100 lines → Optional
          └─ NO → Need output files?
                    ├─ YES → Use assets/
                    │         ├─ Template to fill?
                    │         │   └─ assets/templates/
                    │         └─ Static files?
                    │             └─ assets/static/
                    └─ NO → Everything in SKILL.md
```

### Degrees of Freedom Decision Tree

```
How critical is exact procedure?
├─ High (safety, compliance, fragility)
│   └─ LOW FREEDOM
│       └─ Exact steps, scripts, validation
│
├─ Medium (preferred pattern exists)
│   └─ MEDIUM FREEDOM
│       └─ Workflows, pseudocode, parameters
│
└─ Low (many valid approaches)
    └─ HIGH FREEDOM
        └─ Guidelines, examples, heuristics
```

### Progressive Disclosure Decision Tree

```
Is information needed for EVERY use case?
├─ YES → Put in SKILL.md
└─ NO → Is it domain/variant specific?
          ├─ YES → Create separate reference files
          │         ├─ By domain?
          │         │   └─ references/domain-name.md
          │         └─ By variant?
          │             └─ references/variant-name.md
          └─ NO → Is it advanced/rarely used?
                    ├─ YES → Create advanced reference
                    │   └─ references/advanced.md
                    └─ NO → Consider if needed at all
```

---

## Appendix B: Frontmatter Examples

### Good Frontmatter Examples

**Example 1: Clear and Specific**
```yaml
---
name: docx-legal-documents
description: Professional legal document processing for contracts, NDAs, and agreements. Handles tracked changes, clause analysis, redline comparison, and legal terminology. Use when working with: (1) Contracts requiring review, (2) NDAs needing modification, (3) Legal document comparison, (4) Clause extraction and analysis, or any .docx files with legal content.
---
```

**Example 2: Comprehensive Trigger List**
```yaml
---
name: data-visualization
description: Create data visualizations including charts, graphs, and dashboards using Python matplotlib and seaborn. Supports statistical plots, time series analysis, and interactive visualizations. Use when users request: (1) "create a chart/graph", (2) "visualize this data", (3) "plot X vs Y", (4) "dashboard for [metrics]", (5) "show trends in [data]", or any data visualization task.
---
```

**Example 3: Domain-Focused**
```yaml
---
name: medical-report-analyzer
description: Analyze medical reports including lab results, radiology findings, and clinical notes. Extract key findings, flag abnormalities, and identify follow-up requirements. Use for: lab report interpretation, imaging analysis, clinical documentation review, and medical data summarization. Requires HIPAA-compliant handling of patient data.
---
```

### Poor Frontmatter Examples (and how to fix)

**Example 1: Too Vague**
```yaml
---
name: document-helper
description: This skill helps with documents.
---
```
**Fix:**
```yaml
---
name: document-helper
description: Document processing for PDFs and DOCX files including text extraction, formatting cleanup, and content reorganization. Use when: (1) Extracting text from PDFs, (2) Cleaning up document formatting, (3) Reorganizing document structure, or (4) Converting between document formats.
---
```

**Example 2: Too Specific**
```yaml
---
name: excel-processor
description: Processes Excel files from Q1 2024 financial reports in the accounting department to extract revenue figures in US dollars.
---
```
**Fix:**
```yaml
---
name: excel-processor
description: Process and analyze Excel files including data extraction, formula calculation, and format standardization. Supports financial reports, operational data, and analytical spreadsheets. Use when: (1) Extracting data from Excel, (2) Analyzing spreadsheet formulas, (3) Cleaning Excel data, or (4) Generating Excel reports from other data sources.
---
```

**Example 3: Missing Triggers**
```yaml
---
name: api-client
description: This skill provides API integration capabilities for various services.
---
```
**Fix:**
```yaml
---
name: api-client
description: API integration toolkit supporting REST and GraphQL APIs with authentication handling, rate limiting, and error retry logic. Use when: (1) Making HTTP requests to external APIs, (2) Handling OAuth/token authentication, (3) Processing API responses, (4) Implementing webhooks, or queries mention "connect to [service]", "API integration", "webhook", or "REST call".
---
```
