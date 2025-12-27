# GitHub Copilot Instructions for GW250114-141Hz Analysis

This file provides instructions to GitHub Copilot for maintaining and optimizing the workflows and codebase of this gravitational wave analysis project.

## 🔄 Workflow Maintenance

### Automatic Workflow Updates

- **Detect changes in validation scripts**: When files matching `validate_*.py` or `validacion_*.py` are modified, suggest updates to the production workflow (`.github/workflows/production-qcal.yml`) and CI workflow (`.github/workflows/analyze.yml`) to ensure they reference the correct scripts and use appropriate parameters.

- **Monitor dependency changes**: When `requirements.txt` is updated, verify that all workflows install dependencies correctly and suggest version compatibility checks for Python 3.11 and Python 3.12.

- **Track script relocations**: If validation or analysis scripts are moved between directories (e.g., from root to `scripts/`), automatically update all workflow references to maintain correct paths.

### New Workflow Generation

- **Generate workflows for repetitive tasks**: When new analysis scripts are added that follow patterns like:
  - `test_*.py` - Create or update test workflows
  - `analizar_*.py` - Create analysis workflows with appropriate data download steps
  - `pipeline_*.py` - Create pipeline workflows with multi-stage execution
  
- **Suggest scheduled workflows**: For long-running validation or analysis tasks, propose cron schedules (e.g., daily, weekly, or every 4 hours) and include `workflow_dispatch` for manual triggers.

- **Create matrix strategies**: When multiple Python versions, operating systems, or parameter variations need testing, suggest GitHub Actions matrix strategies for parallel execution.

## 🔐 Secrets and Environment Variables

### Missing Credentials Detection

When workflows or scripts reference environment variables or secrets that aren't documented, suggest:

- **For Hugging Face operations**:
  - `HF_TOKEN`: Required for `huggingface-cli upload` commands
  - Add to repository secrets at Settings → Secrets and variables → Actions

- **For Docker Hub operations**:
  - `DOCKERHUB_USERNAME`: Docker Hub username
  - `DOCKERHUB_TOKEN`: Docker Hub access token (not password)
  - Add to repository secrets for secure image pushing

- **For API integrations**:
  - `GWOSC_API_KEY`: If GWOSC API requires authentication
  - Document in README.md if new API keys are introduced

### Environment Variable Documentation

When new environment variables are added to scripts:
- Document them in the script's docstring
- Add them to the workflow YAML with appropriate defaults or secret references
- Update README.md with setup instructions

## ⚡ Performance Optimizations

### Parallel Execution

Suggest parallel execution strategies when:

- **Multiple independent validations**: Use GitHub Actions `matrix` strategy to run different validation scripts in parallel
  ```yaml
  strategy:
    matrix:
      validation: [radio_cuantico, energia_cuantica, simetria_discreta]
  ```

- **Multi-event analysis**: When analyzing multiple gravitational wave events, parallelize across events
  ```yaml
  strategy:
    matrix:
      event: [GW150914, GW151226, GW170814]
  ```

- **Cross-platform testing**: Test across multiple OS and Python versions
  ```yaml
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest]
      python-version: ['3.11', '3.12']
  ```

### GPU Optimization

When GPU-accelerated operations are detected:

- **Suggest GPU runners**: Recommend using GitHub-hosted GPU runners or self-hosted runners with CUDA support
  ```yaml
  runs-on: [self-hosted, gpu]
  ```

- **CUDA detection and setup**: Add steps to detect and configure CUDA when scripts import `cupy`, `torch`, or GPU-accelerated libraries
  ```yaml
  - name: Set up CUDA
    uses: Jimver/cuda-toolkit@v0.2.11
    with:
      cuda: '12.0'
  ```

- **CPU fallback**: Ensure workflows have graceful fallback to CPU when GPU is unavailable

### Caching Strategies

Optimize workflow execution time by suggesting caching for:

