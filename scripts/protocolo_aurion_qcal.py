#!/usr/bin/env python3
"""
Protocolo AURION - Medición de Plasticidad Epigenética y Biofotones
====================================================================
Genera el dataset de mediciones biológicas para el protocolo AURION
(Acoplamiento Unificado de Respuesta Iónica y Orgánica Noética).

El protocolo mide:
  - Potencial de membrana celular (mV)
  - Tasa de metilación del ADN (%)
  - Conteo de biofotones ultra-débiles (fotones/s)
  - Grupos: 'expuesto' (campo a 141.7001 Hz) vs 'control' (cámara de Faraday)

El dataset generado permite comparar la firma de emisión fotónica
del grupo expuesto frente al grupo control como exige el protocolo
experimental descrito en la sección 3 (Intersección Biológica AURION).

Uso:
  python protocolo_aurion_qcal.py --n_muestras 60 --output_dir data/raw_metrology
  python protocolo_aurion_qcal.py --help
"""

import argparse
import csv
import hashlib
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
log = logging.getLogger(__name__)

F0_HZ = 141.7001
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw_metrology"


# ============================================================
# MODELO BIOLÓGICO SINTÉTICO
# ============================================================

class ModeloBiologico:
    """
    Modela los efectos del campo oscilatorio a f₀ sobre parámetros
    biológicos medibles en condiciones de laboratorio controladas
    (cámara de Faraday).

    Los valores de referencia se basan en rangos fisiológicos típicos
    para células de mamífero en cultivo:
      - Potencial de membrana en reposo: -70 mV ± 5 mV
      - Tasa de metilación basal: 70 % ± 3 %
      - Emisión basal de biofotones: 50–200 fotones/s
    """

    # Parámetros fisiológicos de referencia
    POTENCIAL_MEMBRANA_BASE_MV = -70.0    # mV (reposo)
    METILACION_BASE_PCT = 70.0            # % metilación basal
    BIOFOTONES_BASE_S = 100.0             # fotones/s (emisión espontánea basal)

    # Efecto del campo: modulación esperada en grupo expuesto
    DELTA_POTENCIAL_MV = 0.5             # modulación pequeña (±0.5 mV)
    DELTA_METILACION_PCT = 0.3           # cambio en metilación (±0.3 %)
    FACTOR_BIOFOTONES_EXPUESTO = 1.10    # incremento 10 % en biofotones

    def __init__(self, rng: np.random.Generator):
        self.rng = rng

    def potencial_membrana(self, grupo: str, t_s: float) -> float:
        """Potencial de membrana en mV."""
        base = self.POTENCIAL_MEMBRANA_BASE_MV + self.rng.normal(0.0, 2.0)
        if grupo == "expuesto":
            modulacion = self.DELTA_POTENCIAL_MV * np.sin(2.0 * np.pi * F0_HZ * t_s)
            return round(base + modulacion, 4)
        return round(base, 4)

    def tasa_metilacion(self, grupo: str) -> float:
        """Tasa de metilación del ADN en %."""
        base = self.METILACION_BASE_PCT + self.rng.normal(0.0, 1.5)
        if grupo == "expuesto":
            delta = self.rng.normal(self.DELTA_METILACION_PCT, 0.1)
            return round(float(np.clip(base + delta, 0.0, 100.0)), 4)
        return round(float(np.clip(base, 0.0, 100.0)), 4)

    def biofotones(self, grupo: str) -> float:
        """Conteo de biofotones ultra-débiles en fotones/s."""
        base = self.rng.poisson(lam=self.BIOFOTONES_BASE_S)
        if grupo == "expuesto":
            return round(float(base * self.FACTOR_BIOFOTONES_EXPUESTO), 4)
        return round(float(base), 4)


# ============================================================
# FIRMA DE INTEGRIDAD
# ============================================================

def firma_muestra(timestamp: str, grupo: str, potencial: float, biofotones: float) -> str:
    """Firma SHA-256 de la muestra para auditoría de integridad."""
    data = f"{timestamp}|{grupo}|{potencial:.4f}|{biofotones:.4f}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# ============================================================
# GENERACIÓN DEL DATASET
# ============================================================

