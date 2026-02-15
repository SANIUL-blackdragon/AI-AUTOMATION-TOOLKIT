Listen. I am not putting you in planning mode because you need to be able to see every file. But listen consider yourself in planning more. You need to create a plan to look through everything to make sure there is no fake like NPM library installs because there might be fake installs for libraries that do not exist. You need to make sure everything is fine so we don't get injections. Like no fake library installs, nothing fake should be present. Because skills dot MD is a Instructions file, right? We cannot allow it to do prompt injection in any way or create a attack surface. 
Well, you should also consider this is a skill file, right? So it will not itself have any malware, but it could tell the model to introduce new malware or download stuff that does not exist, which makes sure that we can get injected and stuff We should avoid those. So make sure those do not exist, like we do not want our skip files to exactly become an attack surface. 

Specifically this one. 

Do another thorough check just in case, and then we can sit tight And be relaxed. 

Would you say this specific one can be better? Like as a skill, can it be better? 

Also another agent gave me this checklist. See how these go well with the report and maybe implement in the report as well as to make the report better. 
# Security Audit Checklist

## 1. Package/Dependency Checks
- Verify all NPM packages exist on official registry (npmjs.com)
- Verify all PyPI packages exist on official registry (pypi.org)
- Check package download counts and popularity metrics
- Verify package publisher/organization legitimacy
- Check for typosquatting (misspelled package names)
- Check for dependency confusion (private vs public packages)
- Verify scoped packages (@org/package) belong to legitimate organizations
- Check for postinstall/preinstall script injection
- Verify package.json scripts don't contain malicious hooks
- Check requirements.txt for fake/malicious PyPI packages
- Verify no git+https:// URL installations
- Check for version pinning attacks (malicious specific versions)
- Verify extras/optional dependencies are legitimate

