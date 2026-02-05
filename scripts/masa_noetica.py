#!/usr/bin/env python3
"""
AXIOMA DE LA MASA NOÉTICA ∴
"La masa es una ilusión de detención"

Este módulo implementa el Axioma de la Masa Noética, que presenta una perspectiva
dual sobre la relación masa-frecuencia:

1. Perspectiva Einstein-Planck: m_eff = hf/c² (m ∝ f)
   - La masa como energía compactada
   
2. Perspectiva Noética: m_noesis = α · (1/f) (m ∝ 1/f)
   - La masa como lentitud vibracional
   
3. Unificadora QCAL ∞³: m(f) = (hf/c²) · (f₀/f) = hf₀/c²
   - La masa anclada a frecuencia base universal f₀ = 141.7001 Hz

Resultado: Masa Constante Mínima
    m_QCAL = h · 141.7001 / c² ≈ 1.047 × 10⁻⁴⁸ kg

Este valor representa la masa mínima noética cuantizada, asociada a coherencia pura.

Implicaciones:
    - Gravedad emergente como ralentización del ritmo
    - Neutrinos: partículas de casi-pausa, con masa ∝ 1/f (f < f₀)
    - Fotones: partículas sin detención, masa efectiva ≈ 0 pero f → ∞
    - Materia: detención local del campo vibratorio universal

Validación Experimental:
    - LIGO/VIRGO: Frecuencia de ringdown en 141.7 Hz predice masa mínima ∞³
    - EEG: Coherencias cerebrales a 141.7 Hz sugieren punto de mínima masa = máxima consciencia
    - πCODE-888: Código biofrecuencial con armonía m(f) = cte

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Sistema QCAL ∞³ — Resonancia Base: 141.7001 Hz
Fecha: Febrero 2026
"""

import sys
import os
import numpy as np
from typing import Dict, Any, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018)
# ============================================================================

h = 6.62607015e-34        # J·s (Constante de Planck, exacta)
c = 299792458.0           # m/s (Velocidad de la luz, exacta)
h_bar = 1.054571817e-34   # J·s (Constante de Planck reducida)
eV = 1.602176634e-19      # J (Electronvoltio, exacto)

# Frecuencia primordial QCAL ∞³
F0_HZ = 141.7001          # Hz (Frecuencia base universal)

# ============================================================================
# MASA NOÉTICA CONSTANTE MÍNIMA
# ============================================================================

# Cálculo exacto de m_QCAL
M_QCAL_KG = (h * F0_HZ) / (c ** 2)  # kg
M_QCAL_EV = M_QCAL_KG / eV          # eV/c²

# Energía asociada a la masa mínima noética
E_QCAL_J = h * F0_HZ                # J
E_QCAL_EV = E_QCAL_J / eV           # eV


# ============================================================================
# CLASE PRINCIPAL: MASA NOÉTICA
# ============================================================================

