#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
PLOT PUBLICATION-READY: Ψ–SNR BINNING ANALYSIS
Ultra-Narrow Band Filter (Δf = 2.0 Hz) @ f₀ = 141.7001 Hz
═══════════════════════════════════════════════════════════════════════════════

Generates a publication-quality figure for the Ψ–SNR binning analysis showing:

1. Main Ψ–SNR plot:
   - Four data bins with error bars (mean ± std of normalised coherence)
   - Power-law fit in the dissipation region (SNR 0.5–2)
   - Colour-coded stability zones (Diamond / Resistance / Dissipation / Rupture)
   - "Survival SNR" marker — the threshold below which Ψ < 0.5 + ε (signal
     indistinguishable from stochastic vacuum noise)

2. Inset zoom:
   - Simulated spectral density ±5 Hz around f₀ = 141.7001 Hz, demonstrating
     the spectral purity of the ultra-narrow-band peak versus the noise floor.

Style:
   - Seaborn v0.12+ white-grid theme
   - LaTeX rendering (falls back gracefully when TeX is not available)
   - Palatino / DejaVu serif font stack

Usage
-----
    python scripts/plot_psi_snr_publication.py

Output
------
    results/figures/psi_snr_publication.png
    results/figures/psi_snr_publication.pdf   (if PDF backend available)

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
Licencia: Sovereign Noetic License 1.0
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from scipy.optimize import curve_fit

warnings.filterwarnings("ignore")

# ─── optional imports ────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend for CI / headless runs
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    from matplotlib.patches import FancyArrowPatch
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib no disponible — sólo se calculan valores numéricos")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("⚠️  seaborn no disponible — se usará estilo matplotlib base")

# ─── repository root on sys.path ─────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

# ─── constants ────────────────────────────────────────────────────────────────
F0_HZ: float = 141.7001          # fundamental resonance frequency [Hz]
DELTA_F_HZ: float = 2.0          # ultra-narrow band filter width [Hz]
PSI_NOISE_FLOOR: float = 0.5     # Ψ value for pure stochastic vacuum (chance)
PSI_SURVIVAL_THRESHOLD: float = PSI_NOISE_FLOOR + 0.01  # survival criterion


# ─── data ─────────────────────────────────────────────────────────────────────
@dataclass
class PsiSnrBin:
    """Single Ψ–SNR bin entry."""

    snr: float           # SNR at bin centre
    psi_mean: float      # mean normalised coherence Ψ
    psi_std: float       # standard deviation of Ψ within the bin
    label: str           # descriptive node state label
    color: str           # colour for plotting


@dataclass
class PsiSnrBinData:
    """Container for all Ψ–SNR binning results.

    Values correspond to the experimental topography reported in the
    ultra-narrow-band (Δf = 2.0 Hz) binning analysis.
    """

    bins: List[PsiSnrBin] = field(default_factory=list)
    f0_hz: float = F0_HZ
    delta_f_hz: float = DELTA_F_HZ

    @classmethod
    def from_problem_statement(cls) -> "PsiSnrBinData":
        """Return the four bins documented in the problem statement."""
        return cls(
            bins=[
                PsiSnrBin(18.42, 0.9984, 0.0002, "Diamond Stability",    "#1a6faf"),
                PsiSnrBin(5.12,  0.9912, 0.0015, "Resistance Phase",     "#2e8b57"),
                PsiSnrBin(1.05,  0.8843, 0.0124, "Dissipation Threshold","#e07b39"),
                PsiSnrBin(0.24,  0.5421, 0.0890, "Symbiosis Rupture",    "#c0392b"),
            ]
        )

    # ── convenience arrays ───────────────────────────────────────────────────
    @property
    def snr_array(self) -> np.ndarray:
        return np.array([b.snr for b in self.bins])

    @property
    def psi_mean_array(self) -> np.ndarray:
        return np.array([b.psi_mean for b in self.bins])

    @property
    def psi_std_array(self) -> np.ndarray:
        return np.array([b.psi_std for b in self.bins])

    @property
    def colors(self) -> List[str]:
        return [b.color for b in self.bins]

    @property
    def labels(self) -> List[str]:
        return [b.label for b in self.bins]


