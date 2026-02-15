#!/usr/bin/env python3
"""
scan_code_analysis.py - Detect dangerous code patterns and code execution risks

Scans for:
- Dangerous functions (eval, exec, compile, etc.)
- Code execution patterns
- File system attacks (path traversal, sensitive file access)
- Network operations (data exfiltration patterns)
- Credential/environment access
- Obfuscation patterns
- Persistence mechanisms

Usage: python scan_code_analysis.py <skill-directory>
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

# Dangerous Python functions
DANGEROUS_PYTHON_PATTERNS = [
    # Code execution
    (r'\beval\s*\(', CRITICAL, "eval() - arbitrary code execution"),
    (r'\bexec\s*\(', CRITICAL, "exec() - arbitrary code execution"),
    (r'\bcompile\s*\(', HIGH, "compile() - code compilation"),
    (r'\b__import__\s*\(', CRITICAL, "__import__() - dynamic import"),
    (r'\bimportlib\.import_module', HIGH, "Dynamic import via importlib"),
    (r'\bimportlib\.__import__', HIGH, "Dynamic import via importlib"),

    # Subprocess with shell=True
    (r'\bsubprocess\.(call|run|Popen|check_output|check_call)\s*\([^)]*shell\s*=\s*True', CRITICAL, "subprocess with shell=True - command injection risk"),
    (r'\bos\.system\s*\(', CRITICAL, "os.system() - system command execution"),
    (r'\bos\.popen\s*\(', CRITICAL, "os.popen() - command execution"),
    (r'\bos\.spawn', HIGH, "os.spawn* - process spawning"),
    (r'\bcommands\.getoutput', CRITICAL, "commands.getoutput - deprecated command execution"),
    (r'\bcommands\.getstatusoutput', CRITICAL, "commands.getstatusoutput - deprecated command execution"),

    # Deserialization
    (r'\bpickle\.loads?\s*\(', CRITICAL, "pickle.load(s) - deserialization attack"),
    (r'\byaml\.load\s*\([^)]*\)', CRITICAL, "yaml.load() - deserialization attack (use yaml.safe_load)"),
    (r'\bmarshal\.loads?\s*\(', HIGH, "marshal.load(s) - deserialization"),
    (r'\bshelve\.open', MEDIUM, "shelve.open - potential deserialization"),

    # Dynamic code patterns
    (r'\bgetattr\s*\(\s*\w+\s*,\s*[^)]*\+', HIGH, "getattr with dynamic attribute - potential RCE"),
    (r'\bsetattr\s*\(\s*\w+\s*,\s*[^)]*\+', HIGH, "setattr with dynamic attribute"),
    (r'\bdelattr\s*\(', MEDIUM, "delattr - attribute manipulation"),
    (r'\bglobals\s*\(\)', MEDIUM, "globals() - access to global namespace"),
    (r'\blocals\s*\(\)', MEDIUM, "locals() - access to local namespace"),
    (r'\bvars\s*\(\)', MEDIUM, "vars() - access to object namespace"),
    (r'\bdir\s*\(\)', LOW, "dir() - namespace inspection"),

    # File operations
    (r'\bopen\s*\([^)]*\.\./', CRITICAL, "Path traversal in open()"),
    (r'\bopen\s*\([^)]*/etc/', CRITICAL, "Access to /etc/ - system files"),
    (r'\bopen\s*\([^)]*\.ssh/', CRITICAL, "Access to .ssh/ - SSH keys"),
    (r'\bopen\s*\([^)]*\.aws/', CRITICAL, "Access to .aws/ - AWS credentials"),
    (r'\bopen\s*\([^)]*\.env', HIGH, "Access to .env file"),
    (r'\bopen\s*\([^)]*credentials', CRITICAL, "Access to credentials file"),
    (r'\bopen\s*\([^)]*password', CRITICAL, "Access to password file"),
    (r'\bshutil\.rmtree', HIGH, "shutil.rmtree - recursive directory deletion"),
    (r'\bos\.remove\s*\(', HIGH, "os.remove() - file deletion"),
    (r'\bos\.unlink\s*\(', HIGH, "os.unlink() - file deletion"),
    (r'\bos\.rename\s*\(', MEDIUM, "os.rename() - file manipulation"),
    (r'\bos\.makedirs', MEDIUM, "os.makedirs - directory creation"),
    (r'\bPath\s*\.\s*mkdir', MEDIUM, "Path.mkdir - directory creation"),

    # Network operations
    (r'\brequests\.(get|post|put|delete|patch)\s*\(', HIGH, "HTTP request - potential data exfiltration"),
    (r'\burllib\.request\.urlopen', HIGH, "urllib request - potential data exfiltration"),
    (r'\bhttp\.client\.', MEDIUM, "HTTP client usage"),
    (r'\bsocket\.socket', CRITICAL, "Raw socket - potential C2/exfiltration"),
    (r'\bsocket\.connect', CRITICAL, "Socket connect - potential C2/exfiltration"),
    (r'\bWebSocket', MEDIUM, "WebSocket usage - real-time data channel"),
    (r'\bftplib\.', MEDIUM, "FTP client - file transfer"),
    (r'\bsmtplib\.', MEDIUM, "SMTP client - email sending"),

    # Environment/credentials
    (r'\bos\.environ', CRITICAL, "os.environ access - environment variable access"),
    (r'\bos\.getenv\s*\(', CRITICAL, "os.getenv() - environment variable access"),
    (r'\bgetenv\s*\(', CRITICAL, "getenv() - environment variable access"),
    (r'\benviron\.get', CRITICAL, "environ.get - environment variable access"),
    (r'\bAPI[_-]?KEY', CRITICAL, "API_KEY reference"),
    (r'\bSECRET[_-]?KEY', CRITICAL, "SECRET_KEY reference"),
    (r'\bACCESS[_-]?TOKEN', CRITICAL, "ACCESS_TOKEN reference"),
    (r'\bPRIVATE[_-]?KEY', CRITICAL, "PRIVATE_KEY reference"),
    (r'\bPASSWORD', CRITICAL, "PASSWORD reference"),
    (r'\bAUTH_TOKEN', CRITICAL, "AUTH_TOKEN reference"),

    # Persistence
    (r'\.bashrc', CRITICAL, ".bashrc modification - shell persistence"),
    (r'\.zshrc', CRITICAL, ".zshrc modification - shell persistence"),
    (r'\.profile', CRITICAL, ".profile modification - login persistence"),
    (r'crontab', CRITICAL, "crontab access - scheduled task persistence"),
    (r'/etc/systemd/', CRITICAL, "systemd service - service persistence"),
    (r'launchctl', CRITICAL, "launchctl - macOS persistence"),
    (r'authorized_keys', CRITICAL, "authorized_keys - SSH persistence"),
    (r'\.git/hooks/', HIGH, "Git hooks - development persistence"),

    # Obfuscation
    (r'\bbase64\.b64decode', HIGH, "base64.b64decode - potential obfuscation"),
    (r'\bbase64\.decode', HIGH, "base64 decode - potential obfuscation"),
    (r'\bcodecs\.decode', MEDIUM, "codecs.decode - potential obfuscation"),
    (r'\\x[0-9a-fA-F]{2}', MEDIUM, "Hex escape sequence - potential obfuscation"),
    (r'\\u[0-9a-fA-F]{4}', MEDIUM, "Unicode escape - potential obfuscation"),
    (r'chr\s*\(\s*\d+\s*\)', HIGH, "chr() with numbers - character obfuscation"),
]

# Dangerous JavaScript/TypeScript patterns
DANGEROUS_JS_PATTERNS = [
    # Code execution
    (r'\beval\s*\(', CRITICAL, "eval() - arbitrary code execution"),
    (r'\bFunction\s*\(', CRITICAL, "Function constructor - arbitrary code execution"),
    (r'\bnew\s+Function\s*\(', CRITICAL, "new Function() - arbitrary code execution"),
    (r'\bsetTimeout\s*\(\s*["\'`]', HIGH, "setTimeout with string - code execution"),
    (r'\bsetInterval\s*\(\s*["\'`]', HIGH, "setInterval with string - code execution"),
    (r'\bvm\.(run|compile)', CRITICAL, "vm module - code execution in Node.js"),
    (r'\bchild_process\.(exec|spawn|execSync|spawnSync)', CRITICAL, "child_process - command execution"),
    (r'\brequire\s*\(\s*["\'`]child_process', HIGH, "child_process import"),

    # File system (Node.js)
    (r'\bfs\.(readFile|writeFile|appendFile|unlink|rmdir|mkdir)', HIGH, "fs.* - file system operation"),
    (r'\bfs\.(readFileSync|writeFileSync|appendFileSync|unlinkSync|rmdirSync|mkdirSync)', HIGH, "fs.*Sync - file system operation"),
    (r'\bfs\.promises\.', HIGH, "fs.promises - file system operation"),
    (r'\bpath\.join\s*\([^)]*\.\.', CRITICAL, "Path traversal via path.join"),
    (r'\b__dirname\s*\+', HIGH, "__dirname concatenation - path traversal risk"),
    (r'\b__filename\s*\+', HIGH, "__filename concatenation - path traversal risk"),

    # Network
    (r'\bfetch\s*\(', HIGH, "fetch() - HTTP request"),
    (r'\baxios\.', HIGH, "axios - HTTP request"),
    (r'\bhttp\.request', HIGH, "http.request - HTTP request"),
    (r'\bhttps\.request', HIGH, "https.request - HTTP request"),
    (r'\bWebSocket', MEDIUM, "WebSocket - real-time data channel"),
    (r'\bnet\.connect', CRITICAL, "net.connect - raw socket"),
    (r'\bdgram\.', CRITICAL, "dgram - UDP socket"),

    # Process/environment
    (r'\bprocess\.env', CRITICAL, "process.env - environment variable access"),
    (r'\bprocess\.exit', MEDIUM, "process.exit - process termination"),
    (r'\bprocess\.cwd', LOW, "process.cwd - current directory"),

    # Obfuscation
    (r'\batob\s*\(', HIGH, "atob() - base64 decode"),
    (r'\bbtoa\s*\(', MEDIUM, "btoa() - base64 encode"),
    (r'\bBuffer\.from\s*\([^)]*,\s*["\'`]base64', HIGH, "Buffer base64 decode"),
]

# Dangerous shell patterns
DANGEROUS_SHELL_PATTERNS = [
    (r'rm\s+-rf', CRITICAL, "rm -rf - force recursive deletion"),
    (r'shred', HIGH, "shred - secure file deletion"),
    (r'chmod\s+[0-7]{3,4}', MEDIUM, "chmod - permission change"),
    (r'chown\s+', MEDIUM, "chown - ownership change"),
    (r'>\s*/etc/', CRITICAL, "Write to /etc/ - system modification"),
    (r'>\s*~/.', CRITICAL, "Write to home directory - persistence"),
    (r'curl\s+.*\|\s*(ba)?sh', CRITICAL, "curl | sh - remote script execution"),
    (r'wget\s+.*\|\s*(ba)?sh', CRITICAL, "wget | sh - remote script execution"),
    (r'eval\s+', CRITICAL, "eval - command execution"),
    (r'exec\s+', CRITICAL, "exec - command execution"),
    (r'source\s+', MEDIUM, "source - script execution"),
    (r'\$\(', HIGH, "$() - command substitution"),
    (r'`[^`]+`', HIGH, "Backticks - command substitution"),
]


def find_code_files(directory: Path) -> List[Path]:
    """Find all code files to scan."""
    extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash', '.zsh', '.ps1'}
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f'*{ext}'))
    return files


def scan_file(filepath: Path) -> List[Tuple[str, str, int, str, str]]:
    """Scan a single file for dangerous code patterns."""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [(HIGH, f"Could not read file: {e}", 0, "", filepath.name)]

    # Select patterns based on file type
    patterns = []
    if filepath.suffix == '.py':
        patterns = DANGEROUS_PYTHON_PATTERNS
    elif filepath.suffix in {'.js', '.ts', '.jsx', '.tsx'}:
        patterns = DANGEROUS_JS_PATTERNS
    elif filepath.suffix in {'.sh', '.bash', '.zsh'}:
        patterns = DANGEROUS_SHELL_PATTERNS
    else:
        # For other files, check all patterns
        patterns = DANGEROUS_PYTHON_PATTERNS + DANGEROUS_JS_PATTERNS + DANGEROUS_SHELL_PATTERNS

    for pattern, severity, description in patterns:
        try:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                context = lines[line_num - 1] if line_num <= len(lines) else ""
                findings.append((severity, description, line_num, context[:80], filepath.name))
        except re.error:
            continue

    return findings


def check_for_obfuscated_content(filepath: Path) -> List[Tuple[str, str, int, str, str]]:
    """Check for signs of obfuscated or encoded content."""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception:
        return findings

    # Check for very long lines (minified/obfuscated)
    for i, line in enumerate(lines, 1):
        if len(line) > 500:
            findings.append((MEDIUM, f"Very long line ({len(line)} chars) - possibly obfuscated", i, line[:80], filepath.name))

    # Check for unusual character density
    for i, line in enumerate(lines, 1):
        if len(line) > 50:
            # Count non-alphanumeric, non-whitespace characters
            special = sum(1 for c in line if not c.isalnum() and not c.isspace())
            if special / len(line) > 0.5:
                findings.append((MEDIUM, "High special character density - possibly obfuscated", i, line[:80], filepath.name))

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_code_analysis.py <skill-directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    files = find_code_files(directory)

    all_findings = []
    for filepath in files:
        findings = scan_file(filepath)
        all_findings.extend(findings)

        # Check for obfuscation
        obf_findings = check_for_obfuscated_content(filepath)
        all_findings.extend(obf_findings)

    # Deduplicate findings
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f[1], f[2], f[4])  # issue, line, filename
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by severity
    severity_order = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
    unique_findings.sort(key=lambda x: (severity_order.get(x[0], 4), x[4], x[2]))

    # Output results
    if not unique_findings:
        print("[PASS] No dangerous code patterns detected")
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
