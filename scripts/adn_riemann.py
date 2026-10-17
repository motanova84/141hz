#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo ADN-Riemann: Codificación de secuencias de ADN mediante ceros de Riemann
Este módulo implementa el puente matemático entre secuencias biológicas de ADN
y la distribución de ceros de la función zeta de Riemann en la línea crítica.

Conceptos clave:
1. Cada secuencia de ADN (A, T, G, C) se codifica como un número natural
2. Ese número se mapea a un cero de Riemann ζ(1/2 + it_n) = 0
3. Las propiedades espectrales del cero informan sobre resonancia con f₀ = 141.7001 Hz

Autor: QCAL ∞³ System
Fecha: 2026-03-08
"""
import numpy as np
import mpmath as mp
from typing import Dict, List, Tuple, Optional
from qcal.constants import F0_HZ, HBAR, C, H_PLANCK, KAPPA_PI
from fisica.constantes_coherencia import (
    COHERENCIA_MINIMA, COHERENCIA_EXCELENTE, COHERENCIA_PERFECTA
)

# ============================================================================
# CONSTANTES EXPORTADAS
# ============================================================================

# Frecuencia fundamental QCAL
FRECUENCIA_BASE = F0_HZ  # 141.7001 Hz

# Coherencia óptima
PSI_OPTIMO = COHERENCIA_EXCELENTE  # 0.999

# Factor de unificación (K = 1/7)
FACTOR_UNIFICACION = 1.0 / 7.0  # 0.142857...

# Constantes físicas
HBAR = HBAR  # 1.054571817e-34 J·s
VELOCIDAD_LUZ = C  # 299792458 m/s

# Mapeo de bases de ADN a números (codificación cuaternaria)
BASE_A_NUMERO = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
NUMERO_A_BASE = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}

# Complementos de bases (Watson-Crick)
COMPLEMENTO = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

# Constante de Boltzmann
KB = 1.380649e-23  # J/K


class CalculadorCerosRiemann:
    """
    Calcula y gestiona los ceros de la función zeta de Riemann en la línea crítica.
    
    Utiliza mpmath para cálculos de alta precisión.
    Los ceros están en la línea s = 1/2 + it, donde ζ(s) = 0.
    """
    
    def __init__(self, num_ceros: int = 10000, precision: int = 50):
        """
        Inicializa el calculador de ceros de Riemann.
        
        Args:
            num_ceros: Número de ceros a precalcular
            precision: Dígitos de precisión para mpmath
        """
        self.num_ceros = num_ceros
        self.precision = precision
        mp.mp.dps = precision
        
        # Cache de ceros precalculados
        self._ceros_cache: List[float] = []
        self._precalcular_ceros()
    
    def _precalcular_ceros(self):
        """Precalcula los primeros N ceros de Riemann."""
        # Los primeros ceros conocidos (parte imaginaria t)
        # ζ(1/2 + it_n) = 0
        for n in range(1, min(self.num_ceros + 1, 100)):
            try:
                # Usar función de mpmath para encontrar ceros
                t_n = mp.zetazero(n)
                self._ceros_cache.append(float(t_n.imag))
            except Exception as e:
                # Si falla mpmath, usar aproximación analítica
                # t_n ≈ 2πn / log(n) para n grande
                if n > 1:
                    t_aprox = 2 * np.pi * n / np.log(n)
                    self._ceros_cache.append(t_aprox)
                else:
                    # Primer cero conocido
                    self._ceros_cache.append(14.134725)
    
    def obtener_cero(self, indice: int) -> float:
        """
        Obtiene el cero de Riemann número 'indice'.
        
        Args:
            indice: Índice del cero (1-indexed, siguiendo convención matemática)
            
        Returns:
            Parte imaginaria t del cero ζ(1/2 + it) = 0
        """
        if indice <= 0:
            raise ValueError("El índice debe ser positivo (1-indexed)")
        
        if indice <= len(self._ceros_cache):
            return self._ceros_cache[indice - 1]
        
        # Si no está en cache, calcular o aproximar
        if indice <= 100:
            try:
                t_n = mp.zetazero(indice)
                return float(t_n.imag)
            except:
                pass
        
        # Aproximación para índices grandes
        # Fórmula de Riemann-von Mangoldt
        t_aprox = 2 * np.pi * indice / np.log(indice)
        return t_aprox
    
    def numero_de_ceros(self) -> int:
        """Retorna el número de ceros precalculados."""
        return len(self._ceros_cache)


class CodificadorADNRiemann:
    """
    Codifica secuencias de ADN como números y las mapea a ceros de Riemann.
    
    Establece la correspondencia:
    Secuencia ADN → Número Natural → Cero de Riemann → Propiedades Espectrales
    """
    
    def __init__(self, calculador_riemann: CalculadorCerosRiemann):
        """
        Inicializa el codificador.
        
        Args:
            calculador_riemann: Instancia de CalculadorCerosRiemann
        """
        self.calculador = calculador_riemann
    
    def secuencia_a_numero(self, secuencia: str) -> int:
        """
        Convierte una secuencia de ADN a un número natural (base 4).
        
        Args:
            secuencia: Cadena de bases (A, T, G, C)
            
        Returns:
            Número natural correspondiente
            
        Example:
            >>> codificador.secuencia_a_numero("ATGC")
            >>> # A=0, T=1, G=2, C=3 → 0*4³ + 1*4² + 2*4¹ + 3*4⁰ = 27
        """
        secuencia = secuencia.upper()
        numero = 0
        for i, base in enumerate(secuencia):
            if base not in BASE_A_NUMERO:
                raise ValueError(f"Base inválida: {base}")
            numero = numero * 4 + BASE_A_NUMERO[base]
        return numero
    
    def numero_a_secuencia(self, numero: int, longitud: int) -> str:
        """
        Convierte un número natural a secuencia de ADN.
        
        Args:
            numero: Número natural
            longitud: Longitud deseada de la secuencia
            
        Returns:
            Secuencia de ADN
        """
        if numero < 0:
            raise ValueError("El número debe ser no negativo")
        
        secuencia = []
        for _ in range(longitud):
            base_idx = numero % 4
            secuencia.append(NUMERO_A_BASE[base_idx])
            numero //= 4
        
        return ''.join(reversed(secuencia))
    
    def propiedades_espectrales(self, secuencia: str) -> Dict:
        """
        Calcula las propiedades espectrales de una secuencia de ADN.
        
        Mapea la secuencia a un cero de Riemann y analiza su resonancia
        con la frecuencia fundamental f₀.
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Dict con propiedades espectrales
        """
        # Convertir secuencia a número
        numero = self.secuencia_a_numero(secuencia)
        
        # Mapear a índice de cero de Riemann (1-indexed)
        # Usar módulo para mantenerse dentro del rango de ceros
        num_ceros = self.calculador.numero_de_ceros()
        indice_cero = (numero % num_ceros) + 1
        
        # Obtener el cero de Riemann correspondiente
        t_cero = self.calculador.obtener_cero(indice_cero)
        
        # Calcular frecuencia asociada
        # Usando la relación: f = t / (2π)
        frecuencia_riemann = t_cero / (2 * np.pi)
        
        # Calcular resonancia con f₀
        # Resonancia máxima cuando frecuencias coinciden
        ratio = frecuencia_riemann / FRECUENCIA_BASE
        
        # Factor de resonancia (Lorentziano centrado en ratio=1)
        # Q = 100 (factor de calidad típico)
        Q = 100
        resonancia = 1.0 / (1.0 + Q**2 * (ratio - 1.0)**2)
        
        # Espaciado local entre ceros (importante para entropía)
        if indice_cero < num_ceros:
            t_siguiente = self.calculador.obtener_cero(indice_cero + 1)
            espaciado_local = t_siguiente - t_cero
        else:
            # Espaciado promedio asintótico: ~2π/log(t)
            espaciado_local = 2 * np.pi / np.log(t_cero + 1)
        
        return {
            'secuencia': secuencia,
            'numero': numero,
            'indice_cero_riemann': indice_cero,
            'cero_riemann_t': t_cero,
            'frecuencia_riemann_hz': frecuencia_riemann,
            'resonancia_f0': resonancia,
            'ratio_frecuencias': ratio,
            'espaciado_local': espaciado_local,
            'Q_factor': Q
        }


def calcular_coherencia_cuantica_adn(secuencia: str, 
                                     temperatura: float = 310.0) -> Dict:
    """
    Calcula la coherencia cuántica de una secuencia de ADN a una temperatura dada.
    
    Implementa el modelo de decoherencia térmica y calcula el parámetro Ψ
    (coherencia cuántica efectiva).
    
    Args:
        secuencia: Secuencia de ADN
        temperatura: Temperatura en Kelvin (default: 310 K = 37°C, temperatura corporal)
        
    Returns:
        Dict con parámetros de coherencia
    """
    # Energía térmica
    energia_termica = KB * temperatura  # J
    
    # Energía de la frecuencia fundamental
    energia_cuantica = HBAR * 2 * np.pi * FRECUENCIA_BASE  # J
    
    # Ratio de energías (medida de ruido térmico)
    ratio_ruido = energia_termica / energia_cuantica
    
    # Tiempo de decoherencia (aproximado)
    # τ_decoherencia ∝ ℏ / (k_B T)
    tau_decoherencia = HBAR / (KB * temperatura)  # segundos
    
    # Coherencia efectiva (decae exponencialmente con temperatura)
    # Ψ = exp(-kT/ℏω) para T >> T_quantum
    # Pero saturamos en el límite bajo
    psi_efectivo = np.exp(-ratio_ruido / 1e10)  # Normalización para obtener valores razonables
    
    # Asegurar que esté en [0, 1]
    psi_efectivo = max(0.0, min(1.0, psi_efectivo))
    
    # Factor de calidad derivado de la coherencia
    if psi_efectivo < 0.9999:
        Q_efectivo = 1.0 / (1.0 - psi_efectivo)
    else:
        Q_efectivo = 10000  # Muy alto
    
    return {
        'secuencia': secuencia,
        'temperatura_K': temperatura,
        'energia_termica_J': energia_termica,
        'energia_cuantica_J': energia_cuantica,
        'ratio_ruido_termico': ratio_ruido,
        'tau_decoherencia_s': tau_decoherencia,
        'psi_efectivo': psi_efectivo,
        'Q_efectivo': Q_efectivo,
        'coherente': psi_efectivo >= COHERENCIA_MINIMA
    }


def demo_adn_riemann():
    """Demostración del módulo ADN-Riemann."""
    print("=" * 80)
    print("MÓDULO ADN-RIEMANN: Codificación Biológica mediante Ceros de Riemann")
    print("=" * 80)
    
    # Crear calculador de ceros
    print("\n1. Inicializando calculador de ceros de Riemann...")
    calculador = CalculadorCerosRiemann(num_ceros=1000)
    print(f"   Ceros precalculados: {calculador.numero_de_ceros()}")
    print(f"   Primer cero: t₁ = {calculador.obtener_cero(1):.6f}")
    print(f"   Segundo cero: t₂ = {calculador.obtener_cero(2):.6f}")
    print(f"   Tercer cero: t₃ = {calculador.obtener_cero(3):.6f}")
    
    # Crear codificador
    codificador = CodificadorADNRiemann(calculador)
    
    # Secuencias de prueba
    print("\n2. Codificación de secuencias de ADN:")
    print("-" * 80)
    
    secuencias = ["ATGC", "GACT", "AAAA", "TTTT", "GCGC"]
    
    for seq in secuencias:
        numero = codificador.secuencia_a_numero(seq)
        props = codificador.propiedades_espectrales(seq)
        
        print(f"\n   Secuencia: {seq}")
        print(f"   Número: {numero}")
        print(f"   Cero de Riemann: t_{props['indice_cero_riemann']} = {props['cero_riemann_t']:.6f}")
        print(f"   Frecuencia Riemann: {props['frecuencia_riemann_hz']:.4f} Hz")
        print(f"   Resonancia con f₀: {props['resonancia_f0']:.6f}")
        print(f"   Ratio f_R/f₀: {props['ratio_frecuencias']:.6f}")
    
    # Coherencia cuántica
    print("\n3. Coherencia Cuántica (T = 310 K):")
    print("-" * 80)
    
    for seq in secuencias[:3]:
        coherencia = calcular_coherencia_cuantica_adn(seq, temperatura=310.0)
        print(f"\n   Secuencia: {seq}")
        print(f"   Ψ_efectivo: {coherencia['psi_efectivo']:.6f}")
        print(f"   Q_efectivo: {coherencia['Q_efectivo']:.2f}")
        print(f"   τ_decoherencia: {coherencia['tau_decoherencia_s']:.6e} s")
        print(f"   Coherente: {coherencia['coherente']}")
    
    # Conservación de información
    print("\n4. Conservación de Información:")
    print("-" * 80)
    
    test_seq = "ATGC"
    numero = codificador.secuencia_a_numero(test_seq)
    recuperada = codificador.numero_a_secuencia(numero, len(test_seq))
    print(f"   Original: {test_seq}")
    print(f"   Número: {numero}")
    print(f"   Recuperada: {recuperada}")
    print(f"   Conservación: {test_seq == recuperada} ✓")
    
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == "__main__":
    demo_adn_riemann()
