# Figures Directory

This directory contains figures for the LaTeX paper.

## Expected Figures

The following figures are referenced in `paper_definitivo.tex`:

### 1. `gw_spectrum.png` (Figure 1)
**Description:** Gravitational wave frequency spectrum from GW150914  
**Caption:** Espectro de frecuencias del evento GW150914 mostrando la señal persistente en 141.7001 Hz. El análisis espectral fue realizado utilizando transformadas de Fourier con ventanas Hann durante la fase de ringdown.

**How to generate:**
```bash
# From repository root
python scripts/analisis_catalogo_o4.py
# Or use existing visualization scripts
python gw_spectral_evidence.py
```

The generated figure should show:
- X-axis: Frequency (Hz), range approximately 100-200 Hz
- Y-axis: Spectral power density
- Clear peak at 141.7001 Hz
- Background noise level for comparison

### 2. `llm_architecture.png` (Figure 2)
**Description:** QCAL-LLM architecture diagram  
**Caption:** Arquitectura del sistema QCAL-LLM mostrando la integración de la modulación temporal en el motor de inferencia de Llama-4-Maverick-405B. La cadencia de tokens se sincroniza mediante un reloj de precisión a 141.7001 Hz.

**How to create:**
You can create this diagram using:
- Draw.io (diagrams.net)
- TikZ (LaTeX)
- Python matplotlib/seaborn
- Any vector graphics tool

The diagram should show:
- Llama-4-Maverick-405B model architecture
- Token generation pipeline
- Clock/timer module at 141.7001 Hz
- Feedback loop for synchronization
- Input/output data flow

## Adding Figures to the Paper

Once you have generated or created the figures:

1. Place the image files in this directory:
   ```bash
   cp your_gw_spectrum.png figures/gw_spectrum.png
   cp your_llm_architecture.png figures/llm_architecture.png
   ```

2. Edit `paper_definitivo.tex`:
   - Uncomment the `\includegraphics` lines
   - Comment out or remove the `\fbox` placeholder lines

3. Recompile the paper:
   ```bash
   cd papers/
   make
   # or
   ./compile.sh
   ```

## Placeholder Mode

Currently, the LaTeX document uses placeholder boxes (using `\fbox` and `\parbox`) to indicate where the figures should appear. This allows the document to compile successfully even without the actual image files.

## Image Format Recommendations

- **Format:** PNG or PDF (vector preferred for diagrams)
- **Resolution:** At least 300 DPI for raster images
- **Width:** Images are set to 0.8-0.9\textwidth in the LaTeX document
- **Color:** RGB color space, high contrast for readability

## Existing Visualizations in Repository

The repository already contains several relevant visualizations that could be used or adapted:

- `coherence_f0_scales.png` - Multi-scale coherence visualization
- `gw_spectral_evidence.png` - Gravitational wave spectrum
- `espectro_energia_universal.png` - Universal energy spectrum
- `explicacion_consistencia_l1.png` - L1 detector consistency
- `modulation_traces.png` - Modulation traces

Check the root directory and `results/` subdirectories for these files.
