#!/usr/bin/env python3
"""
Security Test: Detect Accidentally Committed Tokens

This test scans the repository for patterns that match common API tokens
and secrets. It fails if any suspicious patterns are found, preventing
accidental token commits.

Usage:
    python tests/test_security_no_tokens.py
    pytest tests/test_security_no_tokens.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


# Patterns for common token formats
TOKEN_PATTERNS = {
    'huggingface': re.compile(r'hf_[A-Za-z0-9]{30,}'),
    'openai': re.compile(r'sk-[A-Za-z0-9]{32,}'),
    'anthropic': re.compile(r'sk-ant-[A-Za-z0-9]{32,}'),
    'github': re.compile(r'gh[pousr]_[A-Za-z0-9]{36,}'),
    'aws_access': re.compile(r'AKIA[0-9A-Z]{16}'),
    'generic_api': re.compile(r'api[_-]?key[_-]?[=:]\s*[\'"][A-Za-z0-9]{32,}[\'"]', re.IGNORECASE),
}

# Directories to skip
SKIP_DIRS = {
    '.git',
    '.github',
    'venv',
    '.venv',
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    'node_modules',
    'data',
    'results',
    'resultados',
    '.well-known',
}

# File extensions to check
CHECK_EXTENSIONS = {
    '.py',
    '.js',
    '.ts',
    '.sh',
    '.bash',
    '.yml',
    '.yaml',
    '.json',
    '.toml',
    '.cfg',
    '.ini',
    '.md',
    '.txt',
    '.env.example',  # Check example env files
}

# Files to always skip
SKIP_FILES = {
    '.env',  # Local env files (should be in .gitignore)
    '.env.local',
    'ENV.lock',  # May contain package hashes
    'requirements.txt',  # May contain hashes in comments
}

# Allowed patterns (false positives)
ALLOWED_PATTERNS = [
    r'hf_[X]{30,}',  # Example tokens with X's
    r'sk-[X]{32,}',  # Example tokens with X's
    r'your_token_here',
    r'your_key_here',
    r'your_api_key',
    r'example_token',
    r'test_token',
    r'dummy_token',
    r'placeholder',
]


def is_allowed_pattern(text: str) -> bool:
    """Check if the text matches any allowed pattern."""
    for pattern in ALLOWED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def scan_file(file_path: Path) -> List[Tuple[str, str, int]]:
    """
    Scan a file for token patterns.
    
    Returns:
        List of (token_type, matched_text, line_number) tuples
    """
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Skip lines that are clearly examples or documentation
                if is_allowed_pattern(line):
                    continue
                
                # Check each token pattern
                for token_type, pattern in TOKEN_PATTERNS.items():
                    matches = pattern.findall(line)
                    for match in matches:
                        findings.append((token_type, match, line_num))
    
    except (UnicodeDecodeError, PermissionError):
        # Skip files that can't be read
        pass
    
    return findings


def scan_repository(repo_root: Path) -> List[Tuple[Path, str, str, int]]:
    """
    Scan entire repository for tokens.
    
    Returns:
        List of (file_path, token_type, matched_text, line_number) tuples
    """
    all_findings = []
    
    for root, dirs, files in os.walk(repo_root):
        # Remove skip directories from traversal
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file_name in files:
            # Skip files by name
            if file_name in SKIP_FILES:
                continue
            
            # Check file extension
            file_path = Path(root) / file_name
            if file_path.suffix not in CHECK_EXTENSIONS and file_path.name not in CHECK_EXTENSIONS:
                continue
            
            # Skip this test file itself
            if file_path.name == 'test_security_no_tokens.py':
                continue
            
            # Scan the file
            findings = scan_file(file_path)
            for token_type, matched_text, line_num in findings:
                all_findings.append((file_path, token_type, matched_text, line_num))
    
    return all_findings


def test_no_tokens_in_repository():
    """Test that no API tokens are committed to the repository."""
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    # Scan repository
    findings = scan_repository(repo_root)
    
    # Report findings
    if findings:
        print("\n" + "=" * 80)
        print("❌ SECURITY ERROR: Detected potential API tokens in repository!")
        print("=" * 80)
        
        for file_path, token_type, matched_text, line_num in findings:
            rel_path = file_path.relative_to(repo_root)
            # Mask the token for security (show only first/last 4 chars if long enough)
            if len(matched_text) > 12:
                masked = f"{matched_text[:4]}...{matched_text[-4:]}"
            else:
                masked = "*" * len(matched_text)
            
            print(f"\n📄 File: {rel_path}")
            print(f"   Line: {line_num}")
            print(f"   Type: {token_type}")
            print(f"   Token: {masked}")
        
        print("\n" + "=" * 80)
        print("🔧 REMEDIATION STEPS:")
        print("=" * 80)
        print("1. Immediately revoke the exposed token(s) at the service provider")
        print("2. Generate new token(s) with appropriate scopes")
        print("3. Remove tokens from files and commit history:")
        print("   git filter-branch --force --index-filter \\")
        print("     'git rm --cached --ignore-unmatch <file>' \\")
        print("     --prune-empty --tag-name-filter cat -- --all")
        print("4. Store tokens securely:")
        print("   - Use environment variables: export HF_TOKEN=your_token")
        print("   - Use .env files (ensure .gitignore includes .env)")
        print("   - Use secret management services")
        print("\nSee SECURITY.md for detailed guidelines.")
        print("=" * 80 + "\n")
        
        assert False, f"Found {len(findings)} potential token(s) in repository. See output above."
    
    else:
        print("\n✅ PASS: No API tokens detected in repository")


def main():
    """Run the test as a standalone script."""
    try:
        test_no_tokens_in_repository()
        print("\n✅ All security checks passed!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Security check failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
