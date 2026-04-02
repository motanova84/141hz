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

## 🌐 Ecosistema Matemático Externo

Este repositorio es parte de un ecosistema matemático más amplio que valida y conecta los resultados fundamentales de QCAL ∞³. Los siguientes repositorios hermanos proporcionan contexto y validación matemática:

### Repositorios Hermanos

1. **riemann-adelic-operator** (motanova84/riemann-adelic-operator)
   - **Qué aporta**: Operador D(s) ≡ Ξ(s) que demuestra que los ceros de ζ(s) están en la línea crítica σ=½
   - **Conexión QCAL**: Los primeros 5 ceros γₙ de ζ(s) determinan los modos de resonancia f_n = F0·γₙ/γ₁
   - **Validación**: Espaciado GUE de niveles espectrales, verificación σ=½
   - **Importancia**: Justifica la línea crítica en el reloj QCAL y los modos fundamentales

2. **bsd-conjecture-proof** (motanova84/bsd-conjecture-proof)
   - **Qué aporta**: Espectro adélico BSD conectado con curvas elípticas y puntos racionales
   - **Conexión QCAL**: Pico BSD p=17 (ciclo Magicicada 17 años), modos BIO-LOCK desde kernel K_E(1)
   - **Validación**: Conexión entre geometría algebraica y frecuencia fundamental F0=141.7001 Hz
   - **Importancia**: Demuestra que f₀ emerge de la estructura aritmética profunda del universo

3. **navier-stokes-global-regularity** (motanova84/navier-stokes-global-regularity)
   - **Qué aporta**: ν_min QCAL (viscosidad mínima cuántica), Reynolds cuántico
   - **Conexión QCAL**: Cota ‖u(t)‖²_H¹, prueba de regularidad global del fluido
   - **Validación**: Vincula la regularidad del fluido con el operador de coherencia unitaria
   - **Importancia**: Conecta mecánica de fluidos con coherencia cuántica biológica

4. **ramsey-theory-gue** (motanova84/ramsey-theory-gue)
   - **Qué aporta**: R(5,5)=43, R(6,6)=108, φ_R=43/108
   - **Conexión QCAL**: Cota vibracional κ_Π=2.5773, espaciado GUE en números de Ramsey
   - **Validación**: Conecta teoría de grafos extremal con niveles de energía cuánticos
   - **Importancia**: Demuestra que los números de Ramsey siguen el mismo patrón espectral que los ceros de Riemann

5. **p-vs-np-complexity** (motanova84/p-vs-np-complexity)
   - **Qué aporta**: κ_Π=2.5773 como invariante de complejidad, clasificación P-trivial/P/NP-hard por Ψ
   - **Conexión QCAL**: Horizonte de trazabilidad computacional definido por coherencia cuántica
   - **Validación**: Reduce complejidad computacional a O(1) por resonancia en f₀
   - **Importancia**: Conecta complejidad computacional con geometría espectral

6. **141hz-empirical-validation** (motanova84/141hz-empirical-validation)
   - **Qué aporta**: Validación empírica F0 (99,78%, Wang et al. 2025), octavas armónicas
   - **Conexión QCAL**: Ψ_empírica=0.9978, confirmación experimental de la teoría
   - **Validación**: Datos LIGO/GWOSC, AT2020afhd (Wang et al. Science Advances 2025)
   - **Importancia**: Proporciona verificación experimental directa de las predicciones teóricas

### Uso del Contexto Externo

El módulo `contexto_ecosistema/` en este repositorio mantiene una instantánea actualizada de los resultados clave de los repositorios hermanos:

```python
# Importar contexto de Riemann
from contexto_ecosistema import riemann_adelic_context

# Obtener los primeros 5 ceros de ζ(s)
zeros = riemann_adelic_context.get_riemann_zeros()

# Calcular modos de resonancia
modes = riemann_adelic_context.compute_resonance_modes(zeros)
```

### Sincronización Automática

El flujo de trabajo `.github/workflows/sync_contexto_externo.yml` se ejecuta semanalmente para:
- Leer commits y READMEs de los 6 repositorios hermanos vía GitHub API
- Actualizar `contexto_ecosistema/snapshot_externo.md` con el estado actual
- Hacer commit automático si hubo cambios

Esto garantiza que cualquier agente futuro tenga siempre acceso al contexto más reciente del ecosistema matemático completo.

## 📝 Summary

These instructions help GitHub Copilot:
1. Automatically maintain workflows when code changes
2. Suggest optimizations for parallel execution and GPU usage
3. Detect missing secrets and environment variables
4. Ensure Python 3.11+ compatibility
5. Follow scientific computing best practices
6. Maintain code quality and reproducibility
7. Understand and utilize the external mathematical ecosystem context

When in doubt, prioritize reproducibility and scientific rigor over convenience.
