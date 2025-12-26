#!/usr/bin/env python3
"""
Utility module for user confirmation prompts.
Provides consistent yes/no prompts across scripts with optional bypass flags.
"""
import sys
import argparse


def confirm_action(message, default='n', auto_yes=False):
    """
    Ask user for confirmation before proceeding with an action.
    
    Args:
        message (str): The confirmation question to display
        default (str): Default response ('y' or 'n')
        auto_yes (bool): If True, automatically return True without prompting
    
    Returns:
        bool: True if user confirms, False otherwise
    
    Examples:
        >>> if confirm_action("Download 500MB of data?"):
        ...     download_data()
        
        >>> if confirm_action("Delete all files?", default='n', auto_yes=args.yes):
        ...     delete_files()
    """
    if auto_yes:
        print(f"{message} [y/n]: y (auto-confirmed)")
        return True
    
    # Prepare prompt with default indicator
    if default.lower() == 'y':
        prompt = f"{message} [Y/n]: "
    else:
        prompt = f"{message} [y/N]: "
    
    while True:
        try:
            response = input(prompt).strip().lower()
            
            # Use default if user just presses Enter
            if response == '':
                response = default.lower()
            
            if response in ['y', 'yes', 'si', 'sí']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Por favor responde 'y' (sí) o 'n' (no).")
        except (EOFError, KeyboardInterrupt):
            print("\n\nOperación cancelada por el usuario.")
            sys.exit(1)


def add_confirmation_args(parser):
    """
    Add standard confirmation bypass arguments to an ArgumentParser.
    
    Args:
        parser (argparse.ArgumentParser): The parser to add arguments to
    
    Example:
        >>> parser = argparse.ArgumentParser()
        >>> add_confirmation_args(parser)
        >>> args = parser.parse_args()
        >>> if confirm_action("Continue?", auto_yes=args.yes):
        ...     continue_operation()
    """
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Automatically answer yes to all prompts (non-interactive mode)'
    )
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        dest='yes',
        help='Alias for --yes (skip confirmation prompts)'
    )


def confirm_data_download(size_mb, auto_yes=False):
    """
    Specialized confirmation for data downloads.
    
    Args:
        size_mb (float): Approximate size of download in MB
        auto_yes (bool): If True, skip confirmation
    
    Returns:
        bool: True if user confirms download
    """
    message = f"Descargar aproximadamente {size_mb:.1f} MB de datos de GWOSC?"
    return confirm_action(message, default='y', auto_yes=auto_yes)


def confirm_file_deletion(path, auto_yes=False):
    """
    Specialized confirmation for file/directory deletion.
    
    Args:
        path (str): Path to be deleted
        auto_yes (bool): If True, skip confirmation
    
    Returns:
        bool: True if user confirms deletion
    """
    message = f"¿Eliminar '{path}' y todo su contenido?"
    return confirm_action(message, default='n', auto_yes=auto_yes)


def confirm_long_running_operation(operation_name, estimated_time_min, auto_yes=False):
    """
    Specialized confirmation for long-running operations.
    
    Args:
        operation_name (str): Name of the operation
        estimated_time_min (int): Estimated time in minutes
        auto_yes (bool): If True, skip confirmation
    
    Returns:
        bool: True if user confirms operation
    """
    message = f"Ejecutar '{operation_name}' (tiempo estimado: ~{estimated_time_min} min)?"
    return confirm_action(message, default='y', auto_yes=auto_yes)


if __name__ == '__main__':
    # Test the confirmation functions
    print("Testing user_confirmation module...\n")
    
    # Test basic confirmation
    print("Test 1: Basic confirmation")
    if confirm_action("¿Continuar con test 1?", default='y'):
        print("✅ Test 1 confirmed\n")
    else:
        print("❌ Test 1 cancelled\n")
    
    # Test auto-yes
    print("Test 2: Auto-yes mode")
    if confirm_action("¿Continuar con test 2?", auto_yes=True):
        print("✅ Test 2 auto-confirmed\n")
    
    # Test data download confirmation
    print("Test 3: Data download confirmation")
    if confirm_data_download(150.5, auto_yes=False):
        print("✅ Download confirmed\n")
    else:
        print("❌ Download cancelled\n")
    
    print("All tests completed.")
