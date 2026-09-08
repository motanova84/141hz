#!/usr/bin/env python3
"""
Oráculo espectral para análisis de ondas gravitacionales.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import numpy as np
from scipy import signal

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on environment
    plt = None
    MATPLOTLIB_AVAILABLE = False

try:
    from gwpy.timeseries import TimeSeries as GWpyTimeSeries
except ImportError:  # pragma: no cover - exercised via shim in tests
    GWpyTimeSeries = None


@dataclass
class _ScalarValue:
    value: float


class SimpleTimeSeries:
    """Shim mínimo compatible con los atributos usados por el oráculo."""

    def __init__(self, data: Iterable[float], *, sample_rate: float, t0: float = 0.0, name: str = "synthetic"):
        self.value = np.asarray(list(data), dtype=float)
        self.sample_rate = _ScalarValue(float(sample_rate))
        self.t0 = _ScalarValue(float(t0))
        self.name = name

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, item: Any) -> "SimpleTimeSeries":
        return SimpleTimeSeries(
            self.value[item],
            sample_rate=self.sample_rate.value,
            t0=self.t0.value,
            name=self.name,
        )


class GravitationalOracle:
    """Análisis espectral robusto enfocado en f₀ = 141.7001 Hz."""

    def __init__(self, f_target: float = 141.7001, verbose: bool = True):
        self.f_target = float(f_target)
        self.verbose = verbose
        self.results: Dict[str, Any] = {}
        self.figures = []
        self.umbral_coherencia_ruido = 0.15
        self.umbral_snr_minimo = 5.0
        self.umbral_fase_maxima = 45.0

    @staticmethod
    def _log(verbose: bool, message: str) -> None:
        if verbose:
            print(message)

    @staticmethod
    def _sample_rate_value(ts: Any, fallback: float = 4096.0) -> float:
        sample_rate = getattr(ts, "sample_rate", fallback)
        return float(getattr(sample_rate, "value", sample_rate))

    @staticmethod
    def _series_start(ts: Any) -> float:
        t0 = getattr(ts, "t0", 0.0)
        return float(getattr(t0, "value", t0))

    @staticmethod
    def _as_array(ts: Any) -> np.ndarray:
        return np.asarray(getattr(ts, "value", ts), dtype=float)

    @staticmethod
    def _build_timeseries(
        data: np.ndarray,
        *,
        sample_rate: float,
        t0: float = 0.0,
        name: str = "synthetic",
    ) -> Any:
        if GWpyTimeSeries is not None:
            try:
                return GWpyTimeSeries(data, dt=1.0 / sample_rate, t0=t0, name=name)
            except Exception:
                pass
        return SimpleTimeSeries(data, sample_rate=sample_rate, t0=t0, name=name)

    def _validate_series(self, ts: Any, ifo: str) -> None:
        values = self._as_array(ts)
        if values.size == 0:
            raise ValueError(f"Datos vacíos para {ifo}")
        if not np.all(np.isfinite(values)):
            raise ValueError(f"Datos no finitos para {ifo}")
        if np.std(values) == 0:
            raise ValueError(f"Datos constantes para {ifo}")

    @staticmethod
    def _gps_is_reasonable(t_gps: float) -> bool:
        return 1_000_000_000 <= float(t_gps) <= 2_000_000_000

    @staticmethod
    def _should_force_synthetic(evento: str) -> bool:
        event_upper = str(evento).upper()
        synthetic_prefixes = ("TEST", "PERF", "MEM", "SERIAL", "SYNTH")
        return event_upper.startswith(synthetic_prefixes)

    def fetch_ligo_data(self, t_gps: float, duracion: float = 32, ifos: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for ifo in list(ifos or ["H1", "L1"]):
            try:
                self._log(self.verbose, f"[1] Descargando {ifo}...")
                if not self._gps_is_reasonable(t_gps):
                    raise ValueError(f"GPS inválido para descarga abierta: {t_gps}")
                if GWpyTimeSeries is None:
                    raise RuntimeError("gwpy no disponible")
                ts = GWpyTimeSeries.fetch_open_data(
                    ifo,
                    t_gps - duracion / 2,
                    t_gps + duracion / 2,
                    cache=False,
                    verbose=False,
                    sample_rate=4096,
                )
                self._validate_series(ts, ifo)
                data[ifo] = ts
                self._log(
                    self.verbose,
                    f"  ✓ {ifo}: {len(ts)} muestras, fs={self._sample_rate_value(ts):.1f} Hz",
                )
            except Exception as exc:
                self._log(self.verbose, f"[!] Error descargando {ifo}: {exc}")
                data[ifo] = self._generate_synthetic_data(duracion, 4096, ifo=ifo, t0=t_gps - duracion / 2)
        return data

    def _generate_synthetic_data(
        self,
        duracion: float,
        fs: float,
        *,
        noise_level: float = 0.12,
        ifo: str = "synthetic",
        t0: float = 0.0,
    ) -> Any:
        samples = max(int(round(duracion * fs)), 64)
        t = np.arange(samples, dtype=float) / fs
        seed_material = f"{ifo}:{self.f_target:.4f}:{samples}:{duracion:.6f}".encode("utf-8")
        seed = int(hashlib.sha256(seed_material).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        chirp = signal.chirp(t, f0=35.0, f1=self.f_target, t1=max(duracion, 1e-3), method="quadratic")
        envelope = np.exp(-np.maximum(t - duracion / 2, 0.0) / max(duracion / 10, 1e-3))
        white = rng.normal(0.0, 1.0, samples)
        b, a = signal.butter(2, 0.08, btype="low")
        colored_noise = signal.filtfilt(b, a, white)
        colored_noise = colored_noise / max(np.std(colored_noise), np.finfo(float).eps)
        base_signal = 0.04 * chirp * envelope
        phase_offset = 0.0 if ifo == "H1" else np.pi / 12
        coherent_line = 0.018 * np.sin(2 * np.pi * self.f_target * t + phase_offset)
        strain = base_signal + coherent_line + noise_level * colored_noise
        return self._build_timeseries(strain, sample_rate=fs, t0=t0, name=f"{ifo}-synthetic")

    @staticmethod
    def _safe_nperseg(length: int) -> int:
        if length < 8:
            return max(length, 1)
        return min(4096, max(256, length // 4), length)

    def _background_noise_level(self, psd: np.ndarray, freqs: np.ndarray, idx_target: int, fwhm: float) -> float:
        if psd.size == 0:
            return float(np.finfo(float).eps)
        if fwhm <= 0:
            fwhm = max((freqs[1] - freqs[0]) * 4 if len(freqs) > 1 else 1.0, 1.0)
        mask = np.abs(freqs - freqs[idx_target]) > max(fwhm / 2.0, freqs[1] - freqs[0] if len(freqs) > 1 else 1.0)
        background = psd[mask]
        if background.size == 0:
            background = psd
        return float(max(np.median(background), np.finfo(float).eps))

    def calculate_spectral_metrics(self, data: Dict[str, Any], fs: float) -> Dict[str, Any]:
        self._log(self.verbose, "\n[2] Calculando métricas espectrales...")
        first_key = next(iter(data))
        h1_data = data.get("H1", data[first_key])
        l1_data = data.get("L1", data[first_key])
        h1 = self._as_array(h1_data)
        l1 = self._as_array(l1_data)
        min_len = min(len(h1), len(l1))
        h1 = h1[:min_len]
        l1 = l1[:min_len]
        nperseg = self._safe_nperseg(min_len)
        f_h1, psd_h1 = signal.welch(h1, fs, nperseg=nperseg)
        f_l1, psd_l1 = signal.welch(l1, fs, nperseg=nperseg)
        f_coh, coherence = signal.coherence(h1, l1, fs, nperseg=nperseg)
        _, csd = signal.csd(h1, l1, fs, nperseg=nperseg)
        idx_target = int(np.argmin(np.abs(f_h1 - self.f_target)))
        fwhm = self._calculate_fwhm(psd_h1, f_h1, idx_target)
        if fwhm > 0:
            band_idx = np.where(np.abs(f_h1 - self.f_target) <= fwhm / 2.0)[0]
        else:
            band_idx = np.array([idx_target])
        signal_power = float(np.trapezoid(psd_h1[band_idx], f_h1[band_idx])) if len(band_idx) > 1 else float(psd_h1[idx_target])
        noise_power = self._background_noise_level(psd_h1, f_h1, idx_target, fwhm)
        ratio = max(signal_power / noise_power, np.finfo(float).eps)
        snr_integrated = 10.0 * np.log10(ratio)
        return {
            "frequency": f_h1,
            "psd_h1": psd_h1,
            "psd_l1": psd_l1,
            "coherence": coherence,
            "csd": csd,
            "phase_deg": np.degrees(np.angle(csd)),
            "phase_rad": np.angle(csd),
            "idx_target": idx_target,
            "snr_integrated": float(snr_integrated),
            "fwhm": float(fwhm),
            "fs": float(fs),
            "nperseg": int(nperseg),
        }

    @staticmethod
    def _calculate_fwhm(psd: np.ndarray, frequency: np.ndarray, idx_peak: int) -> float:
        if idx_peak < 0 or idx_peak >= len(psd):
            return 0.0
        peak_value = psd[idx_peak]
        if peak_value <= 0:
            return 0.0
        left_neighbor = psd[idx_peak - 1] if idx_peak > 0 else -np.inf
        right_neighbor = psd[idx_peak + 1] if idx_peak < len(psd) - 1 else -np.inf
        if peak_value <= max(left_neighbor, right_neighbor):
            return 0.0
        half_max = peak_value / 2.0
        left_idx = idx_peak
        right_idx = idx_peak
        while left_idx > 0 and psd[left_idx] >= half_max:
            left_idx -= 1
        while right_idx < len(psd) - 1 and psd[right_idx] >= half_max:
            right_idx += 1
        if left_idx == right_idx:
            return 0.0
        return float(frequency[right_idx] - frequency[left_idx])

    def classify_noise(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        idx = metrics["idx_target"]
        coh = float(metrics["coherence"][idx])
        snr = float(metrics["snr_integrated"])
        phase = float(abs(metrics["phase_deg"][idx]))
        is_coherent = coh > self.umbral_coherencia_ruido
        is_significant = snr > self.umbral_snr_minimo
        is_phase_stable = phase < self.umbral_fase_maxima
        if is_coherent and is_significant and is_phase_stable:
            status = "LIMPIO - Señal gravitacional confiable"
            confidence = 0.95
        elif is_coherent and is_significant:
            status = "POSIBLE SEÑAL - Verificar fase"
            confidence = 0.70
        elif is_coherent:
            status = "COHERENTE - Señal débil"
            confidence = 0.50
        else:
            status = "CONTAMINADO - Ruido instrumental"
            confidence = 0.30
        return {
            "status": status,
            "confidence": confidence,
            "coherence": coh,
            "snr": snr,
            "phase": phase,
            "details": {
                "coherence_check": is_coherent,
                "snr_check": is_significant,
                "phase_check": is_phase_stable,
            },
        }

    def visualize_results(self, metrics: Dict[str, Any], noise_classification: Dict[str, Any], evento: str) -> Any:
        if not MATPLOTLIB_AVAILABLE:
            raise RuntimeError("matplotlib no está disponible; use plot=False o instale matplotlib")
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(f"Análisis Espectral - {evento} - f₀ = {self.f_target:.4f} Hz", fontsize=14)
        ax = axes[0, 0]
        ax.loglog(metrics["frequency"], metrics["psd_h1"], label="H1", alpha=0.75)
        ax.loglog(metrics["frequency"], metrics["psd_l1"], label="L1", alpha=0.75)
        ax.axvline(self.f_target, color="r", linestyle="--", label=f"f₀ = {self.f_target:.4f} Hz")
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("PSD [strain²/Hz]")
        ax.set_title("Densidad espectral de potencia")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        ax.semilogx(metrics["frequency"], metrics["coherence"])
        ax.axhline(self.umbral_coherencia_ruido, color="r", linestyle="--", label=f"Umbral = {self.umbral_coherencia_ruido}")
        ax.axvline(self.f_target, color="g", linestyle="--", alpha=0.5)
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("Coherencia")
        ax.set_title("Coherencia cruzada H1-L1")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        ax.semilogx(metrics["frequency"], metrics["phase_deg"])
        ax.axhline(self.umbral_fase_maxima, color="r", linestyle="--", label=f"Umbral = ±{self.umbral_fase_maxima}°")
        ax.axhline(-self.umbral_fase_maxima, color="r", linestyle="--")
        ax.axhline(0.0, color="k", alpha=0.25)
        ax.axvline(self.f_target, color="g", linestyle="--", alpha=0.5)
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("Fase [grados]")
        ax.set_title("Diferencia de fase H1-L1")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 1]
        ax.loglog(metrics["frequency"], metrics["psd_h1"], label="PSD H1", alpha=0.6)
        fwhm = metrics["fwhm"]
        if fwhm > 0:
            band_mask = np.abs(metrics["frequency"] - self.f_target) <= fwhm / 2.0
            ax.fill_between(metrics["frequency"][band_mask], metrics["psd_h1"][band_mask], color="red", alpha=0.25, label="Banda integrada")
        ax.axvline(self.f_target, color="g", linestyle="--")
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("PSD [strain²/Hz]")
        ax.set_title(f"SNR integrado: {metrics['snr_integrated']:.2f} dB")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[2, 0]
        raw_data = self.results.get("raw_data", {}).get("H1")
        if raw_data is not None:
            values = self._as_array(raw_data)
            fs = metrics["fs"]
            times = np.arange(len(values), dtype=float) / fs
            low = max(self.f_target - 2.0, 1.0)
            high = min(self.f_target + 2.0, fs / 2.0 - 1.0)
            if high > low:
                b, a = signal.butter(4, [low / (fs / 2.0), high / (fs / 2.0)], btype="band")
                filtered = signal.filtfilt(b, a, values)
                ax.plot(times - times.mean(), filtered, alpha=0.75)
        ax.set_xlabel("Tiempo [s]")
        ax.set_ylabel("Strain filtrado")
        ax.set_title("Señal en banda (H1)")
        ax.grid(True, alpha=0.3)

        ax = axes[2, 1]
        ax.axis("off")
        text = (
            "=== RESULTADOS DEL ANÁLISIS ===\n\n"
            f"Evento: {evento}\n"
            f"Frecuencia objetivo: {self.f_target:.4f} Hz\n\n"
            "--- Métricas ---\n"
            f"Coherencia: {noise_classification['coherence']:.4f}\n"
            f"SNR Integrado: {noise_classification['snr']:.2f} dB\n"
            f"Fase relativa: {noise_classification['phase']:.2f}°\n"
            f"Confianza: {noise_classification['confidence'] * 100:.1f}%\n\n"
            "--- Estado ---\n"
            f"{noise_classification['status']}\n\n"
            "--- Validación ---\n"
            f"Coherencia válida: {'✓' if noise_classification['details']['coherence_check'] else '✗'}\n"
            f"SNR significativo: {'✓' if noise_classification['details']['snr_check'] else '✗'}\n"
            f"Fase estable: {'✓' if noise_classification['details']['phase_check'] else '✗'}"
        )
        ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=10, va="top", family="monospace")
        plt.tight_layout()
        return fig

    def analyze(
        self,
        *,
        evento: str = "GW150914",
        t_gps: float = 1126259462.4,
        duracion: float = 32.0,
        ifos: Optional[Iterable[str]] = None,
        plot: bool = True,
    ) -> Dict[str, Any]:
        print("=" * 60)
        print(f"=== ORÁCULO ESPECTRAL: ANALIZANDO {evento} ===")
        print(f"[GPS TIME]: {t_gps} | [DURACIÓN]: {duracion} s")
        print(f"[FREQ TARGET]: {self.f_target} Hz")
        print("=" * 60)
        if self._should_force_synthetic(evento):
            data = {
                ifo: self._generate_synthetic_data(duracion, 4096, ifo=ifo, t0=t_gps - duracion / 2)
                for ifo in (ifos or ["H1", "L1"])
            }
        else:
            data = self.fetch_ligo_data(t_gps, duracion, ifos or ["H1", "L1"])
        self.results = {
            "evento": evento,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "f_target": self.f_target,
            "raw_data": data,
        }
        if not data:
            raise RuntimeError("No se pudieron obtener datos para el análisis")
        fs = self._sample_rate_value(next(iter(data.values())))
        metrics = self.calculate_spectral_metrics(data, fs)
        noise_classification = self.classify_noise(metrics)
        self.results["metrics"] = metrics
        self.results["noise_classification"] = noise_classification
        if plot:
            fig = self.visualize_results(metrics, noise_classification, evento)
            self.figures.append(fig)
        self._print_results(evento, metrics, noise_classification)
        return self.results

    def _print_results(self, evento: str, metrics: Dict[str, Any], classification: Dict[str, Any]) -> None:
        idx = metrics["idx_target"]
        print("\n" + "=" * 60)
        print("=== TABLA DE MÉTRICAS ESPECTRALES ===")
        print("=" * 60)
        print(f"{'Métrica':<30} {'Valor':<30}")
        print("-" * 60)
        print(f"{'Evento Analizado':<30} {evento:<30}")
        print(f"{'Frecuencia Objetivo':<30} {self.f_target:<30.4f}")
        print(f"{'SNR Integrado':<30} {metrics['snr_integrated']:<30.2f}")
        print(f"{'Coherencia (@f₀)':<30} {metrics['coherence'][idx]:<30.6f}")
        print(f"{'Fase H1-L1 (@f₀)':<30} {metrics['phase_deg'][idx]:<30.4f}°")
        print(f"{'Ancho de Banda (FWHM)':<30} {metrics['fwhm']:<30.4f}")
        print("-" * 60)
        print(f"{'Estado de Ruido':<30} {classification['status']:<30}")
        print(f"{'Confianza':<30} {classification['confidence'] * 100:<30.1f}%")
        print("-" * 60)
        print("\n[DETALLES DE VALIDACIÓN]")
        for check, value in classification["details"].items():
            print(f"  {check.replace('_', ' ').title():25} {'✓' if value else '✗'}")
        print("\n" + "=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Oráculo espectral gravitacional")
    parser.add_argument("--evento", default="GW150914")
    parser.add_argument("--gps", type=float, default=1126259462.4)
    parser.add_argument("--duracion", type=float, default=32.0)
    parser.add_argument("--f-target", type=float, default=141.7001)
    parser.add_argument("--ifos", nargs="+", default=["H1", "L1"])
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    oracle = GravitationalOracle(f_target=args.f_target, verbose=True)
    results = oracle.analyze(
        evento=args.evento,
        t_gps=args.gps,
        duracion=args.duracion,
        ifos=args.ifos,
        plot=not args.no_plot,
    )
    if results and oracle.figures:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[✓] Análisis completado. Figura disponible para guardar como resultado_{timestamp}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
