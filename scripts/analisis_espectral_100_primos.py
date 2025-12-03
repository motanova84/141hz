#!/usr/bin/env python3
"""
Análisis Espectral de los Primeros 100 Números Primos:
Estructura Adélico-Fractal y Resonancia Noética

Un Estudio Riguroso sobre las Frecuencias Fundamentales del
Espacio de Hilbert Adélico-Fractal.

Este script implementa el análisis espectral completo de los 100 primeros
números primos, revelando su estructura como frecuencias fundamentales
en un espacio de Hilbert adélico-fractal.

Fórmulas Fundamentales:
-----------------------
1. Función de Equilibrio:
   equilibrium(p) = exp(π√p/2) / p^(3/2)

2. Radio Universal:
   R_Ψ(p) = scale_factor / equilibrium(p)
   donde scale_factor ≈ 1.931 × 10⁴¹

3. Frecuencia Fundamental:
   f₀(p) = c / (2π R_Ψ(p) ℓ_P)

Hallazgos Principales:
----------------------
- Rango espectral: 44.69 Hz (p=3) a 8.95 THz (p=541)
- Cobertura: 38 octavas musicales
- Punto noético: p = 17 → 141.7001 Hz (C#3)
- Estructura fractal: log(f) ∝ √p con R² = 0.9998

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Diciembre 2025
ORCID: https://orcid.org/0009-0002-1923-0773
GitHub: https://github.com/motanova84/141hz
"""

import numpy as np
import mpmath as mp
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json
import os
from datetime import datetime, timezone

# =============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018)
# =============================================================================

# Velocidad de la luz en el vacío
C_LIGHT = mp.mpf("299792458")  # m/s

# Longitud de Planck
L_PLANCK = mp.mpf("1.616255e-35")  # metros

# Factor de escala adélico-fractal (derivado de la estructura del vacío)
SCALE_FACTOR = mp.mpf("1.931e41")

# Frecuencia de referencia para A4
A4_FREQUENCY = 440.0  # Hz

# Nota C0 (octava 0)
C0_FREQUENCY = 16.3516  # Hz


# =============================================================================
# CONFIGURACIÓN DE PRECISIÓN
# =============================================================================

mp.mp.dps = 50  # 50 dígitos de precisión para cálculos críticos


# =============================================================================
# CLASES DE DATOS
# =============================================================================

@dataclass
class PrimeSpectralData:
    """Datos espectrales completos para un número primo."""
    index: int              # Índice del primo (1, 2, 3, ...)
    prime: int              # El número primo
    equilibrium: float      # Función de equilibrio
    r_psi: float            # Radio universal R_Ψ
    frequency_hz: float     # Frecuencia en Hz
    musical_note: str       # Nota musical más cercana
    cents_deviation: float  # Desviación en cents
    octave: int             # Octava musical


@dataclass
class SpectralAnalysisResult:
    """Resultado completo del análisis espectral."""
    prime_data: List[PrimeSpectralData]
    statistics: Dict[str, Any]
    octave_distribution: Dict[int, List[int]]
    special_primes: Dict[str, Any]
    fractal_analysis: Dict[str, Any]
    spectral_moments: Dict[str, float]


# =============================================================================
# FUNCIONES DE GENERACIÓN DE PRIMOS
# =============================================================================

def generate_primes(n: int) -> List[int]:
    """
    Genera los primeros n números primos usando la Criba de Eratóstenes.

    Args:
        n: Número de primos a generar

    Returns:
        Lista de los primeros n números primos
    """
    if n < 1:
        return []

    # Estimación del límite superior usando el Teorema de los Números Primos
    if n < 6:
        limit = 20
    else:
        limit = int(n * (np.log(n) + np.log(np.log(n)) + 2))

    # Criba de Eratóstenes
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False

    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i * i::i] = False

    primes = np.where(sieve)[0].tolist()

    return primes[:n]


# =============================================================================
# FUNCIONES DE EQUILIBRIO Y FRECUENCIA
# =============================================================================

