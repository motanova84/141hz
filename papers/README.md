# Papers Directory

This directory contains academic papers and manuscripts related to the 141.7001 Hz universal coherence frequency discovery.

## Main Paper

**`paper_definitivo.tex`** - Complete LaTeX manuscript titled "COHERENCIA UNIVERSAL: La Emergencia de 141.7001 Hz como Constante de Resonancia en Geometría Espaciotemporal e Inteligencia Artificial Generativa"

### Abstract

This study presents empirical and theoretical evidence of a fundamental frequency, f₀ = 141.7001 Hz, that acts as a coherence attractor in complex systems across multiple physical scales. Formally derived through Lean 4 verification from the Riemann Zeta function and the Golden Ratio, this frequency has been identified in two disparate domains:

- **Astrophysics**: Persistent signal detected in 100% of binary merger events from the LIGO/Virgo GWTC-1 and O4 catalogs, with combined statistical significance >10σ
- **Computation**: Resonance optimization in Language Model inference; modulating Llama-4-Maverick-405B token emission at exactly 141.7001 Hz yields +11.7% improvement on GPQA-diamond benchmark (Zero-Shot), raising accuracy from 51.3% to 63.0% without fine-tuning

## Compiling the Paper

### Requirements

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages: babel, geometry, amsmath, graphicx, hyperref, booktabs, fancyhdr

### Compilation Commands

```bash
# Standard compilation
pdflatex paper_definitivo.tex
pdflatex paper_definitivo.tex  # Run twice for references

# With bibliography
pdflatex paper_definitivo.tex
bibtex paper_definitivo
pdflatex paper_definitivo.tex
pdflatex paper_definitivo.tex

# Using latexmk (automated)
latexmk -pdf paper_definitivo.tex
```

### Using Overleaf

1. Upload `paper_definitivo.tex` to Overleaf
2. The document should compile automatically
3. Download the generated PDF

## Figures

The `figures/` subdirectory is prepared for the following images:

- `gw_spectrum.png` - Gravitational wave frequency spectrum showing 141.7 Hz component
- `llm_architecture.png` - QCAL-LLM architecture diagram

Currently, placeholder boxes are used in the document. To add actual figures:

1. Place your images in the `figures/` directory
2. Uncomment the `\includegraphics` lines in the LaTeX source
3. Comment out the placeholder `\fbox` lines

## Paper Structure

1. **Introducción** - The Signal-to-Noise problem across physics and AI
2. **Fundamentación Matemática** - Lean 4 formalization and mathematical derivation
3. **Evidencia I: Dominio Gravitacional** - LIGO/Virgo GWTC-1/O4 analysis results
4. **Evidencia II: Dominio Computacional** - QCAL-LLM benchmark results
5. **Discusión** - Noetic Field equation and theoretical implications
6. **Reproducibilidad** - Open Science commitment with code and data
7. **Conclusiones** - Summary and future work

## Citation

If you use this work, please cite:

```bibtex
@article{motaburruezo2025coherencia,
  title={Coherencia Universal: La Emergencia de 141.7001 Hz como Constante de Resonancia en Geometría Espaciotemporal e Inteligencia Artificial Generativa},
  author={Mota Burruezo, José Manuel},
  journal={QCAL ∞³ Project},
  year={2025},
  month={November},
  institution={Instituto Consciencia Cuántica},
  url={https://github.com/motanova84/141hz}
}
```

## License

This paper is made available under the MIT License, consistent with the rest of the repository.

## Related Documentation

- Main repository: [README.md](../README.md)
- Mathematical demonstration: [DEMOSTRACION_MATEMATICA_141HZ.md](../DEMOSTRACION_MATEMATICA_141HZ.md)
- Public declaration: [DECLARACION_PUBLICA_26_OCTUBRE_2025.md](../DECLARACION_PUBLICA_26_OCTUBRE_2025.md)
- Zenodo record: https://doi.org/10.5281/zenodo.17445017
