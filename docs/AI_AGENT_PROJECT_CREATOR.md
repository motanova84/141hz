# AI Agent for Automated Project Creation

## Overview

The AI Agent for Automated Project Creation is an intelligent system that automatically generates, configures, and activates new analysis projects within the GW250114-141Hz analysis framework. It ensures complete coherence with existing project structure, coding standards, and CI/CD workflows.

## Features

### 🤖 Intelligent Project Generation
- **Template-based creation**: Generates projects from proven templates
- **Type-aware**: Supports event analysis, validation methods, and tools
- **Smart naming**: Handles naming conventions automatically
- **Coherent structure**: Follows established project patterns

### 📝 Automatic Code Generation
- **Analysis scripts**: Complete implementation with data download, preprocessing, and SNR calculation
- **Test suites**: Full unit tests with mocks and synthetic data
- **Documentation**: Comprehensive markdown documentation with usage examples
- **Workflow automation**: GitHub Actions workflows for CI/CD

### 🔄 CI/CD Integration
- **Workflow creation**: Automatic GitHub Actions workflow generation
- **Makefile updates**: Adds targets for new projects
- **Test automation**: Integrates with existing test infrastructure
- **Scheduled runs**: Configures automated analysis schedules

### ✅ Quality Assurance
- **Coherence validation**: Ensures compatibility with existing code
- **Naming consistency**: Follows project naming conventions
- **Code standards**: Generates PEP 8 compliant code
- **Documentation standards**: Maintains documentation quality

## Installation

The AI agent is included in the project. No additional installation required:

```bash
# Clone repository (if not already done)
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Setup environment
make setup
```

## Usage

### Command Line Interface

#### Create Event Analysis Project

Generate a complete analysis project for a gravitational wave event:

```bash
python scripts/ai_agent_project_creator.py \\
  --type event \\
  --name GW250115 \\
  --description "Analysis of GW250115 event at 141.7001 Hz"
```

This creates:
- `scripts/analizar_gw250115.py` - Main analysis script
- `scripts/test_gw250115.py` - Test suite
- `docs/GW250115_ANALYSIS.md` - Documentation
- `.github/workflows/gw250115.yml` - CI/CD workflow
- `projects/gw250115_metadata.json` - Project metadata
- Updates to `Makefile` with new targets

#### Create Validation Project

Generate a validation method project:

```bash
python scripts/ai_agent_project_creator.py \\
  --type validation \\
  --name coherence_multi_scale \\
  --description "Multi-scale coherence validation for f₀"
```

This creates:
- `scripts/validacion_coherence_multi_scale.py` - Validation script
- `.github/workflows/coherence_multi_scale.yml` - CI/CD workflow
- `projects/coherence_multi_scale_metadata.json` - Metadata
- Updates to `Makefile`

#### List Created Projects

View all projects created by the AI agent:

```bash
python scripts/ai_agent_project_creator.py --list
```

### Using Make Targets

After creating a project, use Make for common operations:

```bash
# For event analysis projects
make analyze-gw250115     # Run analysis
make test-gw250115        # Run tests

# For validation projects
make validate-coherence_multi_scale  # Run validation
```

## Project Types

### Event Analysis (`--type event`)

Creates a complete gravitational wave event analysis project:

**Generated Components:**
- Main analysis script with:
  - GWOSC data download
  - Standard LIGO preprocessing
  - SNR calculation at 141.7001 Hz
  - Multi-detector support (H1, L1, V1, K1)
  - Result visualization
  - JSON output
  
- Test suite with:
  - Initialization tests
  - Mock data download tests
  - Synthetic signal tests
  - Result validation tests
  
- Documentation with:
  - Usage examples
  - API reference
  - Output format description
  - Integration instructions

**Use Cases:**
- New gravitational wave event detection
- Re-analysis of existing events with new methods
- Cross-validation studies

### Validation (`--type validation`)

Creates a scientific validation method project:

**Generated Components:**
- Validation script with:
  - High-precision calculations (mpmath)
  - Theoretical predictions
  - Experimental comparisons
  - Statistical tests
  
- Documentation with:
  - Mathematical foundation
  - Validation criteria
  - Interpretation guide

**Use Cases:**
- New theoretical predictions
- Parameter space exploration
- Consistency checks
- Alternative derivations

## Generated File Structure

