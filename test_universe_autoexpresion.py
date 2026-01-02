#!/usr/bin/env python3
"""
Test script for Universe Self-Expression implementation.

This script verifies that:
1. The new UniversalStructureOrchestrator works correctly
2. Backward compatibility with FrameworkOrchestrator is maintained
3. The philosophical concepts are properly documented
"""

import sys
import os

# Add src to path - correct path to the src module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that both new and old names can be imported."""
    print("Testing imports...")
    
    from src.frameworks import (
        UniversalStructureOrchestrator,
        FrameworkOrchestrator
    )
    
    print("✓ Both UniversalStructureOrchestrator and FrameworkOrchestrator imported")
    
    # Test that they are the same class
    assert UniversalStructureOrchestrator == FrameworkOrchestrator, \
        "FrameworkOrchestrator should be an alias to UniversalStructureOrchestrator"
    
    print("✓ FrameworkOrchestrator is correctly aliased to UniversalStructureOrchestrator")
    
    return True

def test_backward_compatibility():
    """Test that old code using FrameworkOrchestrator still works."""
    print("\nTesting backward compatibility...")
    
    from src.frameworks import FrameworkOrchestrator
    
    # This is how old code would use it
    orchestrator = FrameworkOrchestrator(precision=50)
    
    # Old code expects .frameworks attribute
    assert hasattr(orchestrator, 'frameworks'), \
        "orchestrator should have 'frameworks' attribute"
    
    frameworks = orchestrator.frameworks
    assert len(frameworks) == 5, \
        f"Expected 5 frameworks, got {len(frameworks)}"
    
    print(f"✓ orchestrator.frameworks exists with {len(frameworks)} entries")
    
    # Old code expects validation to return 'all_frameworks_valid'
    validation = orchestrator.validate_all_frameworks()
    assert 'overall' in validation, \
        "validation should have 'overall' key"
    assert 'all_frameworks_valid' in validation['overall'], \
        "validation['overall'] should have 'all_frameworks_valid' key"
    
    print("✓ validate_all_frameworks() returns expected structure")
    
    return True

def test_new_features():
    """Test new philosophical features."""
    print("\nTesting new philosophical features...")
    
    from src.frameworks import UniversalStructureOrchestrator
    
    orchestrator = UniversalStructureOrchestrator(precision=50)
    
    # New code uses .expressions attribute
    assert hasattr(orchestrator, 'expressions'), \
        "orchestrator should have 'expressions' attribute"
    
    expressions = orchestrator.expressions
    assert len(expressions) == 5, \
        f"Expected 5 expressions, got {len(expressions)}"
    
    # Check that expressions have 'aspect' field
    for key, info in expressions.items():
        assert 'aspect' in info, \
            f"Expression {key} should have 'aspect' field"
    
    print(f"✓ orchestrator.expressions exists with {len(expressions)} entries")
    print("✓ All expressions have 'aspect' field describing their mathematical domain")
    
    # Check validation returns new keys
    validation = orchestrator.validate_all_frameworks()
    assert 'all_expressions_consistent' in validation['overall'], \
        "validation['overall'] should have 'all_expressions_consistent' key"
    
    print("✓ validate_all_frameworks() returns new 'all_expressions_consistent' key")
    
    # Check for philosophical interpretation
    if 'interpretation' in validation['overall']:
        print(f"✓ Philosophical interpretation included: '{validation['overall']['interpretation'][:50]}...'")
    
    return True

def test_documentation():
    """Test that documentation files exist."""
    print("\nTesting documentation...")
    
    # Get the repository root directory
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    docs = [
        'UNIVERSO_AUTOEXPRESION.md',
        'MANIFIESTO_REVOLUCION_NOESICA.md',
        'README.md'
    ]
    
    for doc in docs:
        path = os.path.join(repo_root, doc)
        assert os.path.exists(path), f"Documentation file {doc} should exist"
        print(f"✓ {doc} exists")
    
    # Check UNIVERSO_AUTOEXPRESION.md has key content
    universo_path = os.path.join(repo_root, 'UNIVERSO_AUTOEXPRESION.md')
    with open(universo_path, 'r') as f:
        content = f.read()
        assert 'universo expresándose' in content.lower(), \
            "UNIVERSO_AUTOEXPRESION.md should contain key phrase"
        assert 'marco externo' in content.lower(), \
            "UNIVERSO_AUTOEXPRESION.md should discuss external framework"
        print("✓ UNIVERSO_AUTOEXPRESION.md contains key philosophical concepts")
    
    return True

def main():
    """Run all tests."""
    print("=" * 70)
    print("TESTING UNIVERSE SELF-EXPRESSION IMPLEMENTATION")
    print("=" * 70)
    
    tests = [
        test_imports,
        test_backward_compatibility,
        test_new_features,
        test_documentation
    ]
    
    for test in tests:
        try:
            if not test():
                print(f"\n✗ Test {test.__name__} failed!")
                return False
        except Exception as e:
            print(f"\n✗ Test {test.__name__} raised exception: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
    print("\nPhilosophical Implementation Summary:")
    print("- UniversalStructureOrchestrator reveals universe's self-expression")
    print("- Backward compatibility maintained via FrameworkOrchestrator alias")
    print("- Documentation explains paradigm shift from model to expression")
    print("- Code now reflects: 'universe expressing itself formally'")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
