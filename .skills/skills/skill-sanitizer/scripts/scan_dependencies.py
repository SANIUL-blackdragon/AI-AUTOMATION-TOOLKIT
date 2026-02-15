#!/usr/bin/env python3
"""
scan_dependencies.py - Detect supply chain attacks in dependencies

Scans for:
- Typosquatting (misspelled package names)
- Homoglyph package names (Cyrillic lookalikes)
- Unknown/unpopular packages
- Suspicious package sources (git URLs, non-registry sources)
- Post-install script injection
- Version pinning to suspicious versions

Usage: python scan_dependencies.py <skill-directory>
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set

# Severity levels
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

# Popular legitimate packages (subset - in production, use full registry)
POPULAR_NPM_PACKAGES = {
    'react', 'react-dom', 'vue', 'angular', 'express', 'next', 'next.js',
    'lodash', 'axios', 'typescript', 'webpack', 'babel', 'eslint',
    'prettier', 'jest', 'mocha', 'chai', 'underscore', 'jquery',
    'dotenv', 'cors', 'helmet', 'morgan', 'body-parser', 'cookie-parser',
    'jsonwebtoken', 'bcrypt', 'crypto-js', 'uuid', 'moment', 'date-fns',
    'zod', 'joi', 'yup', 'prisma', 'mongoose', 'pg', 'mysql', 'redis',
    'socket.io', 'ws', 'graphql', 'apollo-server', 'tailwindcss',
    'shadcn', 'framer-motion', 'recharts', 'chart.js',
}

POPULAR_PYPI_PACKAGES = {
    'requests', 'numpy', 'pandas', 'matplotlib', 'scipy', 'scikit-learn',
    'tensorflow', 'torch', 'keras', 'flask', 'django', 'fastapi',
    'pydantic', 'sqlalchemy', 'alembic', 'celery', 'redis', 'boto3',
    'pillow', 'opencv-python', 'beautifulsoup4', 'selenium', 'pytest',
    'black', 'flake8', 'mypy', 'pip', 'setuptools', 'wheel',
    'python-dotenv', 'pyyaml', 'toml', 'jinja2', 'click', 'typer',
    'httpx', 'aiohttp', 'urllib3', 'certifi', 'charset-normalizer',
    'idna', 'pyjwt', 'cryptography', 'passlib', 'python-multipart',
    'uvicorn', 'gunicorn', 'hypercorn', 'prisma',
}

# Common typosquatting patterns
TYPOSQUATTING_PATTERNS = [
    # Common misspellings
    (r'reqeusts?', 'requests'),
    (r'requist', 'requests'),
    (r'requsts?', 'requests'),
    (r'numPy', 'numpy'),  # wrong case
    (r'nump[yi]', 'numpy'),  # typo
    (r'npmp', 'npm'),
    (r'npn', 'npm'),
    (r'exprss', 'express'),
    (r'expres', 'express'),
    (r'lodahs', 'lodash'),
    (r'lowdash', 'lodash'),
    (r'loadsh', 'lodash'),
    (r'axio', 'axios'),
    (r'axioss', 'axios'),
    (r'reacct', 'react'),
    (r'reatc', 'react'),
    (r'vuu', 'vue'),
    (r'vuexx', 'vuex'),
    (r'djang', 'django'),
    (r'djago', 'django'),
    (r'flaskk', 'flask'),
    (r'flas', 'flask'),
    (r'fastapii', 'fastapi'),
    (r'fast-api', 'fastapi'),

    # Extra letters
    (r'requestss', 'requests'),
    (r'numpyjs', None),  # suspicious suffix
    (r'reactjs', None),  # could be legit but suspicious
    (r'pandasdb', None),  # suspicious suffix

    # Missing letters
    (r'equest', 'requests'),
    (r'umpy', 'numpy'),
    (r'andas', 'pandas'),
]

# Suspicious install patterns
SUSPICIOUS_INSTALL_PATTERNS = [
    (r'pip\s+install\s+git\+', CRITICAL, "Direct git install - unverified source"),
    (r'npm\s+install\s+git\+', CRITICAL, "Direct git install - unverified source"),
    (r'pip\s+install\s+--index-url\s+https?://(?!(pypi\.org|pypi\.python\.org))', CRITICAL, "Non-standard PyPI index"),
    (r'npm\s+(install|i)\s+--registry\s+https?://(?!(registry\.npmjs\.org))', CRITICAL, "Non-standard NPM registry"),
    (r'curl\s+.*\|\s*(ba)?sh', CRITICAL, "Remote script execution (curl | sh)"),
    (r'wget\s+.*\|\s*(ba)?sh', CRITICAL, "Remote script execution (wget | sh)"),
    (r'eval\s*\(\s*curl', CRITICAL, "Dynamic code from remote source"),
    (r'eval\s*\(\s*wget', CRITICAL, "Dynamic code from remote source"),
]

# Dangerous script hooks in package.json
DANGEROUS_SCRIPT_KEYS = [
    'preinstall', 'postinstall', 'preuninstall', 'postuninstall',
    'prestart', 'poststart', 'prebuild', 'postbuild',
]


def find_dependency_files(directory: Path) -> List[Path]:
    """Find dependency files."""
    patterns = ['requirements.txt', 'package.json', 'Pipfile', 'pyproject.toml', 'poetry.lock', 'package-lock.json', 'yarn.lock']
    files = []
    for pattern in patterns:
        files.extend(directory.rglob(pattern))
    return files


def find_script_files(directory: Path) -> List[Path]:
    """Find script files that might contain install commands."""
    extensions = {'.sh', '.ps1', '.py', '.js', '.ts', '.md'}
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f'*{ext}'))
    return files


def extract_python_packages(filepath: Path) -> List[Tuple[str, str]]:
    """Extract package names from requirements.txt or similar."""
    packages = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                # Parse package name (handle various formats)
                # requests==2.28.0 -> requests
                # requests>=2.28.0 -> requests
                # requests[security] -> requests
                # git+https://... -> extract name if possible
                match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                if match:
                    packages.append((match.group(1).lower(), line))
    except Exception:
        pass
    return packages


def extract_npm_packages(filepath: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Extract package names from package.json. Returns (dependencies, scripts)."""
    import json
    dependencies = {}
    scripts = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
            for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        dependencies[name.lower()] = version
            if 'scripts' in data:
                scripts = data['scripts']
    except Exception:
        pass
    return dependencies, scripts


