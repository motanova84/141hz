# User Confirmation Feature

## Overview

This repository now includes user confirmation prompts for operations that:
- Download large amounts of data
- Delete files or directories
- Take significant time to complete

This prevents accidental data downloads or deletions while still allowing automated workflows through bypass flags.

## Features

### 1. **Interactive Confirmation Prompts**

Scripts now ask for user confirmation before:
- Downloading data from GWOSC (~150 MB)
- Deleting generated files and directories
- Running long-running analysis operations

### 2. **Automated Workflow Support**

All confirmation prompts can be bypassed using:
- `--yes` or `-y` flag in Python scripts
- `-force` suffix in Makefile targets

This ensures CI/CD pipelines and automated workflows continue to work without interruption.

### 3. **Bilingual Support**

Confirmation prompts accept responses in both English and Spanish:
- English: `y`, `yes`, `n`, `no`
- Spanish: `s`, `si`, `sí`, `n`, `no`

## Usage

### Python Scripts

#### With Confirmation (Interactive)
```bash
# User will be prompted to confirm
python3 scripts/descargar_datos.py
```

Output:
```
Descargando datos de control GW150914...
Descargar aproximadamente 150.0 MB de datos de GWOSC? [Y/n]: 
```

#### Without Confirmation (Automated)
```bash
# Auto-confirms all prompts
python3 scripts/descargar_datos.py --yes
# or
python3 scripts/descargar_datos.py -y
```

Output:
```
Descargando datos de control GW150914...
Descargar aproximadamente 150.0 MB de datos de GWOSC? [y/n]: y (auto-confirmed)
```

### Makefile Targets

#### With Confirmation (Interactive)
```bash
# User will be prompted to confirm
make data    # Download data
make clean   # Delete files
```

#### Without Confirmation (Automated)
```bash
# Auto-confirms all operations
make data-force    # Download without prompt
make clean-force   # Clean without prompt
```

## Implementation Details

### Core Module: `user_confirmation.py`

The `scripts/user_confirmation.py` module provides:

```python
from user_confirmation import (
    confirm_action,              # General yes/no confirmation
    confirm_data_download,       # Data download confirmation
    confirm_file_deletion,       # File deletion confirmation
    confirm_long_running_operation,  # Long operation confirmation
    add_confirmation_args        # Add --yes/-y args to argparse
)
```

### Example Integration

```python
import argparse
from user_confirmation import confirm_data_download, add_confirmation_args

def main(auto_yes=False):
    # Ask for confirmation
    if not confirm_data_download(size_mb=150, auto_yes=auto_yes):
        print("Operation cancelled")
        return
    
    # Proceed with download
    download_data()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    add_confirmation_args(parser)  # Adds --yes and --no-confirm
    args = parser.parse_args()
    
    main(auto_yes=args.yes)
```

## Modified Files

### Python Scripts
- **`scripts/descargar_datos.py`**: Added confirmation before downloading GWOSC data
  - New flags: `--yes`, `-y`, `--no-confirm`
  
### Makefile
- **`data`**: Now prompts before downloading (interactive)
- **`data-force`**: Downloads without prompt (automated)
- **`clean`**: Now prompts before deleting (interactive)
- **`clean-force`**: Cleans without prompt (automated)
- **`help`**: Updated to document new targets

### New Files
- **`scripts/user_confirmation.py`**: Core confirmation module
- **`scripts/test_user_confirmation.py`**: Test suite for confirmations
- **`USER_CONFIRMATION.md`**: This documentation file

## Testing

### Run Automated Tests
```bash
python3 scripts/test_user_confirmation.py
```

### Manual Interactive Testing
```bash
# Test basic confirmation
python3 scripts/user_confirmation.py

# Test data download script
python3 scripts/descargar_datos.py

# Test Makefile targets
make data
make clean
```

## CI/CD Integration

Automated workflows should use the bypass flags:

```yaml
# GitHub Actions example
- name: Download data
  run: make data-force  # No prompt

- name: Clean workspace
  run: make clean-force  # No prompt
```

Or with Python scripts:
```yaml
- name: Download data
  run: python3 scripts/descargar_datos.py --yes
```

## Benefits

1. **Safety**: Prevents accidental data downloads or deletions
2. **User-friendly**: Clear prompts with sensible defaults
3. **Automation-ready**: Full support for non-interactive workflows
4. **Bilingual**: Supports English and Spanish responses
5. **Consistent**: Unified confirmation interface across all scripts

## Future Enhancements

Potential additions:
- [ ] Add confirmation to more scripts (long-running analyses)
- [ ] Environment variable support (e.g., `AUTO_CONFIRM=1`)
- [ ] Configuration file for default behavior
- [ ] More granular confirmation levels (--confirm-download, --confirm-delete)

## Support

For issues or questions about user confirmation:
- Check this documentation
- Run tests: `python3 scripts/test_user_confirmation.py`
- Review examples in `scripts/user_confirmation.py`