### Event Analysis Project: `GW250115`

```
.
├── scripts/
│   ├── analizar_gw250115.py      # Main analysis script
│   └── test_gw250115.py          # Test suite
├── docs/
│   └── GW250115_ANALYSIS.md      # Documentation
├── .github/
│   └── workflows/
│       └── gw250115.yml          # CI/CD workflow
├── projects/
│   └── gw250115_metadata.json    # Project metadata
└── Makefile                       # Updated with new targets
```

### Validation Project: `coherence_test`

```
.
├── scripts/
│   └── validacion_coherence_test.py  # Validation script
├── .github/
│   └── workflows/
│       └── coherence_test.yml        # CI/CD workflow
├── projects/
│   └── coherence_test_metadata.json  # Metadata
└── Makefile                           # Updated
```

## Example Workflows

### Example 1: Analyze New Event

```bash
# Step 1: Create project
python scripts/ai_agent_project_creator.py \\
  --type event \\
  --name GW250115 \\
  --description "Analysis of GW250115 binary black hole merger"

# Step 2: Update GPS time in generated script
# Edit scripts/analizar_gw250115.py and set GPS time

# Step 3: Run tests
make test-gw250115

# Step 4: Run analysis
make analyze-gw250115

# Step 5: Review results
cat results/gw250115_results.json
open results/figures/gw250115_snr.png
```

### Example 2: Create Validation Method

```bash
# Step 1: Create project
python scripts/ai_agent_project_creator.py \\
  --type validation \\
  --name harmonic_series \\
  --description "Validation of harmonic series f_n = f₀/π^(2n)"

# Step 2: Customize validation logic
# Edit scripts/validacion_harmonic_series.py

# Step 3: Run validation
make validate-harmonic_series

# Step 4: Review results
cat results/validacion_harmonic_series.json
```

### Example 3: Batch Project Creation

```bash
#!/bin/bash
# Create multiple event projects

events=(
  "GW250115:Analysis of GW250115"
  "GW250116:Analysis of GW250116"
  "GW250117:Analysis of GW250117"
)

for entry in "${events[@]}"; do
  IFS=: read -r name desc <<< "$entry"
  python scripts/ai_agent_project_creator.py \\
    --type event \\
    --name "$name" \\
    --description "$desc"
done

# List all created projects
python scripts/ai_agent_project_creator.py --list
```

## Generated Code Features

### Analysis Scripts

All generated analysis scripts include:

- ✅ **GWOSC Integration**: Automatic data download
- ✅ **Standard Preprocessing**: High-pass, notch filters
- ✅ **SNR Calculation**: At target frequency (141.7001 Hz)
- ✅ **Multi-detector Support**: H1, L1, V1, K1
- ✅ **Visualization**: Automatic plot generation
- ✅ **JSON Output**: Structured results
- ✅ **Error Handling**: Graceful failure management
- ✅ **Logging**: Informative progress messages
- ✅ **CLI Arguments**: Flexible command-line interface

### Test Scripts

All generated test scripts include:

- ✅ **Unit Tests**: Component-level testing
- ✅ **Mock Tests**: Network-free testing
- ✅ **Synthetic Data**: Signal injection tests
- ✅ **Edge Cases**: Boundary condition testing
- ✅ **Result Validation**: Output structure tests
- ✅ **File I/O Tests**: Save/load testing
- ✅ **Coverage**: Comprehensive test coverage

### Workflows

All generated workflows include:

- ✅ **Test Job**: Automated testing on push/PR
- ✅ **Analysis Job**: Scheduled/manual analysis
- ✅ **Caching**: Dependency caching for speed
- ✅ **Artifacts**: Result preservation
- ✅ **Error Handling**: Continue-on-error for data issues
- ✅ **Multi-Python**: Python 3.11+ support

## Customization

### Modify Generated Scripts

After generation, you can customize:

1. **GPS Time**: Update event GPS time in analysis scripts
2. **Detectors**: Change detector list
3. **Frequency**: Adjust target frequency or bandwidth
4. **Analysis Logic**: Add custom analysis steps
5. **Visualization**: Customize plots
6. **Output Format**: Modify result structure

### Extend Templates

To add new project types:

1. Create new template class in `ai_agent_project_creator.py`
2. Inherit from `ProjectTemplate`
3. Implement required methods:
   - `generate_*_script()`
   - `generate_documentation()`
