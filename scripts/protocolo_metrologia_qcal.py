#!/usr/bin/env python3
"""
Protocolo de Metrología QCAL - Puente hacia el Plano Observable
================================================================
Implementa el protocolo de medición estándar para la cuantificación
empírica de la coherencia Ψ_emp en el marco QCAL ∞³.

Metodología:
  1. Generación de serie temporal QRNG (fotones de Poisson simulados)
  2. Cálculo de entropía local S(t) = log(I / A_eff) en ventana deslizante
  3. Cálculo de Ψ_emp = 1 - (S_max - S_local) / S_max
  4. Exportación a data/raw_metrology/ en formato CSV auditable

Uso:
  python protocolo_metrologia_qcal.py --frequency 141.7001 --duration_s 300
  python protocolo_metrologia_qcal.py --frequency 0 --duration_s 60 --output baseline
  python protocolo_metrologia_qcal.py --help

Referencia: Protocolo de Metrología QCAL, sección 1 - El Puente Metrológico
"""

import argparse
import csv
import hashlib
import logging
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# CONSTANTES
# ============================================================

F0_HZ = 141.7001          # Frecuencia portadora fundamental (Hz)
N_NODOS = 7               # Área efectiva por defecto (nodos BAL-003)
INTENSIDAD_BASE = 418.0   # Intensidad de referencia (picodes/s)
SAMPLE_RATE_DEFAULT_HZ = 1.0     # Serie de baja resolución: 1 evento/segundo
SAMPLE_RATE_HIGH_HZ = 1000.0    # Serie de alta resolución: 1000 muestras/segundo
RUIDO_STD = 1e-6                 # Desviación estándar del ruido residual

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw_metrology"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
log = logging.getLogger(__name__)


# ============================================================
# CÁLCULO DE ENTROPÍA LOCAL
# ============================================================

def entropia_local(intensidad: float, a_eff: float) -> float:
    """
    Entropía local de la información: S = log(I / A_eff).

    Representa los bits por unidad de área efectiva en el sustrato receptor.

    Parámetros
    ----------
    intensidad : float
        Densidad de corriente de bits (picodes/s).
    a_eff : float
        Área efectiva (m² o nodos).

    Retorna
    -------
    float
        Entropía local en nats.
    """
    ratio = max(intensidad / a_eff, 1e-12)
    return float(np.log(ratio))


def psi_emp(s_local: float, s_max: float) -> float:
    """
    Coherencia empírica normalizada.

    Ψ_emp = 1 - (S_max - S_local) / S_max

    El valor tiende a 1 cuando la entropía local se aproxima a S_max
    (estado coherente máximo) y a 0 en el estado de ruido puro.

    Parámetros
    ----------
    s_local : float
        Entropía local de la medición actual.
    s_max : float
        Entropía de referencia máxima (línea de base de ruido).

    Retorna
    -------
    float
        Coherencia empírica en [0, 1].
    """
    if abs(s_max) < 1e-15:
        return 0.0
    return float(np.clip(1.0 - (s_max - s_local) / s_max, 0.0, 1.0))


# ============================================================
# FIRMA CRIPTOGRÁFICA
# ============================================================

def firma_sha256(timestamp: str, frecuencia: float, intensidad: float, psi: float) -> str:
    """Genera firma SHA-256 del evento para auditoría de integridad."""
    data = f"{timestamp}|{frecuencia:.6f}|{intensidad:.6f}|{psi:.8f}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# ============================================================
# GENERADOR DE SERIE TEMPORAL QRNG
# ============================================================