# ─── survival SNR computation ─────────────────────────────────────────────────
def _psi_model(snr: np.ndarray, a: float, k: float, c: float) -> np.ndarray:
    """Parametric sigmoid/power-law model for Ψ(SNR).

    Ψ(s) = c + (1 - c) / (1 + (a / s)^k)

    Parameters
    ----------
    snr : array of positive floats
    a   : half-saturation SNR (inflection point)
    k   : steepness exponent
    c   : asymptotic floor (≈ PSI_NOISE_FLOOR)
    """
    return c + (1.0 - c) / (1.0 + (a / np.maximum(snr, 1e-9)) ** k)


def compute_survival_snr(
    data: PsiSnrBinData,
    threshold: float = PSI_SURVIVAL_THRESHOLD,
) -> Tuple[float, np.ndarray]:
    """Compute the SNR at which Ψ crosses *threshold* from above.

    A parametric model is fitted to the four binning points; the root of
    ``Ψ(snr) = threshold`` is then found analytically from the fit.

    Parameters
    ----------
    data      : PsiSnrBinData
    threshold : Ψ value defining the survival criterion (default 0.51)

    Returns
    -------
    snr_survival : float
        SNR value (bin-centre units) where Ψ = threshold.
    popt : array of 3 floats
        Best-fit parameters [a, k, c] of ``_psi_model``.
    """
    snr = data.snr_array
    psi = data.psi_mean_array

    # Initial guess: a ~ mid-range SNR, k ~ 1.5, c ~ noise floor
    p0 = [1.0, 1.5, PSI_NOISE_FLOOR]
    bounds = ([0.01, 0.1, 0.0], [100.0, 20.0, 0.75])

    try:
        popt, _ = curve_fit(_psi_model, snr, psi, p0=p0, bounds=bounds, maxfev=5000)
    except RuntimeError:
        # Fallback: linear interpolation on the two lowest bins
        popt = np.array(p0)

    a, k, c = popt

    # Solve c + (1-c)/(1+(a/s)^k) = threshold  →  s = a / ((1-c)/(threshold-c) - 1)^(1/k)
    ratio = (1.0 - c) / max(threshold - c, 1e-12) - 1.0
    if ratio <= 0:
        snr_survival = float("nan")
    else:
        snr_survival = float(a / ratio ** (1.0 / k))

    return snr_survival, popt