4. Add to `AIProjectAgent.create_project()` switch

## Integration with Existing Projects

### Naming Conventions

The AI agent follows these conventions:

- **Scripts**: `analizar_<name>.py`, `validacion_<name>.py`
- **Tests**: `test_<name>.py`
- **Docs**: `<NAME>_ANALYSIS.md`
- **Workflows**: `<name>.yml`
- **Metadata**: `<name>_metadata.json`

### Makefile Integration

Generated Makefile targets:

- **Event Analysis**: `make analyze-<name>`, `make test-<name>`
- **Validation**: `make validate-<name>`

### CI/CD Integration

Generated workflows automatically:

- Run on push/PR to main branch
- Execute tests before analysis
- Upload artifacts with retention policies
- Support manual triggers via workflow_dispatch

## Troubleshooting

### Common Issues

#### Issue: Script generation fails

**Solution**: Check permissions and directory structure
```bash
# Ensure scripts directory exists
mkdir -p scripts

# Check write permissions
ls -la scripts/
```

#### Issue: Makefile not updated

**Solution**: Verify Makefile has help target marker
```bash
# Check for marker in Makefile
grep "# Show available targets" Makefile
```

#### Issue: Tests fail after generation

**Solution**: Install dependencies
```bash
make setup
```

### Debug Mode

For verbose output:
```bash
python scripts/ai_agent_project_creator.py \\
  --type event \\
  --name GW250115 \\
  --description "Test" \\
  --verbose
```

## Best Practices

### Project Naming

- **Events**: Use official GW catalog names (GW250115)
- **Validations**: Use descriptive names (coherence_multi_scale)
- **Avoid**: Spaces, special characters (except `-` and `_`)

### Description Writing

- Be concise but informative
- Include key analysis target
- Mention novel aspects
- Reference related work

### Post-Creation

1. **Review generated code**: Ensure it meets requirements
2. **Update GPS times**: For event analysis
3. **Run tests**: Verify functionality
4. **Customize**: Adapt to specific needs
5. **Document changes**: Update docs if modified
6. **Commit**: Add to version control

## Advanced Usage

### Programmatic Usage

```python
from scripts.ai_agent_project_creator import AIProjectAgent

# Create agent
agent = AIProjectAgent()

# Create multiple projects
projects = [
    ('event', 'GW250115', 'Event 1'),
    ('event', 'GW250116', 'Event 2'),
    ('validation', 'test_coherence', 'Validation 1')
]

for ptype, name, desc in projects:
    metadata = agent.create_project(ptype, name, desc)
    print(f"Created: {metadata['name']}")

# List all projects
for project in agent.list_projects():
    print(f"{project['name']} ({project['type']})")
```

### Custom Templates

Create custom templates by extending base classes:

```python
from scripts.ai_agent_project_creator import ProjectTemplate

class MyCustomTemplate(ProjectTemplate):
    def generate_custom_script(self):
        # Custom generation logic
        return script_content
```

## Testing

### Run Agent Tests

```bash
# Run all tests
python scripts/test_ai_agent_project_creator.py

# Specific test class
python -m unittest scripts.test_ai_agent_project_creator.TestProjectTemplates

# Specific test
python -m unittest scripts.test_ai_agent_project_creator.TestProjectTemplates.test_event_script_generation
```

### Coverage

```bash
# With coverage
pip install coverage
coverage run scripts/test_ai_agent_project_creator.py
coverage report
coverage html  # Generate HTML report
```

## Contributing

To contribute new templates or features:

1. Fork repository
2. Create feature branch
3. Add template class
4. Add tests
5. Update documentation
6. Submit pull request

## References

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [README.md](../README.md) - Main project documentation
- [PAPER.md](../PAPER.md) - Theoretical foundation
- [GitHub Copilot Instructions](../.github/copilot-instructions.md) - Automation guidelines

## Support

For issues or questions:

- Open an issue on GitHub
- Check existing documentation
- Review generated code examples
- Contact: institutoconsciencia@proton.me

## License

MIT License - See [LICENSE](../LICENSE)

## Changelog

### v1.0.0 (2025-01-26)
- Initial release
- Event analysis template
- Validation template
- Full CI/CD integration
- Comprehensive test suite
- Complete documentation

---

Generated by AI Agent Project Creator v1.0.0