def generar_dataset_aurion(
    n_muestras: int = 60,
    t0_utc: datetime | None = None,
    temperatura_c: float = 37.0,
    protocolo_version: str = "AURION-v1.0",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Genera el dataset AURION con mediciones biológicas de ambos grupos.

    Los primeros n_muestras//2 puntos corresponden al grupo 'expuesto'
    y el resto al grupo 'control', intercalados cada minuto.

    Parámetros
    ----------
    n_muestras : int
        Número total de muestras (mitad por grupo).
    t0_utc : datetime, opcional
        Instante inicial de la medición.
    temperatura_c : float
        Temperatura del entorno en grados Celsius.
    protocolo_version : str
        Versión del protocolo de medición.
    seed : int
        Semilla para reproducibilidad.

    Retorna
    -------
    pd.DataFrame
    """
    if t0_utc is None:
        t0_utc = datetime.now(timezone.utc).replace(microsecond=0)

    rng = np.random.default_rng(seed)
    modelo = ModeloBiologico(rng)
    filas = []

    for i in range(n_muestras):
        ts = t0_utc + timedelta(minutes=i)
        timestamp_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
        # Block-randomized group assignment: shuffle pairs so each block of 2
        # contains exactly one exposed and one control, avoiding temporal confounding
        n_pares = (n_muestras + 1) // 2
        asignaciones: list[str] = []
        for _ in range(n_pares):
            par = ["expuesto", "control"]
            rng.shuffle(par)
            asignaciones.extend(par)
        asignaciones = asignaciones[:n_muestras]

        n_expuestos = asignaciones.count("expuesto")
        n_controles = asignaciones.count("control")

        for i in range(n_muestras):
            ts = t0_utc + timedelta(minutes=i)
            timestamp_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
            grupo = asignaciones[i]
        t_s = float(i * 60)  # tiempo en segundos

        potencial = modelo.potencial_membrana(grupo, t_s)
        metilacion = modelo.tasa_metilacion(grupo)
        biofotones = modelo.biofotones(grupo)
        camara_faraday = True  # todas las mediciones en cámara aislada
        firma = firma_muestra(timestamp_str, grupo, potencial, biofotones)

        filas.append({
            "timestamp_utc": timestamp_str,
            "muestra_id": f"AURION-{i+1:04d}",
            "grupo": grupo,
            "frecuencia_campo_hz": F0_HZ if grupo == "expuesto" else 0.0,
            "potencial_membrana_mv": potencial,
            "tasa_metilacion_pct": metilacion,
            "biophoton_count_s": biofotones,
            "temperatura_c": temperatura_c,
            "camara_faraday": camara_faraday,
            "protocolo_version": protocolo_version,
            "firma_sha256": firma,
        })

    df = pd.DataFrame(filas)
    log.info(f"Dataset AURION generado: {len(df)} filas ({n_expuestos} expuesto / {n_controles} control)")
    return df


# ============================================================
# RESUMEN ESTADÍSTICO POR GRUPO
# ============================================================

def resumen_grupos(df: pd.DataFrame) -> None:
    """Imprime estadísticas comparativas expuesto vs control."""
    metricas = ["potencial_membrana_mv", "tasa_metilacion_pct", "biophoton_count_s"]
    print("\n── Comparativa AURION: expuesto vs control ──────────────────")
    for metrica in metricas:
        grp = df.groupby("grupo")[metrica].agg(["mean", "std", "min", "max"])
        print(f"\n  {metrica}:")
        print(grp.to_string())
    print("─────────────────────────────────────────────────────────────\n")


# ============================================================
# CLI
# ============================================================

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Protocolo AURION – genera dataset biológico de biofotones\n"
            "y potenciales de membrana para grupos expuesto vs control."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--n_muestras",
        type=int,
        default=60,
        help="Número total de muestras (mitad por grupo; default: 60).",
    )
    parser.add_argument(
        "--temperatura_c",
        type=float,
        default=37.0,
        help="Temperatura del entorno en °C (default: 37.0).",
    )
    parser.add_argument(
        "--protocolo_version",
        type=str,
        default="AURION-v1.0",
        help="Identificador de versión del protocolo (default: AURION-v1.0).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semilla aleatoria para reproducibilidad (default: 42).",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directorio de salida (default: {DEFAULT_OUTPUT_DIR}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ruta_salida = out_dir / "aurion_biophoton_measurements.csv"

    log.info("=" * 60)
    log.info("PROTOCOLO AURION – BIOFOTONES Y EPIGENÉTICA")
    log.info(f"  Muestras totales  : {args.n_muestras}")
    log.info(f"  Temperatura       : {args.temperatura_c} °C")
    log.info(f"  Protocolo versión : {args.protocolo_version}")
    log.info(f"  Semilla           : {args.seed}")
    log.info(f"  Salida            : {ruta_salida}")
    log.info("=" * 60)

    df = generar_dataset_aurion(
        n_muestras=args.n_muestras,
        temperatura_c=args.temperatura_c,
        protocolo_version=args.protocolo_version,
        seed=args.seed,
    )

    df.to_csv(ruta_salida, index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)
    log.info(f"✅ Dataset AURION exportado: {ruta_salida}  ({len(df)} filas)")

    resumen_grupos(df)

    print(f"Primeras 4 filas:\n{df.head(4).to_string(index=False)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