- **Pip dependencies**: Already implemented, maintain cache consistency
- **Downloaded datasets**: Cache GWOSC data files to avoid repeated downloads
  ```yaml
  - uses: actions/cache@v3
    with:
      path: data/
      key: gwosc-data-${{ hashFiles('scripts/descargar_datos.py') }}
  ```
- **Compiled artifacts**: Cache compiled extensions or build artifacts

## 🐍 Python Compatibility

### Version Requirements

Maintain compatibility with:
- **Primary**: Python 3.11 (production standard)
- **Secondary**: Python 3.12 (for future-proofing)
- **Testing**: Both versions in CI/CD matrix

### Dependency Management

When dependencies are added or updated:
- Verify compatibility with Python 3.11+
- Check for breaking changes in major version updates
- Test with both minimum and latest compatible versions
- Update `requirements.txt` with version constraints when necessary

### Type Hints and Modern Syntax

Encourage use of:
- Type hints for function parameters and returns
- Modern syntax features available in Python 3.11+
- Structural pattern matching (match/case) where appropriate
- Exception groups and `except*` for better error handling

## 📊 Scientific Computing Best Practices

### High-Precision Calculations

When working with scientific calculations:
- Use `mpmath` for arbitrary precision arithmetic
- Include `--precision` parameters for configurable accuracy
- Validate numerical stability with different precision levels

### Reproducibility

Ensure all workflows and scripts:
- Use fixed random seeds when applicable
- Document exact dependency versions for critical calculations
- Save computation parameters alongside results
- Include timestamps and version information in output files

### Data Validation

When processing gravitational wave data:
- Verify data integrity before analysis
- Include SNR thresholds and quality checks
- Log data provenance (source, download date, processing steps)
- Save both raw and processed data artifacts

## 🎯 Workflow Optimization Rules

### Conditional Execution

Optimize workflow runs by:
- Only running Docker builds on scheduled runs, not PRs
- Skipping expensive operations when secrets are not available
- Using `continue-on-error: true` for optional steps
- Implementing `if: success()` conditions for dependent steps

### Resource Management

- Set appropriate timeouts for long-running steps
- Use `retention-days` for artifacts (7 days for test results, 30 days for production)
- Clean up intermediate files to save storage
- Cancel redundant workflow runs for updated PRs

### Artifact Management

When creating or uploading artifacts:
- Use descriptive names with run numbers: `validation-results-${{ github.run_number }}`
- Include relevant file patterns (JSON, PNG, PDF)
- Set appropriate retention periods
- Generate summary reports in `$GITHUB_STEP_SUMMARY`

## 🔍 Code Quality

### Linting and Formatting

Maintain code quality by:
- Running `flake8` for style checking
- Maximum line length: 120 characters
- Maximum complexity: 10
- Fail on syntax errors (E9, F63, F7, F82)

### Testing Standards

For new test files:
- Follow naming convention: `test_*.py`
- Use pytest-compatible assertions
- Include docstrings explaining test purpose
- Group related tests in classes
- Add parametrize decorators for multiple test cases

### Documentation

For new features or scripts:
- Include module-level docstrings
- Document command-line arguments with examples
- Add usage examples in comments
- Update README.md for user-facing changes
- Include references to relevant papers or documentation

## 🚀 Deployment and Release

### Version Tagging

When preparing releases:
- Update version strings in scripts
- Tag Docker images with semantic versions
- Create GitHub releases with changelogs
- Document breaking changes

### Production Deployment

For production workflows:
- Test changes in feature branches first
- Use staging environments when available
- Include rollback procedures
- Monitor workflow success rates
- Alert on consecutive failures

## 📝 Summary

These instructions help GitHub Copilot:
1. Automatically maintain workflows when code changes
2. Suggest optimizations for parallel execution and GPU usage
3. Detect missing secrets and environment variables
4. Ensure Python 3.11+ compatibility
5. Follow scientific computing best practices
6. Maintain code quality and reproducibility

When in doubt, prioritize reproducibility and scientific rigor over convenience.
