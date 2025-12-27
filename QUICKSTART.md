# ⚡ Quick Start Guide - 15 Minutes to First Analysis

Get up and running with GW250114-141Hz Analysis in just 15 minutes with these 5 simple commands.

## 🎯 Prerequisites

- **Python 3.11 or 3.12** installed
- **5 GB free disk space** (for dependencies and test data)
- **Internet connection** (for dependency installation)
- **Terminal/Command line** access

Check your Python version:
```bash
python3 --version  # Should show 3.11.x or 3.12.x
```

If you need to install Python 3.11+:
- **Ubuntu/Debian**: `sudo apt install python3.11 python3.11-venv`
- **macOS**: `brew install python@3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

## 🚀 5-Command Quick Start

### 1. Clone Repository (30 seconds)

```bash
git clone https://github.com/motanova84/141hz.git && cd 141hz
```

**What it does**: Downloads the complete project to your local machine and enters the directory.

---

### 2. Create Virtual Environment (1 minute)

```bash
python3 -m venv venv && source venv/bin/activate
```

**Windows users**: Replace `source venv/bin/activate` with `venv\Scripts\activate`

**What it does**: Creates an isolated Python environment to avoid conflicts with system packages.

**Tip**: You should see `(venv)` prefix in your terminal prompt when activated.

---

### 3. Install Dependencies (3-5 minutes)

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**What it does**: Installs all required Python packages (numpy, scipy, matplotlib, gwpy, etc.).

**Note**: This may take several minutes depending on your internet speed.

**Alternative** (if pip install fails due to network issues):
```bash
make setup  # Uses make with timeout handling
```

---

### 4. Generate Test Data (1 minute)

```bash
make test-data
```

**What it does**: 
- Attempts to download real GWOSC gravitational wave data
- Falls back to generating synthetic test data if download fails
- Creates `data/` directory with sample event data

**For real data** (requires internet and confirmation):
```bash
make data  # Interactive: asks for confirmation
# or
make data-force  # Non-interactive: downloads without asking
```

---

### 5. Run Analysis (2-5 minutes)

```bash
make analyze
```

**What it does**: Runs the complete analysis pipeline:
1. Spectral analysis at 141.7001 Hz
2. Multi-detector coherence check
3. Statistical significance calculations
4. Generates figures and JSON results

**Output location**: 
- **Figures**: `results/figures/*.png`
- **Data**: `results/*.json`
- **Logs**: Terminal output

---

## 📊 View Your Results

After running the analysis, check the results:

```bash
# List all generated figures
ls -lh results/figures/

# View results summary
cat results/analysis_summary.json

# Or open figures with default viewer
open results/figures/spectral_analysis_141hz.png  # macOS
xdg-open results/figures/spectral_analysis_141hz.png  # Linux
start results/figures/spectral_analysis_141hz.png  # Windows
```

**Expected output**:
- `spectral_analysis_141hz.png` - Power spectral density around 141.7 Hz
- `multi_detector_coherence.png` - H1/L1/V1 correlation
- `significance_distribution.png` - Statistical significance plot
- `analysis_summary.json` - Numerical results

---

## 🎉 Success! What's Next?

Congratulations! You've completed your first gravitational wave analysis at 141.7 Hz.

### Next Steps

**Explore validation scripts**:
```bash
make validate  # Run all validation pipelines
make test-3-pilares  # Test the 3 pillars (empirical, formal, LLM)
```

**Interactive experience**:
```bash
make listen  # "Ahora te toca escuchar" - interactive discovery
```

**Advanced analysis**:
```bash
make multi-event-snr  # Analyze multiple GWTC events
make busqueda-gwtc1  # Systematic GWTC-1 search
```

### 📚 Documentation

- **Full Documentation**: [README.md](README.md)
- **Scientific Standards**: [DISCOVERY_STANDARDS.md](DISCOVERY_STANDARDS.md)
- **Release Notes**: [RELEASE_NOTES_V1.md](RELEASE_NOTES_V1.md)
- **3 Pillars Method**: [README_SECTION_3_PILARES.md](README_SECTION_3_PILARES.md)

### 🧪 Run Tests

Verify everything is working correctly:

```bash
# Run unit tests
python -m pytest tests/ -v

# Run specific test
python tests/test_security_no_tokens.py

# Run integration tests
make test-multievento
make test-discovery-standards
```

### 🐳 Docker Alternative

If you prefer Docker instead of local installation:

```bash
# Pull CPU image
docker pull ghcr.io/motanova84/141hz:v1.0.0

# Run analysis in container
docker run --rm -v $(pwd)/results:/app/results ghcr.io/motanova84/141hz:v1.0.0 make analyze

# View results in local results/ directory
```

**GPU support**:
```bash
docker pull ghcr.io/motanova84/141hz:v1.0.0-gpu
docker run --gpus all --rm -v $(pwd)/results:/app/results ghcr.io/motanova84/141hz:v1.0.0-gpu
```

### ☁️ Google Colab (Zero Installation)

Try the analysis in your browser without any installation:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/motanova84/141hz/blob/main/notebooks/quickstart.ipynb)

**Features**:
- No local installation required
- Free GPU access (limited hours)
- Interactive notebooks with visualizations
- Simulated data by default (real data optional)

---

## 🛠️ Troubleshooting

### Problem: `python3: command not found`

**Solution**: Install Python 3.11+ (see Prerequisites section)

---

### Problem: `pip install` fails with SSL errors

**Solution**: Try with timeout and retry:
```bash
pip install --timeout 60 --retries 3 -r requirements.txt
```

Or install critical packages only:
```bash
pip install numpy scipy matplotlib gwpy
```

---

### Problem: `make: command not found`

**Solution**: 
- **Ubuntu/Debian**: `sudo apt install make`
- **macOS**: `xcode-select --install`
- **Windows**: Install [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm)

Alternatively, run commands directly:
```bash
python scripts/analizar_ringdown.py
python scripts/analizar_l1.py
```

---

### Problem: Out of memory during analysis

**Solution**: Use test data instead of real data:
```bash
# Generate smaller synthetic dataset
make test-data

# Or analyze single event
python scripts/analizar_ringdown.py --event GW150914 --duration 32
```

---

### Problem: No results generated

**Solution**: Check for errors in the log:
```bash
make analyze 2>&1 | tee analysis.log
cat analysis.log | grep -i error
```

Check data availability:
```bash
make check-data
```

---

### Problem: Permission denied errors

**Solution**: Ensure you have write permissions:
```bash
chmod +x scripts/*.py
mkdir -p results/figures
chmod -R u+w results/
```

---

## 📧 Get Help

Still stuck? Here's how to get help:

1. **Check existing issues**: https://github.com/motanova84/141hz/issues
2. **Open a new issue**: Include error messages and system info
3. **Discussions**: https://github.com/motanova84/141hz/discussions
4. **Documentation**: Check [README.md](README.md) for detailed guides

**System info to include**:
```bash
python3 --version
pip --version
uname -a  # Linux/macOS
systeminfo  # Windows
```

---

## 🎓 Learning Resources

### Understanding the Analysis

- **What is 141.7001 Hz?**: See [PAPER.md](PAPER.md) for theoretical background
- **Gravitational Waves 101**: [LIGO Science Education](https://www.ligo.caltech.edu/page/educational-resources)
- **GWOSC Tutorial**: [GWOSC Tutorials](https://gwosc.org/tutorial/)

### Python for Science

- **NumPy**: https://numpy.org/doc/stable/user/quickstart.html
- **SciPy**: https://docs.scipy.org/doc/scipy/tutorial/
- **Matplotlib**: https://matplotlib.org/stable/tutorials/index.html
- **GWpy**: https://gwpy.github.io/docs/stable/

### Reproducible Research

- **Zenodo**: https://zenodo.org
- **FAIR Principles**: https://www.go-fair.org/fair-principles/
- **Reproducibility Guide**: [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)

---

## ⏱️ Estimated Times

Summary of time for each step:

| Step | Time | Notes |
|------|------|-------|
| Clone repository | 30s | Depends on internet speed |
| Create venv | 1min | Very fast |
| Install dependencies | 3-5min | Main bottleneck |
| Generate test data | 1min | Real data: 2-10min |
| Run analysis | 2-5min | Depends on CPU |
| **Total** | **~10-15min** | **First-time setup** |

**Subsequent runs**: ~2-5 minutes (skip steps 1-3)

---

## 🚀 Ready for Production?

Once you're comfortable with the quick start:

1. **Run full validation**: `make validate` (~10-30 minutes)
2. **Generate release package**: See [RELEASE_NOTES_V1.md](RELEASE_NOTES_V1.md)
3. **Set up CI/CD**: See [.github/workflows/](. github/workflows/)
4. **Deploy Docker**: See [Dockerfile](Dockerfile) and [Dockerfile.gpu](Dockerfile.gpu)

---

## 📄 License & Citation

**Software**: MIT License - See [LICENSE](LICENSE)

**Citation** (if you use this in research):
```bibtex
@software{motaburruezo2025gw141hz,
  author = {Mota Burruezo, José Manuel},
  title = {GW250114-141Hz Analysis: Quantum Gravity Analysis of Gravitational Waves},
  year = 2025,
  version = {v1.0.0},
  doi = {10.5281/zenodo.17445017},
  url = {https://doi.org/10.5281/zenodo.17445017}
}
```

---

**Last Updated**: 2025-01-01  
**Version**: v1.0.0  
**Feedback**: Open an issue or discussion on GitHub

*¡Bienvenido al análisis de ondas gravitacionales!* 🌌
