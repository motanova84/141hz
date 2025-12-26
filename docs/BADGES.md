# Badge Documentation

This document describes all badges used in README.md and ensures they are real, functional, and accurately represent the project status.

## Badge Inventory

### 1. Continuous Integration / Continuous Deployment

#### CI Badge
- **Badge:** `![CI](https://github.com/motanova84/141hz/actions/workflows/analyze.yml/badge.svg)`
- **Type:** Dynamic
- **Status:** ✅ Working
- **Purpose:** Shows the status of the CI/CD pipeline (tests and analysis)
- **Workflow:** `.github/workflows/analyze.yml`
- **Updates:** Automatically on every push/PR
- **Link:** https://github.com/motanova84/141hz/actions/workflows/analyze.yml

#### CD Badge
- **Badge:** `![CD](https://github.com/motanova84/141hz/actions/workflows/production-qcal.yml/badge.svg)`
- **Type:** Dynamic
- **Status:** ✅ Working
- **Purpose:** Shows the status of the production deployment pipeline
- **Workflow:** `.github/workflows/production-qcal.yml`
- **Updates:** Automatically every 4 hours or on manual trigger
- **Link:** https://github.com/motanova84/141hz/actions/workflows/production-qcal.yml

### 2. License

#### MIT License Badge
- **Badge:** `![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)`
- **Type:** Static
- **Status:** ✅ Working
- **Purpose:** Indicates the project uses MIT License
- **File:** `LICENSE` (verified to exist)
- **Link:** None (informational only)

### 3. Technology Stack

#### Python Version Badge
- **Badge:** `![Python](https://img.shields.io/badge/python-3.11+-blue.svg)`
- **Type:** Static
- **Status:** ✅ Working
- **Purpose:** Shows minimum Python version required
- **Verified Against:**
  - `.github/workflows/analyze.yml` → Python 3.11 ✅
  - `.github/workflows/production-qcal.yml` → Python 3.11 ✅
  - `.github/workflows/update_coherence_visualization.yml` → Python 3.11 ✅
- **Consistency:** All workflows now use Python 3.11

#### GWPy Version Badge
- **Badge:** `[![GWPy](https://img.shields.io/badge/GWPy-3.0+-green)](https://gwpy.github.io/)`
- **Type:** Static with link
- **Status:** ✅ Working
- **Purpose:** Shows GWPy library version used
- **Verified Against:** `requirements.txt` → `gwpy>=3.0.0` ✅
- **Link:** https://gwpy.github.io/
- **Note:** Changed from "3.0.13" to "3.0+" to reflect version range

### 4. Quality and Reproducibility

#### Reproducibility Badge
- **Badge:** `![Reproducible](https://img.shields.io/badge/reproducibility-100%25-success)`
- **Type:** Static
- **Status:** ✅ Working
- **Purpose:** Statement badge indicating 100% reproducibility commitment
- **Evidence:**
  - Docker container available
  - All code in version control
  - Public data sources (GWOSC)
  - Automated CI/CD pipeline
  - requirements.txt with pinned versions

### 5. Academic and Research

#### Zenodo DOI Badge
- **Badge:** `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17379721.svg)](https://doi.org/10.5281/zenodo.17379721)`
- **Type:** Dynamic (Zenodo-generated)
- **Status:** ✅ Working
- **Purpose:** Provides permanent identifier for citation
- **DOI:** 10.5281/zenodo.17379721
- **Link:** https://doi.org/10.5281/zenodo.17379721
- **Note:** Zenodo DOI format is correct; badge is official Zenodo SVG

#### Open Science Badge
- **Badge:** `[![Open Science](https://img.shields.io/badge/Open-Science-brightgreen)](https://www.fosteropenscience.eu/)`
- **Type:** Static with link
- **Status:** ✅ Working
- **Purpose:** Declares commitment to open science principles
- **Link:** https://www.fosteropenscience.eu/

### 6. Accessibility

#### AI Accessible Badge
- **Badge:** `[![AI Accessible](https://img.shields.io/badge/AI-Accessible-blueviolet)](AI_ACCESSIBILITY.md)`
- **Type:** Static with local link
- **Status:** ✅ Working
- **Purpose:** Indicates full AI accessibility
- **File:** `AI_ACCESSIBILITY.md` (verified to exist)
- **Link:** Local file in repository

