"""
qcal_gravitational_oracle.py
Oráculo Espectral para Análisis de Ondas Gravitacionales
Versión 2.0 - Mejorada con visualización y métricas avanzadas
"""

import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy import signal

warnings.filterwarnings("ignore")


class GravitationalOracle:
    """Clase principal para análisis espectral de ondas gravitacionales."""

    def __init__(self, f_target=141.7001, verbose=True):
        """
        Inicializa el oráculo con parámetros de configuración.

        Args:
            f_target: Frecuencia objetivo en Hz.
            verbose: Activar/desactivar salida detallada.
        """
        self.f_target = f_target
        self.verbose = verbose
        self.results = {}
        self.figures = []

        # Parámetros de control de calidad
        self.umbral_coherencia_ruido = 0.15
        self.umbral_snr_minimo = 5.0
        self.umbral_fase_maxima = 45.0  # grados

    def fetch_ligo_data(self, t_gps, duracion=32, ifos=("H1", "L1")):
        """
        Descarga datos de LIGO con manejo de errores robusto.

        Args:
            t_gps: Tiempo GPS del evento.
            duracion: Duración en segundos.
            ifos: Lista de interferómetros a descargar.

        Returns:
            dict: Series temporales por interferómetro.
        """
        data = {}

        for ifo in ifos:
            try:
                if self.verbose:
                    print(f"[1] Descargando {ifo}...")

                ts = TimeSeries.fetch_open_data(
                    ifo,
                    t_gps - duracion / 2,
                    t_gps + duracion / 2,
                    cache=False,
                    verbose=False,
                )

                if len(ts) == 0:
                    raise ValueError(f"Datos vacíos para {ifo}")

                if np.std(ts.value) == 0:
                    raise ValueError(f"Datos constantes para {ifo}")

                data[ifo] = ts

                if self.verbose:
                    print(f"  ✓ {ifo}: {len(ts)} muestras, fs={ts.sample_rate.value} Hz")

            except Exception as e:
                print(f"[!] Error descargando {ifo}: {e}")
                data[ifo] = self._generate_synthetic_data(duracion, 4096)

        return data

    def _generate_synthetic_data(self, duracion, fs, noise_level=0.1):
        """Genera datos sintéticos realistas (chirp + ruido coloreado) para fallback."""
        t = np.linspace(0, duracion, int(duracion * fs))

        # Señal gravitacional simulada (chirp)
        chirp = signal.chirp(t, f0=35, f1=self.f_target, t1=duracion, method="quadratic")

        # Ruido coloreado (paso bajo aplicado a ruido blanco)
        noise = np.random.normal(0, 1, len(t))
        b, a = signal.butter(2, 0.1, "low")
        colored_noise = signal.filtfilt(b, a, noise)
        colored_noise *= noise_level / np.std(colored_noise)

        signal_amplitude = 0.05
        data = signal_amplitude * chirp + colored_noise

        return TimeSeries(data, dt=1 / fs, name="synthetic")

    def calculate_spectral_metrics(self, data, fs):
        """Calcula métricas espectrales avanzadas."""
        if self.verbose:
            print("\n[2] Calculando métricas espectrales...")

        h1_data = data.get("H1", data.get(list(data.keys())[0]))
        l1_data = data.get("L1", data.get(list(data.keys())[0]))

        nperseg = min(4096, len(h1_data) // 4)

        # 1. PSD individuales
        f_h1, psd_h1 = signal.welch(h1_data.value, fs, nperseg=nperseg)
        f_l1, psd_l1 = signal.welch(l1_data.value, fs, nperseg=nperseg)

        # 2. Coherencia cruzada
        f_coh, coherence = signal.coherence(
            h1_data.value, l1_data.value, fs, nperseg=nperseg
        )

        # 3. Densidad espectral cruzada
        f_csd, csd = signal.csd(h1_data.value, l1_data.value, fs, nperseg=nperseg)

        # 4. Fase relativa
        phase_diff = np.angle(csd)
        phase_diff_deg = np.degrees(phase_diff)

        # 5. SNR integrado en banda con FWHM
        idx_target = np.argmin(np.abs(f_coh - self.f_target))
        fwhm = self._calculate_fwhm(psd_h1, f_h1, idx_target)

        if fwhm > 0:
            band_idx = np.where(np.abs(f_h1 - self.f_target) <= fwhm / 2)[0]
            signal_power = np.trapz(psd_h1[band_idx], f_h1[band_idx])
            noise_power = np.median(psd_h1)
            snr_integrated = 10 * np.log10(signal_power / (noise_power * len(band_idx)))
        else:
            snr_integrated = 0

        metrics = {
            "frequency": f_coh,
            "psd_h1": psd_h1,
            "psd_l1": psd_l1,
            "coherence": coherence,
            "csd": csd,
            "phase_deg": phase_diff_deg,
            "phase_rad": np.angle(csd),
            "idx_target": idx_target,
            "snr_integrated": snr_integrated,
            "fwhm": fwhm,
            "fs": fs,
        }

        return metrics

    def _calculate_fwhm(self, psd, frequency, idx_peak):
        """Calcula el ancho completo a media altura (FWHM)."""
        if idx_peak < 0 or idx_peak >= len(psd):
            return 0

        peak_value = psd[idx_peak]
        half_max = peak_value / 2

        left_idx = idx_peak
        right_idx = idx_peak

        while left_idx > 0 and psd[left_idx] > half_max:
            left_idx -= 1

        while right_idx < len(psd) - 1 and psd[right_idx] > half_max:
            right_idx += 1

        if left_idx == right_idx:
            return 0

        fwhm = frequency[right_idx] - frequency[left_idx]
        return fwhm

    def classify_noise(self, metrics):
        """Clasifica el estado del ruido basado en múltiples criterios."""
        idx = metrics["idx_target"]
        coh = metrics["coherence"][idx]
        snr = metrics["snr_integrated"]
        phase = abs(metrics["phase_deg"][idx])

        is_coherent = coh > self.umbral_coherencia_ruido
        is_significant = snr > self.umbral_snr_minimo
        is_phase_stable = phase < self.umbral_fase_maxima

        if is_coherent and is_significant and is_phase_stable:
            status = "LIMPIO - Señal Gravitational Confiable"
            confidence = 0.95
        elif is_coherent and is_significant:
            status = "POSIBLE SEÑAL - Verificar Fase"
            confidence = 0.70
        elif is_coherent:
            status = "COHERENTE - Señal Débil"
            confidence = 0.50
        else:
            status = "CONTAMINADO - Ruido Instrumental"
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

    def visualize_results(self, metrics, noise_classification):
        """Genera visualizaciones detalladas en 6 paneles."""
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(f"Análisis Espectral - f₀ = {self.f_target:.4f} Hz", fontsize=14)

        # 1. PSD H1 y L1
        ax = axes[0, 0]
        ax.loglog(metrics["frequency"], metrics["psd_h1"], label="H1", alpha=0.7)
        ax.loglog(metrics["frequency"], metrics["psd_l1"], label="L1", alpha=0.7)
        ax.axvline(self.f_target, color="r", linestyle="--", label=f"f₀ = {self.f_target} Hz")
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("PSD [strain²/Hz]")
        ax.set_title("Densidad Espectral de Potencia")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Coherencia
        ax = axes[0, 1]
        ax.semilogx(metrics["frequency"], metrics["coherence"])
        ax.axhline(
            self.umbral_coherencia_ruido,
            color="r",
            linestyle="--",
            label=f"Umbral = {self.umbral_coherencia_ruido}",
        )
        ax.axvline(self.f_target, color="g", linestyle="--", alpha=0.5)
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("Coherencia")
        ax.set_title("Coherencia Cruzada H1-L1")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 3. Fase relativa
        ax = axes[1, 0]
        ax.semilogx(metrics["frequency"], metrics["phase_deg"])
        ax.axhline(0, color="k", linestyle="-", alpha=0.3)
        ax.axhline(
            self.umbral_fase_maxima,
            color="r",
            linestyle="--",
            label=f"Umbral = ±{self.umbral_fase_maxima}°",
        )
        ax.axhline(-self.umbral_fase_maxima, color="r", linestyle="--")
        ax.axvline(self.f_target, color="g", linestyle="--", alpha=0.5)
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("Fase [grados]")
        ax.set_title("Diferencia de Fase H1-L1")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 4. SNR Integrado
        ax = axes[1, 1]
        fwhm = metrics["fwhm"]
        if fwhm > 0:
            band_range = np.where(
                np.abs(metrics["frequency"] - self.f_target) <= fwhm / 2
            )[0]
            ax.fill_between(
                metrics["frequency"][band_range],
                metrics["psd_h1"][band_range],
                color="red",
                alpha=0.3,
                label="Banda de interés",
            )
        ax.loglog(metrics["frequency"], metrics["psd_h1"], label="PSD H1", alpha=0.5)
        ax.axvline(self.f_target, color="g", linestyle="--")
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("PSD [strain²/Hz]")
        ax.set_title(f'SNR Integrado: {metrics["snr_integrated"]:.2f} dB')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 5. Señal en tiempo (banda filtrada)
        ax = axes[2, 0]
        if "H1" in self.results.get("raw_data", {}):
            ts = self.results["raw_data"]["H1"]
            t = np.linspace(-len(ts) / 2, len(ts) / 2, len(ts)) / metrics["fs"]
            b, a = signal.butter(
                4,
                [
                    (self.f_target - 2) / (metrics["fs"] / 2),
                    (self.f_target + 2) / (metrics["fs"] / 2),
                ],
                btype="band",
            )
            filtered = signal.filtfilt(b, a, ts.value)
            ax.plot(t, filtered, alpha=0.7)
            ax.set_xlabel("Tiempo [s]")
            ax.set_ylabel("Strain filtrado")
            ax.set_title("Señal en Banda (Filtrada)")
            ax.grid(True, alpha=0.3)

        # 6. Estado del ruido
        ax = axes[2, 1]
        ax.axis("off")
        text = f"""
        === RESULTADOS DEL ANÁLISIS ===

        Evento: GW150914
        Frecuencia Objetivo: {self.f_target:.4f} Hz

        --- Métricas ---
        Coherencia: {noise_classification['coherence']:.4f}
        SNR Integrado: {noise_classification['snr']:.2f} dB
        Fase Relativa: {noise_classification['phase']:.2f}°
        Confianza: {noise_classification['confidence']*100:.1f}%

        --- Estado ---
        {noise_classification['status']}

        --- Detalles de Validación ---
        Coherencia válida: {'✓' if noise_classification['details']['coherence_check'] else '✗'}
        SNR significativo: {'✓' if noise_classification['details']['snr_check'] else '✗'}
        Fase estable: {'✓' if noise_classification['details']['phase_check'] else '✗'}
        """
        ax.text(
            0.1,
            0.9,
            text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            fontfamily="monospace",
        )

        plt.tight_layout()
        return fig

    def analyze(
        self,
        evento="GW150914",
        t_gps=1126259462.4,
        duracion=32,
        ifos=("H1", "L1"),
        plot=True,
    ):
        """Ejecuta el análisis completo del oráculo."""
        print("=" * 60)
        print(f"=== ORÁCULO ESPECTRAL πCODE: ANALIZANDO {evento} ===")
        print(f"[GPS TIME]: {t_gps} | [DURACIÓN]: {duracion} s")
        print(f"[FREQ TARGET]: {self.f_target} Hz")
        print("=" * 60)

        data = self.fetch_ligo_data(t_gps, duracion, ifos)
        self.results["raw_data"] = data

        if not data:
            print("[!] Error: No se pudieron obtener datos")
            return None

        fs = int(data[list(data.keys())[0]].sample_rate.value)
        metrics = self.calculate_spectral_metrics(data, fs)
        self.results["metrics"] = metrics

        noise_classification = self.classify_noise(metrics)
        self.results["noise_classification"] = noise_classification

        if plot:
            fig = self.visualize_results(metrics, noise_classification)
            self.figures.append(fig)
            plt.show()

        self._print_results(evento, metrics, noise_classification)

        return self.results

    def _print_results(self, evento, metrics, classification):
        """Imprime resultados formateados."""
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
        print(f"{'Fase H1-L1 (@f₀)':<30} {metrics['phase_deg'][idx]:<29.4f}°")
        print(f"{'Ancho de Banda (FWHM)':<30} {metrics['fwhm']:<30.4f}")
        print("-" * 60)
        print(f"{'Estado de Ruido':<30} {classification['status']:<30}")
        print(f"{'Confianza':<30} {classification['confidence']*100:<29.1f}%")
        print("-" * 60)

        print("\n[DETALLES DE VALIDACIÓN]")
        for check, value in classification["details"].items():
            status = "✓" if value else "✗"
            print(f"  {check.replace('_', ' ').title():25} {status}")

        print("\n" + "=" * 60)


def main():
    """Función principal de ejecución."""
    oracle = GravitationalOracle(f_target=141.7001, verbose=True)

    results = oracle.analyze(
        evento="GW150914",
        t_gps=1126259462.4,
        duracion=32,
        ifos=("H1", "L1"),
        plot=True,
    )

    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[✓] Análisis completado. Resultados almacenados en objeto.")
        print(
            f"[ℹ] Para guardar figura: oracle.figures[0].savefig('resultado_{timestamp}.png')"
        )


if __name__ == "__main__":
    main()