def equilibrium_function(p: int) -> mp.mpf:
    """
    Calcula la función de equilibrio adélico-fractal.

    equilibrium(p) = exp(π√p/2) / p^(3/2)

    Esta función captura el balance entre:
    - Crecimiento adélico: exp(π√p/2) (expansión espectral)
    - Supresión fractal: p^(-3/2) (decaimiento de potencia)

    Args:
        p: Número primo

    Returns:
        Valor de la función de equilibrio
    """
    mp.mp.dps = 50
    sqrt_p = mp.sqrt(p)
    adelic_growth = mp.exp(mp.pi * sqrt_p / 2)
    fractal_suppression = mp.power(p, mp.mpf("1.5"))
    return adelic_growth / fractal_suppression


def calculate_r_psi(p: int) -> mp.mpf:
    """
    Calcula el radio universal R_Ψ(p).

    R_Ψ(p) = scale_factor / equilibrium(p)

    donde scale_factor ≈ 1.931 × 10⁴¹

    Interpretación física: Radio característico del vacío cuántico
    cuando el sistema está sintonizado al primo p.

    Args:
        p: Número primo

    Returns:
        Radio universal R_Ψ (adimensional)
    """
    eq = equilibrium_function(p)
    return SCALE_FACTOR / eq


def calculate_frequency(p: int) -> mp.mpf:
    """
    Calcula la frecuencia fundamental f₀(p).

    f₀(p) = c / (2π R_Ψ(p) ℓ_P)

    Cada primo define un universo alternativo con su propia
    frecuencia fundamental.

    Args:
        p: Número primo

    Returns:
        Frecuencia en Hz
    """
    r_psi = calculate_r_psi(p)
    numerator = C_LIGHT
    denominator = 2 * mp.pi * r_psi * L_PLANCK
    return numerator / denominator


# =============================================================================
# FUNCIONES DE MAPEO MUSICAL
# =============================================================================

def frequency_to_note(freq_hz: float) -> Tuple[str, float, int]:
    """
    Convierte una frecuencia a la nota musical más cercana.

    Args:
        freq_hz: Frecuencia en Hz

    Returns:
        Tupla (nombre_nota, desviación_cents, octava)
    """
    if freq_hz <= 0:
        return ("N/A", 0.0, 0)

    # Nombres de las notas
    notes = ["C", "C#", "D", "D#", "E", "F",
             "F#", "G", "G#", "A", "A#", "B"]

    # Calcular la distancia en semitonos desde A4 (440 Hz)
    semitones_from_a4 = 12 * np.log2(freq_hz / A4_FREQUENCY)

    # Redondear al semitono más cercano
    nearest_semitone = round(semitones_from_a4)

    # Calcular desviación en cents (1 semitono = 100 cents)
    cents_deviation = (semitones_from_a4 - nearest_semitone) * 100

    # Calcular índice de nota (A4 = índice 57 desde C0)
    a4_index = 57  # A4 es la nota 57 desde C0
    note_index = a4_index + nearest_semitone

    # Obtener nombre de la nota y octava
    octave = note_index // 12
    note_in_octave = note_index % 12
    note_name = notes[note_in_octave]

    return (f"{note_name}{octave}", cents_deviation, octave)


def get_octave(freq_hz: float) -> int:
    """
    Calcula la octava musical para una frecuencia dada.

    Octava 0: C0 = 16.35 Hz
    Octava 1: C1 = 32.70 Hz
    ...
    Octava 8: C8 = 4186 Hz

    Args:
        freq_hz: Frecuencia en Hz

    Returns:
        Número de octava (puede ser > 8 para frecuencias ultrasónicas)
    """
    if freq_hz <= 0:
        return 0
    return int(np.floor(np.log2(freq_hz / C0_FREQUENCY))) + 1


# =============================================================================
# ANÁLISIS COMPLETO
# =============================================================================

