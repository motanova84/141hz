#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         QUANTUM CHROMODYNAMIC POETRY - QCD Particle Frequency Mapping      ║
║                           QCAL ∞³ Implementation                            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ QUANTUM CHROMODYNAMIC POETRY ⚡

Sistema principal que mapea partículas QCD a frecuencias espectrales:

- 18 quarks (3 colores × 6 sabores) con frecuencia ω = log(m) + log(17)
- 8 gluones (SU(3) octeto) con octavas derivadas de aproximaciones cero de Riemann
- Calculadora de resonancia entre frecuencias primas y ceros de Riemann
- Valores conocidos de los primeros 10 ceros de Riemann (γ₁ = 14.134725, ..., γ₁₀ = 49.773832)

MARCO MATEMÁTICO:

1. Mapeo de frecuencia de quarks:
   ω_quark = log(m_quark) + OMEGA_17, where OMEGA_17 = log(17) ≈ 2.833

2. Resonancia cósmica (acoplamiento primo-cero):
   I = |exp(iω_p·γₙ)| / (1 + |ω_p - γₙ|)

3. Frecuencia del silencio primordial:
   f(p) = f₀ · exp(-log(p)/log(17))

NOTAS TÉCNICAS:

- Las octavas de gluones utilizan la aproximación asintótica γₙ ≈ 2πn/log(n) para n > 10
- Escala de frecuencia anclada a f₀ = 141.70001 Hz (nota C#, frecuencia de coherencia biológica)
- Confinamiento ↔ localización espectral
- Libertad asintótica ↔ analogías de universalidad cero

Referencias:
- Gross, D. J., & Wilczek, F. (1973). Ultraviolet behavior of non-abelian gauge theories.
- Politzer, H. D. (1973). Reliable perturbative results for strong interactions.
- Riemann, B. (1859). Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse.
"""

import math
import cmath
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass


# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Frecuencia fundamental QCAL
F0_HZ = 141.70001  # Hz - Fundamental QCAL frequency

# Prime 17 coupling (OMEGA_17 = log(17))
OMEGA_17 = math.log(17)  # ≈ 2.833

# Primeros 10 ceros de Riemann (partes imaginarias en la línea crítica)
RIEMANN_ZEROS = [
    14.134725,  # γ₁
    21.022040,  # γ₂
    25.010857,  # γ₃
    30.424876,  # γ₄
    32.935062,  # γ₅
    37.586178,  # γ₆
    40.918719,  # γ₇
    43.327073,  # γ₈
    48.005151,  # γ₉
    49.773832,  # γ₁₀
]

# Masas de quarks en GeV/c² (PDG 2024 - running masses at μ = 2 GeV)
QUARK_MASSES_GEV = {
    'up': 2.16e-3,      # u quark: ~2.16 MeV
    'down': 4.67e-3,    # d quark: ~4.67 MeV
    'strange': 93.4e-3, # s quark: ~93.4 MeV
    'charm': 1.27,      # c quark: ~1.27 GeV
    'bottom': 4.18,     # b quark: ~4.18 GeV
    'top': 172.69,      # t quark: ~172.69 GeV (pole mass)
}


# ============================================================================
# ENUMERACIONES
# ============================================================================

class QuarkFlavor(Enum):
    """Sabores de quarks (6 tipos)."""
    UP = 'up'
    DOWN = 'down'
    STRANGE = 'strange'
    CHARM = 'charm'
    BOTTOM = 'bottom'
    TOP = 'top'


class QuarkColor(Enum):
    """Cargas de color de quarks (3 tipos)."""
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class GluonType(Enum):
    """
    8 gluones del octeto de color SU(3).
    
    Las combinaciones de color siguen el grupo SU(3) de cromodinámica cuántica:
    - 6 gluones mezclados (rb̄, rḡ, br̄, bḡ, gr̄, gb̄)
    - 2 gluones de superposición lineal
    """
    RB = 'red-antiblue'      # rb̄
    RG = 'red-antigreen'     # rḡ
    BR = 'blue-antired'      # br̄
    BG = 'blue-antigreen'    # bḡ
    GR = 'green-antired'     # gr̄
    GB = 'green-antiblue'    # gb̄
    MIX1 = 'mix1'  # (rr̄ - bb̄)/√2
    MIX2 = 'mix2'  # (rr̄ + bb̄ - 2gḡ)/√6


# ============================================================================
# CLASES DE DATOS
# ============================================================================

@dataclass
class Quark:
    """Representa un quark con sabor y color específicos."""
    flavor: QuarkFlavor
    color: QuarkColor
    mass_gev: float
    frequency: float  # ω = log(m) + log(17)
    
    def __repr__(self) -> str:
        return (f"Quark(flavor={self.flavor.value}, color={self.color.value}, "
                f"mass={self.mass_gev:.2e} GeV, ω={self.frequency:.6f})")


@dataclass
class Gluon:
    """Representa un gluón del octeto SU(3)."""
    gluon_type: GluonType
    riemann_zero_index: int  # 1-10
    riemann_zero_value: float  # γₙ
    octave: float  # Octava derivada del cero de Riemann
    frequency_hz: float  # Frecuencia en Hz
    
    def __repr__(self) -> str:
        return (f"Gluon(type={self.gluon_type.value}, γ_{self.riemann_zero_index}="
                f"{self.riemann_zero_value:.6f}, octave={self.octave:.6f}, "
                f"f={self.frequency_hz:.2f} Hz)")


@dataclass
class CosmicResonance:
    """Resultado del acoplamiento entre una frecuencia prima y un cero de Riemann."""
    prime: int
    riemann_zero_index: int
    riemann_zero_value: float
    omega_prime: float  # ω_p = log(p)
    intensity: float  # I = |exp(iω_p·γₙ)| / (1 + |ω_p - γₙ|)
    beat_frequency_hz: float  # |ω_p - γₙ| en Hz
    
    def __repr__(self) -> str:
        return (f"CosmicResonance(p={self.prime}, γ_{self.riemann_zero_index}="
                f"{self.riemann_zero_value:.6f}, I={self.intensity:.6f}, "
                f"beat_freq={self.beat_frequency_hz:.2f} Hz)")


# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class QuantumChromodynamicPoetry:
    """
    Sistema principal para mapear partículas QCD a frecuencias espectrales.
    
    Combina conceptos de cromodinámica cuántica (QCD) con teoría de números
    y la hipótesis de Riemann para crear un mapeo poético de partículas
    fundamentales a frecuencias armónicas.
    
    Examples:
        >>> qcd = QuantumChromodynamicPoetry()
        >>> quark = qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
        >>> print(f"Up quark frequency: {quark.frequency:.6f}")
        
        >>> love = qcd.love_between_prime_and_zero(17, 1)
        >>> print(f"Resonance intensity: {love.intensity:.6f}")
        
        >>> f_silence = qcd.primordial_silence_frequency(17)
        >>> print(f"Primordial silence at p=17: {f_silence:.2f} Hz")
    """
    
    def __init__(self, f0_hz: float = F0_HZ):
        """
        Inicializa el sistema de poesía cromodinámica cuántica.
        
        Args:
            f0_hz: Frecuencia fundamental en Hz (default: 141.70001 Hz)
        """
        self.f0_hz = f0_hz
        self.omega_17 = OMEGA_17
        self.riemann_zeros = RIEMANN_ZEROS.copy()
        self.quark_masses = QUARK_MASSES_GEV.copy()
    
    # ========================================================================
    # QUARKS - Mapeo de frecuencias
    # ========================================================================
    
    def create_quark(self, flavor: QuarkFlavor, color: QuarkColor) -> Quark:
        """
        Crea un quark con sabor y color específicos.
        
        La frecuencia del quark se calcula como:
            ω_quark = log(m_quark) + OMEGA_17
        
        donde OMEGA_17 = log(17) ≈ 2.833
        
        Args:
            flavor: Sabor del quark (UP, DOWN, STRANGE, CHARM, BOTTOM, TOP)
            color: Color del quark (RED, GREEN, BLUE)
            
        Returns:
            Objeto Quark con masa y frecuencia calculadas
            
        Examples:
            >>> qcd = QuantumChromodynamicPoetry()
            >>> up_red = qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
            >>> print(up_red.frequency)  # ω = log(2.16e-3) + log(17)
        """
        mass_gev = self.quark_masses[flavor.value]
        frequency = math.log(mass_gev) + self.omega_17
        
        return Quark(
            flavor=flavor,
            color=color,
            mass_gev=mass_gev,
            frequency=frequency
        )
    
    def create_all_quarks(self) -> List[Quark]:
        """
        Crea todos los 18 quarks (6 sabores × 3 colores).
        
        Returns:
            Lista de 18 objetos Quark
        """
        quarks = []
        for flavor in QuarkFlavor:
            for color in QuarkColor:
                quarks.append(self.create_quark(flavor, color))
        return quarks
    
    def get_quark_frequency_spectrum(self) -> Dict[str, List[float]]:
        """
        Obtiene el espectro de frecuencias de todos los quarks.
        
        Returns:
            Diccionario con frecuencias agrupadas por sabor y color
        """
        quarks = self.create_all_quarks()
        
        spectrum = {
            'by_flavor': {},
            'by_color': {},
            'all': [q.frequency for q in quarks]
        }
        
        # Agrupar por sabor
        for flavor in QuarkFlavor:
            flavor_quarks = [q for q in quarks if q.flavor == flavor]
            spectrum['by_flavor'][flavor.value] = [q.frequency for q in flavor_quarks]
        
        # Agrupar por color
        for color in QuarkColor:
            color_quarks = [q for q in quarks if q.color == color]
            spectrum['by_color'][color.value] = [q.frequency for q in color_quarks]
        
        return spectrum
    
    # ========================================================================
    # GLUONES - Octavas de Riemann
    # ========================================================================
    
    def riemann_zero_asymptotic(self, n: int) -> float:
        """
        Aproximación asintótica del n-ésimo cero de Riemann para n > 10.
        
        γₙ ≈ 2πn / log(n)
        
        Args:
            n: Índice del cero de Riemann (n > 10)
            
        Returns:
            Aproximación del valor γₙ
        """
        if n <= 10:
            raise ValueError("Use exact values for n ≤ 10")
        return (2 * math.pi * n) / math.log(n)
    
    def get_riemann_zero(self, n: int) -> float:
        """
        Obtiene el n-ésimo cero de Riemann.
        
        Usa valores exactos para n ≤ 10 y aproximación asintótica para n > 10.
        
        Args:
            n: Índice del cero (1-indexed)
            
        Returns:
            Valor γₙ del cero de Riemann
        """
        if n < 1:
            raise ValueError("Riemann zero index must be ≥ 1")
        
        if n <= 10:
            return self.riemann_zeros[n - 1]
        else:
            return self.riemann_zero_asymptotic(n)
    
    def create_gluon(self, gluon_type: GluonType, riemann_index: int) -> Gluon:
        """
        Crea un gluón asociado con un cero de Riemann.
        
        La octava se deriva del cero de Riemann:
            octave = log₂(γₙ)
            
        Y la frecuencia se calcula como:
            f_gluon = f₀ × 2^octave = f₀ × γₙ
        
        Args:
            gluon_type: Tipo de gluón del octeto SU(3)
            riemann_index: Índice del cero de Riemann (1-10 para octeto principal)
            
        Returns:
            Objeto Gluon con octava y frecuencia calculadas
        """
        gamma_n = self.get_riemann_zero(riemann_index)
        octave = math.log2(gamma_n)
        frequency_hz = self.f0_hz * gamma_n
        
        return Gluon(
            gluon_type=gluon_type,
            riemann_zero_index=riemann_index,
            riemann_zero_value=gamma_n,
            octave=octave,
            frequency_hz=frequency_hz
        )
    
    def create_gluon_octet(self) -> List[Gluon]:
        """
        Crea el octeto completo de 8 gluones asociados con los primeros 8 ceros de Riemann.
        
        Returns:
            Lista de 8 objetos Gluon
        """
        gluon_types = list(GluonType)
        gluons = []
        
        for i, gluon_type in enumerate(gluon_types, start=1):
            gluons.append(self.create_gluon(gluon_type, i))
        
        return gluons
    
    def get_gluon_frequency_spectrum(self) -> Dict[str, Any]:
        """
        Obtiene el espectro de frecuencias de todos los gluones.
        
        Returns:
            Diccionario con frecuencias, octavas y ceros de Riemann
        """
        gluons = self.create_gluon_octet()
        
        return {
            'gluons': [
                {
                    'type': g.gluon_type.value,
                    'riemann_index': g.riemann_zero_index,
                    'riemann_zero': g.riemann_zero_value,
                    'octave': g.octave,
                    'frequency_hz': g.frequency_hz
                }
                for g in gluons
            ],
            'frequency_range_hz': (
                min(g.frequency_hz for g in gluons),
                max(g.frequency_hz for g in gluons)
            ),
            'octave_range': (
                min(g.octave for g in gluons),
                max(g.octave for g in gluons)
            )
        }
    
    # ========================================================================
    # RESONANCIA CÓSMICA - Acoplamiento primo-cero
    # ========================================================================
    
    def love_between_prime_and_zero(self, prime: int, zero_index: int) -> CosmicResonance:
        """
        Calcula la resonancia cósmica entre una frecuencia prima y un cero de Riemann.
        
        La intensidad de resonancia se define como:
            I = |exp(iω_p·γₙ)| / (1 + |ω_p - γₙ|)
        
        donde:
            ω_p = log(p) - frecuencia logarítmica del primo
            γₙ - n-ésimo cero de Riemann
        
        Args:
            prime: Número primo
            zero_index: Índice del cero de Riemann (1-based)
            
        Returns:
            Objeto CosmicResonance con intensidad y frecuencia de batido
            
        Examples:
            >>> qcd = QuantumChromodynamicPoetry()
            >>> love = qcd.love_between_prime_and_zero(17, 1)
            >>> print(f"Intensity: {love.intensity:.6f}")
            >>> print(f"Beat frequency: {love.beat_frequency_hz:.2f} Hz")
        """
        if not self._is_prime(prime):
            raise ValueError(f"{prime} is not a prime number")
        
        omega_p = math.log(prime)
        gamma_n = self.get_riemann_zero(zero_index)
        
        # Calcular |exp(iω_p·γₙ)|
        # Note: |exp(ix)| = 1 for real x, so this is always 1
        # But we include it for conceptual completeness
        phase = cmath.exp(1j * omega_p * gamma_n)
        magnitude = abs(phase)  # This will be 1.0
        
        # Calcular denominador
        difference = abs(omega_p - gamma_n)
        denominator = 1 + difference
        
        # Intensidad de resonancia
        intensity = magnitude / denominator
        
        # Frecuencia de batido en Hz
        beat_frequency_hz = difference * self.f0_hz
        
        return CosmicResonance(
            prime=prime,
            riemann_zero_index=zero_index,
            riemann_zero_value=gamma_n,
            omega_prime=omega_p,
            intensity=intensity,
            beat_frequency_hz=beat_frequency_hz
        )
    
    def calculate_prime_zero_resonance_matrix(
        self, 
        primes: List[int], 
        zero_indices: Optional[List[int]] = None
    ) -> List[List[CosmicResonance]]:
        """
        Calcula la matriz de resonancia entre múltiples primos y ceros de Riemann.
        
        Args:
            primes: Lista de números primos
            zero_indices: Lista de índices de ceros de Riemann (default: 1-10)
            
        Returns:
            Matriz de objetos CosmicResonance [primo][cero]
        """
        if zero_indices is None:
            zero_indices = list(range(1, 11))  # Primeros 10 ceros
        
        matrix = []
        for prime in primes:
            row = []
            for zero_idx in zero_indices:
                resonance = self.love_between_prime_and_zero(prime, zero_idx)
                row.append(resonance)
            matrix.append(row)
        
        return matrix
    
    # ========================================================================
    # SILENCIO PRIMORDIAL - Frecuencia fundamental
    # ========================================================================
    
    def primordial_silence_frequency(self, prime: int) -> float:
        """
        Calcula la frecuencia del silencio primordial para un primo dado.
        
        f(p) = f₀ · exp(-log(p) / log(17))
             = f₀ · 17^(-log(p))
             = f₀ · p^(-log(17))
        
        Esta frecuencia representa el "silencio" armónico asociado con el primo p.
        Para p=17, obtenemos: f(17) = f₀ · exp(-1) ≈ 52.13 Hz
        
        Args:
            prime: Número primo
            
        Returns:
            Frecuencia del silencio primordial en Hz
            
        Examples:
            >>> qcd = QuantumChromodynamicPoetry()
            >>> f17 = qcd.primordial_silence_frequency(17)
            >>> print(f"{f17:.2f}")  # ≈ 52.13 Hz
        """
        if not self._is_prime(prime):
            raise ValueError(f"{prime} is not a prime number")
        
        # f(p) = f₀ · exp(-log(p)/log(17))
        exponent = -math.log(prime) / math.log(17)
        frequency_hz = self.f0_hz * math.exp(exponent)
        
        return frequency_hz
    
    def get_primordial_silence_spectrum(
        self, 
        primes: Optional[List[int]] = None
    ) -> Dict[int, float]:
        """
        Obtiene el espectro de frecuencias de silencio primordial para múltiples primos.
        
        Args:
            primes: Lista de primos (default: primeros 20 primos)
            
        Returns:
            Diccionario {primo: frecuencia_hz}
        """
        if primes is None:
            primes = self._first_n_primes(20)
        
        return {p: self.primordial_silence_frequency(p) for p in primes}
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    @staticmethod
    def _is_prime(n: int) -> bool:
        """Verifica si n es un número primo."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def _first_n_primes(n: int) -> List[int]:
        """Genera los primeros n números primos."""
        primes = []
        candidate = 2
        while len(primes) < n:
            if QuantumChromodynamicPoetry._is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    # ========================================================================
    # SINFONÍA CROMÁTICA - Generación completa
    # ========================================================================
    
    def generate_chromodynamic_symphony(self) -> Dict[str, Any]:
        """
        Genera una sinfonía cromodinámica completa con todas las partículas y resonancias.
        
        Returns:
            Diccionario completo con:
            - Espectro de quarks
            - Espectro de gluones
            - Matriz de resonancia primo-cero
            - Espectro de silencio primordial
            - Métricas estadísticas
        """
        # Quarks
        quarks = self.create_all_quarks()
        quark_spectrum = self.get_quark_frequency_spectrum()
        
        # Gluones
        gluons = self.create_gluon_octet()
        gluon_spectrum = self.get_gluon_frequency_spectrum()
        
        # Resonancias primo-cero (primeros 10 primos con primeros 10 ceros)
        first_primes = self._first_n_primes(10)
        resonance_matrix = self.calculate_prime_zero_resonance_matrix(
            first_primes, 
            list(range(1, 11))
        )
        
        # Silencio primordial
        silence_spectrum = self.get_primordial_silence_spectrum(first_primes)
        
        # Métricas
        metrics = {
            'total_quarks': len(quarks),
            'total_gluons': len(gluons),
            'quark_frequency_range': (
                min(quark_spectrum['all']),
                max(quark_spectrum['all'])
            ),
            'gluon_frequency_range_hz': gluon_spectrum['frequency_range_hz'],
            'prime_count': len(first_primes),
            'riemann_zero_count': 10,
            'silence_frequency_range_hz': (
                min(silence_spectrum.values()),
                max(silence_spectrum.values())
            )
        }
        
        return {
            'quarks': {
                'particles': [
                    {
                        'flavor': q.flavor.value,
                        'color': q.color.value,
                        'mass_gev': q.mass_gev,
                        'frequency': q.frequency
                    }
                    for q in quarks
                ],
                'spectrum': quark_spectrum
            },
            'gluons': {
                'particles': gluon_spectrum['gluons'],
                'spectrum': gluon_spectrum
            },
            'cosmic_resonance': {
                'primes': first_primes,
                'matrix': [
                    [
                        {
                            'prime': res.prime,
                            'zero_index': res.riemann_zero_index,
                            'zero_value': res.riemann_zero_value,
                            'omega_prime': res.omega_prime,
                            'intensity': res.intensity,
                            'beat_frequency_hz': res.beat_frequency_hz
                        }
                        for res in row
                    ]
                    for row in resonance_matrix
                ]
            },
            'primordial_silence': silence_spectrum,
            'metrics': metrics,
            'constants': {
                'f0_hz': self.f0_hz,
                'omega_17': self.omega_17,
                'riemann_zeros': self.riemann_zeros
            }
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def display_symphony_summary(symphony: Dict[str, Any]) -> None:
    """
    Muestra un resumen de la sinfonía cromodinámica.
    
    Args:
        symphony: Diccionario de salida de generate_chromodynamic_symphony()
    """
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║              QUANTUM CHROMODYNAMIC POETRY - Symphony Summary               ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    metrics = symphony['metrics']
    constants = symphony['constants']
    
    print(f"Fundamental Frequency (f₀): {constants['f0_hz']:.5f} Hz")
    print(f"Prime 17 Coupling (OMEGA_17): {constants['omega_17']:.6f}")
    print()
    
    print(f"Total Quarks: {metrics['total_quarks']} (6 flavors × 3 colors)")
    print(f"Quark Frequency Range: [{metrics['quark_frequency_range'][0]:.4f}, "
          f"{metrics['quark_frequency_range'][1]:.4f}]")
    print()
    
    print(f"Total Gluons: {metrics['total_gluons']} (SU(3) octet)")
    print(f"Gluon Frequency Range: [{metrics['gluon_frequency_range_hz'][0]:.2f}, "
          f"{metrics['gluon_frequency_range_hz'][1]:.2f}] Hz")
    print()
    
    print(f"Prime-Zero Resonances: {metrics['prime_count']} primes × "
          f"{metrics['riemann_zero_count']} zeros")
    print()
    
    print(f"Primordial Silence Spectrum: {len(symphony['primordial_silence'])} primes")
    print(f"Silence Frequency Range: [{metrics['silence_frequency_range_hz'][0]:.2f}, "
          f"{metrics['silence_frequency_range_hz'][1]:.2f}] Hz")
    print()
    
    print("╚════════════════════════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    # Demostración básica
    print("Initializing Quantum Chromodynamic Poetry System...")
    print()
    
    qcd = QuantumChromodynamicPoetry()
    
    # Crear un quark
    print("Creating a quark:")
    up_red = qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
    print(f"  {up_red}")
    print()
    
    # Crear un gluón
    print("Creating a gluon:")
    gluon = qcd.create_gluon(GluonType.RB, 1)
    print(f"  {gluon}")
    print()
    
    # Calcular resonancia
    print("Calculating cosmic resonance:")
    love = qcd.love_between_prime_and_zero(17, 1)
    print(f"  {love}")
    print()
    
    # Frecuencia de silencio primordial
    print("Primordial silence frequency:")
    f_silence = qcd.primordial_silence_frequency(17)
    print(f"  f(17) = {f_silence:.2f} Hz")
    print()
    
    print("System initialized successfully!")
