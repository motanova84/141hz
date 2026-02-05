# Biological Periodicity and Environmental Data Integration

## Overview

This module extends the 141Hz quantum resonance framework to analyze biological periodicities across multiple species and integrates real-world environmental data from NOAA and NASA POWER APIs.

## 🌟 Features

### 1. Real-World Data APIs
- **NASA POWER API**: Access to global solar, meteorological, and agricultural data
- **NOAA Climate Data Online (CDO)**: Historical and real-time climate data from weather stations worldwide
- Automated data fetching, caching, and validation

### 2. Multi-Species Analysis
- **Arabidopsis thaliana**: Circadian rhythms, ultradian rhythms, photoperiod responses
- **Trichogramma**: Developmental cycles (egg, larva, pupa, adult stages)
- **Human**: Circadian, ultradian, and physiological rhythms
- Extensible framework for adding new species

### 3. Reproducible Notebooks
- **Google Colab**: One-click execution in the cloud
- **Binder**: Interactive Jupyter environment without local installation
- **JupyterHub**: Compatible with institutional computing platforms
- Full documentation and examples included

### 4. Peer Review Ready
- Automated validation tests
- Data quality checks
- Reproducibility verification
- LaTeX manuscript template for arXiv/PNAS submission

## 📦 Installation

### Local Installation

```bash
# Clone repository
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Install dependencies
pip install -r requirements.txt

# Set up API credentials (optional)
export NOAA_API_TOKEN="your_token_here"
```

### Cloud Execution

**Google Colab**: Click the badge in the notebook  
**Binder**: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/motanova84/141hz/main?filepath=notebooks/biological_rhythms_environmental_data.ipynb)

## 🚀 Quick Start

### 1. Run Biological Analysis

```python
from scripts.biological_periodicity import ArabidopsisAnalyzer

# Analyze Arabidopsis circadian rhythms
analyzer = ArabidopsisAnalyzer()
results = analyzer.analyze_all_periods()

# Display harmonic relationships
for rhythm, data in results['periods'].items():
    print(f"{rhythm}: Harmonic n={data['nearest_harmonic']}")
```

### 2. Fetch Environmental Data

```python
from scripts.api_clients import NASAPowerAPIClient

# Initialize NASA POWER client
client = NASAPowerAPIClient()

# Fetch agricultural data
data = client.get_agricultural_data(
    latitude=32.8875,   # Salk Institute
    longitude=-117.2426,
    start_date='20240101',
    end_date='20240131'
)
```

### 3. Run Validation Tests

```bash
cd scripts
python test_biological_periodicity.py
```

## 📊 Data Sources

### NASA POWER API
- **URL**: https://power.larc.nasa.gov/
- **Coverage**: Global
- **Resolution**: Daily
- **Parameters**: Temperature, solar radiation, humidity, precipitation
- **License**: Public domain (NASA data policy)
- **Authentication**: None required

### NOAA Climate Data Online
- **URL**: https://www.ncdc.noaa.gov/cdo-web/
- **Coverage**: Global weather stations
- **Resolution**: Hourly to monthly
- **Authentication**: Free API token required
- **Sign up**: https://www.ncdc.noaa.gov/cdo-web/token

## 🔬 Scientific Methods

### Harmonic Analysis

For each biological period T (in hours), we calculate:

1. **Frequency**: `f = 1 / (T × 3600)` Hz
2. **Harmonic ratio**: `r = f₀ / f` where f₀ = 141.7001 Hz
3. **Nearest harmonic**: `n = round(r)`
4. **Deviation**: `δ = |r - n| / n`

A period is considered harmonic if δ < 0.01 (within 1%).

### Species Analyzed

| Species | Rhythms | Reference |
|---------|---------|-----------|
| *Arabidopsis thaliana* | Circadian (24h), Ultradian (3h, 8h) | McClung (2006) |
| *Trichogramma* | Developmental cycles (24h, 48h, 96h, 168h) | Cônsoli & Parra (1999) |
| *Homo sapiens* | Circadian (24h), Ultradian (1.5h) | Various |

## 📝 Academic Paper

A complete manuscript template is provided in `papers/biological_periodicity_arxiv.tex`.

### Compilation

```bash
cd papers
pdflatex biological_periodicity_arxiv.tex
bibtex biological_periodicity_arxiv
pdflatex biological_periodicity_arxiv.tex
pdflatex biological_periodicity_arxiv.tex
```

### Submission to arXiv

1. Review and customize the manuscript
2. Compile to PDF
3. Submit to arXiv category: q-bio.QM (Quantitative Methods) or physics.bio-ph (Biological Physics)
4. Include data availability statement and GitHub link

## 🧪 Validation and Testing

### Automated Tests

```bash
# Run all validation tests
python scripts/test_biological_periodicity.py

# Expected output:
# ✓ API Clients validated
# ✓ Biological Analysis validated
# ✓ Harmonic Accuracy validated
# ✓ Data Quality validated
```

### Manual Verification

1. **Open the Jupyter notebook**: `notebooks/biological_rhythms_environmental_data.ipynb`
2. **Run all cells**: Kernel → Restart & Run All
3. **Check outputs**: Verify plots and statistical summaries
4. **Review validation report**: Check `validation_report.json`

## 📚 References

1. McClung, C.R. (2006). Plant Circadian Rhythms. *Plant Cell* 18(4): 792-803
2. Cônsoli, F.L. & Parra, J.R.P. (1999). Trichogramma biology. *Ann. Entomol. Soc. Am.* 92(4): 491-498
3. NASA POWER Project: https://power.larc.nasa.gov/
4. NOAA CDO: https://www.ncdc.noaa.gov/cdo-web/

## 🤝 Contributing

Contributions are welcome! To add a new species:

1. Add periodicities to `KNOWN_PERIODS` in `biological_periodicity.py`
2. Create a specialized analyzer class (see `ArabidopsisAnalyzer` example)
3. Add tests to `test_biological_periodicity.py`
4. Update documentation

## 📄 License

- **Code**: MIT License
- **Documentation**: CC-BY 4.0
- **Data**: Respective licenses (NASA: public domain, NOAA: public domain)

## 📧 Contact

**Author**: José Manuel Mota Burruezo  
**Email**: jmmb@concienciacuantica.org  
**Repository**: https://github.com/motanova84/141hz  
**DOI**: 10.5281/zenodo.17445017

## 🙏 Acknowledgments

- NASA POWER team for providing open environmental data
- NOAA for climate data access
- Open-source scientific computing community
- Binder and Google Colab for reproducible computing infrastructure
