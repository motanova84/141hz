# 🌌 GW250114 - Complex Workflows Documentation

This directory contains the complete workflow infrastructure for the GW250114 gravitational wave analysis project.

## 📋 Overview

We have implemented a comprehensive suite of **10+ specialized workflows** that run validations, analysis, and tests in parallel using matrix strategies across multiple Python versions (3.11 & 3.12) and operating systems.

## 🔄 Workflow Categories

### 1. Core CI/CD Workflows

#### **analyze.yml** - CI/CD Tests and Analysis
- **Trigger:** Push/PR to main, manual
- **Purpose:** Main continuous integration workflow
- **Jobs:** Unit tests, linting, scientific analysis
- **Python Versions:** 3.11, 3.12
- **Matrix Strategy:** Yes

#### **production-qcal.yml** - QCAL Production Cycle
- **Trigger:** Every 4 hours, manual
- **Purpose:** Production validation and deployment
- **Jobs:** Core validation, result aggregation, Docker builds, HuggingFace uploads
- **Python Version:** 3.11

### 2. Validation Workflows

#### **quantum-validations.yml** - Quantum Validations
- **Trigger:** Push, PR, daily at 06:00 UTC, manual
- **Purpose:** Quantum theory validations
- **Matrix:**
  - Python: 3.11, 3.12
  - Validations: radio_cuantico, energia_cuantica, alpha_psi, compactificacion_quintica, numerica_5_7f
- **Total Jobs:** 10 (5 validations × 2 Python versions)

#### **alternative-validations.yml** - Alternative Validation Methods
- **Trigger:** Push, PR, weekly Monday 08:00 UTC, manual
- **Purpose:** Alternative analysis methods
- **Matrix:**
  - Python: 3.11, 3.12
  - Methods: autoencoder, wavelet, interferometrica, coherencia
- **Total Jobs:** 8 (4 methods × 2 Python versions)

#### **scientific-validation.yml** - 3 Pillars Scientific Validation
- **Trigger:** Push, PR, daily at 02:00 UTC, manual
- **Purpose:** Scientific method validation (reproducibility, falsifiability, evidence)
- **Jobs:**
  - Three pillars validation (3 pillars × 2 Python versions)
  - Complete 3 pillars validation
  - Discovery standards (>10σ)
  - Falsification protocol
  - Experimental protocols
- **Total Jobs:** 12+

### 3. Analysis Workflows

#### **multi-event-analysis.yml** - Multi-Event Analysis
- **Trigger:** Push, PR, twice daily (00:00, 12:00 UTC), manual
- **Purpose:** Analyze multiple gravitational wave events
- **Matrix:**
  - Python: 3.11, 3.12
  - Events: GW150914, GW151226, GW170814, GW200129, GW250114
- **Additional Jobs:** Multi-event SNR, Bayesian multi-event
- **Total Jobs:** 14 (5 events × 2 versions + 4 additional)

#### **detector-analysis.yml** - Detector-Specific Analysis
- **Trigger:** Push, PR, daily at 04:00 UTC, manual
- **Purpose:** Analyze specific detector data
- **Matrix:**
  - Python: 3.11, 3.12
  - Detectors: KAGRA_K1, LIGO_L1, ASD_141Hz
- **Additional Jobs:** Ringdown analysis
- **Total Jobs:** 8

#### **advanced-analysis.yml** - Advanced Analysis Methods
- **Trigger:** Push, PR, weekly Friday 10:00 UTC, manual
- **Purpose:** Advanced mathematical and theoretical analysis
- **Matrix:**
  - Python: 3.11, 3.12
  - Methods: analisis_avanzado, analisis_estadistico_avanzado, analisis_noesico, campo_conciencia
- **Additional Jobs:** Algebraic tower, discrete symmetry, Acto III quantum
- **Total Jobs:** 14

