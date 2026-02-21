# Skill Sanitization Report

**Skill Name**: [skill-name]
**Skill Path**: [path/to/skill]
**Scan Date**: [YYYY-MM-DD HH:MM:SS]
**Sanitizer Version**: 1.0

---

## Executive Summary

**Status**: [CLEAN / QUESTIONABLE / SUSPICIOUS / MALICIOUS]

**Recommendation**: [ACCEPT / ACCEPT WITH CAUTION / INVESTIGATE / REJECT]

**Summary**: [1-2 sentence summary of findings]

---

## Deterministic Scan Results

### scan_unicode.py

**Status**: [PASS / FAIL]

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |

**Findings**:
```
[PASTE FINDINGS OR "No Unicode attacks detected"]
```

### scan_patterns.py

**Status**: [PASS / FAIL]

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |

**Findings**:
```
[PASTE FINDINGS OR "No prompt injection patterns detected"]
```

### scan_dependencies.py

**Status**: [PASS / FAIL]

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |

**Findings**:
```
[PASTE FINDINGS OR "No supply chain attacks detected"]
```

### scan_code_analysis.py

**Status**: [PASS / FAIL]

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |

**Findings**:
```
[PASTE FINDINGS OR "No dangerous code patterns detected"]
```

### Deterministic Summary

| Script | Status | Critical | High | Medium | Low |
|--------|--------|----------|------|--------|-----|
| scan_unicode.py | [PASS/FAIL] | [N] | [N] | [N] | [N] |
| scan_patterns.py | [PASS/FAIL] | [N] | [N] | [N] | [N] |
| scan_dependencies.py | [PASS/FAIL] | [N] | [N] | [N] | [N] |
| scan_code_analysis.py | [PASS/FAIL] | [N] | [N] | [N] | [N] |
| **TOTAL** | — | [N] | [N] | [N] | [N] |

---

## Probabilistic Analysis Results

*Performed when deterministic scans pass but suspicion remains, or when requested.*

### Described Behaviors

Extracted from skill description and body:

| Category | Described Behavior |
|----------|-------------------|
| **INPUT** | [What data it accepts, from where] |
| **OUTPUT** | [What it produces, where it goes] |
| **NETWORK** | [URLs/endpoints it claims to contact] |
| **FILES** | [Files it claims to read/write] |
| **EXECUTION** | [Scripts/code it claims to run] |
| **TARGETS** | [Intended recipients/destinations] |

### Actual Behaviors

Extracted from skill files:

| Category | Actual Behavior |
|----------|-----------------|
| **INPUT** | [What data it actually accepts] |
| **OUTPUT** | [What it actually produces] |
| **NETWORK** | [URLs/endpoints it actually contacts] |
| **FILES** | [Files it actually reads/writes] |
| **EXECUTION** | [Scripts/code it actually runs] |
| **TARGETS** | [Actual recipients/destinations] |

### Behavior-Description Alignment

| Behavior | Described | Actual | Status |
|----------|-----------|--------|--------|
| [Behavior 1] | ✓/✗ | ✓/✗ | [MATCH / VIOLATION] |
| [Behavior 2] | ✓/✗ | ✓/✗ | [MATCH / VIOLATION] |
| [Behavior 3] | ✓/✗ | ✓/✗ | [MATCH / VIOLATION] |

### Violations Found

| Severity | Category | Violation | Details |
|----------|----------|-----------|---------|
| [CRITICAL/HIGH/MEDIUM/LOW] | [Category] | [Description] | [File:line, context] |

---

## Deep Analysis

*Document findings from deep analysis techniques if performed.*

### Hidden Target Analysis

[Analysis of visible vs hidden targets, or "Not applicable"]

### Data Flow Analysis

[Analysis of data paths, or "Not applicable"]

### Semantic Instruction Analysis

[Analysis of creative language patterns, or "Not applicable"]

### Dependency Chain Analysis

[Analysis of dependency risks, or "Not applicable"]

### Time-Based/Conditional Analysis

[Analysis of time bombs or conditional attacks, or "Not applicable"]

---

## Final Determination

### Findings Summary

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |

### Status Criteria

| Status | Criteria |
|--------|----------|
| **MALICIOUS** | Any CRITICAL finding |
| **SUSPICIOUS** | Multiple HIGH findings or behavior-description violations |
| **QUESTIONABLE** | Any MEDIUM/LOW findings |
| **CLEAN** | No findings |

### Determination

**Status**: [MALICIOUS / SUSPICIOUS / QUESTIONABLE / CLEAN]

**Reasoning**: [Explain why this status was chosen]

### Recommendation

| Status | Recommendation |
|--------|----------------|
| **MALICIOUS** | REJECT - Do not use this skill |
| **SUSPICIOUS** | INVESTIGATE - Requires explanation before use |
| **QUESTIONABLE** | ACCEPT WITH CAUTION - Document and monitor |
| **CLEAN** | ACCEPT - Skill passes sanitization |

**Recommendation**: [REJECT / INVESTIGATE / ACCEPT WITH CAUTION / ACCEPT]

**Action Items**:
- [Action item 1, if any]
- [Action item 2, if any]

---

## Appendix: Skill Metadata

### Files Scanned

| File | Type | Size |
|------|------|------|
| [filename] | [type] | [size] |

### Dependencies

| Package | Version | Source |
|---------|---------|--------|
| [package name] | [version] | [npm/PyPI/git] |

### Skill Description

```
[PASTE SKILL DESCRIPTION FROM FRONTMATTER]
```

---

## Report Information

**Generated by**: skill-sanitizer v1.0
**Report Format**: Markdown
**Scan Duration**: [X seconds]

---

## Usage Notes

This report documents the security analysis of an AI agent skill. The skill was analyzed using:

1. **Deterministic scanning** - Pattern matching for known attack signatures
2. **Probabilistic analysis** - Semantic understanding for novel attacks
3. **Behavior-description alignment** - Verification that skill does exactly what it claims

For questions about this report or the skill-sanitizer, refer to the SKILL.md documentation.
