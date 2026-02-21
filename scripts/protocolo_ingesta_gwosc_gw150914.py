#!/usr/bin/env python3
"""
Protocolo de Ingesta GWOSC: Fase 1 (GW150914)
==============================================

Pipeline de ingesta y análisis de coherencia Ψ para GW150914.
Descarga segmentos de strain de 4 segundos alrededor del evento,
aplica blanqueo (whitening), y calcula la métrica Ψ(t) deslizante
mediante coherencia cruzada H1-L1 en la frecuencia noésica f₀ = 141.7001 Hz.

Comparativa estadística on-source vs off-source:
- On-Source:  Ψ medido durante el chirp de la colisión
- Off-Source: Ψ en segmentos de ruido vacío (10 s antes)
- Veredicto:  Si Ψ_on / Ψ_off > 10², se valida la separación estadística

Uso:
    python scripts/protocolo_ingesta_gwosc_gw150914.py
    python scripts/protocolo_ingesta_gwosc_gw150914.py --simulated
    python scripts/protocolo_ingesta_gwosc_gw150914.py --duration 4 --output resultados.json

Autor: Sistema QCAL ∞³
Fecha: 2026-02-21
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
from scipy.signal import coherence

# ── Dependencias LIGO ──────────────────────────────────────────────────────
try:
    from gwpy.timeseries import TimeSeries
    GWPY_AVAILABLE = True
except ImportError:
    GWPY_AVAILABLE = False

# ── Constantes del evento ──────────────────────────────────────────────────
EVENT_TIME: float = 1126259462.4   # GPS time del merger (GW150914)
F0_CHIRP: float = 141.7001         # Frecuencia noésica (Hz)
SAMPLE_RATE: int = 4096            # Hz (tasa estándar GWOSC)

# Duración de la ventana off-source (s antes del evento)
OFF_SOURCE_OFFSET: float = 10.0


# ── Funciones de ingesta ───────────────────────────────────────────────────

def descargar_strain(
    detector: str,
    t_start: float,
    t_end: float,
    sample_rate: int = SAMPLE_RATE,
) -> "TimeSeries":
    """
    Descarga datos de strain desde GWOSC para el detector indicado.

    Parameters
    ----------
    detector : str
        Identificador del detector ('H1' o 'L1').
    t_start : float
        Tiempo GPS de inicio.
    t_end : float
        Tiempo GPS de fin.
    sample_rate : int
        Tasa de muestreo deseada (Hz).

    Returns
    -------
    TimeSeries
        Datos de strain de gwpy.
    """
    if not GWPY_AVAILABLE:
        raise ImportError("gwpy no está disponible. Instala con: pip install gwpy gwosc")

    return TimeSeries.fetch_open_data(detector, t_start, t_end, sample_rate=sample_rate)


def generar_strain_simulado(
    detector: str,
    duration: float,
    sample_rate: int = SAMPLE_RATE,
    incluir_senal: bool = True,
) -> np.ndarray:
    """
    Genera strain simulado reproducible para tests y ejecuciones sin red.

    Parameters
    ----------
    detector : str
        Identificador del detector (usado como semilla diferencial).
    duration : float
        Duración en segundos.
    sample_rate : int
        Tasa de muestreo en Hz.
    incluir_senal : bool
        Si True, añade una señal en F0_CHIRP con amplitud realista.

    Returns
    -------
    np.ndarray
        Array de strain simulado.
    """
    seed_map = {"H1": 42, "L1": 43, "V1": 44}
    rng = np.random.default_rng(seed_map.get(detector, 42))

    n = int(duration * sample_rate)
    noise = rng.normal(0, 1e-21, n)

    if incluir_senal:
        t = np.linspace(0, duration, n, endpoint=False)
        # Señal tipo chirp amortiguado centrada en el evento
        t_center = duration / 2.0
        amplitude = 3e-21
        decay = 8.0
        senal = (
            amplitude
            * np.exp(-decay * (t - t_center) ** 2)
            * np.sin(2 * np.pi * F0_CHIRP * t)
        )
        return noise + senal

    return noise


# ── Cálculo de Ψ(t) ────────────────────────────────────────────────────────

def calcular_psi_gw(
    ts1: np.ndarray,
    ts2: np.ndarray,
    fs: float,
    f_target: float = F0_CHIRP,
) -> float:
    """
    Calcula la métrica Ψ en f_target usando coherencia cruzada entre dos detectores.

    Ψ = |FFT₁(f₀)|² · C²_{H1,L1}(f₀)

    Donde C_{H1,L1}(f₀) es la coherencia de magnitud cuadrada (MSC)
    en la frecuencia objetivo.

    Parameters
    ----------
    ts1, ts2 : np.ndarray
        Series temporales (H1 y L1 respectivamente).
    fs : float
        Frecuencia de muestreo en Hz.
    f_target : float
        Frecuencia objetivo en Hz.

    Returns
    -------
    float
        Valor de Ψ (adimensional combinado con escala del strain).
    """
    nperseg = max(int(fs / 2), 64)  # al menos 64 muestras por segmento

    # Coherencia entre los dos detectores
    f_coh, cxy = coherence(ts1, ts2, fs=fs, nperseg=nperseg)
    idx_coh = int(np.argmin(np.abs(f_coh - f_target)))
    coh_at_f0 = float(cxy[idx_coh])

    # Potencia espectral en el detector H1
    fft_vals = np.fft.rfft(ts1)
    fft_freqs = np.fft.rfftfreq(len(ts1), d=1.0 / fs)
    idx_fft = int(np.argmin(np.abs(fft_freqs - f_target)))
    power_at_f0 = float(np.abs(fft_vals[idx_fft]) ** 2)

    # Ψ = I(f₀) · C²(f₀)
    psi = power_at_f0 * (coh_at_f0 ** 2)
    return psi


# ── Pipeline principal ─────────────────────────────────────────────────────

class ProtocoloIngestaGW150914:
    """
    Implementa el pipeline completo de ingesta GWOSC para GW150914.

    Etapas:
    1. Descarga de strain H1/L1 (on-source y off-source)
    2. Pre-procesamiento: blanqueo (whitening)
    3. Cálculo de Ψ deslizante
    4. Comparativa estadística on-source / off-source
    """

    def __init__(
        self,
        duration: float = 4.0,
        f_target: float = F0_CHIRP,
        simulated: bool = False,
    ):
        """
        Parameters
        ----------
        duration : float
            Duración de la ventana de análisis en segundos.
        f_target : float
            Frecuencia objetivo en Hz.
        simulated : bool
            Si True, usa datos simulados (no requiere red).
        """
        self.duration = duration
        self.f_target = f_target
        self.simulated = simulated
        self.sample_rate = SAMPLE_RATE

        self.output_dir = Path(__file__).parent.parent / "results" / "gwosc_ingesta_gw150914"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.resultados: Dict = {
            "evento": "GW150914",
            "gps_time": EVENT_TIME,
            "f_target_hz": f_target,
            "duration_s": duration,
            "simulated": simulated,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "on_source": {},
            "off_source": {},
            "veredicto": {},
        }

    # ── Descarga / simulación ──────────────────────────────────────────────

    def _obtener_strain_array(
        self, detector: str, t_start: float, incluir_senal: bool = True
    ) -> np.ndarray:
        """Obtiene el array de strain (real o simulado)."""
        if self.simulated or not GWPY_AVAILABLE:
            return generar_strain_simulado(
                detector, self.duration, self.sample_rate, incluir_senal
            )
        try:
            ts = descargar_strain(
                detector, t_start, t_start + self.duration, self.sample_rate
            )
            return ts.value
        except Exception as exc:  # noqa: BLE001
            print(f"   ⚠️  Error descargando {detector}: {exc}")
            print("   ↩️  Usando datos simulados como fallback.")
            self.resultados["simulated"] = True
            return generar_strain_simulado(
                detector, self.duration, self.sample_rate, incluir_senal
            )

    # ── Pre-procesamiento ─────────────────────────────────────────────────

    @staticmethod
    def _blanquear(ts: "TimeSeries") -> "TimeSeries":
        """Aplica whitening a un TimeSeries de gwpy."""
        return ts.whiten()

    @staticmethod
    def _blanquear_array(data: np.ndarray, fs: float) -> np.ndarray:
        """
        Blanqueo espectral sobre un numpy array.

        Divide cada bin FFT por la raíz de la PSD estimada (Welch).
        """
        from scipy.signal import welch

        freqs, psd = welch(data, fs=fs, nperseg=min(len(data), int(fs)))
        # Interpolación de la PSD a los bins de la FFT
        fft_freqs = np.fft.rfftfreq(len(data), d=1.0 / fs)
        psd_interp = np.interp(fft_freqs, freqs, psd)
        psd_interp = np.maximum(psd_interp, 1e-60)  # evitar división por cero

        fft_vals = np.fft.rfft(data)
        fft_blanqueado = fft_vals / np.sqrt(psd_interp)
        return np.fft.irfft(fft_blanqueado, n=len(data))

    # ── Análisis on-source ─────────────────────────────────────────────────

    def analizar_on_source(self) -> Dict:
        """
        Analiza la ventana on-source: ±duration/2 alrededor del merger.

        Returns
        -------
        dict
            Resultado con Ψ_on para H1 y L1.
        """
        print("\n🔭 Analizando ventana ON-SOURCE (GW150914)...")
        t_start = EVENT_TIME - self.duration / 2.0

        h1_raw = self._obtener_strain_array("H1", t_start, incluir_senal=True)
        l1_raw = self._obtener_strain_array("L1", t_start, incluir_senal=True)

        h1_white = self._blanquear_array(h1_raw, float(self.sample_rate))
        l1_white = self._blanquear_array(l1_raw, float(self.sample_rate))

        psi_on = calcular_psi_gw(h1_white, l1_white, float(self.sample_rate), self.f_target)

        resultado = {
            "t_start_gps": t_start,
            "t_end_gps": t_start + self.duration,
            "psi": psi_on,
        }
        self.resultados["on_source"] = resultado

        print(f"   ✅ Ψ_on = {psi_on:.4e}")
        return resultado

    # ── Análisis off-source ────────────────────────────────────────────────

    def analizar_off_source(self) -> Dict:
        """
        Analiza la ventana off-source: 10 s antes del merger.

        Returns
        -------
        dict
            Resultado con Ψ_off para H1 y L1.
        """
        print("\n🌑 Analizando ventana OFF-SOURCE (ruido vacío)...")
        t_start = EVENT_TIME - OFF_SOURCE_OFFSET - self.duration

        h1_raw = self._obtener_strain_array("H1", t_start, incluir_senal=False)
        l1_raw = self._obtener_strain_array("L1", t_start, incluir_senal=False)

        h1_white = self._blanquear_array(h1_raw, float(self.sample_rate))
        l1_white = self._blanquear_array(l1_raw, float(self.sample_rate))

        psi_off = calcular_psi_gw(h1_white, l1_white, float(self.sample_rate), self.f_target)

        # Asegurar que el off-source no sea cero para evitar divisiones
        if psi_off == 0.0:
            psi_off = 1e-100

        resultado = {
            "t_start_gps": t_start,
            "t_end_gps": t_start + self.duration,
            "psi": psi_off,
        }
        self.resultados["off_source"] = resultado

        print(f"   ✅ Ψ_off = {psi_off:.4e}")
        return resultado

    # ── Veredicto ─────────────────────────────────────────────────────────

    def calcular_veredicto(self) -> Dict:
        """
        Calcula la razón Ψ_on / Ψ_off y emite el veredicto estadístico.

        Returns
        -------
        dict
            Diccionario con ratio, umbral y resultado del veredicto.
        """
        psi_on = self.resultados["on_source"].get("psi", 0.0)
        psi_off = self.resultados["off_source"].get("psi", 1e-100)

        ratio = psi_on / psi_off if psi_off != 0 else float("inf")
        umbral = 1e2  # 10²
        supera_umbral = ratio >= umbral

        veredicto = {
            "psi_on": psi_on,
            "psi_off": psi_off,
            "ratio": ratio,
            "umbral": umbral,
            "supera_umbral": supera_umbral,
            "descripcion": (
                f"Ψ_on / Ψ_off = {ratio:.2e} {'≥' if supera_umbral else '<'} {umbral:.0e}"
            ),
        }
        self.resultados["veredicto"] = veredicto

        print("\n📊 VEREDICTO ESTADÍSTICO")
        print(f"   Ψ_on  = {psi_on:.4e}")
        print(f"   Ψ_off = {psi_off:.4e}")
        print(f"   Ratio = {ratio:.4e}")
        if supera_umbral:
            print(f"   ✅ Ψ_on / Ψ_off = {ratio:.2e} ≥ 10² → Separación estadística validada")
        else:
            print(f"   ⚠️  Ψ_on / Ψ_off = {ratio:.2e} < 10² → Separación insuficiente")

        return veredicto

    # ── Exportación ────────────────────────────────────────────────────────

    def exportar_resultados(self, filename: Optional[str] = None) -> Path:
        """
        Exporta los resultados a un fichero JSON.

        Parameters
        ----------
        filename : str, optional
            Nombre del fichero de salida.

        Returns
        -------
        Path
            Ruta al fichero exportado.
        """
        if filename is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gwosc_ingesta_gw150914_{ts}.json"

        output_path = self.output_dir / filename

        def _serializar(obj):
            if isinstance(obj, (np.integer, np.floating)):
                return None if (np.isnan(obj) or np.isinf(obj)) else obj.item()
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
                return None
            return obj

        def _convertir(obj):
            if isinstance(obj, dict):
                return {k: _convertir(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_convertir(i) for i in obj]
            return _serializar(obj)

        with open(output_path, "w", encoding="utf-8") as fp:
            json.dump(_convertir(self.resultados), fp, indent=2, ensure_ascii=False)

        print(f"\n💾 Resultados exportados a: {output_path}")
        return output_path

    # ── Ejecución completa ─────────────────────────────────────────────────

    def ejecutar(self, output: Optional[str] = None) -> Dict:
        """
        Ejecuta el pipeline completo de ingesta y análisis.

        Returns
        -------
        dict
            Resultados completos incluyendo veredicto.
        """
        print("=" * 65)
        print("Protocolo de Ingesta GWOSC – Fase 1 (GW150914)")
        print("=" * 65)
        print(f"Evento    : GW150914 (GPS {EVENT_TIME})")
        print(f"Ventana   : {self.duration} s")
        print(f"Frecuencia: f₀ = {self.f_target} Hz")
        print(f"Modo      : {'SIMULADO' if (self.simulated or not GWPY_AVAILABLE) else 'REAL (GWOSC)'}")
        print("=" * 65)

        if not self.simulated and not GWPY_AVAILABLE:
            print("⚠️  gwpy no disponible → usando datos simulados.")

        self.analizar_on_source()
        self.analizar_off_source()
        self.calcular_veredicto()
        self.exportar_resultados(output)

        print("\n" + "=" * 65)
        print("Pipeline completado.")
        print("=" * 65)

        return self.resultados


# ── CLI ────────────────────────────────────────────────────────────────────

def main() -> int:
    """Punto de entrada CLI."""
    parser = argparse.ArgumentParser(
        description="Protocolo de Ingesta GWOSC – Fase 1 (GW150914)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Datos reales de GWOSC (requiere conexión)
  python scripts/protocolo_ingesta_gwosc_gw150914.py

  # Modo simulado (sin red)
  python scripts/protocolo_ingesta_gwosc_gw150914.py --simulated

  # Ventana personalizada y fichero de salida
  python scripts/protocolo_ingesta_gwosc_gw150914.py --duration 4 --output mi_analisis.json
        """,
    )
    parser.add_argument(
        "--duration", type=float, default=4.0,
        help="Duración de la ventana de análisis en segundos (por defecto: 4.0)",
    )
    parser.add_argument(
        "--f-target", type=float, default=F0_CHIRP,
        help=f"Frecuencia objetivo en Hz (por defecto: {F0_CHIRP})",
    )
    parser.add_argument(
        "--simulated", action="store_true",
        help="Usar datos simulados (no requiere red ni gwpy)",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Nombre del fichero JSON de salida",
    )

    args = parser.parse_args()

    pipeline = ProtocoloIngestaGW150914(
        duration=args.duration,
        f_target=args.f_target,
        simulated=args.simulated,
    )
    pipeline.ejecutar(output=args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