#### **special-analysis.yml** - Special Analysis Methods
- **Trigger:** Push, PR, weekly Saturday 14:00 UTC, manual
- **Purpose:** Specialized analysis tools
- **Jobs:**
  - PyCBC analysis (2 Python versions)
  - SAGE protocol (2 Python versions)
  - EVAC potential (2 Python versions)
  - GWTC-1 systematic search (2 Python versions)
  - Corrections and derivations (2 Python versions)
- **Total Jobs:** 10

### 4. Testing Workflows

#### **comprehensive-testing.yml** - Comprehensive Testing Suite
- **Trigger:** Push, PR, daily at 00:00 UTC, manual
- **Purpose:** Complete test coverage
- **Matrix:**
  - Unit tests: Linux + macOS × Python 3.11, 3.12 = 4 jobs
  - Integration tests: 4 test suites × 2 Python versions = 8 jobs
  - Performance tests: 2 Python versions
- **Total Jobs:** 14+

### 5. Automation & Monitoring Workflows

#### **master-orchestration.yml** - Master Workflow Orchestration
- **Trigger:** Manual, weekly Sunday 00:00 UTC
- **Purpose:** Coordinate execution of all workflows
- **Features:**
  - Selective workflow triggering
  - Configurable via workflow_dispatch inputs
  - Triggers all 8 main validation/analysis workflows

#### **workflow-health-check.yml** - Workflow Health Monitoring
- **Trigger:** Manual, daily at 08:00 UTC
- **Purpose:** Monitor health of all workflows
- **Features:**
  - Checks status of all workflows
  - Dependency health check
  - Security vulnerability scanning
  - Generates comprehensive health report

#### **update_coherence_visualization.yml** - Auto-Update Coherence Visualization
- **Trigger:** Push, manual, daily at 00:00 UTC
- **Purpose:** Generate and commit coherence visualization
- **Python Version:** 3.9

#### **dependency-health.yml** - Dependency Health Check
- **Trigger:** Weekly Wednesday 10:00 UTC, manual, PR on requirements.txt
- **Purpose:** Monitor dependency security and updates
- **Features:**
  - pip-audit security scanning
  - Outdated package detection
  - Python 3.11 & 3.12 compatibility testing
  - Auto-create issues for vulnerabilities

### 6. Project Management Workflows

#### **workflow-intelligence.yml** - Workflow Intelligence
- **Trigger:** Various events
- **Purpose:** Automated workflow management and optimization

#### **pr-review-automation.yml** - PR Review Automation
- **Trigger:** Pull requests
- **Purpose:** Automated code review

#### **issue-management.yml** - Issue Management
- **Trigger:** Issue events
- **Purpose:** Automated issue handling

#### **auto-label.yml** - Auto-Labeling
- **Trigger:** PR/Issue events
- **Purpose:** Automatic label assignment

#### **auto-update-docs.yml** - Auto-Update Documentation
- **Trigger:** Push to main
- **Purpose:** Keep documentation synchronized

#### **create-labels.yml** - Create Standard Labels
- **Trigger:** Manual
- **Purpose:** Initialize repository labels

## 🎯 Matrix Strategy Benefits

All validation and analysis workflows use **matrix strategies** for:

1. **Parallel Execution:** Run multiple configurations simultaneously
2. **Python Version Coverage:** Test both 3.11 (production) and 3.12 (future-proofing)
3. **Cross-Platform Testing:** Some workflows test on Linux and macOS
4. **Multiple Validation Methods:** Run different validation approaches in parallel

## 📊 Workflow Statistics

- **Total Workflows:** 18
- **Validation Workflows:** 4
- **Analysis Workflows:** 4
- **Testing Workflows:** 1
- **Orchestration Workflows:** 2
- **Automation Workflows:** 7
- **Total Parallel Jobs:** 90+ (with all matrix combinations)
- **Python Versions Tested:** 2 (3.11, 3.12)
- **Operating Systems Tested:** 2 (Ubuntu, macOS)

## 🚀 Usage

### Run Individual Workflow

From the GitHub Actions tab, select any workflow and click "Run workflow".

### Run All Workflows (Orchestrated)

