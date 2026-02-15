#!/usr/bin/env python3
"""
scan_patterns.py - Detect prompt injection and malicious instruction patterns

Scans for:
- Direct prompt injection ("ignore previous instructions", etc.)
- Jailbreak patterns (DAN, etc.)
- Instruction override attempts
- System prompt manipulation
- Hidden instruction patterns in markdown
- Tool poisoning patterns

Usage: python scan_patterns.py <skill-directory>
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Severity levels
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

# Attack patterns from Attack Surface Report Section 1 & 3
PROMPT_INJECTION_PATTERNS = [
    # Direct instruction override
    (r'ignore\s+(all\s+)?previous\s+instructions?', CRITICAL, "Direct prompt injection: instruction override"),
    (r'ignore\s+(all\s+)?prior\s+instructions?', CRITICAL, "Direct prompt injection: instruction override"),
    (r'disregard\s+(all\s+)?previous\s+instructions?', CRITICAL, "Direct prompt injection: instruction override"),
    (r'forget\s+(everything|all)', HIGH, "Instruction override attempt"),
    (r'you\s+are\s+now\s+(a|an)\s+\w+', CRITICAL, "Agent hijacking: role redefinition"),
    (r'new\s+role[:\s]', CRITICAL, "Agent hijacking: new role assignment"),
    (r'your\s+new\s+role\s+is', CRITICAL, "Agent hijacking: new role assignment"),

    # Jailbreak patterns
    (r'do\s+anything\s+now', CRITICAL, "DAN jailbreak pattern"),
    (r'dan\s*mode', CRITICAL, "DAN jailbreak pattern"),
    (r'jailbreak', CRITICAL, "Jailbreak keyword"),
    (r'enable\s+developer\s+mode', HIGH, "Developer mode bypass"),
    (r'enable\s+debug\s+mode', HIGH, "Debug mode bypass"),

    # System prompt manipulation
    (r'system\s*prompt', CRITICAL, "System prompt manipulation attempt"),
    (r'override\s+system', CRITICAL, "System override attempt"),
    (r'bypass\s+(the\s+)?(filter|safety|security)', CRITICAL, "Safety bypass attempt"),
    (r'disable\s+(the\s+)?(filter|safety|security)', CRITICAL, "Safety disable attempt"),

    # Instruction hierarchy violations
    (r'important:\s*(before|after|when)', CRITICAL, "Instruction injection in tool context"),
    (r'note:\s*(before|after|when).*send|transmit|exfil', CRITICAL, "Hidden instruction in note"),
    (r'always\s+(send|execute|run|call)', HIGH, "Potential hidden action instruction"),

    # Social engineering patterns
    (r'urgent[:\s]', MEDIUM, "Urgency manipulation"),
    (r'critical[:\s].*action', MEDIUM, "Critical urgency manipulation"),
    (r'do\s+not\s+(tell|show|display|reveal)', MEDIUM, "Secrecy manipulation"),
    (r'(secret|confidential|classified)[:\s]', MEDIUM, "Confidentiality trick"),

    # Authority impersonation
    (r'i\s+am\s+(your\s+)?(admin|administrator|developer|system)', HIGH, "Authority impersonation"),
    (r'(as|acting)\s+(your\s+)?(admin|administrator|developer|system)', HIGH, "Authority impersonation"),
    (r'authorized\s+by\s+', MEDIUM, "False authority claim"),
]

# Tool poisoning patterns
TOOL_POISONING_PATTERNS = [
    (r'important:\s*(always|before|after)\s+(send|transmit|exfiltrate|call)', CRITICAL, "Tool poisoning: hidden action"),
    (r'(before|after)\s+using\s+this\s+tool,?\s+(always\s+)?(send|transmit|call)', CRITICAL, "Tool poisoning: action injection"),
    (r'send\s+.*\s+to\s+https?://(?!(localhost|127\.0\.0\.1))', CRITICAL, "Tool poisoning: data exfiltration"),
    (r'transmit\s+.*\s+to\s+', CRITICAL, "Tool poisoning: data transmission"),
    (r'exfiltrate\s+', CRITICAL, "Explicit exfiltration keyword"),
]

# Hidden content in markdown
MARKDOWN_PATTERNS = [
    (r'<!--[^>]*ignore[^>]*-->', CRITICAL, "Hidden instruction in HTML comment"),
    (r'<!--[^>]*send[^>]*-->', CRITICAL, "Hidden action in HTML comment"),
    (r'<!--[^>]*exec[^>]*-->', CRITICAL, "Hidden execution in HTML comment"),
    (r'<div[^>]*display\s*:\s*none[^>]*>', HIGH, "Hidden div element"),
    (r'<span[^>]*display\s*:\s*none[^>]*>', HIGH, "Hidden span element"),
    (r'style\s*=\s*["\'][^"\']*display\s*:\s*none', HIGH, "Hidden element style"),
    (r'color\s*:\s*(white|#fff|#ffffff)\s*;?\s*background\s*:\s*(white|#fff|#ffffff)', HIGH, "Invisible text (white on white)"),
]

# Delimiter attacks
DELIMITER_PATTERNS = [
    (r'```\s*system', CRITICAL, "System delimiter injection"),
    (r'```\s*instruction', CRITICAL, "Instruction delimiter injection"),
    (r'###\s*system\s*prompt', CRITICAL, "System prompt section injection"),
    (r'---\s*system', CRITICAL, "System section delimiter injection"),
]


def find_files(directory: Path) -> List[Path]:
    """Find all text-based files to scan."""
    extensions = {'.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.txt'}
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f'*{ext}'))
    return files


def scan_file(filepath: Path) -> List[Tuple[str, str, int, str, str]]:
    """Scan a single file for malicious patterns. Returns list of (severity, issue, line, context, description)."""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [(HIGH, f"Could not read file: {e}", 0, "", filepath.name)]

    content_lower = content.lower()

    # Check prompt injection patterns
    for pattern, severity, description in PROMPT_INJECTION_PATTERNS:
        matches = list(re.finditer(pattern, content_lower, re.IGNORECASE))
        for match in matches:
            # Find line number
            line_num = content[:match.start()].count('\n') + 1
            context = lines[line_num - 1] if line_num <= len(lines) else ""
            findings.append((severity, description, line_num, context[:80], filepath.name))

    # Check tool poisoning patterns
    for pattern, severity, description in TOOL_POISONING_PATTERNS:
        matches = list(re.finditer(pattern, content_lower, re.IGNORECASE))
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            context = lines[line_num - 1] if line_num <= len(lines) else ""
            findings.append((severity, description, line_num, context[:80], filepath.name))

    # Check markdown patterns
    for pattern, severity, description in MARKDOWN_PATTERNS:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            context = lines[line_num - 1] if line_num <= len(lines) else ""
            findings.append((severity, description, line_num, context[:80], filepath.name))

    # Check delimiter patterns
    for pattern, severity, description in DELIMITER_PATTERNS:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            context = lines[line_num - 1] if line_num <= len(lines) else ""
            findings.append((severity, description, line_num, context[:80], filepath.name))

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_patterns.py <skill-directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    files = find_files(directory)

    all_findings = []
    for filepath in files:
        findings = scan_file(filepath)
        all_findings.extend(findings)

    # Deduplicate findings (same issue on same line)
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f[1], f[2], f[4])  # issue, line, filename
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by severity
    severity_order = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
    unique_findings.sort(key=lambda x: severity_order.get(x[0], 4))

    # Output results
    if not unique_findings:
        print("[PASS] No prompt injection patterns detected")
        return 0

    for severity, issue, line, context, filename in unique_findings:
        print(f"[{severity}] {filename}:{line} - {issue}")
        if context.strip():
            print(f"    Context: {context.strip()[:100]}")

    # Return non-zero if critical or high findings
    critical_count = sum(1 for f in unique_findings if f[0] == CRITICAL)
    high_count = sum(1 for f in unique_findings if f[0] == HIGH)

    if critical_count > 0 or high_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
