#!/usr/bin/env python3
"""
LaTeX Document Validator
Validates the syntax and structure of paper_definitivo.tex
"""

import re
import sys
from pathlib import Path

def validate_latex_file(filepath):
    """Validate basic LaTeX syntax and structure"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    warnings = []
    
    # Check for balanced braces
    if content.count('{') != content.count('}'):
        errors.append(f"Unbalanced braces: {content.count('{')} opening vs {content.count('}')} closing")
    
    # Check for balanced brackets
    if content.count('[') != content.count(']'):
        warnings.append(f"Unbalanced brackets: {content.count('[')} opening vs {content.count(']')} closing")
    
    # Check for required document structure
    required_commands = [
        r'\\documentclass',
        r'\\begin{document}',
        r'\\end{document}',
        r'\\title',
        r'\\author',
        r'\\maketitle'
    ]
    
    for cmd in required_commands:
        if not re.search(cmd, content):
            errors.append(f"Missing required command: {cmd}")
    
    # Check for balanced environments
    begin_envs = re.findall(r'\\begin\{(\w+)\}', content)
    end_envs = re.findall(r'\\end\{(\w+)\}', content)
    
    if len(begin_envs) != len(end_envs):
        errors.append(f"Unbalanced environments: {len(begin_envs)} begin vs {len(end_envs)} end")
    
    # Check for specific environments
    for env in set(begin_envs):
        if begin_envs.count(env) != end_envs.count(env):
            errors.append(f"Unbalanced environment '{env}': {begin_envs.count(env)} begin vs {end_envs.count(env)} end")
    
    # Check for figures
    figure_count = len(re.findall(r'\\begin\{figure\}', content))
    caption_count = len(re.findall(r'\\caption\{', content))
    
    if figure_count > 0:
        print(f"✓ Found {figure_count} figure(s)")
        if caption_count < figure_count:
            warnings.append(f"Some figures may be missing captions: {figure_count} figures, {caption_count} captions")
    
    # Check for tables
    table_count = len(re.findall(r'\\begin\{table\}', content))
    if table_count > 0:
        print(f"✓ Found {table_count} table(s)")
    
    # Check for equations
    equation_count = len(re.findall(r'\\begin\{equation\}', content))
    inline_math = len(re.findall(r'\$.*?\$', content))
    
    if equation_count > 0:
        print(f"✓ Found {equation_count} numbered equation(s)")
    if inline_math > 0:
        print(f"✓ Found {inline_math} inline math expression(s)")
    
    # Check for sections
    sections = re.findall(r'\\section\{([^}]+)\}', content)
    subsections = re.findall(r'\\subsection\{([^}]+)\}', content)
    
    print(f"✓ Found {len(sections)} section(s)")
    print(f"✓ Found {len(subsections)} subsection(s)")
    
    # Check for bibliography
    if r'\begin{thebibliography}' in content:
        bibitem_count = len(re.findall(r'\\bibitem\{', content))
        print(f"✓ Found bibliography with {bibitem_count} item(s)")
    
    # Check for abstract
    if r'\begin{abstract}' in content:
        print(f"✓ Found abstract")
    else:
        warnings.append("No abstract found")
    
    # Check for Spanish language
    if 'spanish' in content or 'babel' in content:
        print(f"✓ Spanish language support configured")
    
    # Report results
    print("\n" + "="*60)
    if not errors and not warnings:
        print("✅ Validation PASSED: No errors or warnings found")
        return 0
    
    if warnings:
        print(f"⚠️  {len(warnings)} warning(s) found:")
        for w in warnings:
            print(f"  - {w}")
    
    if errors:
        print(f"\n❌ {len(errors)} error(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    
    return 0

def main():
    """Main validation function"""
    print("LaTeX Document Validator")
    print("="*60)
    
    tex_file = Path(__file__).parent / "paper_definitivo.tex"
    
    if not tex_file.exists():
        print(f"❌ Error: File not found: {tex_file}")
        return 1
    
    print(f"Validating: {tex_file.name}\n")
    
    return validate_latex_file(tex_file)

if __name__ == "__main__":
    sys.exit(main())
