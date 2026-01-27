# 🤖 AI Agent for Automated Project Creation

## Quick Start

```bash
# Create a new gravitational wave event analysis project
python scripts/ai_agent_project_creator.py \
  --type event \
  --name GW250115 \
  --description "Analysis of GW250115 binary black hole merger at 141.7001 Hz"

# Create a new validation method project
python scripts/ai_agent_project_creator.py \
  --type validation \
  --name coherence_multi_scale \
  --description "Multi-scale coherence validation for fundamental frequency"

# List all created projects
python scripts/ai_agent_project_creator.py --list

# Run demonstration
make demo-ai-agent

# Run tests
make test-ai-agent
```

## What It Does

The AI Agent automatically:

1. **Generates complete analysis scripts** with:
   - GWOSC data download
   - Standard LIGO preprocessing
   - SNR calculation at 141.7001 Hz
   - Multi-detector support
   - Visualization
   - JSON output

2. **Creates comprehensive test suites** with:
   - Unit tests
   - Mock tests
   - Synthetic signal tests
   - Integration tests

3. **Writes documentation** with:
   - Usage examples
   - API reference
   - Output descriptions

4. **Sets up CI/CD workflows** with:
   - Automated testing
   - Scheduled analysis
   - Artifact storage

5. **Updates Makefile** with:
   - New build targets
   - Test commands
   - Integration targets

## Project Types

### Event Analysis (`--type event`)
Complete analysis project for gravitational wave events.

**Generated files:**
- `scripts/analizar_<name>.py` - Main analysis script
- `scripts/test_<name>.py` - Test suite
- `docs/<NAME>_ANALYSIS.md` - Documentation
- `.github/workflows/<name>.yml` - CI/CD workflow

**Example:**
```bash
python scripts/ai_agent_project_creator.py \
  --type event \
  --name GW250115 \
  --description "Analysis of GW250115"
```

### Validation (`--type validation`)
Scientific validation method projects.

**Generated files:**
- `scripts/validacion_<name>.py` - Validation script
- `.github/workflows/<name>.yml` - CI/CD workflow

**Example:**
```bash
python scripts/ai_agent_project_creator.py \
  --type validation \
  --name harmonic_series \
  --description "Validation of harmonic frequency series"
```

## Features

### 🎯 Coherence with Existing Project
- Follows established naming conventions
- Uses same code structure and patterns
- Integrates with existing CI/CD
- Maintains documentation standards

### 📊 Data-Driven Generation
- Templates based on successful implementations
- Proven analysis patterns
- Standard preprocessing pipelines
- Validated test strategies

### 🔄 Full Automation
- No manual file creation needed
- Automatic integration with build system
- Self-documenting code
- Ready to run immediately

### ✅ Quality Assurance
- Generated code is PEP 8 compliant
- Includes comprehensive tests
- Documentation is complete
- CI/CD is configured

## Usage Examples

### Create Multiple Projects

```python
from scripts.ai_agent_project_creator import AIProjectAgent

agent = AIProjectAgent()

# Create several event analysis projects
events = ['GW250115', 'GW250116', 'GW250117']
for event in events:
    agent.create_project(
        'event',
        event,
        f'Analysis of {event} at 141.7001 Hz'
    )

# List all created
for project in agent.list_projects():
    print(f"{project['name']}: {project['type']}")
```

### Customize Generated Code

After generation, customize the script:

```python
# Edit scripts/analizar_gw250115.py
# Update GPS time, detectors, analysis parameters
```

Then run:
```bash
make test-gw250115    # Run tests
make analyze-gw250115 # Run analysis
```

## Documentation

- **Full Guide**: [docs/AI_AGENT_PROJECT_CREATOR.md](AI_AGENT_PROJECT_CREATOR.md)
- **API Reference**: Inline documentation in `scripts/ai_agent_project_creator.py`
- **Examples**: `scripts/demo_ai_agent.py`

## Testing

```bash
# Run all tests (15 tests)
make test-ai-agent

# Or directly
python scripts/test_ai_agent_project_creator.py
```

## Architecture

```
AIProjectAgent
├── EventAnalysisTemplate
│   ├── generate_analysis_script()
│   ├── generate_test_script()
│   └── generate_documentation()
└── ValidationTemplate
    ├── generate_validation_script()
    └── generate_documentation()
```

## Requirements

- Python 3.11+
- Standard project dependencies (requirements.txt)

## Integration

### With Makefile
All generated projects automatically get Makefile targets.

### With CI/CD
GitHub Actions workflows are created automatically.

### With Documentation
Documentation is generated and linked.

## Benefits

1. **Speed**: Create complete projects in seconds
2. **Consistency**: All projects follow same patterns
3. **Quality**: Generated code is tested and documented
4. **Maintainability**: Updates to templates benefit all projects
5. **Scalability**: Easy to create many projects

## Future Enhancements

- [ ] Tool project type for utilities
- [ ] Interactive project wizard
- [ ] Template customization via config files
- [ ] Integration with project planning tools
- [ ] Automatic dependency detection

## Support

- Documentation: [docs/AI_AGENT_PROJECT_CREATOR.md](AI_AGENT_PROJECT_CREATOR.md)
- Issues: GitHub Issues
- Examples: `make demo-ai-agent`

## License

MIT License - Same as main project

---

Generated by AI Agent Project Creator v1.0.0