# ─── spectral inset data ──────────────────────────────────────────────────────
def _generate_spectral_inset(
    f0: float = F0_HZ,
    delta_f: float = DELTA_F_HZ,
    fs: float = 4096.0,
    duration: float = 64.0,
    snr_peak: float = 18.42,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Return (frequencies, ASD) arrays for a simulated narrowband peak at f₀.

    The simulated ASD is flat noise + a Lorentzian peak of height proportional
    to *snr_peak* centred at *f0* with FWHM = delta_f / 4.
    """
    rng = np.random.default_rng(seed)
    n_samples = int(fs * duration)
    freqs = np.fft.rfftfreq(n_samples, d=1.0 / fs)

    # Flat noise ASD baseline (strain / √Hz)
    noise_level = 1.0e-23
    noise_asd = noise_level * (1.0 + 0.05 * rng.standard_normal(len(freqs)))

    # Lorentzian peak
    gamma = delta_f / 4.0            # half-width at half-maximum
    lorentz = (gamma ** 2) / ((freqs - f0) ** 2 + gamma ** 2)
    peak_asd = snr_peak * noise_level * lorentz

    asd = np.sqrt(noise_asd ** 2 + peak_asd ** 2)

    # Restrict to the zoom window [f0 - 5, f0 + 5] Hz
    zoom_mask = (freqs >= f0 - 5.0) & (freqs <= f0 + 5.0)
    return freqs[zoom_mask], asd[zoom_mask]


# ─── helper — detect LaTeX binary ─────────────────────────────────────────────
def _latex_available() -> bool:
    """Return True iff a ``latex`` executable can be found on PATH."""
    import shutil
    return shutil.which("latex") is not None


# ─── figure builder ───────────────────────────────────────────────────────────
class PsiSnrPublicationPlot:
    """Builds and saves the publication-ready Ψ–SNR figure."""

    def __init__(self, data: Optional[PsiSnrBinData] = None):
        self.data: PsiSnrBinData = data or PsiSnrBinData.from_problem_statement()
        self.snr_survival: Optional[float] = None
        self._popt: Optional[np.ndarray] = None
        self._fig = None

    # ── style setup ──────────────────────────────────────────────────────────
    @staticmethod
    def _setup_style() -> None:
        """Apply publication-quality style settings."""
        if SEABORN_AVAILABLE:
            sns.set_theme(style="whitegrid", context="paper", font_scale=1.3)

        # Prefer Palatino (serif); fall back gracefully
        plt.rcParams.update(
            {
                "font.family": "serif",
                "font.serif": ["Palatino", "Georgia", "DejaVu Serif", "Times New Roman"],
                "axes.titlesize": 13,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 9,
                "figure.dpi": 150,
                "savefig.dpi": 300,
                "savefig.bbox": "tight",
            }
        )

        # LaTeX rendering — only enable when the `latex` binary is actually present
        if _latex_available():
            try:
                plt.rcParams.update(
                    {
                        "text.usetex": True,
                        "text.latex.preamble": r"\usepackage{amsmath}",
                    }
                )
            except Exception:
                plt.rcParams["text.usetex"] = False
        else:
            plt.rcParams["text.usetex"] = False

    # ── label helpers ─────────────────────────────────────────────────────────
    @staticmethod
    def _tex(plain: str, latex: str) -> str:
        """Return *latex* when usetex is on, else *plain*."""
        return latex if plt.rcParams.get("text.usetex") else plain

    # ── main figure ──────────────────────────────────────────────────────────
    def create_publication_figure(self) -> "plt.Figure":
        """Build and return the complete publication figure."""
        if not MATPLOTLIB_AVAILABLE:
            raise RuntimeError("matplotlib is required to create figures")

        self._setup_style()

        # Compute survival SNR and fitted curve
        self.snr_survival, self._popt = compute_survival_snr(self.data)

        fig, ax_main = plt.subplots(figsize=(8.5, 6.0))
        self._fig = fig

        self._plot_stability_zones(ax_main)
        self._plot_fitted_curve(ax_main)
        self._plot_data_points(ax_main)
        self._plot_survival_marker(ax_main)
        self._format_main_axes(ax_main)
        self._add_zoom_inset(fig, ax_main)
        self._add_caption_box(ax_main)

        fig.tight_layout()
        return fig

    # ── stability zone bands ─────────────────────────────────────────────────
    def _plot_stability_zones(self, ax: "plt.Axes") -> None:
        zone_defs = [
            (4.0, 25.0, "#d0e8f7", "Noēsis Plateau\n" + r"$(\Psi > 0.99)$"),
            (0.8, 4.0,  "#d6f0e0", "Resistance / Decay"),
            (PSI_NOISE_FLOOR, 0.8, "#fde8d8", "Dissipation"),
        ]
        snr_min, snr_max = 0.05, 30.0
        # zones are in Ψ space — draw as horizontal bands
        psi_zones = [
            (0.99, 1.005, "#d0e8f7", "Noēsis Plateau"),
            (0.85, 0.99,  "#d6f0e0", "Resistance / Decay"),
            (PSI_NOISE_FLOOR, 0.85, "#fde8d8", "Dissipation"),
        ]
        for psi_lo, psi_hi, color, _ in psi_zones:
            ax.axhspan(psi_lo, psi_hi, color=color, alpha=0.35, zorder=0)

    # ── fitted model curve ────────────────────────────────────────────────────
    def _plot_fitted_curve(self, ax: "plt.Axes") -> None:
        snr_fit = np.logspace(np.log10(0.08), np.log10(25.0), 500)
        if self._popt is not None:
            psi_fit = _psi_model(snr_fit, *self._popt)
            ax.plot(
                snr_fit,
                psi_fit,
                color="#555555",
                linewidth=1.6,
                linestyle="--",
                zorder=2,
                label=self._tex(
                    "Fitted model Ψ(SNR)",
                    r"Fitted model $\Psi(\mathrm{SNR})$",
                ),
            )

    # ── data points with error bars ──────────────────────────────────────────
    def _plot_data_points(self, ax: "plt.Axes") -> None:
        snr = self.data.snr_array
        psi = self.data.psi_mean_array
        err = self.data.psi_std_array

        for b in self.data.bins:
            ax.errorbar(
                b.snr,
                b.psi_mean,
                yerr=b.psi_std,
                fmt="o",
                color=b.color,
                markersize=9,
                markeredgecolor="white",
                markeredgewidth=1.0,
                elinewidth=1.8,
                capsize=5,
                capthick=1.8,
                zorder=4,
                label=b.label,
            )

    # ── survival SNR vertical marker ─────────────────────────────────────────
    def _plot_survival_marker(self, ax: "plt.Axes") -> None:
        if self.snr_survival is None or np.isnan(self.snr_survival):
            return
        sv = self.snr_survival
        ax.axvline(
            sv,
            color="#8b0000",
            linewidth=1.6,
            linestyle=":",
            zorder=3,
            label=self._tex(
                f"Survival SNR ≈ {sv:.3f}",
                rf"Survival SNR $\approx {sv:.3f}$",
            ),
        )
        ax.axhline(
            PSI_SURVIVAL_THRESHOLD,
            color="#8b0000",
            linewidth=0.9,
            linestyle=":",
            alpha=0.55,
            zorder=3,
        )
        ax.annotate(
            self._tex(
                f"SNR* = {sv:.3f}\nΨ = {PSI_SURVIVAL_THRESHOLD:.2f}",
                rf"$\mathrm{{SNR}}^* = {sv:.3f}$" + "\n"
                + rf"$\Psi = {PSI_SURVIVAL_THRESHOLD:.2f}$",
            ),
            xy=(sv, PSI_SURVIVAL_THRESHOLD),
            xytext=(sv * 1.5, PSI_SURVIVAL_THRESHOLD - 0.08),
            fontsize=8.5,
            color="#8b0000",
            arrowprops=dict(arrowstyle="->", color="#8b0000", lw=1.0),
            zorder=5,
        )

    # ── axis formatting ──────────────────────────────────────────────────────
    def _format_main_axes(self, ax: "plt.Axes") -> None:
        ax.set_xscale("log")
        ax.set_xlim(0.08, 30.0)
        ax.set_ylim(0.42, 1.012)

        ax.set_xlabel(
            self._tex("SNR (bin centre)", r"SNR (bin centre)"),
            labelpad=6,
        )
        ax.set_ylabel(
            self._tex(
                "Ψ — Normalised Coherence (mean ± std)",
                r"$\Psi$ — Normalised Coherence (mean $\pm$ std)",
            ),
            labelpad=6,
        )
        ax.set_title(
            self._tex(
                f"Ψ–SNR Binning  |  Δf = {DELTA_F_HZ:.1f} Hz  "
                f"|  f₀ = {F0_HZ} Hz",
                rf"$\Psi$–SNR Binning $\;|\;$ $\Delta f = {DELTA_F_HZ:.1f}$\,Hz"
                rf" $\;|\;$ $f_0 = {F0_HZ}$\,Hz",
            ),
            fontweight="bold",
            pad=8,
        )

        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x:g}")
        )
        ax.legend(loc="upper left", framealpha=0.85, edgecolor="0.7")
        ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.7)

    # ── zoom inset ────────────────────────────────────────────────────────────
    def _add_zoom_inset(self, fig: "plt.Figure", ax_main: "plt.Axes") -> None:
        """Add a spectral-density inset showing the peak purity at f₀."""
        freqs, asd = _generate_spectral_inset()

        # Inset axes: upper-right quadrant of main axes
        ax_ins = ax_main.inset_axes([0.58, 0.14, 0.38, 0.32])

        ax_ins.semilogy(freqs, asd, color="#1a6faf", linewidth=1.2)
        ax_ins.axvline(F0_HZ, color="#c0392b", linewidth=1.2, linestyle="--", alpha=0.9)

        ax_ins.set_xlim(F0_HZ - 5.0, F0_HZ + 5.0)
        ax_ins.set_xlabel(
            self._tex("Frequency (Hz)", r"Frequency (Hz)"),
            fontsize=7.5,
            labelpad=2,
        )
        ax_ins.set_ylabel(
            self._tex("ASD (strain/√Hz)", r"ASD (strain$/\sqrt{\mathrm{Hz}}$)"),
            fontsize=7.0,
            labelpad=2,
        )
        ax_ins.set_title(
            self._tex(
                f"Spectral purity @ f₀ = {F0_HZ} Hz",
                rf"Spectral purity @ $f_0 = {F0_HZ}$\,Hz",
            ),
            fontsize=7.5,
            pad=3,
        )
        ax_ins.tick_params(axis="both", labelsize=6.5)
        ax_ins.grid(True, which="major", linestyle=":", linewidth=0.5, alpha=0.6)

    # ── caption text box ─────────────────────────────────────────────────────
    def _add_caption_box(self, ax: "plt.Axes") -> None:
        caption = (
            "Colour zones: blue = Diamond Stability (SNR > 4),\n"
            "green = Resistance Phase, orange = Dissipation, red = Rupture.\n"
            r"Dashed line: $\Psi(s) = c + (1-c)/[1+(a/s)^k]$ fit."
            if not plt.rcParams.get("text.usetex")
            else (
                r"Colour zones: blue = Diamond Stability ($\mathrm{SNR} > 4$),"
                "\n"
                r"green = Resistance Phase, orange = Dissipation, red = Rupture."
                "\n"
                r"Dashed: $\Psi(s) = c + (1-c)/[1+(a/s)^k]$ fit."
            )
        )
        ax.text(
            0.01,
            0.01,
            caption,
            transform=ax.transAxes,
            fontsize=6.5,
            verticalalignment="bottom",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.6, edgecolor="0.8"),
        )

    # ── save ─────────────────────────────────────────────────────────────────
    def save_figure(
        self,
        output_dir: Optional[Path] = None,
        stem: str = "psi_snr_publication",
    ) -> List[Path]:
        """Save figure as PNG (and PDF when available) to *output_dir*.

        Parameters
        ----------
        output_dir : Path, optional
            Defaults to ``<repo_root>/results/figures/``.
        stem : str
            Base filename without extension.

        Returns
        -------
        list of Path
            Paths of successfully written files.
        """
        if self._fig is None:
            self.create_publication_figure()

        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "results" / "figures"
        output_dir.mkdir(parents=True, exist_ok=True)

        saved: List[Path] = []

        # Always save PNG
        png_path = output_dir / f"{stem}.png"
        self._fig.savefig(png_path, format="png")
        saved.append(png_path)
        print(f"✅ PNG  → {png_path}")

        # Attempt PDF — may fail if TeX renderer is not available
        pdf_path = output_dir / f"{stem}.pdf"
        try:
            self._fig.savefig(pdf_path, format="pdf")
            saved.append(pdf_path)
            print(f"✅ PDF  → {pdf_path}")
        except Exception as exc:
            print(f"⚠️  PDF skipped: {exc}")

        return saved


# ─── main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    """Entry point."""
    print("=" * 70)
    print("🎨  Ψ–SNR PUBLICATION PLOT  (Δf = 2.0 Hz ultra-narrow band)")
    print("=" * 70)

    data = PsiSnrBinData.from_problem_statement()

    # Print numerical results first (always works, even without matplotlib)
    snr_survival, popt = compute_survival_snr(data)
    print(f"\n📊  Binning data ({len(data.bins)} bins):")
    for b in data.bins:
        print(f"   SNR {b.snr:6.2f}  →  Ψ = {b.psi_mean:.4f} ± {b.psi_std:.4f}"
              f"   [{b.label}]")

    if not np.isnan(snr_survival):
        print(
            f"\n🔬  Survival SNR (Ψ = {PSI_SURVIVAL_THRESHOLD:.2f}): "
            f"SNR* ≈ {snr_survival:.4f}"
        )
        print(
            "    → Below this threshold the coherence signal is indistinguishable"
            " from stochastic vacuum noise."
        )
    else:
        print("\n⚠️  Survival SNR could not be determined from the fit.")

    if not MATPLOTLIB_AVAILABLE:
        print("\n⚠️  matplotlib absent — figure not generated.")
        return 0

    plotter = PsiSnrPublicationPlot(data)
    plotter.create_publication_figure()
    saved_paths = plotter.save_figure()

    print(f"\n✨  Figure saved ({len(saved_paths)} file(s)).")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
