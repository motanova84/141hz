# LaTeX Paper Compilation Guide

This guide provides detailed instructions for compiling the "Coherencia Universal" LaTeX paper.

## Quick Start

### Option 1: Using Overleaf (Recommended - No Installation Required)

1. Visit [Overleaf](https://www.overleaf.com)
2. Create a free account or log in
3. Click "New Project" → "Upload Project"
4. Create a ZIP file with the papers directory:
   ```bash
   cd /path/to/141hz
   zip -r coherencia-universal.zip papers/
   ```
5. Upload the ZIP file to Overleaf
6. The paper will compile automatically
7. Download the PDF from the Overleaf interface

### Option 2: Local Compilation (Requires LaTeX Installation)

#### Prerequisites

Install a LaTeX distribution for your operating system:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**macOS:**
```bash
# Using Homebrew
brew install --cask mactex

# Or download from: https://www.tug.org/mactex/
```

**Windows:**
- Download and install [MiKTeX](https://miktex.org/download)
- Or download [TeX Live](https://www.tug.org/texlive/)

#### Compilation Commands

**Method 1: Using the provided script**
```bash
cd papers/
./compile.sh
```

**Method 2: Using Make**
```bash
cd papers/
make
```

**Method 3: Manual compilation**
```bash
cd papers/
pdflatex paper_definitivo.tex
pdflatex paper_definitivo.tex  # Run twice for references
```

**Method 4: With bibliography (full compilation)**
```bash
cd papers/
pdflatex paper_definitivo.tex
bibtex paper_definitivo
pdflatex paper_definitivo.tex
pdflatex paper_definitivo.tex
```

## Required LaTeX Packages

The paper requires the following LaTeX packages (usually included in full TeX distributions):

- `babel` (Spanish language support)
- `geometry` (page layout)
- `amsmath`, `amssymb`, `amsfonts` (mathematical symbols and equations)
- `graphicx` (figure inclusion)
- `hyperref` (hyperlinks and PDF metadata)
- `booktabs` (professional tables)
- `fancyhdr` (custom headers/footers)
- `inputenc` (UTF-8 encoding)

If you're missing packages, most distributions will offer to install them automatically during compilation.

## Troubleshooting

### Problem: "Package not found" errors

**Solution:** Install the missing package or use a full TeX distribution:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# MiKTeX (Windows) - usually auto-installs packages
# Check: Settings → Packages → Install missing packages on-the-fly
```

### Problem: "File not found: figures/gw_spectrum.png"

**Solution:** Ensure you have the figures in the correct location:
```bash
cd papers/
ls -l figures/
# Should show: gw_spectrum.png, llm_architecture.png
```

If figures are missing, they should be generated or copied from the repository:
```bash
# From repository root
cp gw_spectral_evidence.png papers/figures/gw_spectrum.png
cp comparative_benchmarks.png papers/figures/llm_architecture.png
```

### Problem: Compilation hangs or shows errors

**Solution 1:** Clean auxiliary files and recompile
```bash
cd papers/
make clean
make
```

**Solution 2:** Check the log file for specific errors
```bash
cd papers/
cat paper_definitivo.log | grep -i error
```

### Problem: PDF not generated

**Solution:** Try interactive mode to see errors:
```bash
cd papers/
pdflatex paper_definitivo.tex
# Don't use -interaction=nonstopmode to see errors
```

## Output Files

After successful compilation, you'll find:

- **`paper_definitivo.pdf`** - The final paper (main output)
- `paper_definitivo.aux` - Auxiliary file for references
- `paper_definitivo.log` - Compilation log
- `paper_definitivo.out` - Hyperref metadata
- `paper_definitivo.bbl` - Bibliography (if using BibTeX)

Only the `.pdf` file is needed for distribution.

## Cleaning Up

To remove auxiliary files:
```bash
cd papers/
make clean
# or
./compile.sh clean
```

To remove all generated files including PDF:
```bash
cd papers/
make distclean
# or
./compile.sh distclean
```

## Alternative: Docker-based Compilation

If you prefer not to install LaTeX locally, you can use a Docker container:

```bash
# Using official TeX Live Docker image
docker run --rm -v $(pwd):/data \
    texlive/texlive:latest \
    pdflatex -output-directory=/data /data/paper_definitivo.tex
```

## Viewing the PDF

**Linux:**
```bash
xdg-open paper_definitivo.pdf
```

**macOS:**
```bash
open paper_definitivo.pdf
```

**Windows:**
```powershell
start paper_definitivo.pdf
```

Or use any PDF viewer of your choice.

## Paper Statistics

After compilation, you can check paper statistics:

```bash
# Word count (approximate)
pdftotext paper_definitivo.pdf - | wc -w

# Page count
pdfinfo paper_definitivo.pdf | grep Pages

# File size
ls -lh paper_definitivo.pdf
```

## Additional Resources

- **LaTeX Documentation:** https://www.latex-project.org/help/documentation/
- **Overleaf Guides:** https://www.overleaf.com/learn
- **TeX StackExchange:** https://tex.stackexchange.com/
- **CTAN (Package Repository):** https://www.ctan.org/

## Support

If you encounter issues not covered in this guide:

1. Check the paper's README: `papers/README.md`
2. Review LaTeX log file: `papers/paper_definitivo.log`
3. Open an issue on GitHub: https://github.com/motanova84/141hz/issues
4. Contact: institutoconsciencia@proton.me

## Citation

If you compile and use this paper, please cite:

```bibtex
@article{motaburruezo2025coherencia,
  title={Coherencia Universal: La Emergencia de 141.7001 Hz como 
         Constante de Resonancia en Geometría Espaciotemporal e 
         Inteligencia Artificial Generativa},
  author={Mota Burruezo, José Manuel},
  journal={QCAL ∞³ Project},
  year={2025},
  institution={Instituto Consciencia Cuántica}
}
```