class ProtocoloMedicion:
    """
    Implementa el protocolo de medición QCAL descrito en el Puente Metrológico.

    Simula un generador de eventos cuánticos aleatorios (QRNG) basado en tiempos
    de llegada de fotones individuales (distribución de Poisson), acoplado a los
    nodos de procesamiento ATLAS3 / BAL-003.
    """

    def __init__(
        self,
        frecuencia_hz: float = F0_HZ,
        a_eff: float = float(N_NODOS),
        seed: int = 42,
        nodo_id: str = "BAL-003",
        sample_rate_hz: float = SAMPLE_RATE_DEFAULT_HZ,
    ):
        self.frecuencia_hz = frecuencia_hz
        self.a_eff = a_eff
        self.rng = np.random.default_rng(seed)
        self.nodo_id = nodo_id
        self.sample_rate_hz = sample_rate_hz

    # ----------------------------------------------------------
    # Paso 1 – Línea de base: S_max (entropía máxima sin señal)
    # ----------------------------------------------------------

    def calcular_s_max(self, n_muestras: int = 120) -> float:
        """
        Calcula S_max: entropía de referencia máxima en ausencia de
        sintonización armónica (estado de ruido puro).

        Modela tiempos de llegada de fotones como proceso de Poisson.
        """
        intensidades_ruido = self.rng.poisson(lam=INTENSIDAD_BASE, size=n_muestras).astype(float)
        entropias = [entropia_local(i, self.a_eff) for i in intensidades_ruido if i > 0]
        return float(np.mean(entropias))

    # ----------------------------------------------------------
    # Paso 2 – Inyección de la frecuencia portadora
    # ----------------------------------------------------------

    def _intensidad_con_portadora(self, t_segundos: float) -> float:
        """
        Modula la intensidad de flujo con la frecuencia portadora f₀.

        La modulación sinusoidal replica la inyección de pulsos
        electromagnéticos/lógicos modulados a f₀.

        Nota: para que la FFT detecte la portadora en la serie de intensidad,
        la frecuencia de muestreo debe superar 2 × f₀ (criterio de Nyquist).
        """
        if self.frecuencia_hz == 0.0:
            # Modo control: sólo ruido térmico y estocástico
            ruido_termico = self.rng.poisson(lam=INTENSIDAD_BASE)
            return float(ruido_termico)

        portadora = np.sin(2.0 * np.pi * self.frecuencia_hz * t_segundos)
        amplitud = INTENSIDAD_BASE * 0.002  # modulación <0.5%
        ruido_termico = float(self.rng.normal(0.0, INTENSIDAD_BASE * 0.001))
        return INTENSIDAD_BASE + amplitud * portadora + ruido_termico

    # ----------------------------------------------------------
    # Generación del dataset
    # ----------------------------------------------------------

    def generar_dataset(
        self,
        duracion_s: int = 300,
        t0_utc: datetime | None = None,
    ) -> pd.DataFrame:
        """
        Genera la serie temporal completa del protocolo de medición.

        Parámetros
        ----------
        duracion_s : int
            Duración total de la medición en segundos.
        t0_utc : datetime, opcional
            Instante de inicio de la medición (UTC). Si None, usa ahora.

        Retorna
        -------
        pd.DataFrame
            Dataset con columnas del estándar de auditoría QCAL.

        Notas
        -----
        El número total de muestras es `duracion_s × sample_rate_hz`.
        Para detectar la portadora f₀ en la FFT de intensidad_picode_s,
        use sample_rate_hz ≥ 2 × f₀ (e.g., 1000 Hz para f₀=141.7001 Hz).
        """
        if t0_utc is None:
            t0_utc = datetime.now(timezone.utc).replace(microsecond=0)

        dt = 1.0 / self.sample_rate_hz  # intervalo de muestreo en segundos
        n_samples = int(duracion_s * self.sample_rate_hz)

        log.info("Calculando S_max (línea de base de entropía)...")
        # Use at least 5% of total samples for baseline, minimum 120
        n_baseline = max(120, n_samples // 20)
        s_max = self.calcular_s_max(n_muestras=n_baseline)
        log.info(f"  S_max = {s_max:.6f} nats  |  sample_rate = {self.sample_rate_hz} Hz  |  baseline_n = {n_baseline}")

        filas = []
        for i in range(n_samples):
            t_s = i * dt
            ts = t0_utc + timedelta(seconds=t_s)
            # Use microsecond resolution to ensure unique timestamps at any sample rate
            timestamp_str = ts.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ts.microsecond:06d}Z"

            intensidad = self._intensidad_con_portadora(t_s)

            s_local = entropia_local(max(intensidad, 1e-9), self.a_eff)
            psi = psi_emp(s_local, s_max)
            ruido = float(abs(self.rng.normal(0.0, RUIDO_STD)))
            psi_con_ruido = float(np.clip(psi + self.rng.normal(0.0, RUIDO_STD), 0.0, 1.0))

            firma = firma_sha256(timestamp_str, self.frecuencia_hz, intensidad, psi_con_ruido)

            filas.append({
                "timestamp_utc": timestamp_str,
                "frecuencia_estimulo_hz": round(self.frecuencia_hz, 6),
                "intensidad_picode_s": round(intensidad, 6),
                "a_eff_m2_nodos": round(self.a_eff, 4),
                "psi_emp_calc": round(psi_con_ruido, 8),
                "ruido_residual_dpsi": round(ruido, 8),
                "nodo_id": self.nodo_id,
                "firma_sha256": firma,
            })

        df = pd.DataFrame(filas)
        log.info(f"Dataset generado: {len(df)} filas, f={self.frecuencia_hz} Hz")
        return df