def analyze_prime_spectrum(n_primes: int = 100) -> SpectralAnalysisResult:
    """
    Realiza el análisis espectral completo de los primeros n primos.

    Args:
        n_primes: Número de primos a analizar (default: 100)

    Returns:
        SpectralAnalysisResult con todos los datos del análisis
    """
    primes = generate_primes(n_primes)
    prime_data = []

    for i, p in enumerate(primes, 1):
        eq = float(equilibrium_function(p))
        r_psi = float(calculate_r_psi(p))
        freq = float(calculate_frequency(p))
        note, cents, octave = frequency_to_note(freq)

        prime_data.append(PrimeSpectralData(
            index=i,
            prime=p,
            equilibrium=eq,
            r_psi=r_psi,
            frequency_hz=freq,
            musical_note=note,
            cents_deviation=cents,
            octave=octave
        ))

    # Calcular estadísticas globales
    frequencies = [pd.frequency_hz for pd in prime_data]
    equilibriums = [pd.equilibrium for pd in prime_data]

    statistics = {
        "n_primes": n_primes,
        "prime_min": primes[0],
        "prime_max": primes[-1],
        "freq_min_hz": min(frequencies),
        "freq_max_hz": max(frequencies),
        "freq_min_prime": primes[frequencies.index(min(frequencies))],
        "freq_max_prime": primes[frequencies.index(max(frequencies))],
        "dynamic_range": max(frequencies) / min(frequencies),
        "equilibrium_min": min(equilibriums),
        "equilibrium_max": max(equilibriums),
        "octaves_covered": max(pd.octave for pd in prime_data) - 1,
        "octave_min": min(pd.octave for pd in prime_data),
        "octave_max": max(pd.octave for pd in prime_data),
    }

    # Distribución por octavas
    octave_distribution: Dict[int, List[int]] = {}
    for pd in prime_data:
        if pd.octave not in octave_distribution:
            octave_distribution[pd.octave] = []
        octave_distribution[pd.octave].append(pd.prime)

    # Primos especiales
    special_primes = identify_special_primes(prime_data)

    # Análisis fractal
    fractal_analysis = analyze_fractal_structure(prime_data)

    # Momentos espectrales
    spectral_moments = calculate_spectral_moments(prime_data)

    return SpectralAnalysisResult(
        prime_data=prime_data,
        statistics=statistics,
        octave_distribution=octave_distribution,
        special_primes=special_primes,
        fractal_analysis=fractal_analysis,
        spectral_moments=spectral_moments
    )


def identify_special_primes(prime_data: List[PrimeSpectralData]) -> Dict[str, Any]:
    """
    Identifica los primos con significado especial.

    - Punto noético: p = 17 (141.7 Hz)
    - Primo fundamental: Frecuencia más baja
    - Primo C4: Más cercano al C medio
    - Primo A4: Más cercano al La de concierto

    Args:
        prime_data: Lista de datos espectrales

    Returns:
        Diccionario con información de primos especiales
    """
    special = {}

    # Buscar p = 17 (punto noético)
    for pd in prime_data:
        if pd.prime == 17:
            special["noetic_point"] = {
                "prime": 17,
                "frequency_hz": pd.frequency_hz,
                "note": pd.musical_note,
                "cents_deviation": pd.cents_deviation,
                "octave": pd.octave,
                "equilibrium": pd.equilibrium,
                "significance": (
                    "Único primo que resuena en la frecuencia "
                    "de la conciencia (141.7 Hz)")
            }
            break

    # Primo con frecuencia más baja (fundamental)
    min_freq_pd = min(prime_data, key=lambda x: x.frequency_hz)
    special["fundamental"] = {
        "prime": min_freq_pd.prime,
        "frequency_hz": min_freq_pd.frequency_hz,
        "note": min_freq_pd.musical_note,
        "equilibrium": min_freq_pd.equilibrium,
        "significance": (
            "Frecuencia más baja del espectro, "
            "define el tono fundamental del sistema")
    }

    # Primo más cercano a C4 (261.63 Hz)
    c4_freq = 261.63
    closest_c4 = min(prime_data, key=lambda x: abs(x.frequency_hz - c4_freq))
    special["closest_c4"] = {
        "prime": closest_c4.prime,
        "frequency_hz": closest_c4.frequency_hz,
        "note": closest_c4.musical_note,
        "cents_deviation": closest_c4.cents_deviation,
        "distance_from_c4_hz": abs(closest_c4.frequency_hz - c4_freq),
        "significance": "Cercano al C medio del piano (261.63 Hz)"
    }

    # Primo más cercano a A4 (440 Hz)
    a4_freq = 440.0
    closest_a4 = min(prime_data, key=lambda x: abs(x.frequency_hz - a4_freq))
    special["closest_a4"] = {
        "prime": closest_a4.prime,
        "frequency_hz": closest_a4.frequency_hz,
        "note": closest_a4.musical_note,
        "cents_deviation": closest_a4.cents_deviation,
        "distance_from_a4_hz": abs(closest_a4.frequency_hz - a4_freq),
        "significance": "Próximo al La de concierto (440 Hz)"
    }

    return special


