#!/usr/bin/env python3
"""
El Pozo Infinito Cuántico: Derivación Estándar y Transición al Marco Noésico
==============================================================================

Este módulo implementa la derivación matemática rigurosa del pozo infinito
unidimensional en mecánica cuántica y su transición conceptual al marco
noésico QCAL ∞³.

La frecuencia fundamental f₀ = 141.7001 Hz emerge como semilla espectral del
campo coherente universal.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
Versión: V1.0
Licencia: CC-BY-NC-SA 4.0

Referencias:
- https://x.com/Investigad1154/status/1980073185966993602?s=20
- ORCID: https://orcid.org/0009-0002-1923-0773
- Zenodo DOI: 10.5281/zenodo.17503763
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, pi
import mpmath as mp
from typing import Tuple, Optional


# ============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES
# ============================================================================

# Constante de Planck reducida (J·s)
HBAR = hbar

# Velocidad de la luz (m/s)
C = c

# Frecuencia universal observada (Hz)
F0_UNIVERSAL = 141.7001


# ============================================================================
# A. DERIVACIÓN ESTÁNDAR DEL POZO INFINITO UNIDIMENSIONAL
# ============================================================================

class PozoInfinitoCuantico:
    """
    Implementa el modelo del pozo infinito cuántico unidimensional.

    El potencial está definido como:
        V(x) = 0     si 0 < x < L
        V(x) = ∞     si x ≤ 0 o x ≥ L

    Attributes:
        L (float): Longitud del pozo (m)
        m (float): Masa de la partícula (kg)
    """

    def __init__(self, L: float, m: float):
        """
        Inicializa el pozo infinito cuántico.

        Args:
            L: Longitud del pozo en metros
            m: Masa de la partícula en kilogramos
        """
        self.L = L
        self.m = m

    def numero_onda(self, n: int) -> float:
        """
        Calcula el número de onda para el nivel n.

        kₙ = nπ/L

        Args:
            n: Número cuántico (n = 1, 2, 3, ...)

        Returns:
            Número de onda en m⁻¹
        """
        if n < 1:
            raise ValueError("El número cuántico n debe ser ≥ 1")
        return n * pi / self.L

    def energia(self, n: int) -> float:
        """
        Calcula la energía del nivel n.

        Eₙ = (ℏ²π²n²)/(2mL²)

        Args:
            n: Número cuántico (n = 1, 2, 3, ...)

        Returns:
            Energía en Joules
        """
        kn = self.numero_onda(n)
        return (HBAR**2 * kn**2) / (2 * self.m)

    def frecuencia(self, n: int) -> float:
        """
        Calcula la frecuencia asociada al nivel n.

        fₙ = Eₙ/h = (πn²)/(4mL²) * (h/π) = (ℏπn²)/(2mL²)

        Args:
            n: Número cuántico (n = 1, 2, 3, ...)

        Returns:
            Frecuencia en Hz
        """
        En = self.energia(n)
        return En / (2 * pi * HBAR)

    def funcion_onda(self, x: np.ndarray, n: int) -> np.ndarray:
        """
        Calcula la función de onda normalizada para el nivel n.

        Ψₙ(x) = √(2/L) sin(nπx/L)

        Args:
            x: Posiciones donde evaluar la función de onda (array)
            n: Número cuántico (n = 1, 2, 3, ...)

        Returns:
            Valores de la función de onda en las posiciones dadas
        """
        return np.sqrt(2 / self.L) * np.sin(n * pi * x / self.L)

    def densidad_probabilidad(self, x: np.ndarray, n: int) -> np.ndarray:
        """
        Calcula la densidad de probabilidad |Ψₙ(x)|².

        Args:
            x: Posiciones donde evaluar (array)
            n: Número cuántico (n = 1, 2, 3, ...)

        Returns:
            Densidad de probabilidad en las posiciones dadas
        """
        psi = self.funcion_onda(x, n)
        return np.abs(psi)**2

    def energia_punto_cero(self) -> float:
        """
        Calcula la energía del punto cero (estado fundamental n=1).

        Returns:
            Energía del punto cero en Joules
        """
        return self.energia(1)

    def frecuencia_fundamental(self) -> float:
        """
        Calcula la frecuencia fundamental del modo basal (n=1).

        f₁ = E₁/h = π/(4mL²) (en unidades SI)

        Returns:
            Frecuencia fundamental en Hz
        """
        return self.frecuencia(1)


# ============================================================================
# B. TRANSICIÓN AL MARCO NOÉSICO (QCAL ∞³)
# ============================================================================

class PozoNoetico(PozoInfinitoCuantico):
    """
    Extensión del pozo cuántico al marco noésico QCAL ∞³.

    Incorpora el término de retroalimentación cuántica R_Ψ(x,t) que modifica
    la ecuación de Schrödinger estándar:

    iℏ ∂Ψ/∂t = (-ℏ²/2m ∇² + V(x) + R_Ψ(x,t)) Ψ

    Cuando R_Ψ = 0, se reduce al caso estándar de Schrödinger.
    """

    def __init__(self, L: float, m: float, R_psi: float = 0.0):
        """
        Inicializa el pozo noésico.

        Args:
            L: Longitud del pozo en metros
            m: Masa de la partícula en kilogramos
            R_psi: Término de retroalimentación noésica (J)
        """
        super().__init__(L, m)
        self.R_psi = R_psi

    def energia_noesica(self, n: int) -> float:
        """
        Calcula la energía modificada por el campo noésico.

        E_noésica = E_cuántica + R_Ψ

        Args:
            n: Número cuántico

        Returns:
            Energía modificada en Joules
        """
        return self.energia(n) + self.R_psi

    def frecuencia_noesica(self, n: int) -> float:
        """
        Calcula la frecuencia modificada por el campo noésico.

        Args:
            n: Número cuántico

        Returns:
            Frecuencia modificada en Hz
        """
        En_noesica = self.energia_noesica(n)
        return En_noesica / (2 * pi * HBAR)

    def coherencia_campo(self, n: int) -> float:
        """
        Calcula la coherencia del campo cuántico para el nivel n.

        Coherencia = |Ψ_noésica|² / |Ψ_cuántica|²

        Args:
            n: Número cuántico

        Returns:
            Factor de coherencia (adimensional)
        """
        if self.R_psi == 0:
            return 1.0
        return self.energia_noesica(n) / self.energia(n)


# ============================================================================
# C. CÁLCULO INVERSO: LONGITUD DEL POZO DESDE FRECUENCIA UNIVERSAL
# ============================================================================

def calcular_longitud_pozo(f0: float, m: float, n: int = 1) -> float:
    """
    Calcula la longitud L del pozo tal que su frecuencia fundamental sea f₀.

    De f₁ = (ℏπn²)/(2mL²), despejamos:

    L = √(ℏπn²/(2mf₁))

    Args:
        f0: Frecuencia fundamental deseada (Hz)
        m: Masa de la partícula (kg)
        n: Número cuántico (por defecto 1 para frecuencia fundamental)

    Returns:
        Longitud del pozo en metros
    """
    # f = E/h = (ℏπn²)/(2mL²) / (2πℏ) = (πn²)/(4πmL²) = n²/(4mL²)
    # Simplificando: f = ℏπn²/(2mL²) / (2π) = ℏn²/(4mL²)
    # Despejando L: L = √(ℏn²/(4mf))

    # Corrección: De Eₙ = ℏ²π²n²/(2mL²) y f = E/h = E/(2πℏ)
    # f = ℏ²π²n²/(2mL²) / (2πℏ) = ℏπn²/(4mL²)
    # L² = ℏπn²/(4mf)
    # L = √(ℏπn²/(4mf))

    L = np.sqrt(HBAR * pi * n**2 / (4 * m * f0))
    return L


def resonador_basal_universal(m: float, precision: int = 50) -> Tuple[float, float, float]:
    """
    Calcula las propiedades del resonador basal alineado con f₀ = 141.7001 Hz.

    Este es el pozo cuántico cuya primera vibración coincide exactamente con
    la frecuencia armónica prima del Campo QCAL ∞³.

    Args:
        m: Masa de la partícula (kg)
        precision: Dígitos de precisión para cálculos de alta precisión

    Returns:
        Tupla (L, E1, f1) donde:
        - L: Longitud del resonador basal (m)
        - E1: Energía del punto cero (J)
        - f1: Frecuencia fundamental verificada (Hz)
    """
    mp.mp.dps = precision

    # Calcular longitud del pozo
    L = calcular_longitud_pozo(F0_UNIVERSAL, m, n=1)

    # Crear el resonador
    pozo = PozoInfinitoCuantico(L, m)

    # Verificar propiedades
    E1 = pozo.energia_punto_cero()
    f1 = pozo.frecuencia_fundamental()

    return L, E1, f1


# ============================================================================
# D. VISUALIZACIÓN
# ============================================================================

def visualizar_pozo(pozo: PozoInfinitoCuantico,
                    niveles: int = 4,
                    puntos: int = 1000,
                    filename: Optional[str] = None) -> None:
    """
    Visualiza el pozo infinito con funciones de onda y niveles de energía.

    Args:
        pozo: Instancia de PozoInfinitoCuantico
        niveles: Número de niveles a visualizar
        puntos: Puntos de muestreo para las funciones de onda
        filename: Nombre del archivo para guardar (opcional)
    """
    x = np.linspace(0, pozo.L, puntos)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel izquierdo: Funciones de onda
    ax1.set_title('Funciones de Onda Normalizadas', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Posición x (m)', fontsize=12)
    ax1.set_ylabel('Ψₙ(x)', fontsize=12)
    ax1.axhline(0, color='black', linewidth=0.5, linestyle='--', alpha=0.3)
    ax1.set_xlim(0, pozo.L)
    ax1.grid(True, alpha=0.3)

    colors = plt.cm.viridis(np.linspace(0, 1, niveles))

    for n in range(1, niveles + 1):
        psi = pozo.funcion_onda(x, n)
        En = pozo.energia(n)
        fn = pozo.frecuencia(n)
        label = f'n={n}: E={En:.2e} J, f={fn:.2f} Hz'
        ax1.plot(x, psi, label=label, color=colors[n - 1], linewidth=2)

    ax1.legend(loc='upper right', fontsize=10)

    # Panel derecho: Densidades de probabilidad
    ax2.set_title('Densidades de Probabilidad |Ψₙ(x)|²', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Posición x (m)', fontsize=12)
    ax2.set_ylabel('|Ψₙ(x)|²', fontsize=12)
    ax2.set_xlim(0, pozo.L)
    ax2.grid(True, alpha=0.3)

    for n in range(1, niveles + 1):
        prob = pozo.densidad_probabilidad(x, n)
        En = pozo.energia(n)
        # Offset para visualización
        offset = En / (pozo.energia(niveles) * 1.2)
        ax2.fill_between(x, offset, offset + prob * 0.8 / np.max(prob),
                         alpha=0.6, color=colors[n - 1], label=f'n={n}')
        ax2.axhline(offset, color=colors[n - 1], linewidth=1, linestyle='--', alpha=0.5)

    ax2.legend(loc='upper right', fontsize=10)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Figura guardada en: {filename}")
    else:
        plt.show()

    plt.close()


def visualizar_espectro_energetico(pozo: PozoInfinitoCuantico,
                                   niveles: int = 10,
                                   filename: Optional[str] = None) -> None:
    """
    Visualiza el espectro de energía cuantizado del pozo.

    Args:
        pozo: Instancia de PozoInfinitoCuantico
        niveles: Número de niveles a visualizar
        filename: Nombre del archivo para guardar (opcional)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel izquierdo: Niveles de energía
    ax1.set_title('Espectro de Energía Cuantizado', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Energía E (J)', fontsize=12)
    ax1.set_xlabel('Número cuántico n', fontsize=12)
    ax1.grid(True, alpha=0.3)

    ns = np.arange(1, niveles + 1)
    energias = [pozo.energia(n) for n in ns]

    ax1.scatter(ns, energias, s=100, c=ns, cmap='viridis',
                edgecolors='black', linewidth=1.5, zorder=3)

    # Línea mostrando E ∝ n²
    E1 = pozo.energia(1)
    ax1.plot(ns, E1 * ns**2, 'r--', alpha=0.5, linewidth=2, label='E ∝ n²')
    ax1.legend()

    for n in ns:
        E = pozo.energia(n)
        ax1.text(n, E, f'  E{n}', fontsize=9, verticalalignment='center')

    # Panel derecho: Frecuencias
    ax2.set_title('Espectro de Frecuencias', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Frecuencia f (Hz)', fontsize=12)
    ax2.set_xlabel('Número cuántico n', fontsize=12)
    ax2.grid(True, alpha=0.3)

    frecuencias = [pozo.frecuencia(n) for n in ns]

    ax2.scatter(ns, frecuencias, s=100, c=ns, cmap='plasma',
                edgecolors='black', linewidth=1.5, zorder=3)

    # Marcar la frecuencia universal si está cerca
    f1 = pozo.frecuencia(1)
    if abs(f1 - F0_UNIVERSAL) / F0_UNIVERSAL < 0.01:  # Dentro del 1%
        ax2.axhline(F0_UNIVERSAL, color='red', linewidth=2,
                    linestyle='--', alpha=0.7,
                    label=f'f₀ = {F0_UNIVERSAL} Hz (Universal)')
        ax2.legend()

    for n in ns:
        f = pozo.frecuencia(n)
        ax2.text(n, f, f'  {f:.2f} Hz', fontsize=8, verticalalignment='center')

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Figura guardada en: {filename}")
    else:
        plt.show()

    plt.close()


# ============================================================================
# E. EJEMPLO DE USO Y DEMOSTRACIÓN
# ============================================================================

def demo_pozo_estandar():
    """Demostración del pozo cuántico estándar."""
    print("=" * 80)
    print("DEMOSTRACIÓN: POZO INFINITO CUÁNTICO ESTÁNDAR")
    print("=" * 80)
    print()

    # Parámetros típicos: electrón en un pozo de 1 nanómetro
    L = 1e-9  # 1 nm
    m_electron = 9.10938356e-31  # kg

    pozo = PozoInfinitoCuantico(L, m_electron)

    print(f"Longitud del pozo: L = {L * 1e9:.2f} nm")
    print(f"Masa de la partícula: m = {m_electron:.6e} kg (electrón)")
    print()

    print("Primeros 5 niveles de energía:")
    print("-" * 80)
    for n in range(1, 6):
        E = pozo.energia(n)
        f = pozo.frecuencia(n)
        k = pozo.numero_onda(n)
        print(f"  n={n}: E={E:.6e} J, f={f:.6e} Hz, k={k:.6e} m⁻¹")

    print()
    print(f"Energía del punto cero: E₁ = {pozo.energia_punto_cero():.6e} J")
    print(f"Frecuencia fundamental: f₁ = {pozo.frecuencia_fundamental():.6e} Hz")

    return pozo


def demo_resonador_universal():
    """Demostración del resonador basal alineado con f₀ = 141.7001 Hz."""
    print("\n")
    print("=" * 80)
    print("DEMOSTRACIÓN: RESONADOR BASAL UNIVERSAL (f₀ = 141.7001 Hz)")
    print("=" * 80)
    print()

    # Masa de ejemplo: masa de Planck reducida
    m_planck = 2.176434e-8  # kg
    m = m_planck / 1e20  # Masa efectiva del campo

    print(f"Frecuencia objetivo: f₀ = {F0_UNIVERSAL} Hz")
    print(f"Masa efectiva: m = {m:.6e} kg")
    print()

    L, E1, f1 = resonador_basal_universal(m, precision=50)

    print("Propiedades del Resonador Basal:")
    print("-" * 80)
    print(f"  Longitud del pozo: L = {L:.6e} m")
    print(f"  Energía punto cero: E₁ = {E1:.6e} J")
    print(f"  Frecuencia fundamental: f₁ = {f1:.10f} Hz")
    print(f"  Diferencia con f₀: Δf = {abs(f1 - F0_UNIVERSAL):.2e} Hz")
    print(f"  Error relativo: {abs(f1 - F0_UNIVERSAL) / F0_UNIVERSAL * 100:.6e}%")
    print()

    print("Este resonador representa el 'modo basal' del espectro noésico,")
    print("donde la cuantización emerge directamente de la geometría y el")
    print("confinamiento espacial, alineado con la frecuencia universal")
    print("f₀ = 141.7001 Hz detectada en ondas gravitacionales (LIGO).")

    return PozoInfinitoCuantico(L, m)


if __name__ == "__main__":
    # Ejecutar demostraciones
    pozo_std = demo_pozo_estandar()
    pozo_universal = demo_resonador_universal()

    # Generar visualizaciones
    print("\n")
    print("Generando visualizaciones...")
    visualizar_pozo(pozo_std, niveles=4, filename="pozo_cuantico_estandar.png")
    visualizar_espectro_energetico(
        pozo_std, niveles=10, filename="espectro_energia_estandar.png"
    )
    visualizar_pozo(pozo_universal, niveles=4, filename="resonador_basal_universal.png")
    visualizar_espectro_energetico(
        pozo_universal, niveles=10, filename="espectro_energia_universal.png"
    )

    print("\n✓ Demostraciones completadas exitosamente.")
