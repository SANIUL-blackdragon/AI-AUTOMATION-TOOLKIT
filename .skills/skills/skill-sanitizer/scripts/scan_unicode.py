#!/usr/bin/env python3
"""
scan_unicode.py - Detect Unicode and encoding attacks in skill files

Scans for:
- Zero-width characters (U+200B, U+200C, U+200D, U+FEFF)
- Unicode Tags Block (U+E0000-U+E007F) - completely invisible
- Homoglyph substitution (Cyrillic lookalikes)
- Bidirectional text override characters
- Non-printable control characters

Usage: python scan_unicode.py <skill-directory>
"""

import os
import sys
import unicodedata
from pathlib import Path
from typing import List, Tuple

# Severity levels
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

# Attack patterns from Attack Surface Report Section 11
ZERO_WIDTH_CHARS = {
    '\u200B': ('Zero Width Space', HIGH),
    '\u200C': ('Zero Width Non-Joiner', HIGH),
    '\u200D': ('Zero Width Joiner', HIGH),
    '\uFEFF': ('Byte Order Mark / Zero Width No-Break Space', MEDIUM),
}

# Unicode Tags Block (U+E0000-U+E007F) - completely invisible
TAGS_BLOCK_START = 0xE0000
TAGS_BLOCK_END = 0xE007F

# Bidirectional override characters
BIDI_CHARS = {
    '\u202A': ('Left-to-Right Embedding', CRITICAL),
    '\u202B': ('Right-to-Left Embedding', CRITICAL),
    '\u202C': ('Pop Directional Formatting', HIGH),
    '\u202D': ('Left-to-Right Override', CRITICAL),
    '\u202E': ('Right-to-Left Override', CRITICAL),
    '\u2066': ('Left-to-Right Isolate', HIGH),
    '\u2067': ('Right-to-Left Isolate', HIGH),
    '\u2068': ('First Strong Isolate', HIGH),
    '\u2069': ('Pop Directional Isolate', HIGH),
}

# Common homoglyphs (Cyrillic characters that look like Latin)
HOMOGLYPHS = {
    # Cyrillic lookalikes
    '\u0430': ('Cyrillic Small Letter A', 'a'),  # looks like 'a'
    '\u0435': ('Cyrillic Small Letter Ie', 'e'),  # looks like 'e'
    '\u043E': ('Cyrillic Small Letter O', 'o'),  # looks like 'o'
    '\u0440': ('Cyrillic Small Letter Er', 'p'),  # looks like 'p'
    '\u0441': ('Cyrillic Small Letter Es', 'c'),  # looks like 'c'
    '\u0443': ('Cyrillic Small Letter U', 'y'),  # looks like 'y'
    '\u0445': ('Cyrillic Small Letter Ha', 'x'),  # looks like 'x'
    '\u0456': ('Cyrillic Small Letter Byelorussian-Ukrainian I', 'i'),  # looks like 'i'
    '\u0458': ('Cyrillic Small Letter Je', 'j'),  # looks like 'j'
    '\u0410': ('Cyrillic Capital Letter A', 'A'),  # looks like 'A'
    '\u0412': ('Cyrillic Capital Letter Ve', 'B'),  # looks like 'B'
    '\u0415': ('Cyrillic Capital Letter Ie', 'E'),  # looks like 'E'
    '\u041A': ('Cyrillic Capital Letter Ka', 'K'),  # looks like 'K'
    '\u041C': ('Cyrillic Capital Letter Em', 'M'),  # looks like 'M'
    '\u041D': ('Cyrillic Capital Letter En', 'H'),  # looks like 'H'
    '\u041E': ('Cyrillic Capital Letter O', 'O'),  # looks like 'O'
    '\u0420': ('Cyrillic Capital Letter Er', 'P'),  # looks like 'P'
    '\u0421': ('Cyrillic Capital Letter Es', 'C'),  # looks like 'C'
    '\u0422': ('Cyrillic Capital Letter Te', 'T'),  # looks like 'T'
    '\u0425': ('Cyrillic Capital Letter Ha', 'X'),  # looks like 'X'
}

# Control characters that may be suspicious
SUSPICIOUS_CATEGORIES = ['Cc', 'Cf', 'Co', 'Cn']


def find_files(directory: Path) -> List[Path]:
    """Find all text-based files to scan."""
    extensions = {'.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.txt', '.sh', '.ps1'}
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f'*{ext}'))
    return files


def scan_file(filepath: Path) -> List[Tuple[str, str, int, str, str]]:
    """Scan a single file for Unicode attacks. Returns list of (severity, issue, line, context, description)."""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [(HIGH, f"Could not read file: {e}", 0, "", filepath.name)]

    # Check for zero-width characters
    for char, (name, severity) in ZERO_WIDTH_CHARS.items():
        if char in content:
            for i, line in enumerate(lines, 1):
                if char in line:
                    findings.append((severity, f"Invisible character: {name} (U+{ord(char):04X})", i, line[:80], filepath.name))

    # Check for Unicode Tags Block (completely invisible)
    for i, line in enumerate(lines, 1):
        for char in line:
            codepoint = ord(char)
            if TAGS_BLOCK_START <= codepoint <= TAGS_BLOCK_END:
                findings.append((CRITICAL, f"Unicode Tags Block character (U+{codepoint:04X}) - completely invisible", i, line[:80], filepath.name))

    # Check for bidirectional override characters
    for char, (name, severity) in BIDI_CHARS.items():
        if char in content:
            for i, line in enumerate(lines, 1):
                if char in line:
                    findings.append((severity, f"Bidirectional override: {name} (U+{ord(char):04X})", i, line[:80], filepath.name))

    # Check for homoglyphs (especially in package names, URLs, commands)
    for i, line in enumerate(lines, 1):
        for char in line:
            if char in HOMOGLYPHS:
                name, looks_like = HOMOGLYPHS[char]
                # Higher severity if in potentially dangerous context
                if any(kw in line.lower() for kw in ['import', 'from', 'package', 'require', 'url', 'http', 'git', 'npm', 'pip']):
                    findings.append((CRITICAL, f"Homoglyph in code context: '{char}' ({name}) looks like '{looks_like}'", i, line[:80], filepath.name))
                else:
                    findings.append((HIGH, f"Homoglyph: '{char}' ({name}) looks like '{looks_like}'", i, line[:80], filepath.name))

    # Check for suspicious control characters
    for i, line in enumerate(lines, 1):
        for char in line:
            category = unicodedata.category(char)
            if category in SUSPICIOUS_CATEGORIES:
                # Skip newlines, tabs, and common whitespace
                if char in '\n\r\t ':
                    continue
                codepoint = ord(char)
                if codepoint > 127:  # Only flag non-ASCII control chars
                    findings.append((MEDIUM, f"Suspicious control character: U+{codepoint:04X} ({unicodedata.name(char, 'Unknown')})", i, line[:80], filepath.name))

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_unicode.py <skill-directory>")
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

    # Sort by severity
    severity_order = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
    all_findings.sort(key=lambda x: severity_order.get(x[0], 4))

    # Output results
    if not all_findings:
        print("[PASS] No Unicode attacks detected")
        return 0

    for severity, issue, line, context, filename in all_findings:
        print(f"[{severity}] {filename}:{line} - {issue}")
        if context.strip():
            print(f"    Context: {context.strip()[:100]}")

    # Return non-zero if critical or high findings
    critical_count = sum(1 for f in all_findings if f[0] == CRITICAL)
    high_count = sum(1 for f in all_findings if f[0] == HIGH)

    if critical_count > 0 or high_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