### 7. Interactive Tools

#### Google Colab Badge
- **Badge:** `[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/motanova84/141hz/blob/main/notebooks/141hz_validation.ipynb)`
- **Type:** Dynamic (Google-generated)
- **Status:** ✅ Working
- **Purpose:** One-click access to run analysis in Google Colab
- **Notebook:** `notebooks/141hz_validation.ipynb` (verified to exist)
- **Link:** https://colab.research.google.com/github/motanova84/141hz/blob/main/notebooks/141hz_validation.ipynb

### 8. Funding

#### GitHub Sponsors Badge
- **Badge:** `[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-❤️-ff69b4)](https://github.com/sponsors/motanova84)`
- **Type:** Static with link
- **Status:** ✅ Working
- **Purpose:** Provides funding support link
- **Configuration:** `.github/FUNDING.yml` (verified to exist)
- **Link:** https://github.com/sponsors/motanova84
- **Note:** Appears multiple times in README (top and funding section)

## Badge Validation

All badges have been validated using `scripts/validate_badges.py`:

```bash
python3 scripts/validate_badges.py
```

**Validation Results:**
- ✅ All workflow files exist
- ✅ License file exists
- ✅ Documentation files exist
- ✅ Python versions are consistent (3.11)
- ✅ GWPy version matches requirements
- ✅ All badge URLs are properly formatted
- ✅ All linked resources are accessible

## Maintenance

### When to Update Badges

1. **Python Version Badge**
   - Update when minimum Python version changes
   - Must match all workflow files
   - Update analyze.yml, production-qcal.yml, and other workflows

2. **GWPy Version Badge**
   - Update when minimum GWPy version in requirements.txt changes
   - Use version range (e.g., "3.0+") not specific version

3. **CI/CD Badges**
   - Automatically updated by GitHub Actions
   - No manual intervention needed
   - Check if workflow file is renamed

4. **DOI Badge**
   - Update when new Zenodo version is released
   - Format: `10.5281/zenodo.XXXXXXX`
   - Badge URL and link URL must match

### Badge Consistency Checks

Run the validation script regularly:

```bash
# Validate all badges
python3 scripts/validate_badges.py

# Add to CI pipeline
- name: Validate badges
  run: python3 scripts/validate_badges.py
```

## Badge Best Practices

1. **Use Dynamic Badges When Possible**
   - GitHub Actions badges update automatically
   - Zenodo badges reflect latest version
   - Shields.io supports many dynamic sources

2. **Link Badges to Resources**
   - Badges should be clickable when relevant
   - Link to workflow runs, documentation, external sites

3. **Keep Badges Accurate**
   - Version numbers must match actual requirements
   - Status badges should reflect real state
   - Remove badges for removed features

4. **Badge Placement**
   - Important badges at top of README
   - Group related badges together
   - Don't overcrowd with too many badges

## Troubleshooting

### Badge Not Showing

1. Check image URL is accessible
2. Verify badge syntax: `![Alt](image-url)` or `[![Alt](image-url)](link-url)`
3. For GitHub Actions badges, ensure workflow file exists
4. Clear browser cache

### Badge Shows Wrong Status

1. For CI/CD badges: Check workflow run history
2. For version badges: Verify against source files
3. For DOI badges: Verify DOI exists on Zenodo

### Badge Link Broken

1. Verify target file/URL exists
2. Check for typos in file paths
3. For external links, check domain is accessible
4. For workflow links, ensure workflow file name matches

## References

- [Shields.io](https://shields.io/) - Badge generation service
- [GitHub Actions Badges](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)
- [Zenodo DOI](https://zenodo.org/)
- [Google Colab](https://colab.research.google.com/)

---

<!-- NOTE: Update the "Last Updated" date manually, or consider automating this field to prevent it from becoming stale. -->
**Last Updated:** 2025-10-26  
**Validated By:** scripts/validate_badges.py  
**Status:** ✅ All badges working correctly
