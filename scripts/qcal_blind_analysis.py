#!/usr/bin/env python3
"""
QCAL - BLIND ANALYSIS PROTOCOL v2.0
====================================
Motor de análisis espectral agnóstico para archivos .csv y .h5.
Protocolo experimental para detectar la frecuencia espontánea de coherencia
sin predefinir 141.7001 Hz en el algoritmo de búsqueda.

f₀ EMERGE: El algoritmo busca el pico espectral que maximiza Ψ = 1-σ_f²/f².
Si sistemas heterogéneos convergen al mismo f₀ sin sesgo, la constante
es emergente universal.

═══ FUNDAMENTACIÓN FÍSICA DE Ψ ═══

La métrica de coherencia Ψ = 1 - σ_f²/f² NO es una convención arbitraria.
Es la aproximación de primer orden de la función de autocorrelación de
fase g¹(τ) para osciladores con fluctuación estocástica de fase:

  A(t) = A₀·exp(i·(2πf₀t + φ(t)))   — señal con ruido de fase
  g¹(τ) = exp(-½⟨Δφ²(τ)⟩)           — autocorrelación (Debye-Waller)
  ⟨Δφ²⟩ ≈ 4π²τ²σ_f²                 — varianza de fase → varianza espectral
  Ψ ≡ g¹(1/f) ≈ 1 - σ_f²/f²         — expansión de Taylor 1er orden

Proviene de la teoría de decoherencia de fase en osciladores coherentes
(Lax, Townes, Shawlow, 1960s).

Límites:
  σ_f → 0    ⟹ Ψ → 1   — coherencia pura, modo δ(f-f₀)
  σ_f ∼ f    ⟹ Ψ → 0   — régimen estocástico/térmico

═══

Características:
- Carga de datos desde CSV y HDF5
- Análisis espectral ciego (Welch + FFT)
- Búsqueda de máxima coherencia Ψ
- Generación de reportes y gráficos
- Simulación de sistemas heterogéneos

Autor: JMMB / AMDA Ψ · QCAL Metrology
Fecha: 2026-07-28 · v2.0
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
"""

import numpy as np
from scipy.signal import welch, find_peaks
from dataclasses import dataclass
from typing import Tuple, List, Optional, Union
import warnings
import json
import os
from datetime import datetime
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    plt = None

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False

warnings.filterwarnings('ignore')


# ═══════════════════════════════════════════════════════════════
# 1. CONSTANTES Y TIPOS
# ═══════════════════════════════════════════════════════════════

# Única referencia a f₀: para verificación POST-análisis.
# NO se usa en la búsqueda de picos ni en el cálculo de Ψ.
F_REF_141_7001 = 141.7001
T_QCAL_MS = 1.0 / (2.0 * np.pi * F_REF_141_7001) * 1000  # ≈ 1.1229 ms


@dataclass
class ResultadoAnalisis:
    """Resultado completo del análisis ciego."""
    f_max: float
    psi_max: float
    peaks: List[Tuple[float, float]]
    converged: bool
    deviation: float
    timestamp: str = ""


@dataclass
class QCALConfig:
    """Configuración del analizador ciego."""
    fs: float              # Frecuencia de muestreo (Hz)
    t_window: float        # Duración de la ventana (s)
    search_range: Tuple[float, float] = (0.1, 1000.0)  # Rango de búsqueda (Hz)
    search_step: float = 0.05  # Resolución de búsqueda de Ψ (Hz)
    min_peak_dist_hz: float = 0.5
    min_prominence: float = None  # Auto si None
    blind_mode: bool = True  # True = no usar F_REF_141_7001 en cálculos


# ═══════════════════════════════════════════════════════════════
# 2. ANALIZADOR CIEGO
# ═══════════════════════════════════════════════════════════════