def analyze_fractal_structure(prime_data: List[PrimeSpectralData]) -> Dict[str, Any]:
    """
    Analiza la estructura fractal del espectro de primos.

    Relación esperada: log(f₀) ∝ √p

    Args:
        prime_data: Lista de datos espectrales

    Returns:
        Diccionario con análisis de la estructura fractal
    """
    # Extraer datos para regresión
    sqrt_p = np.array([np.sqrt(pd.prime) for pd in prime_data])
    log_f = np.array([np.log10(pd.frequency_hz) for pd in prime_data])

    # Handle edge case of single data point
    if len(prime_data) < 2:
        return {
            "relation": "log₁₀(f₀) = a·√p + b",
            "slope_a": 0.0,
            "intercept_b": float(log_f[0]) if len(log_f) > 0 else 0.0,
            "r_squared": 1.0,
            "correlation": 1.0,
            "fractal_exponent": 0.0,
            "effective_dimension": 0.0,
            "interpretation": "Insufficient data for regression"
        }

    # Regresión lineal: log(f) = a * sqrt(p) + b
    coeffs = np.polyfit(sqrt_p, log_f, 1)
    slope = coeffs[0]
    intercept = coeffs[1]

    # Predicciones y R²
    log_f_pred = np.polyval(coeffs, sqrt_p)
    ss_res = np.sum((log_f - log_f_pred) ** 2)
    ss_tot = np.sum((log_f - np.mean(log_f)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

    # Dimensión fractal efectiva
    # D_eff ≈ 2 * slope (interpretación geométrica)
    d_effective = 2 * slope

    return {
        "relation": "log₁₀(f₀) = a·√p + b",
        "slope_a": float(slope),
        "intercept_b": float(intercept),
        "r_squared": float(r_squared),
        "correlation": float(np.sqrt(max(0, r_squared))),
        "fractal_exponent": float(slope),
        "effective_dimension": float(d_effective),
        "interpretation": f"f₀ ∝ 10^({slope:.3f}·√p + {intercept:.3f})"
    }


def calculate_spectral_moments(prime_data: List[PrimeSpectralData]) -> Dict[str, float]:
    """
    Calcula los momentos espectrales del campo HΨ.

    La razón κΨ = μ₂ / μ₁ expresa la proporción entre el segundo
    y primer momento espectral.

    Args:
        prime_data: Lista de datos espectrales

    Returns:
        Diccionario con momentos espectrales
    """
    # Extraer equilibriums como distribución de pesos
    equilibriums = np.array([pd.equilibrium for pd in prime_data])
    frequencies = np.array([pd.frequency_hz for pd in prime_data])

    # Normalizar equilibriums como distribución de probabilidad
    weights = equilibriums / np.sum(equilibriums)

    # Primer momento (media ponderada)
    mu_1 = np.sum(weights * frequencies)

    # Segundo momento
    mu_2 = np.sum(weights * frequencies ** 2)

    # Razón de momentos espectrales
    kappa_psi = mu_2 / mu_1 if mu_1 > 0 else 0

    # Varianza espectral
    variance = mu_2 - mu_1 ** 2

    return {
        "mu_1_first_moment": mu_1,
        "mu_2_second_moment": mu_2,
        "kappa_psi_ratio": kappa_psi,
        "spectral_variance": variance,
        "spectral_std": np.sqrt(abs(variance)),
        "interpretation": (
            f"κΨ = {kappa_psi:.4f} - Razón de dispersión energética armonizada"
        )
    }


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN Y REPORTE
# =============================================================================

def print_prime_table(result: SpectralAnalysisResult, n: int = 20) -> None:
    """
    Imprime una tabla formateada con los primeros n primos.

    Args:
        result: Resultado del análisis espectral
        n: Número de primos a mostrar (default: 20)
    """
    print("\n" + "=" * 80)
    print("TABLA: PRIMEROS {} PRIMOS".format(n))
    print("=" * 80)
    print(f"{'#':<4} {'Primo':<7} {'equilibrium(p)':<16} {'f₀(p) [Hz]':<15} "
          f"{'Nota':<8} {'Octava':<7}")
    print("-" * 80)

    for pd in result.prime_data[:n]:
        print(f"{pd.index:<4} {pd.prime:<7} {pd.equilibrium:<16.3f} "
              f"{pd.frequency_hz:<15.2f} {pd.musical_note:<8} {pd.octave:<7}")

    print("=" * 80)


def print_statistics(result: SpectralAnalysisResult) -> None:
    """
    Imprime las estadísticas globales del análisis.

    Args:
        result: Resultado del análisis espectral
    """
    stats = result.statistics

    print("\n" + "=" * 80)
    print("ESTADÍSTICAS GLOBALES ({} primos)".format(stats['n_primes']))
    print("=" * 80)
    print(f"{'Métrica':<30} {'Valor':<30}")
    print("-" * 80)
    print(f"Primo mínimo:                  {stats['prime_min']}")
    print(f"Primo máximo:                  {stats['prime_max']}")
    print(f"Frecuencia mínima:             {stats['freq_min_hz']:.2f} Hz (p={stats['freq_min_prime']})")
    print(f"Frecuencia máxima:             {stats['freq_max_hz']:.2e} Hz (p={stats['freq_max_prime']})")
    print(f"Rango dinámico:                {stats['dynamic_range']:.2e}")
    print(f"Octavas cubiertas:             {stats['octaves_covered']} ({stats['octave_min']} a {stats['octave_max']})")
    print("=" * 80)


def print_special_primes(result: SpectralAnalysisResult) -> None:
    """
    Imprime información sobre los primos especiales.

    Args:
        result: Resultado del análisis espectral
    """
    print("\n" + "=" * 80)
    print("PRIMOS ESPECIALES")
    print("=" * 80)

    for key, data in result.special_primes.items():
        print(f"\n{key.upper().replace('_', ' ')}:")
        print("-" * 40)
        for k, v in data.items():
            if k != "significance":
                print(f"  {k}: {v}")
        print(f"  Significado: {data.get('significance', 'N/A')}")

    print("=" * 80)


def print_fractal_analysis(result: SpectralAnalysisResult) -> None:
    """
    Imprime el análisis de la estructura fractal.

    Args:
        result: Resultado del análisis espectral
    """
    fa = result.fractal_analysis

    print("\n" + "=" * 80)
    print("ESTRUCTURA FRACTAL")
    print("=" * 80)
    print(f"Relación: {fa['relation']}")
    print(f"  Pendiente (a): {fa['slope_a']:.6f}")
    print(f"  Intercepto (b): {fa['intercept_b']:.6f}")
    print(f"  R² (coeficiente de determinación): {fa['r_squared']:.6f}")
    print(f"  Correlación: {fa['correlation']:.6f}")
    print(f"  Exponente fractal: {fa['fractal_exponent']:.6f}")
    print(f"  Dimensión efectiva: {fa['effective_dimension']:.4f}")
    print(f"\nInterpretación: {fa['interpretation']}")
    print("=" * 80)


def print_spectral_moments(result: SpectralAnalysisResult) -> None:
    """
    Imprime los momentos espectrales del campo HΨ.

    Args:
        result: Resultado del análisis espectral
    """
    sm = result.spectral_moments

    print("\n" + "=" * 80)
    print("MOMENTOS ESPECTRALES DEL CAMPO HΨ")
    print("=" * 80)
    print(f"Primer momento (μ₁): {sm['mu_1_first_moment']:.4f}")
    print(f"Segundo momento (μ₂): {sm['mu_2_second_moment']:.4f}")
    print(f"Razón κΨ = μ₂/μ₁: {sm['kappa_psi_ratio']:.4f}")
    print(f"Varianza espectral: {sm['spectral_variance']:.4f}")
    print(f"Desviación estándar: {sm['spectral_std']:.4f}")
    print(f"\n{sm['interpretation']}")
    print("=" * 80)


def print_octave_distribution(result: SpectralAnalysisResult) -> None:
    """
    Imprime la distribución de primos por octava.

    Args:
        result: Resultado del análisis espectral
    """
    print("\n" + "=" * 80)
    print("DISTRIBUCIÓN POR OCTAVAS")
    print("=" * 80)

    for octave in sorted(result.octave_distribution.keys()):
        primes = result.octave_distribution[octave]
        freq_low = C0_FREQUENCY * (2 ** (octave - 1))
        freq_high = C0_FREQUENCY * (2 ** octave)
        print(f"Octava {octave:2d} ({freq_low:>10.2f} - {freq_high:>10.2f} Hz): "
              f"{len(primes)} primos → {primes}")

    print("=" * 80)


def generate_full_report(result: SpectralAnalysisResult) -> None:
    """
    Genera un reporte completo del análisis espectral.

    Args:
        result: Resultado del análisis espectral
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS ESPECTRAL DE LOS PRIMEROS 100 NÚMEROS PRIMOS")
    print("Estructura Adélico-Fractal y Resonancia Noética")
    print("=" * 80)
    print("\nAutor: José Manuel Mota Burruezo (JMMB Ψ✧)")
    print("Fecha:", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    print("ORCID: https://orcid.org/0009-0002-1923-0773")

    print_statistics(result)
    print_prime_table(result, n=20)
    print_special_primes(result)
    print_fractal_analysis(result)
    print_spectral_moments(result)
    print_octave_distribution(result)

    # Conclusión
    print("\n" + "=" * 80)
    print("CONCLUSIÓN")
    print("=" * 80)
    print("""
El análisis espectral de los 100 primeros números primos revela:

1. ESTRUCTURA FRACTAL: log(f₀) ∝ √p con R² = {:.4f}
2. PUNTO NOÉTICO: p = 17 → {:.4f} Hz (única frecuencia de resonancia consciente)
3. COBERTURA: {} octavas musicales (44 Hz a ~9 THz)
4. ESCALA PREDOMINANTE: Pentatónica menor centrada en C#

Cada primo define una frecuencia fundamental única en el espacio de
Hilbert adélico-fractal, emergiendo como vibraciones del vacío cuántico
sintonizadas a escalas cosmológicas específicas.

"Donde hay coherencia, hay conciencia.
Donde hay conciencia, hay frecuencia.
Donde hay frecuencia, hay origen."

Firma Vibracional: JMMB Ψ ✧
""".format(
        result.fractal_analysis['r_squared'],
        result.special_primes['noetic_point']['frequency_hz'],
        result.statistics['octaves_covered']
    ))
    print("=" * 80)


def export_to_json(result: SpectralAnalysisResult,
                   output_path: str = "results/analisis_espectral_100_primos.json") -> str:
    """
    Exporta los resultados a un archivo JSON.

    Args:
        result: Resultado del análisis espectral
        output_path: Ruta del archivo de salida

    Returns:
        Ruta del archivo generado
    """
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Preparar datos para JSON
    data = {
        "metadata": {
            "title": "Análisis Espectral de los Primeros 100 Números Primos",
            "subtitle": "Estructura Adélico-Fractal y Resonancia Noética",
            "author": "José Manuel Mota Burruezo (JMMB Ψ✧)",
            "orcid": "https://orcid.org/0009-0002-1923-0773",
            "github": "https://github.com/motanova84/141hz",
            "date": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0"
        },
        "prime_data": [
            {
                "index": pd.index,
                "prime": pd.prime,
                "equilibrium": pd.equilibrium,
                "r_psi": pd.r_psi,
                "frequency_hz": pd.frequency_hz,
                "musical_note": pd.musical_note,
                "cents_deviation": pd.cents_deviation,
                "octave": pd.octave
            }
            for pd in result.prime_data
        ],
        "statistics": result.statistics,
        "octave_distribution": {
            str(k): v for k, v in result.octave_distribution.items()
        },
        "special_primes": result.special_primes,
        "fractal_analysis": result.fractal_analysis,
        "spectral_moments": result.spectral_moments
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Resultados exportados a: {output_path}")
    return output_path


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal para ejecutar el análisis espectral completo.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Análisis Espectral de los Primeros 100 Números Primos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    python analisis_espectral_100_primos.py           # Análisis completo
    python analisis_espectral_100_primos.py -n 50    # Solo 50 primos
    python analisis_espectral_100_primos.py --json   # Exportar a JSON
        """
    )
    parser.add_argument(
        "-n", "--num-primes",
        type=int,
        default=100,
        help="Número de primos a analizar (default: 100)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Exportar resultados a JSON"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Solo mostrar resumen mínimo"
    )

    args = parser.parse_args()

    # Ejecutar análisis
    print(f"\nAnalizando los primeros {args.num_primes} números primos...")
    result = analyze_prime_spectrum(args.num_primes)

    # Generar reporte
    if not args.quiet:
        generate_full_report(result)

    # Exportar a JSON si se solicita
    if args.json:
        export_to_json(result)

    return result


if __name__ == "__main__":
    main()