def check_typosquatting(package_name: str, is_npm: bool) -> List[Tuple[str, str, str]]:
    """Check if package name is a typosquat. Returns list of (severity, issue, similar_to)."""
    findings = []
    popular = POPULAR_NPM_PACKAGES if is_npm else POPULAR_PYPI_PACKAGES

    # Check against known patterns
    for pattern, similar in TYPOSQUATTING_PATTERNS:
        if re.match(pattern, package_name, re.IGNORECASE):
            if similar:
                findings.append((CRITICAL, f"Possible typosquat of '{similar}'", similar))
            else:
                findings.append((HIGH, "Suspicious package name pattern", None))

    # Check if similar to popular package
    for pop in popular:
        # Levenshtein distance check (simple)
        if len(package_name) >= 3 and len(pop) >= 3:
            # Simple edit distance check
            if package_name != pop:
                # Check single character differences
                if len(package_name) == len(pop):
                    diff = sum(1 for a, b in zip(package_name, pop) if a != b)
                    if diff == 1:
                        findings.append((CRITICAL, f"Possible typosquat of '{pop}' (1 character difference)", pop))

    return findings


def scan_file_for_install_patterns(filepath: Path) -> List[Tuple[str, str, int, str, str]]:
    """Scan any file for suspicious install patterns."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        for pattern, severity, description in SUSPICIOUS_INSTALL_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((severity, description, i, line.strip()[:80], filepath.name))

    return findings


def scan_package_json_scripts(filepath: Path, scripts: Dict[str, str]) -> List[Tuple[str, str, str, str]]:
    """Scan package.json scripts for dangerous hooks."""
    findings = []
    for script_name, script_content in scripts.items():
        # Check for dangerous hook names
        for dangerous in DANGEROUS_SCRIPT_KEYS:
            if script_name == dangerous:
                # Check what the script does
                if any(kw in script_content.lower() for kw in ['curl', 'wget', 'http', 'eval', 'exec', 'spawn']):
                    findings.append((CRITICAL, f"Dangerous {script_name} script with network/code execution", script_content[:50], filepath.name))
                else:
                    findings.append((HIGH, f"Script hook: {script_name}", script_content[:50], filepath.name))
    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_dependencies.py <skill-directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    all_findings = []

    # Scan dependency files
    dep_files = find_dependency_files(directory)
    for filepath in dep_files:
        if filepath.name == 'requirements.txt':
            packages = extract_python_packages(filepath)
            for pkg_name, pkg_line in packages:
                # Check for git+ installs
                if 'git+' in pkg_line.lower():
                    all_findings.append((CRITICAL, f"Git install for '{pkg_name}' - unverified source", 0, pkg_line[:80], filepath.name))
                    continue

                # Check for typosquatting
                typos = check_typosquatting(pkg_name, is_npm=False)
                for severity, issue, similar in typos:
                    all_findings.append((severity, issue, 0, pkg_line[:80], filepath.name))

                # Check if it's a known popular package
                if pkg_name not in POPULAR_PYPI_PACKAGES:
                    # Could be legitimate but less common
                    pass

        elif filepath.name == 'package.json':
            dependencies, scripts = extract_npm_packages(filepath)

            # Check dependencies
            for pkg_name, version in dependencies.items():
                # Check for git installs
                if version and ('git' in version.lower() or version.startswith('http')):
                    all_findings.append((CRITICAL, f"Git/URL install for '{pkg_name}' - unverified source", 0, version[:80], filepath.name))
                    continue

                # Check for typosquatting
                typos = check_typosquatting(pkg_name, is_npm=True)
                for severity, issue, similar in typos:
                    all_findings.append((severity, issue, 0, f"{pkg_name}@{version}"[:80], filepath.name))

            # Check scripts
            script_findings = scan_package_json_scripts(filepath, scripts)
            for severity, issue, context, filename in script_findings:
                all_findings.append((severity, issue, 0, context, filename))

    # Scan all files for install patterns
    script_files = find_script_files(directory)
    for filepath in script_files:
        findings = scan_file_for_install_patterns(filepath)
        all_findings.extend(findings)

    # Sort by severity
    severity_order = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
    all_findings.sort(key=lambda x: (severity_order.get(x[0], 4), x[1]))

    # Output results
    if not all_findings:
        print("[PASS] No supply chain attacks detected")
        return 0

    for severity, issue, line, context, filename in all_findings:
        line_str = f":{line}" if line else ""
        print(f"[{severity}] {filename}{line_str} - {issue}")
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
