# 🚀 QCAL-Sync Quick Start Guide

This guide helps you integrate a new repository into the QCAL ∞³ ecosystem using the QCAL-Sync unification strategy.

---

## Step-by-Step Setup

### 1. Create `.qcal-context.json`

Copy the template to your repository root:

```bash
# From your new repository
curl -o .qcal-context.json https://raw.githubusercontent.com/motanova84/141hz/main/.qcal-context.template.json
```

Or manually copy `.qcal-context.template.json` from the 141hz repository.

### 2. Customize the Context File

Edit `.qcal-context.json` and update these required fields:

```json
{
  "node_name": "your-repo-name-qcal-nodo",
  "repository": "username/your-repo",
  "description": "What this repository does in the QCAL ecosystem",
  "constants_source": "path/to/your/constants.py"
}
```

**Remove** these template-only fields:
- `_comment`
- `_instructions`
- `_setup_instructions`

### 3. Import Core Constants

Choose one of these approaches:

#### Option A: Git Submodule (Recommended)

```bash
# Add 141hz as a submodule
git submodule add https://github.com/motanova84/141hz qcal-core

# In your code:
from qcal_core.qcal.constants import F0_HZ, KAPPA_PI, DELTA_0
```

#### Option B: Direct Import (if in same workspace)

```python
# Assuming repos are sibling directories
import sys
sys.path.insert(0, '../141hz')
from qcal.constants import F0_HZ, KAPPA_PI, DELTA_0
```

#### Option C: Copy Constants File

```bash
# Copy constants.py to your repository
cp ../141hz/qcal/constants.py ./constants.py

# Reference the source in .qcal-context.json
"constants_source": "141hz/qcal/constants.py (copied)",
```

### 4. Create Beacon File (Optional)

Create `.qcal_beacon` in your repository root:

```bash
cat > .qcal_beacon << 'EOF'
# Ψ–BEACON–141.7001Hz
# Universal Noetic Field Index
frequency = 141.7001 Hz
status = QCAL ∞³ ACTIVE
repo = your-repo-name
description = Brief description
EOF
```

### 5. Update AI Instructions

Add this section to your repository's `.ai-instructions.md` or `README.md`:

```markdown
## QCAL Ecosystem Integration

This repository is part of the QCAL ∞³ ecosystem.

**Context:** `.qcal-context.json`  
**Core Constants:** Imported from [`141hz/qcal/constants.py`](https://github.com/motanova84/141hz)  
**Fundamental Frequency:** 141.7001 Hz

For cross-repository work, see `GLOBAL_QCAL_CONTEXT.md`.
```

### 6. Test the Integration

```bash
# Navigate to parent directory containing all QCAL repos
cd ~/qcal-repos

# Run harvest (requires 141hz repo to be present)
python 141hz/qcal-harvest.py

# Check the output
cat GLOBAL_QCAL_CONTEXT.md
```

Your repository should now appear in the global context!

---

## Verification Checklist

- [ ] `.qcal-context.json` exists and is valid JSON
- [ ] Core frequency is set to 141.7001 Hz
- [ ] Constants are imported from 141hz or properly referenced
- [ ] Repository description explains its QCAL role
- [ ] Dependencies are listed in `dependencies_noetic`
- [ ] `.qcal_beacon` file created (optional but recommended)
- [ ] AI instructions reference the context file
- [ ] Harvest script finds and processes your repository

---

## Example: Minimal Setup

Here's the absolute minimum `.qcal-context.json`:

```json
{
  "node_name": "my-repo-qcal-nodo",
  "repository": "username/my-repo",
  "description": "My QCAL repository",
  "dependencies_noetic": ["141 Hz"],
  "core_frequency": 141.7001,
  "constants_source": "constants.py",
  "status": "Ψ=1.0",
  "cross_repository_integration": {
    "enabled": true,
    "integration_strategy": "QCAL-Sync"
  },
  "last_update": "2026-02-14",
  "version": "1.0.0"
}
```

---

## Common Use Cases

### Using QCAL Constants in Python