1. Go to Actions → Master Workflow Orchestration
2. Click "Run workflow"
3. Select which workflow categories to run (or run all)
4. Click "Run workflow" to start

### Check Workflow Health

1. Go to Actions → Workflow Health Check
2. Click "Run workflow"
3. View the generated health report

## 🔐 Required Secrets

Some workflows require repository secrets:

- `HF_TOKEN`: For Hugging Face dataset uploads (production-qcal.yml)
- `DOCKERHUB_TOKEN`: For Docker Hub image pushes (production-qcal.yml)
- `DOCKERHUB_USERNAME`: Docker Hub username (production-qcal.yml)

Add these in: Settings → Secrets and variables → Actions

## ⚡ Performance Optimizations

All workflows include:

- **Caching:** pip dependencies cached per Python version
- **Parallel Execution:** Matrix strategies for simultaneous runs
- **Data Caching:** GWOSC data cached to avoid re-downloads
- **Conditional Execution:** continue-on-error for non-critical steps
- **Resource Management:** Proper timeouts and retention policies

## 📝 Cron Schedule Summary

| Time (UTC) | Workflow | Frequency |
|------------|----------|-----------|
| 00:00 | Coherence Visualization | Daily |
| 00:00 | Comprehensive Testing | Daily |
| 00:00 | Master Orchestration | Weekly (Sunday) |
| 02:00 | Scientific Validation | Daily |
| 04:00 | Detector Analysis | Daily |
| 06:00 | Quantum Validations | Daily |
| 08:00 | Alternative Validations | Weekly (Monday) |
| 08:00 | Workflow Health Check | Daily |
| 10:00 | Dependency Health | Weekly (Wednesday) |
| 10:00 | Advanced Analysis | Weekly (Friday) |
| 12:00 | Multi-Event Analysis | Twice Daily |
| 14:00 | Special Analysis | Weekly (Saturday) |
| */4 hours | Production QCAL | Every 4 hours |

## 🎭 Workflow Dependencies

```
master-orchestration.yml
    ├─→ quantum-validations.yml
    ├─→ alternative-validations.yml
    ├─→ multi-event-analysis.yml
    ├─→ detector-analysis.yml
    ├─→ scientific-validation.yml
    ├─→ advanced-analysis.yml
    ├─→ special-analysis.yml
    └─→ comprehensive-testing.yml

workflow-health-check.yml
    └─→ (monitors all workflows)

analyze.yml
    └─→ (CI/CD for PRs and pushes)

production-qcal.yml
    └─→ (production deployment)
```

## 🌟 Best Practices

1. **Always test locally first** before relying on CI/CD
2. **Use workflow_dispatch** for manual testing
3. **Check workflow health** regularly
4. **Monitor artifact storage** (cleanup old artifacts)
5. **Review security alerts** from dependency-health workflow
6. **Keep Python versions updated** (currently 3.11 & 3.12)

## 🔍 Troubleshooting

### Workflow Fails

1. Check the workflow logs in Actions tab
2. Look for specific error messages
3. Check if dependencies need updating
4. Verify system dependencies are installed

### All Workflows Failing

1. Run workflow-health-check.yml
2. Check dependency-health.yml for issues
3. Verify requirements.txt is valid
4. Check GitHub Actions status page

### Specific Validation Fails

1. Check if validation script exists
2. Verify input data availability
3. Check for missing dependencies
4. Review validation logic

## 📚 Documentation References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Matrix Strategy Guide](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Caching Dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)

## 🎯 Success Criteria

All workflows are considered "green" when:

- ✅ All validation scripts pass
- ✅ All tests pass with 100% success rate
- ✅ No security vulnerabilities in dependencies
- ✅ All Python versions (3.11 & 3.12) compatible
- ✅ Cross-platform compatibility (Linux, macOS)
- ✅ Artifacts generated successfully
- ✅ No workflow failures in last 7 days

---

**Last Updated:** 2025-10-26

**Maintained by:** GW250114 Analysis Team

**License:** MIT
