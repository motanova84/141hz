# Detection of a 141.7 Hz Spectral Component in GW150914

[![CI Analysis](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/analyze.yml/badge.svg)](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/analyze.yml)
[![Repository Verification](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/verify.yml/badge.svg)](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/verify.yml)
[![DOI](https://zenodo.org/badge/DOI/pending-zenodo.svg)](https://doi.org/pending-zenodo)

Scientific reproducible repository for detecting and analyzing a spectral component at 141.7001 Hz in the gravitational wave event GW150914, based on the predictions of the Noetic Unified Theory.

## 🌊 Overview

This repository implements a complete scientific workflow for detecting spectral components in gravitational wave data from LIGO's GW150914 event. The analysis focuses on the ringdown phase where theoretical predictions suggest the presence of a specific frequency signature at 141.7 Hz.

## 🚀 Automated Workflows

The repository includes comprehensive GitHub Actions workflows that automatically:

- **📊 Analysis Pipeline** (`analyze.yml`): Downloads data, performs spectral analysis, and generates figures
- **🔍 Verification** (`verify.yml`): Validates repository structure and script functionality  
- **🔐 Permissions** (`permissions.yml`): Configures security settings for automated workflows

## 📁 Repository Structure

```
├── scripts/
│   ├── descargar_datos.py     # Download GW150914 data from GWOSC
│   ├── analisis_avanzado.py   # Advanced H1 detector analysis
│   ├── analizar_l1.py         # L1 detector comparative analysis
│   ├── analizar_ringdown.py   # Ringdown phase analysis
│   └── analisis_noesico.py    # Noetic theory predictions
├── .github/workflows/         # Automated CI/CD workflows
├── CITATION.cff              # Citation metadata for Zenodo
├── .zenodo.json             # Zenodo publication metadata
└── verify_repository.sh     # Repository validation script
```

## 🔬 Manual Usage

### Prerequisites
- Python 3.9+
- Internet connection for data download

### Local Installation
```bash
# Clone repository
git clone https://github.com/motanova84/gw250114-141hz-analysis.git
cd gw250114-141hz-analysis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Analysis
```bash
# Download GW150914 data
python scripts/descargar_datos.py

# Run advanced H1 analysis
python scripts/analisis_avanzado.py

# Run L1 comparative analysis
python scripts/analizar_l1.py

# Verify repository status
./verify_repository.sh
```

Results are automatically saved in `results/figures/` directory.

## 📊 Scientific Results

The analysis generates:
- **H1 Spectral Analysis**: Advanced ringdown analysis with 141.7 Hz focus
- **L1 Comparative Study**: Cross-detector validation
- **Q-Transform Spectrograms**: Time-frequency evolution
- **SNR Measurements**: Statistical significance assessment

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@software{mota_burruezo_2025,
  author = {Mota Burruezo, José Manuel},
  title = {Detection of a 141.7 Hz Spectral Component in GW150914},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/motanova84/gw250114-141hz-analysis}
}
```

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a scientific research repository. For questions or contributions, please open an issue or contact the author.

---

**Author**: José Manuel Mota Burruezo  
**Affiliation**: Instituto de Conciencia Cuántica  
**Research Focus**: Gravitational wave spectral analysis and Noetic Unified Theory applications
