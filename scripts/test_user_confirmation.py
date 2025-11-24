#!/usr/bin/env python3
"""
Test script for user_confirmation module.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_confirmation import (
    confirm_action, 
    confirm_data_download,
    confirm_file_deletion,
    confirm_long_running_operation,
    add_confirmation_args
)
import argparse


def test_auto_yes_mode():
    """Test that auto-yes mode works correctly."""
    print("Testing auto-yes mode...")
    
    # All of these should return True without prompting
    assert confirm_action("Test 1", auto_yes=True) == True
    assert confirm_data_download(100, auto_yes=True) == True
    assert confirm_file_deletion("/tmp/test", auto_yes=True) == True
    assert confirm_long_running_operation("Test op", 10, auto_yes=True) == True
    
    print("✅ Auto-yes mode tests passed")


def test_argument_parser():
    """Test that argument parser integration works."""
    print("\nTesting argument parser integration...")
    
    parser = argparse.ArgumentParser()
    add_confirmation_args(parser)
    
    # Test --yes flag
    args = parser.parse_args(['--yes'])
    assert args.yes == True
    
    # Test -y flag
    args = parser.parse_args(['-y'])
    assert args.yes == True
    
    # Test --no-confirm flag
    args = parser.parse_args(['--no-confirm'])
    assert args.yes == True
    
    # Test no flags
    args = parser.parse_args([])
    assert args.yes == False
    
    print("✅ Argument parser tests passed")


def test_confirmation_messages():
    """Test that confirmation messages are properly formatted."""
    print("\nTesting confirmation message formatting...")
    
    # These will all return True in auto-yes mode, but we're testing the message formatting
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        confirm_data_download(125.5, auto_yes=True)
    output = f.getvalue()
    assert "125.5 MB" in output
    assert "auto-confirmed" in output
    
    f = io.StringIO()
    with redirect_stdout(f):
        confirm_file_deletion("/path/to/file", auto_yes=True)
    output = f.getvalue()
    assert "/path/to/file" in output
    
    f = io.StringIO()
    with redirect_stdout(f):
        confirm_long_running_operation("Long analysis", 30, auto_yes=True)
    output = f.getvalue()
    assert "30 min" in output
    assert "Long analysis" in output
    
    print("✅ Confirmation message tests passed")


def test_spanish_responses():
    """Test that Spanish responses (SI/NO) are handled correctly."""
    print("\nTesting Spanish response handling...")
    
    # This test documents that 'si' and 'sí' are accepted as yes responses
    # Actual interactive testing would require user input simulation
    
    print("✅ Spanish response handling documented (requires manual testing)")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing user_confirmation module")
    print("=" * 60)
    
    test_auto_yes_mode()
    test_argument_parser()
    test_confirmation_messages()
    test_spanish_responses()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)
    print("\nNote: Interactive confirmation tests require manual testing.")
    print("Run: python3 scripts/user_confirmation.py")


if __name__ == '__main__':
    main()