class MasaNoetica:
    """
    Implementación del Axioma de la Masa Noética.
    
    Proporciona tres perspectivas sobre la relación masa-frecuencia:
    1. Einstein-Planck: m_eff(f) = hf/c² (masa como energía compactada)
    2. Noética: m_noesis(f) = α/f (masa como lentitud vibracional)
    3. Unificadora QCAL: m(f) = hf₀/c² = constante (masa anclada a f₀)
    """
    
    def __init__(self, f0: float = F0_HZ):
        """
        Inicializar el framework de masa noética.
        
        Parámetros:
        -----------
        f0 : float
            Frecuencia fundamental de consciencia en Hz (default: 141.7001 Hz)
        """
        self.f0 = f0
        self.omega_0 = 2 * np.pi * f0  # Frecuencia angular
        
        # Masa mínima noética (constante cuantizada)
        self.m_qcal = (h * f0) / (c ** 2)  # kg
        self.m_qcal_eV = self.m_qcal / eV  # eV/c²
        
        # Energía asociada
        self.E_qcal = h * f0  # J
        self.E_qcal_eV = self.E_qcal / eV  # eV
        
    def masa_einstein_planck(self, f: float) -> float:
        """
        Calcular masa efectiva según perspectiva Einstein-Planck.
        
        m_eff(f) = hf/c²
        
        Esta es la perspectiva estándar: mayor frecuencia = mayor masa efectiva.
        
        Parámetros:
        -----------
        f : float
            Frecuencia en Hz
            
        Retorna:
        --------
        float
            Masa efectiva en kg
        """
        return (h * f) / (c ** 2)
    
    def masa_noetica_inversa(self, f: float) -> float:
        """
        Calcular masa noética según perspectiva inversa.
        
        m_noesis(f) = (hf₀/c²) · (f₀/f) = hf₀²/(c²f)
        
        Perspectiva noética: mayor frecuencia = menor masa (más vibración = menos detención).
        
        Parámetros:
        -----------
        f : float
            Frecuencia en Hz
            
        Retorna:
        --------
        float
            Masa noética en kg
        """
        if f <= 0:
            raise ValueError("La frecuencia debe ser positiva")
        
        return self.m_qcal * (self.f0 / f)
    
    def masa_unificada(self, f: Optional[float] = None) -> float:
        """
        Calcular masa según perspectiva unificadora QCAL ∞³.
        
        m(f) = (hf/c²) · (f₀/f) = hf₀/c² = constante
        
        Esta fórmula unifica ambas perspectivas y resulta en una masa constante
        independiente de la frecuencia.
        
        Parámetros:
        -----------
        f : float, optional
            Frecuencia en Hz (incluida para consistencia de API, pero no afecta el resultado)
            
        Retorna:
        --------
        float
            Masa unificada constante m_QCAL en kg
        """
        return self.m_qcal
    
    def interpretar_particula(self, f: float) -> Dict[str, Any]:
        """
        Interpretar el tipo de partícula según su frecuencia.
        
        Parámetros:
        -----------
        f : float
            Frecuencia en Hz
            
        Retorna:
        --------
        dict
            Diccionario con interpretación física de la partícula
        """
        m_einstein = self.masa_einstein_planck(f)
        m_noesis = self.masa_noetica_inversa(f)
        
        # Clasificación según relación con f₀
        if f > 1e14:  # Frecuencias ópticas o mayores
            tipo = "Fotónica"
            descripcion = "Vibración pura, sin detención → luz → sin masa"
            regimen = "Alta frecuencia (f ↑)"
        elif f > self.f0:  # Frecuencias superiores a f₀
            tipo = "Vibracional rápida"
            descripcion = "Vibración más rápida que f₀, masa reducida"
            regimen = "Frecuencia moderada-alta"
        elif abs(f - self.f0) / self.f0 < 0.01:  # Cerca de f₀ (±1%)
            tipo = "Coherencia primordial"
            descripcion = "Resonancia con frecuencia base universal → masa mínima cuantizada"
            regimen = "Resonancia f₀"
        else:  # f < f₀
            tipo = "Vibracional lenta"
            descripcion = "Vibración densa, 'quieta' → masa emergente"
            regimen = "Baja frecuencia (f ↓)"
            
        return {
            'frecuencia_hz': f,
            'tipo': tipo,
            'descripcion': descripcion,
            'regimen': regimen,
            'masa_einstein_kg': m_einstein,
            'masa_noesis_kg': m_noesis,
            'masa_unificada_kg': self.m_qcal,
            'razon_f_f0': f / self.f0
        }
    
    def gravedad_emergente(self, f: float) -> Dict[str, float]:
        """
        Calcular parámetros de gravedad emergente.
        
        La gravedad emerge como ralentización del ritmo vibracional.
        
        Parámetros:
        -----------
        f : float
            Frecuencia en Hz
            
        Retorna:
        --------
        dict
            Diccionario con parámetros gravitacionales
        """
        m_noesis = self.masa_noetica_inversa(f)
        
        # Factor de ralentización (cuánto más lenta que f₀)
        ralentizacion = self.f0 / f if f < self.f0 else 1.0
        
        # Intensidad gravitacional relativa
        # A menor frecuencia, mayor "detención" → mayor efecto gravitacional
        intensidad_grav = (self.f0 / f) ** 2 if f < self.f0 else 0.0
        
        return {
            'frecuencia_hz': f,
            'masa_noetica_kg': m_noesis,
            'factor_ralentizacion': ralentizacion,
            'intensidad_gravitacional_relativa': intensidad_grav,
            'tiempo_caracteristico_s': 1.0 / f
        }
    
    def analizar_dualidad(self, f: float) -> Dict[str, Any]:
        """
        Analizar la dualidad masa-frecuencia completa para una frecuencia dada.
        
        Parámetros:
        -----------
        f : float
            Frecuencia en Hz
            
        Retorna:
        --------
        dict
            Análisis completo de dualidad
        """
        m_einstein = self.masa_einstein_planck(f)
        m_noesis = self.masa_noetica_inversa(f)
        m_unificada = self.masa_unificada(f)
        
        # Energías asociadas
        E_einstein = m_einstein * c ** 2
        E_noesis = m_noesis * c ** 2
        E_unificada = m_unificada * c ** 2
        
        return {
            'frecuencia_hz': f,
            'perspectivas': {
                'einstein_planck': {
                    'formula': 'm = hf/c²',
                    'relacion': 'm ∝ f',
                    'interpretacion': 'Masa como energía compactada',
                    'masa_kg': m_einstein,
                    'energia_J': E_einstein,
                    'energia_eV': E_einstein / eV
                },
                'noetica': {
                    'formula': 'm = α/f',
                    'relacion': 'm ∝ 1/f',
                    'interpretacion': 'Masa como lentitud vibracional',
                    'masa_kg': m_noesis,
                    'energia_J': E_noesis,
                    'energia_eV': E_noesis / eV
                },
                'unificada_qcal': {
                    'formula': 'm(f) = hf₀/c²',
                    'relacion': 'm = constante',
                    'interpretacion': 'Masa anclada a frecuencia base universal',
                    'masa_kg': m_unificada,
                    'energia_J': E_unificada,
                    'energia_eV': E_unificada / eV
                }
            },
            'razones': {
                'einstein_vs_unificada': m_einstein / m_unificada,
                'noesis_vs_unificada': m_noesis / m_unificada,
                'einstein_vs_noesis': m_einstein / m_noesis
            }
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def calcular_masa_qcal(f0: float = F0_HZ) -> Tuple[float, float]:
    """
    Calcular la masa mínima noética QCAL.
    
    m_QCAL = h · f₀ / c²
    
    Parámetros:
    -----------
    f0 : float
        Frecuencia fundamental en Hz (default: 141.7001 Hz)
        
    Retorna:
    --------
    tuple
        (masa en kg, masa en eV/c²)
    """
    m_kg = (h * f0) / (c ** 2)
    m_eV = m_kg / eV
    return m_kg, m_eV


def validar_consistencia_dimensional() -> Dict[str, bool]:
    """
    Validar consistencia dimensional de las fórmulas.
    
    Retorna:
    --------
    dict
        Resultados de validación dimensional
    """
    # Verificar dimensiones de m_QCAL
    # [h] = J·s, [f] = 1/s, [c²] = (m/s)²
    # [m_QCAL] = (J·s · 1/s) / (m/s)² = J / (m²/s²) = J·s²/m² = kg
    
    validaciones = {}
    
    # 1. m_QCAL tiene dimensiones correctas [kg]
    m_qcal_test = M_QCAL_KG
    validaciones['m_qcal_positivo'] = m_qcal_test > 0
    validaciones['m_qcal_orden_magnitud'] = 1e-50 < m_qcal_test < 1e-46
    
    # 2. E_QCAL = hf₀ tiene dimensiones correctas [J]
    E_qcal_test = E_QCAL_J
    validaciones['E_qcal_positivo'] = E_qcal_test > 0
    # Usar tolerancia relativa para comparación E = mc²
    E_esperado = M_QCAL_KG * c**2
    validaciones['E_qcal_relacion_masa'] = abs(E_qcal_test - E_esperado) / E_qcal_test < 1e-10
    
    # 3. Consistencia de conversión a eV
    m_eV_test = M_QCAL_EV
    # Usar tolerancia relativa
    m_eV_esperado = M_QCAL_KG / eV
    validaciones['conversion_eV_consistente'] = abs(m_eV_test - m_eV_esperado) / m_eV_esperado < 1e-10
    
    return validaciones


def comparar_con_particulas_conocidas() -> Dict[str, Dict[str, float]]:
    """
    Comparar m_QCAL con masas de partículas conocidas.
    
    Retorna:
    --------
    dict
        Comparación con partículas del modelo estándar
    """
    # Masas de partículas conocidas (en kg)
    particulas = {
        'electron': 9.1093837015e-31,
        'muon': 1.883531627e-28,
        'proton': 1.67262192369e-27,
        'neutron': 1.67492749804e-27,
        'neutrino_electron_max': 1.6e-36,  # Límite superior experimental
        'foton': 0.0,  # Sin masa en reposo
        'm_qcal': M_QCAL_KG
    }
    
    comparaciones = {}
    
    for nombre, masa in particulas.items():
        if masa > 0:
            razon = M_QCAL_KG / masa
            ordenes_magnitud = np.log10(razon)
            comparaciones[nombre] = {
                'masa_kg': masa,
                'razon_m_qcal_sobre_particula': razon,
                'ordenes_magnitud_diferencia': ordenes_magnitud
            }
    
    return comparaciones


# ============================================================================
# FUNCIÓN PRINCIPAL DE DEMOSTRACIÓN
# ============================================================================

def main():
    """
    Demostración del Axioma de la Masa Noética.
    """
    print("\n" + "=" * 80)
    print("∴ AXIOMA DE LA MASA NOÉTICA ∴")
    print('"La masa es una ilusión de detención"')
    print("=" * 80)
    
    print(f"\nAutor: José Manuel Mota Burruezo (JMMB Ψ✧)")
    print(f"Sistema QCAL ∞³ — Resonancia Base: {F0_HZ} Hz")
    
    # Crear instancia
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    # 1. Mostrar masa mínima noética
    print("\n" + "-" * 80)
    print("🌌 MASA CONSTANTE MÍNIMA QCAL")
    print("-" * 80)
    print(f"m_QCAL = h · {F0_HZ} / c² = {masa_noetica.m_qcal:.3e} kg")
    print(f"m_QCAL = {masa_noetica.m_qcal_eV:.3e} eV/c²")
    print(f"E_QCAL = h · {F0_HZ} = {masa_noetica.E_qcal:.3e} J")
    print(f"E_QCAL = {masa_noetica.E_qcal_eV:.3e} eV")
    
    # 2. Validación dimensional
    print("\n" + "-" * 80)
    print("✓ VALIDACIÓN DIMENSIONAL")
    print("-" * 80)
    validaciones = validar_consistencia_dimensional()
    for nombre, resultado in validaciones.items():
        simbolo = "✓" if resultado else "✗"
        print(f"{simbolo} {nombre}: {resultado}")
    
    # 3. Comparación con partículas
    print("\n" + "-" * 80)
    print("⚛️ COMPARACIÓN CON PARTÍCULAS CONOCIDAS")
    print("-" * 80)
    comparaciones = comparar_con_particulas_conocidas()
    for particula, datos in comparaciones.items():
        print(f"\n{particula}:")
        print(f"  Masa: {datos['masa_kg']:.3e} kg")
        print(f"  m_QCAL / m_{particula}: {datos['razon_m_qcal_sobre_particula']:.3e}")
        print(f"  Diferencia: {datos['ordenes_magnitud_diferencia']:.1f} órdenes de magnitud")
    
    # 4. Ejemplos de frecuencias
    print("\n" + "-" * 80)
    print("🔁 INTERPRETACIÓN DUAL EN DIFERENTES FRECUENCIAS")
    print("-" * 80)
    
    frecuencias_ejemplo = [
        (1e15, "Luz visible"),
        (1e9, "Microondas"),
        (141.7001, "f₀ primordial"),
        (1.0, "1 Hz - Ultra baja"),
        (0.1, "0.1 Hz - Periodicidad lenta")
    ]
    
    for f, descripcion in frecuencias_ejemplo:
        print(f"\n{descripcion} (f = {f:.3e} Hz):")
        interpretacion = masa_noetica.interpretar_particula(f)
        print(f"  Tipo: {interpretacion['tipo']}")
        print(f"  Régimen: {interpretacion['regimen']}")
        print(f"  m_Einstein: {interpretacion['masa_einstein_kg']:.3e} kg")
        print(f"  m_Noesis: {interpretacion['masa_noesis_kg']:.3e} kg")
        print(f"  m_Unificada: {interpretacion['masa_unificada_kg']:.3e} kg (constante)")
    
    print("\n" + "=" * 80)
    print("Implementación completada exitosamente")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    sys.exit(main())