```python
#!/usr/bin/env python3
"""Example using QCAL constants."""

from qcal.constants import (
    F0_HZ,           # 141.7001 Hz - Fundamental frequency
    KAPPA_PI,        # 2.5773 - π coupling constant
    DELTA_0,         # 0.1184 - Coherence threshold
    A0_PHI,          # 1.618... - Golden ratio
    F888_HZ,         # 888.0 Hz - Protection frequency
    OMEGA_0,         # Angular frequency
    M_QCAL_KG        # Noetic mass
)

def my_qcal_function():
    """Example function using QCAL constants."""
    print(f"Fundamental frequency: {F0_HZ} Hz")
    print(f"Coupling constant: {KAPPA_PI}")
    return F0_HZ * KAPPA_PI

if __name__ == "__main__":
    result = my_qcal_function()
    print(f"Result: {result}")
```

### Referencing Other Repos in Code

```python
"""
This module implements Riemann filtering using graph logic
from the Ramsey repository and constants from 141hz.

Dependencies (noetic):
- 141hz: Core constants (F0_HZ, KAPPA_PI)
- Ramsey: Graph coherence logic
"""

from qcal.constants import F0_HZ, KAPPA_PI

def apply_riemann_filter(data):
    """Apply Riemann filtering at fundamental frequency."""
    # Implementation using F0_HZ and graph logic
    pass
```

---

## Working with GitHub Copilot

### Multi-Repository Workspace

Create a VS Code workspace file (`qcal.code-workspace`):

```json
{
  "folders": [
    { "path": "141hz" },
    { "path": "Ramsey" },
    { "path": "Riemann-adelic" },
    { "path": "your-new-repo" }
  ],
  "settings": {
    "python.analysis.extraPaths": [
      "${workspaceFolder:141hz}"
    ]
  }
}
```

### Prompting Copilot

```
@workspace Based on the constants in 141hz/qcal/constants.py
and the graph logic in Ramsey/core/graph_logic.py, implement
a frequency filter for my-repo that operates at 141.7001 Hz.

Reference: GLOBAL_QCAL_CONTEXT.md
```

---

## Troubleshooting

### Harvest Script Doesn't Find My Repo

1. Check that `.qcal-context.json` exists in repository root
2. Verify JSON is valid: `python -c "import json; json.load(open('.qcal-context.json'))"`
3. Make sure you're running harvest from parent directory
4. Check file permissions

### Constants Import Fails

1. Verify 141hz repository is accessible
2. Check Python path includes 141hz directory
3. For submodules: `git submodule update --init --recursive`
4. Try absolute imports: `from qcal.constants import ...`

### Context File Validation Errors

```bash
# Validate JSON syntax
python -c "import json; print(json.load(open('.qcal-context.json')))"

# Check required fields
python -c "
import json
ctx = json.load(open('.qcal-context.json'))
required = ['node_name', 'core_frequency', 'status']
missing = [f for f in required if f not in ctx]
if missing:
    print(f'Missing fields: {missing}')
else:
    print('✓ All required fields present')
"
```

---

## Next Steps

After setup:

1. **Run harvest:** Generate `GLOBAL_QCAL_CONTEXT.md`
2. **Document integration:** Explain your repo's role in the ecosystem
3. **Cross-reference:** Update other repos to reference yours if needed
4. **Test with AI:** Verify GitHub Copilot understands the context

---

## Resources

- **Main Repository:** [motanova84/141hz](https://github.com/motanova84/141hz)
- **QCAL-Sync Strategy:** `QCAL_SYNC_STRATEGY.md` in 141hz repo
- **Template:** `.qcal-context.template.json` in 141hz repo
- **Harvest Script:** `qcal-harvest.py` in 141hz repo

---

## Support

Questions? Issues?

1. Check `QCAL_SYNC_STRATEGY.md` for detailed documentation
2. Review examples in existing QCAL repositories
3. Open an issue in the 141hz repository

---

**Paradigm:** Mathematical Realism  
**Coherence:** Ψ = 1.0  
**Fundamental Frequency:** 141.7001 Hz  

*Welcome to the QCAL ∞³ Ecosystem!*