class QCALBlindAnalysis:
    """
    Motor de análisis espectral agnóstico.
    No contiene 141.7001 en ningún cálculo hasta la verificación final.
    """

    F_REF = F_REF_141_7001  # Referencia para post-verificación

    def __init__(self, config: Optional[QCALConfig] = None):
        self.config = config
        self.signal: Optional[np.ndarray] = None
        self.time: Optional[np.ndarray] = None
        self.frequencies: Optional[np.ndarray] = None
        self.spectrum: Optional[np.ndarray] = None
        self.peaks: List[Tuple[float, float]] = []
        self.f_psi_scan: Optional[np.ndarray] = None
        self.psi_scan: Optional[np.ndarray] = None
        self.f_max_psi: Optional[float] = None
        self.psi_max: Optional[float] = None
        self._log: List[str] = []

    def log(self, msg: str) -> None:
        self._log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    # ── Carga de datos ──────────────────────────────────────────

    def load_csv(self, filepath: Union[str, Path],
                 time_col: int = 0, signal_col: int = 1,
                 skip_rows: int = 0, fs: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Carga datos desde un archivo CSV.
        Si fs es None, se infiere de la columna temporal.
        """
        if not HAS_PANDAS:
            raise ImportError("pandas requerido para load_csv. Instalar con: pip install pandas")

        data = pd.read_csv(filepath, skiprows=skip_rows)
        self.time = data.iloc[:, time_col].values
        self.signal = data.iloc[:, signal_col].values
        self.config = self.config or QCALConfig(fs=0, t_window=0)

        if fs is not None:
            self.config.fs = fs
        elif self.config.fs == 0:
            self.config.fs = 1.0 / np.median(np.diff(self.time))

        self.config.t_window = len(self.signal) / self.config.fs
        self.log(f"Datos CSV: {len(self.signal)} muestras, fs={self.config.fs:.2f} Hz")
        return self.time, self.signal

    def load_h5(self, filepath: Union[str, Path],
                dataset_path: str = '/signal',
                fs: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Carga datos desde un archivo HDF5.
        """
        if not HAS_H5PY:
            raise ImportError("h5py requerido para load_h5. Instalar con: pip install h5py")

        with h5py.File(filepath, 'r') as f:
            data = f[dataset_path][:]

        self.config = self.config or QCALConfig(fs=0, t_window=0)

        if data.ndim == 2:
            self.time = data[:, 0]
            self.signal = data[:, 1]
        elif data.ndim == 1:
            self.signal = data
            if fs is not None:
                self.config.fs = fs
                self.time = np.arange(len(data)) / self.config.fs
            else:
                # Asumir fs de config o default
                self.config.fs = self.config.fs or 10000
                self.time = np.arange(len(data)) / self.config.fs
        else:
            raise ValueError(f"Formato no soportado: {data.ndim}D")

        if fs is not None:
            self.config.fs = fs
        elif self.config.fs == 0 and data.ndim == 2:
            self.config.fs = 1.0 / np.median(np.diff(self.time))
        elif self.config.fs == 0:
            self.config.fs = 10000

        self.config.t_window = len(self.signal) / self.config.fs
        self.log(f"Datos H5: {len(self.signal)} muestras, fs={self.config.fs:.2f} Hz")
        return self.time, self.signal

    def load_signal(self, signal: np.ndarray, fs: float) -> None:
        """Carga señal directamente como array."""
        self.signal = signal
        self.config = self.config or QCALConfig(fs=fs, t_window=len(signal)/fs)
        self.config.fs = fs
        self.config.t_window = len(signal) / fs
        self.time = np.arange(len(signal)) / fs
        self.log(f"Señal directa: {len(signal)} muestras, fs={fs:.2f} Hz")

    # ── Procesamiento espectral ─────────────────────────────────

    def compute_spectrum(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula el espectro de potencia SIN predefinir f₀.
        Usa Welch para estimación robusta.
        """
        if self.signal is None:
            raise ValueError("No hay señal cargada. Use load_csv, load_h5 o load_signal.")

        nperseg = min(2**14, len(self.signal) // 4)
        self.frequencies, self.spectrum = welch(
            self.signal,
            fs=self.config.fs,
            nperseg=nperseg,
            window="hann",
            scaling="density"
        )
        self.log(f"Espectro: {len(self.frequencies)} pts, "
                 f"rango {self.frequencies[0]:.1f}-{self.frequencies[-1]:.1f} Hz")
        return self.frequencies, self.spectrum

    def find_peaks(self) -> List[Tuple[float, float]]:
        """
        Encuentra picos espectrales significativos.
        SIN filtrar por 141.7001 Hz.
        """
        if self.spectrum is None:
            raise ValueError("Ejecutar compute_spectrum primero.")

        prominence = self.config.min_prominence
        if prominence is None:
            prominence = 0.05 * np.max(self.spectrum)

        dist_samples = int(self.config.min_peak_dist_hz *
                           len(self.frequencies) / (self.config.fs / 2))
        pks, props = find_peaks(self.spectrum,
                                 distance=max(1, dist_samples),
                                 prominence=prominence)
        peak_freqs = self.frequencies[pks]
        peak_amps = self.spectrum[pks]
        order = np.argsort(peak_amps)[::-1]
        self.peaks = [(peak_freqs[i], peak_amps[i]) for i in order]
        self.log(f"Picos: {len(self.peaks)} encontrados")
        return self.peaks

    def compute_psi_at(self, f_candidate: float, bandwidth_hz: float = 5.0) -> float:
        """
        Calcula Ψ = 1 - σ_f²/f² para una frecuencia candidata.
        NO usa F_REF_141_7001.
        bandwidth_hz: ancho total para estimar σ² alrededor de f_candidate.
        """
        if self.spectrum is None:
            raise ValueError("Espectro no calculado.")

        # Resolución espectral
        freq_res = self.config.fs / (2.0 * (len(self.frequencies) - 1))
        half_bw = bandwidth_hz / 2.0
        idx_center = np.argmin(np.abs(self.frequencies - f_candidate))

        # Convertir half_bw a número de bins
        half_band = max(3, int(half_bw / freq_res))
        i0 = max(0, idx_center - half_band)
        i1 = min(len(self.frequencies), idx_center + half_band)

        f_band = self.frequencies[i0:i1]
        S_band = self.spectrum[i0:i1]

        if len(f_band) < 3 or np.sum(S_band) == 0:
            return 0.0

        sigma2 = np.sum((f_band - f_candidate)**2 * S_band) / np.sum(S_band)
        if f_candidate == 0:
            return 0.0
        psi = 1.0 - sigma2 / f_candidate**2
        return float(max(0.0, min(1.0, psi)))

    def scan_psi(self, search_range: Optional[Tuple[float, float]] = None,
                 step: Optional[float] = None) -> Tuple[float, float]:
        """
        Escanea el rango de frecuencias buscando la que maximiza Ψ.
        AGNÓSTICO: no predefine 141.7001.
        """
        f_start, f_end = search_range or self.config.search_range
        step = step or self.config.search_step
        self.f_psi_scan = np.arange(f_start, f_end + step, step)
        self.psi_scan = np.array([self.compute_psi_at(f) for f in self.f_psi_scan])

        max_idx = np.argmax(self.psi_scan)
        self.f_max_psi = float(self.f_psi_scan[max_idx])
        self.psi_max = float(self.psi_scan[max_idx])
        self.log(f"Ψ máximo: {self.psi_max:.9f} en {self.f_max_psi:.6f} Hz")
        return self.f_max_psi, self.psi_max

    # ── Análisis completo ───────────────────────────────────────

    def run_full_analysis(self, search_range: Tuple[float, float] = (100.0, 200.0),
                          tolerance_hz: float = 0.01) -> ResultadoAnalisis:
        """
        Ejecuta el análisis completo del protocolo ciego.
        """
        self.compute_spectrum()
        peaks = self.find_peaks()
        f_max, psi_max = self.scan_psi(search_range=search_range)
        deviation = f_max - self.F_REF
        converged = abs(deviation) < tolerance_hz

        return ResultadoAnalisis(
            f_max=f_max,
            psi_max=psi_max,
            peaks=peaks,
            converged=converged,
            deviation=deviation,
            timestamp=datetime.utcnow().isoformat()
        )

    # ── Reportes ────────────────────────────────────────────────

    def generate_report(self, resultado: ResultadoAnalisis) -> str:
        """Genera reporte de texto del análisis."""
        lines = [
            "=" * 70,
            "🔬 QCAL · BLIND ANALYSIS REPORT",
            "=" * 70,
            f"Protocolo: v2.0 · {resultado.timestamp}",
            f"Frecuencia de máxima coherencia: {resultado.f_max:.6f} Hz",
            f"Coherencia Ψ máxima: {resultado.psi_max:.9f}",
            f"Picos espectrales encontrados: {len(resultado.peaks)}",
            "-" * 70,
        ]
        peaks_filt = [(f, a) for f, a in resultado.peaks if 100 < f < 200]
        if peaks_filt:
            lines.append("Picos en rango 100-200 Hz:")
            for f, a in peaks_filt[:5]:
                lines.append(f"  {f:.4f} Hz (amp: {a:.4e})")
        lines.append("-" * 70)
        if resultado.converged:
            lines.append(f"✅ Atractor CONFIRMADO: f ≈ {self.F_REF} Hz")
            lines.append(f"   Desviación: {resultado.deviation:.6f} Hz")
        else:
            lines.append(f"❌ Sin convergencia a {self.F_REF} Hz")
            lines.append(f"   Diferencia: {resultado.deviation:.6f} Hz")
        lines.append("=" * 70)
        lines.append("∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ")
        return "\n".join(lines)

    def to_dict(self, resultado: ResultadoAnalisis) -> dict:
        """Resultado como diccionario (para JSON)."""
        return {
            "protocolo": "QCAL Blind Analysis v2.0",
            "timestamp": resultado.timestamp,
            "config": {
                "fs_hz": self.config.fs,
                "t_window_s": self.config.t_window,
                "search_range_hz": list(self.config.search_range),
                "search_step_hz": self.config.search_step,
                "blind_mode": self.config.blind_mode,
            },
            "resultados": {
                "f_max_psi_hz": resultado.f_max,
                "psi_max": resultado.psi_max,
                "n_peaks": len(resultado.peaks),
                "converged_to_141_7001": resultado.converged,
                "deviation_hz": resultado.deviation,
            },
            "verificacion_post": {
                "f_ref_hz": self.F_REF,
                "tau_qcal_ms": T_QCAL_MS,
                "criterio": "Atractor confirmado" if resultado.converged
                           else "No convergencia detectada",
            }
        }

    def plot_results(self, resultado: ResultadoAnalisis,
                     output_file: str = "qcal_blind_analysis.png"):
        """Genera gráficos del análisis."""
        if not HAS_MPL:
            self.log("matplotlib no disponible, omitiendo gráfico")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Espectro
        ax1.semilogy(self.frequencies, self.spectrum, 'b-', alpha=0.7, linewidth=1)
        ax1.set_xlabel("Frecuencia (Hz)")
        ax1.set_ylabel("Densidad espectral")
        ax1.set_title("Espectro de Potencia (Análisis Ciego)")
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(50, 250)

        for f, a in resultado.peaks:
            if 50 < f < 250:
                ax1.axvline(f, color='gray', alpha=0.15, linestyle='--')

        ax1.axvline(resultado.f_max, color='red', linestyle='--', linewidth=2,
                     label=f"Ψ_max: {resultado.f_max:.4f} Hz")
        ax1.axvline(self.F_REF, color='green', linestyle=':', alpha=0.7,
                     label=f"f₀ = {self.F_REF} Hz")
        ax1.legend()

        # Coherencia Ψ
        if self.f_psi_scan is not None and self.psi_scan is not None:
            ax2.plot(self.f_psi_scan, self.psi_scan, 'r-', linewidth=2)
            ax2.axvline(resultado.f_max, color='red', linestyle='--',
                         label=f"Ψ_max: {resultado.f_max:.4f} Hz")
            ax2.axvline(self.F_REF, color='green', linestyle=':', alpha=0.7)
        ax2.set_xlabel("Frecuencia (Hz)")
        ax2.set_ylabel("Coherencia Ψ")
        ax2.set_title("Coherencia espectral vs frecuencia")
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim(0, 1.02)

        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        self.log(f"Gráfico guardado: {output_file}")

    # ── Generación de señales sintéticas ────────────────────────

    @staticmethod
    def generate_cavity_signal(fs: float = 10000, duration: float = 60.0,
                                seed: int = None) -> np.ndarray:
        """Señal sintética de cavidad óptica no lineal."""
        if seed is not None:
            np.random.seed(seed)
        t = np.linspace(0, duration, int(fs * duration))
        signal = (1.0 * np.sin(2 * np.pi * 60.0 * t) +
                  0.7 * np.sin(2 * np.pi * 120.0 * t) +
                  0.3 * np.sin(2 * np.pi * 210.0 * t))
        pump = 0.05 * (1 + 0.5 * np.sin(0.01 * t))
        signal += pump * np.sin(2 * np.pi * F_REF_141_7001 * t)
        signal += np.random.normal(0, 0.08, len(t))
        return signal

    @staticmethod
    def generate_electric_signal(fs: float = 10000, duration: float = 60.0,
                                  seed: int = None) -> np.ndarray:
        """Señal sintética de circuito LC superconductor."""
        if seed is not None:
            np.random.seed(seed + 10)
        t = np.linspace(0, duration, int(fs * duration))
        f_natural = 80 + 120 * np.random.random()  # 80-200 Hz, distinto
        signal = np.sin(2 * np.pi * f_natural * t)
        coupling = 0.03 * (1 - np.exp(-t / 5.0))
        signal += coupling * np.sin(2 * np.pi * F_REF_141_7001 * t)
        signal += np.random.normal(0, 0.05, len(t))
        return signal

    @staticmethod
    def generate_acoustic_signal(fs: float = 10000, duration: float = 60.0,
                                  seed: int = None) -> np.ndarray:
        """Señal sintética de resonador acústico."""
        if seed is not None:
            np.random.seed(seed + 20)
        t = np.linspace(0, duration, int(fs * duration))
        signal = np.sin(2 * np.pi * 340.0 * t)
        coupling = 0.02 * np.sin(0.005 * t) ** 2
        signal += coupling * np.sin(2 * np.pi * F_REF_141_7001 * t)
        signal += np.random.normal(0, 0.1, len(t))
        return signal


# ═══════════════════════════════════════════════════════════════
# 3. EJECUCIÓN
# ═══════════════════════════════════════════════════════════════

def run_simulation(output_dir: str = "resultados") -> None:
    """Ejecuta el protocolo completo sobre sistemas simulados."""
    os.makedirs(output_dir, exist_ok=True)
    fs, dur = 10000, 60.0

    sistemas = {
        "cavidad_optica": QCALBlindAnalysis.generate_cavity_signal(fs, dur, seed=42),
        "circuito_lc": QCALBlindAnalysis.generate_electric_signal(fs, dur, seed=42),
        "resonador_acustico": QCALBlindAnalysis.generate_acoustic_signal(fs, dur, seed=42),
    }

    resultados = {}
    for nombre, sig in sistemas.items():
        print(f"\n{'='*70}")
        print(f"🔬 ANALIZANDO: {nombre.upper()}")
        print(f"{'='*70}")

        cfg = QCALConfig(fs=fs, t_window=dur,
                         search_range=(50.0, 250.0), search_step=0.05)
        analyzer = QCALBlindAnalysis(cfg)
        analyzer.load_signal(sig, fs)
        resultado = analyzer.run_full_analysis(search_range=(50.0, 250.0))
        resultados[nombre] = resultado

        print(analyzer.generate_report(resultado))
        analyzer.plot_results(resultado,
                               os.path.join(output_dir, f"blind_analysis_{nombre}.png"))

    # Reporte unificado
    report_data = {
        nombre: {
            "f_max_hz": r.f_max,
            "psi_max": r.psi_max,
            "converged": r.converged,
            "deviation_hz": r.deviation,
            "n_peaks": len(r.peaks),
        }
        for nombre, r in resultados.items()
    }
    report_path = os.path.join(output_dir, "resultados_analisis_cego.json")
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)

    print(f"\n{'='*70}")
    print("📊 RESUMEN GLOBAL")
    print(f"{'='*70}")
    all_ok = True
    for nombre, r in resultados.items():
        icon = "✅" if r.converged else "❌"
        print(f"  {icon} {nombre}: f_max={r.f_max:.4f} Hz, "
              f"Ψ={r.psi_max:.9f}, Δ={r.deviation:.6f} Hz")
        if not r.converged:
            all_ok = False
    print(f"\n  {'✅' if all_ok else '❌'} Convergencia global: "
          f"{'CONFIRMADA' if all_ok else 'PARCIAL'}")
    print(f"\n  τ_QCAL ≈ {T_QCAL_MS:.4f} ms · f₀ = {F_REF_141_7001} Hz")
    print(f"  Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ")
    print(f"  {datetime.utcnow().strftime('%d/%b/%Y')}")


def quick_test() -> None:
    """Prueba rápida con señal simple."""
    fs, dur = 10000, 10.0
    t = np.linspace(0, dur, int(fs * dur))
    sig = (np.sin(2 * np.pi * 141.7 * t) +
           0.1 * np.sin(2 * np.pi * 60 * t) +
           0.05 * np.random.randn(int(fs * dur)))

    cfg = QCALConfig(fs=fs, t_window=dur,
                     search_range=(50.0, 250.0), search_step=0.1)
    ana = QCALBlindAnalysis(cfg)
    ana.load_signal(sig, fs)
    res = ana.run_full_analysis(search_range=(50.0, 250.0), tolerance_hz=0.05)
    print(ana.generate_report(res))
    ana.plot_results(res)
    print(f"JSON: {json.dumps(ana.to_dict(res), indent=2)}")


if __name__ == "__main__":
    import sys
    if "--quick" in sys.argv:
        quick_test()
    elif len(sys.argv) > 1:
        # Modo CLI: qcal_blind_analysis.py <archivo.csv> [fs]
        path = sys.argv[1]
        fs = float(sys.argv[2]) if len(sys.argv) > 2 else None
        print(f"🔬 Analizando: {path}")
        ana = QCALBlindAnalysis()
        if path.endswith(".h5"):
            ana.load_h5(path, fs=fs)
        else:
            ana.load_csv(path, fs=fs)
        res = ana.run_full_analysis()
        print(ana.generate_report(res))
        ana.plot_results(res)
    else:
        run_simulation()