## 2. Prompt Injection Checks
- Search for "ignore previous instructions"
- Search for "ignore all" commands
- Search for "you are now" / "new role" patterns
- Search for "system prompt" manipulation
- Search for "override" commands
- Search for "disregard" / "forget everything"
- Search for DAN/jailbreak prompts
- Search for delimiter attacks (``` abuse)
- Search for hidden instructions in whitespace
- Check for role-playing tricks
- Check for instruction hierarchy violations
- Search for "as an AI" manipulation patterns

## 3. Invisible Character Checks
- Scan for zero-width spaces (U+200B)
- Scan for zero-width joiners (U+200D)
- Scan for zero-width non-joiners (U+200C)
- Scan for byte order marks (U+FEFF)
- Scan for bidirectional text overrides (RTLO characters)
- Scan for invisible Unicode control characters
- Check for homoglyph attacks (lookalike characters)
- Scan for non-printable ASCII characters
- Check for mixed RTL/LTR text directionality

## 4. Script Analysis (Python/JS)
- Check for eval() usage
- Check for exec() usage
- Check for new Function() constructor
- Check for compile() function
- Check for os.system() calls
- Check for subprocess with shell=True
- Check for dynamic code execution
- Verify no eval() with user input
- Check for import * (wildcard imports)
- Check for __import__() usage
- Check for pickle.loads() ( deserialization)
- Check for yaml.load() without SafeLoader
- Check for json.load() from untrusted sources
- Check for base64 decoding followed by execution
- Check for hex decoding followed by execution
- Verify no obfuscated code
- Check for bytecode manipulation
- Check for code self-modification
- Check for logic bombs (time-based triggers)
- Check for conditional malicious activation

## 5. Network/Communication Checks
- Check for requests.get() calls
- Check for requests.post() calls
- Check for urllib usage
- Check for http.client usage
- Check for socket connections
- Check for fetch() usage
- Check for XMLHttpRequest
- Check for axios or other HTTP libraries
- Verify no external API calls
- Check for DNS resolution attempts
- Check for WebSocket connections
- Check for FTP connections
- Verify localhost-only connections are safe

## 6. File System Checks
- Check for path traversal patterns (../, ..\\)
- Check for absolute path usage (/etc/, C:\)
- Check for file write operations
- Check for file deletion operations
- Check for directory creation outside project
- Check for symlinks/symbolic link usage
- Check for file permission changes (chmod)
- Check for reading sensitive files (~/.ssh, ~/.aws)
- Check for writing to system directories
- Check for hidden file creation
- Check for temporary file handling

## 7. Environment/Credential Checks
- Check for os.environ access
- Check for getenv() usage
- Search for API_KEY patterns
- Search for TOKEN patterns
- Search for SECRET patterns
- Search for PASSWORD patterns
- Search for PRIVATE_KEY patterns
- Check for credential file access (.env, credentials.json)
- Check for SSH key access
- Check for cloud provider credential access
- Check for hardcoded credentials

## 8. System Persistence Checks
- Check for .bashrc modifications
- Check for .zshrc modifications
- Check for .profile modifications
- Check for crontab entries
- Check for systemd service creation
- Check for launchctl (macOS) usage
- Check for Windows registry access
- Check for startup item creation
- Check for SSH authorized_keys modification
- Check for git hooks (pre-commit, post-checkout)
- Check for Docker container escape attempts

## 9. Data Exfiltration Checks
- Check for file upload mechanisms
- Check for data encoding (base64 before sending)
- Check for DNS exfiltration patterns
- Check for HTTP header injection
- Check for query parameter data leakage
- Check for clipboard access
- Check for browser localStorage/sessionStorage access
- Check for cookie theft
- Check for form data interception

## 10. Markdown/Documentation Checks
- Check for HTML comments (<!-- -->)
- Check for hidden markdown sections
- Check for YAML frontmatter injection
- Check for malicious description metadata
- Check for instruction injection in examples
- Check for hidden code blocks
- Check for links to malicious URLs
- Check for image-based attacks (data URIs)
- Check for embedded JavaScript in markdown
- Check for CSS injection

## 11. Template/Configuration Checks
- Check for template injection ({{ }})
- Check for malicious defaults in templates
- Check for YAML injection
- Check for JSON injection
- Check for XML external entity (XXE) attacks
- Check for configuration file manipulation
- Check for .gitignore manipulation
- Check for Dockerfile malicious base images
- Check for docker-compose volume mounts
- Check for CI/CD configuration attacks

## 12. Git-Based Checks
- Check for malicious git hooks
- Check for .gitmodules manipulation
- Check for git clone commands
- Check for git submodule initialization
- Check for git filter-branch usage
- Check for commit history rewriting
- Check for merge conflict injection

## 13. Encoding/Obfuscation Checks
- Check for base64 encoded strings
- Check for hex encoded strings (\x41\x42)
- Check for unicode escapes (\u0041)
- Check for URL encoding (%41)
- Check for HTML entity encoding
- Check for string concatenation evasion
- Check for minified/obfuscated code
- Check for bytecode files (.pyc)
- Check for compiled binary files

## 14. Time-Based/Logic Checks
- Check for datetime.now() comparisons
- Check for time.sleep() usage
- Check for while True loops
- Check for infinite recursion
- Check for resource exhaustion patterns
- Check for delayed activation (logic bombs)
- Check for date-based triggers
- Check for timezone manipulation

## 15. Social Engineering Checks
- Check for urgency keywords ("URGENT", "CRITICAL")
- Check for authority impersonation
- Check for "do not tell" patterns
- Check for confidentiality tricks ("SECRET")
- Check for "backdoor" mentions
- Check for false legitimacy claims
- Check for instruction override attempts
- Check for fear-based language

## 16. Supply Chain Checks
- Check for npm install commands
- Check for pip install commands
- Check for curl | bash patterns
- Check for wget | sh patterns
- Check for remote script execution
- Check for package manager configuration
- Check for lockfile manipulation
- Check for transitive dependency attacks

## 17. Container/Isolation Checks
- Check for Dockerfile presence
- Check for docker-compose.yml presence
- Check for privileged container flags
- Check for host path mounts
- Check for container escape attempts
- Check for .dockerignore manipulation

## 18. Binary/Executable Checks
- Check for .exe files
- Check for .dll files
- Check for .so files
- Check for .dylib files
- Check for compiled binaries
- Check for shell scripts (.sh)
- Check for PowerShell scripts (.ps1)
- Check for batch files (.bat)

## 19. XML/OOXML Specific Checks
- Check for XML external entity (XXE)
- Check for malicious XML schemas
- Check for Office macro injection
- Check for embedded objects
- Check for DTD manipulation
- Check for namespace confusion

## 20. Miscellaneous Checks
- Check for TODO/FIXME comments (verify legitimacy)
- Check for commented-out code
- Check for debug/backdoor accounts
- Check for test credentials
- Check for IP addresses in code
- Check for domain names in code
- Check for email addresses in code
- Check for phone numbers in code

---