# ============================================================
# FUNCIÓN DE EXPORTACIÓN
# ============================================================

def exportar_csv(df: pd.DataFrame, ruta: Path) -> None:
    """Exporta el DataFrame al archivo CSV especificado (UTF-8)."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)
    log.info(f"✅ Dataset exportado: {ruta}  ({len(df)} filas)")


# ============================================================
# CLI
# ============================================================

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Protocolo de Metrología QCAL – genera series temporales auditables\n"
            "de la coherencia Ψ_emp para la frecuencia portadora indicada."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--frequency",
        type=float,
        default=F0_HZ,
        help=f"Frecuencia de estimulación en Hz (default: {F0_HZ}). "
             "Use 0 para generar la línea de base de control.",
    )
    parser.add_argument(
        "--duration_s",
        type=int,
        default=300,
        help="Duración de la medición en segundos (default: 300).",
    )
    parser.add_argument(
        "--a_eff",
        type=float,
        default=float(N_NODOS),
        help=f"Área efectiva en nodos/m² (default: {N_NODOS}).",
    )
    parser.add_argument(
        "--nodo_id",
        type=str,
        default="BAL-003",
        help="Identificador del nodo de medición (default: BAL-003).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semilla aleatoria para reproducibilidad (default: 42).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help=(
            "Nombre base del archivo de salida sin extensión. "
            "Si se omite, se genera automáticamente. "
            "Ejemplo: 'baseline_control' → data/raw_metrology/baseline_control.csv"
        ),
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directorio de salida (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--sample_rate",
        type=float,
        default=SAMPLE_RATE_DEFAULT_HZ,
        help=(
            f"Frecuencia de muestreo en Hz (default: {SAMPLE_RATE_DEFAULT_HZ}). "
            "Use ≥284 Hz para detectar la portadora f₀=141.7001 Hz en la FFT "
            f"(e.g., --sample_rate {SAMPLE_RATE_HIGH_HZ} para serie de alta resolución)."
        ),
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=6,
        help="Número de decimales en psi_emp_calc (default: 6; aumentar para alta precisión).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    out_dir = Path(args.output_dir)

    if args.output:
        nombre_archivo = f"{args.output}.csv"
    elif args.frequency == 0.0:
        nombre_archivo = "qcal_baseline_control.csv"
    else:
        freq_tag = f"{args.frequency:.4f}".replace(".", "_")
        nombre_archivo = f"qcal_raw_measurements_{freq_tag}hz.csv"

    ruta_salida = out_dir / nombre_archivo

    log.info("=" * 60)
    log.info("PROTOCOLO DE METROLOGÍA QCAL")
    log.info(f"  Frecuencia de estimulación : {args.frequency} Hz")
    log.info(f"  Duración                   : {args.duration_s} s")
    log.info(f"  Área efectiva              : {args.a_eff} nodos/m²")
    log.info(f"  Nodo                       : {args.nodo_id}")
    log.info(f"  Sample rate                : {args.sample_rate} Hz")
    log.info(f"  Semilla                    : {args.seed}")
    log.info(f"  Salida                     : {ruta_salida}")
    log.info("=" * 60)

    protocolo = ProtocoloMedicion(
        frecuencia_hz=args.frequency,
        a_eff=args.a_eff,
        seed=args.seed,
        nodo_id=args.nodo_id,
        sample_rate_hz=args.sample_rate,
    )

    df = protocolo.generar_dataset(duracion_s=args.duration_s)

    # --precision controls the number of decimal places in the exported CSV.
    # The generator always computes at full float64 precision internally; this
    # only affects the output representation (min=1, max=8 to stay within
    # the 8-decimal precision used during generation).
    output_precision = max(1, min(args.precision, 8))
    df["psi_emp_calc"] = df["psi_emp_calc"].round(output_precision)

    exportar_csv(df, ruta_salida)

    # Resumen estadístico
    print("\n── Resumen estadístico ──────────────────────────────────────")
    print(df[["intensidad_picode_s", "psi_emp_calc", "ruido_residual_dpsi"]].describe().to_string())
    print(f"\nPrimeras 3 filas:\n{df.head(3).to_string(index=False)}")
    print("─────────────────────────────────────────────────────────────\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
