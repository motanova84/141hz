#!/usr/bin/env python3
"""
Módulo de Simetría Discreta para la Teoría Noésica

Este módulo implementa el grupo de simetría discreta G y el potencial
invariante bajo transformaciones de reescalado logarítmico.

Basado en el problema statement:
- Grupo G = {R_Ψ ↦ π^k R_Ψ | k ∈ Z}
- Potencial periódico V(log R_Ψ) con periodo log π
- Análisis variacional de E_vac(R_Ψ)
"""

import numpy as np
from typing import TYPE_CHECKING, List, Tuple, Dict, Optional
import matplotlib.pyplot as plt
from pathlib import Path

if TYPE_CHECKING:
    import sympy

# Get repository root dynamically
REPO_ROOT = Path(__file__).parent.parent.resolve()

from sympy import symbols, diff, sin, cos, log, pi, sqrt, exp, simplify, lambdify
from sympy import Sum, oo, Derivative, solve, series


class GrupoSimetriaDiscreta:
    """
    Representa el grupo de simetría discreta G = {R_Ψ ↦ π^k R_Ψ | k ∈ Z}
    
    Este es un grupo abeliano isomorfo a Z que actúa sobre el radio R_Ψ
    mediante transformaciones multiplicativas por potencias de π.
    """
    
    def __init__(self):
        self.base = np.pi
        
    def transformar(self, R_psi: float, k: int) -> float:
        """
        Aplica la transformación g_k: R_Ψ ↦ π^k R_Ψ
        
        Args:
            R_psi: Radio inicial
            k: Orden de la transformación (entero)
            
        Returns:
            R_psi transformado por g_k
        """
        return self.base**k * R_psi
    
    def es_invariante(self, funcion, R_psi: float, tol: float = 1e-10) -> bool:
        """
        Verifica si una función es invariante bajo el grupo G
        
        Args:
            funcion: Función callable que toma R_psi
            R_psi: Punto de evaluación
            tol: Tolerancia para la comparación
            
        Returns:
            True si f(π^k R_Ψ) = f(R_Ψ) para varios k
        """
        valor_base = funcion(R_psi)
        
        # Verificar para varios valores de k
        for k in range(-3, 4):
            R_transformado = self.transformar(R_psi, k)
            valor_transformado = funcion(R_transformado)
            
            if abs(valor_transformado - valor_base) > tol:
                return False
                
        return True
    
    def periodo_logaritmico(self) -> float:
        """Retorna el periodo logarítmico log π"""
        return np.log(self.base)


class PotencialInvarianteG:
    """
    Construye el potencial más general invariante bajo el grupo G.
    
    El potencial debe ser periódico en log R_Ψ con periodo log π:
    V(log R_Ψ) = Σ_{m=0}^∞ [a_m cos(2πm log R_Ψ / log π) + b_m sin(2πm log R_Ψ / log π)]
    
    El modo fundamental (m=1) corresponde a A(R_Ψ) = sin²(log R_Ψ / log π)
    """
    
    def __init__(self, n_armonicos: int = 5):
        """
        Args:
            n_armonicos: Número de armónicos a incluir en la expansión de Fourier
        """
        self.n_armonicos = n_armonicos
        self.coeficientes_a = {}  # Coeficientes de coseno
        self.coeficientes_b = {}  # Coeficientes de seno
        
        # Definir símbolo simbólico
        self.R = symbols('R', positive=True, real=True)
        
    def potencial_simbolico(self, incluir_armonicos: bool = True) -> 'sympy.Expr':
        """
        Retorna la expresión simbólica del potencial V(log R_Ψ)
        
        Args:
            incluir_armonicos: Si True, incluye todos los armónicos; si False, solo m=1
            
        Returns:
            Expresión simbólica de SymPy
        """
        V = 0
        
        # Definir coeficientes simbólicos
        max_m = self.n_armonicos if incluir_armonicos else 1
        
        for m in range(1, max_m + 1):
            a_m = symbols(f'a_{m}', real=True)
            b_m = symbols(f'b_{m}', real=True)
            
            # Argumento: 2πm log R / log π
            argumento = 2 * pi * m * log(self.R) / log(pi)
            
            V += a_m * cos(argumento) + b_m * sin(argumento)
            
        return V
    
    def modo_fundamental(self) -> 'sympy.Expr':
        """
        Retorna el modo fundamental (m=1) que corresponde a A(R_Ψ)
        
        Para el término sin²(log R / log π), usamos:
        sin²(x) = (1 - cos(2x))/2
        
        Returns:
            Expresión del modo fundamental
        """
        # A(R_Ψ) = sin²(log R_Ψ / log π)
        argumento = log(self.R) / log(pi)
        return sin(argumento)**2
    
    def evaluar_modo_fundamental(self, R_valores: np.ndarray) -> np.ndarray:
        """
        Evalúa el modo fundamental A(R_Ψ) = sin²(log R / log π)
        
        Args:
            R_valores: Array de valores de R_Ψ
            
        Returns:
            Array con valores de A(R_Ψ)
        """
        log_R = np.log(R_valores)
        log_pi = np.log(np.pi)
        return np.sin(log_R / log_pi)**2
    
    def frecuencias_armonicas(self, f0: float = 141.7001) -> List[float]:
        """
        Calcula las frecuencias de los armónicos superiores
        
        Predicción: f_n = f_0 / (π^(2n)) para n = 1, 2, 3, ...
        
        Args:
            f0: Frecuencia fundamental (Hz)
            
        Returns:
            Lista de frecuencias de armónicos superiores
        """
        frecuencias = [f0]
        
        for n in range(1, self.n_armonicos):
            f_n = f0 / (np.pi**(2*n))
            frecuencias.append(f_n)
            
        return frecuencias


class EnergiaVacio:
    """
    Implementa la energía de vacío completa:
    
    E_vac(R_Ψ) = α/R_Ψ^4 + β·ζ'(1/2)/R_Ψ^2 + γ·Λ²·R_Ψ² + δ·A(R_Ψ)
    
    donde A(R_Ψ) = sin²(log R_Ψ / log π) es el término de simetría discreta.
    """
    
    def __init__(self, alpha: float, beta: float, gamma: float, delta: float,
                 zeta_prime_half: float = -0.9189385332, Lambda: float = 1.0):
        """
        Args:
            alpha: Coeficiente del término R^(-4)
            beta: Coeficiente del término de función zeta
            gamma: Coeficiente del término cosmológico
            delta: Coeficiente del término de simetría discreta
            zeta_prime_half: Valor de ζ'(1/2) ≈ -0.918938533
            Lambda: Constante cosmológica
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.zeta_prime_half = zeta_prime_half
        self.Lambda = Lambda
        
        # Símbolos de SymPy
        self.R = symbols('R', positive=True, real=True)
        
        # Crear potencial invariante
        self.potencial = PotencialInvarianteG()
        
    def energia_simbolica(self) -> 'sympy.Expr':
        """
        Retorna la expresión simbólica completa de E_vac(R)
        
        Returns:
            Expresión de SymPy para la energía de vacío
        """
        R = self.R
        
        # Términos de la energía
        termino_1 = self.alpha / R**4
        termino_2 = self.beta * self.zeta_prime_half / R**2
        termino_3 = self.gamma * self.Lambda**2 * R**2
        termino_4 = self.delta * self.potencial.modo_fundamental()
        
        return termino_1 + termino_2 + termino_3 + termino_4
    
    def evaluar(self, R_valores: np.ndarray) -> np.ndarray:
        """
        Evalúa E_vac(R) para un array de valores de R
        
        Args:
            R_valores: Array de valores de R_Ψ
            
        Returns:
            Array con valores de E_vac
        """
        # Evaluar cada término
        termino_1 = self.alpha / R_valores**4
        termino_2 = self.beta * self.zeta_prime_half / R_valores**2
        termino_3 = self.gamma * self.Lambda**2 * R_valores**2
        termino_4 = self.delta * self.potencial.evaluar_modo_fundamental(R_valores)
        
        return termino_1 + termino_2 + termino_3 + termino_4
    
    def derivada_simbolica(self) -> 'sympy.Expr':
        """
        Calcula ∂E/∂R simbólicamente
        
        Returns:
            Expresión de SymPy para dE/dR
        """
        E = self.energia_simbolica()
        return diff(E, self.R)
    
    def segunda_derivada_simbolica(self) -> 'sympy.Expr':
        """
        Calcula ∂²E/∂R² simbólicamente
        
        Returns:
            Expresión de SymPy para d²E/dR²
        """
        dE = self.derivada_simbolica()
        return diff(dE, self.R)
    
    def encontrar_minimos(self, R_min: float = 0.1, R_max: float = 100.0, 
                          n_celdas: int = 5) -> List[Tuple[float, float]]:
        """
        Encuentra los mínimos de E_vac en varias celdas [π^n, π^(n+1)]
        
        Args:
            R_min: Valor mínimo de R para búsqueda
            R_max: Valor máximo de R para búsqueda  
            n_celdas: Número de celdas a explorar
            
        Returns:
            Lista de tuplas (R_min, E_min) con las posiciones y valores de mínimos
        """
        from scipy.optimize import minimize_scalar
        
        minimos = []
        
        # Determinar rango de celdas en términos de log_π(R)
        log_pi = np.log(np.pi)
        n_start = int(np.floor(np.log(R_min) / log_pi))
        n_end = int(np.ceil(np.log(R_max) / log_pi))
        
        # Limitar a n_celdas
        n_end = min(n_end, n_start + n_celdas)
        
        for n in range(n_start, n_end):
            # Límites de la celda [π^n, π^(n+1)]
            R_inf = np.pi**n
            R_sup = np.pi**(n+1)
            
            # Asegurar que está dentro del rango solicitado
            R_inf = max(R_inf, R_min)
            R_sup = min(R_sup, R_max)
            
            if R_inf >= R_sup:
                continue
            
            # Minimizar en esta celda
            resultado = minimize_scalar(
                self.evaluar,
                bounds=(R_inf, R_sup),
                method='bounded'
            )
            
            if resultado.success:
                minimos.append((resultado.x, resultado.fun))
        
        return minimos
    
    def es_coerciva(self, R_test: np.ndarray = None) -> bool:
        """
        Verifica si E_vac es coerciva (E → ∞ cuando R → 0 o R → ∞)
        
        Args:
            R_test: Valores de R para test (opcional)
            
        Returns:
            True si la función es coerciva
        """
        if R_test is None:
            R_test = np.logspace(-2, 3, 1000)
        
        E_values = self.evaluar(R_test)
        
        # Verificar comportamiento en los extremos
        # Para R → 0: debe dominar α/R^4 → ∞
        E_pequeno = self.evaluar(np.array([1e-3, 1e-4]))
        
        # Para R → ∞: debe dominar γΛ²R² → ∞
        E_grande = self.evaluar(np.array([1e3, 1e4]))
        
        # Coercividad: energía crece en ambos extremos
        return (E_pequeno[1] > E_pequeno[0] and 
                E_grande[1] > E_grande[0])
    
    def estabilidad_minimo(self, R_min: float) -> Dict[str, float]:
        """
        Analiza la estabilidad de un mínimo verificando que d²E/dR² > 0
        
        Args:
            R_min: Posición del mínimo
            
        Returns:
            Diccionario con información sobre estabilidad
        """
        # Evaluar segunda derivada numéricamente
        h = 1e-6
        R_array = np.array([R_min - h, R_min, R_min + h])
        E_array = self.evaluar(R_array)
        
        # Aproximación de segunda derivada por diferencias finitas
        d2E_dR2 = (E_array[2] - 2*E_array[1] + E_array[0]) / h**2
        
        # Evaluar primera derivada para confirmar que es ~0
        dE_dR = (E_array[2] - E_array[0]) / (2*h)
        
        return {
            'R_min': R_min,
            'E_min': E_array[1],
            'dE_dR': dE_dR,
            'd2E_dR2': d2E_dR2,
            'estable': d2E_dR2 > 0,
            'es_minimo': abs(dE_dR) < 1e-3 and d2E_dR2 > 0
        }


def generar_graficos(energia: EnergiaVacio, 
                     R_min: float = 0.1, R_max: float = 100.0,
                     output_file: str = None):
    """
    Genera visualizaciones de E(R) y sus propiedades
    
    Args:
        energia: Instancia de EnergiaVacio
        R_min: Valor mínimo de R para graficar
        R_max: Valor máximo de R para graficar
        output_file: Archivo de salida (opcional)
    """
    # Crear array de valores de R
    R_valores = np.logspace(np.log10(R_min), np.log10(R_max), 1000)
    E_valores = energia.evaluar(R_valores)
    
    # Encontrar mínimos
    minimos = energia.encontrar_minimos(R_min, R_max)
    
    # Crear figura con subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gráfico 1: E(R) completa
    ax1 = axes[0, 0]
    ax1.plot(R_valores, E_valores, 'b-', linewidth=2, label='$E_{vac}(R_\\Psi)$')
    
    # Marcar mínimos
    if minimos:
        R_mins = [m[0] for m in minimos]
        E_mins = [m[1] for m in minimos]
        ax1.plot(R_mins, E_mins, 'ro', markersize=8, label='Mínimos')
    
    ax1.set_xlabel('$R_\\Psi$', fontsize=12)
    ax1.set_ylabel('$E_{vac}$', fontsize=12)
    ax1.set_title('Energía de Vacío Total', fontsize=14, fontweight='bold')
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico 2: Contribución de A(R_Ψ)
    ax2 = axes[0, 1]
    A_valores = energia.potencial.evaluar_modo_fundamental(R_valores)
    ax2.plot(R_valores, A_valores, 'g-', linewidth=2)
    ax2.set_xlabel('$R_\\Psi$', fontsize=12)
    ax2.set_ylabel('$A(R_\\Psi) = \\sin^2(\\log R_\\Psi / \\log \\pi)$', fontsize=10)
    ax2.set_title('Término de Simetría Discreta (Modo Fundamental)', fontsize=12, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    
    # Marcar periodo
    for n in range(-2, 5):
        R_periodo = np.pi**n
        if R_min <= R_periodo <= R_max:
            ax2.axvline(R_periodo, color='r', linestyle='--', alpha=0.3, linewidth=1)
    
    # Gráfico 3: Términos individuales
    ax3 = axes[1, 0]
    term1 = energia.alpha / R_valores**4
    term2 = energia.beta * energia.zeta_prime_half / R_valores**2
    term3 = energia.gamma * energia.Lambda**2 * R_valores**2
    term4 = energia.delta * A_valores
    
    ax3.plot(R_valores, term1, label="$\\alpha/R^4$", alpha=0.7)
    ax3.plot(R_valores, np.abs(term2), label="$|\\beta\\zeta'(1/2)/R^2|$", alpha=0.7)
    ax3.plot(R_valores, term3, label="$\\gamma\\Lambda^2 R^2$", alpha=0.7)
    ax3.plot(R_valores, np.abs(term4), label="$|\\delta A(R)|$", alpha=0.7)
    
    ax3.set_xlabel('$R_\\Psi$', fontsize=12)
    ax3.set_ylabel('Contribución de energía', fontsize=12)
    ax3.set_title('Contribuciones Individuales', fontsize=12, fontweight='bold')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=9)
    
    # Gráfico 4: Predicción de frecuencias armónicas
    ax4 = axes[1, 1]
    frecuencias = energia.potencial.frecuencias_armonicas()
    n_armonicos = len(frecuencias)
    
    ax4.bar(range(n_armonicos), frecuencias, color='purple', alpha=0.7)
    ax4.set_xlabel('Orden del armónico n', fontsize=12)
    ax4.set_ylabel('Frecuencia (Hz)', fontsize=12)
    ax4.set_title('Predicción: Frecuencias Armónicas', fontsize=12, fontweight='bold')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Etiquetar frecuencias
    for i, freq in enumerate(frecuencias):
        ax4.text(i, freq, f'{freq:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado: {output_file}")
    else:
        plt.show()
    
    return fig


def ejemplo_uso():
    """
    Ejemplo de uso del módulo de simetría discreta
    """
    print("=" * 70)
    print("ANÁLISIS DE SIMETRÍA DISCRETA - TEORÍA NOÉSICA")
    print("=" * 70)
    
    # 1. Verificar grupo de simetría
    print("\n1. GRUPO DE SIMETRÍA DISCRETA G")
    print("-" * 70)
    grupo = GrupoSimetriaDiscreta()
    print(f"   Grupo: G = {{R_Ψ ↦ π^k R_Ψ | k ∈ Z}}")
    print(f"   Periodo logarítmico: log π = {grupo.periodo_logaritmico():.6f}")
    
    # Verificar invariancia de A(R)
    potencial = PotencialInvarianteG()
    R_test = 5.0
    es_inv = grupo.es_invariante(potencial.evaluar_modo_fundamental, R_test)
    print(f"   A(R) es invariante bajo G: {es_inv}")
    
    # 2. Modo fundamental
    print("\n2. MODO FUNDAMENTAL")
    print("-" * 70)
    print("   A(R_Ψ) = sin²(log R_Ψ / log π)")
    print(f"   Evaluado en R = π: A(π) = {potencial.evaluar_modo_fundamental(np.array([np.pi]))[0]:.6f}")
    print(f"   Evaluado en R = π²: A(π²) = {potencial.evaluar_modo_fundamental(np.array([np.pi**2]))[0]:.6f}")
    
    # 3. Predicción de frecuencias armónicas
    print("\n3. PREDICCIÓN DE FRECUENCIAS ARMÓNICAS")
    print("-" * 70)
    frecuencias = potencial.frecuencias_armonicas()
    print(f"   f₀ = {frecuencias[0]:.4f} Hz (fundamental)")
    for i, freq in enumerate(frecuencias[1:], 1):
        print(f"   f_{i} = {freq:.4f} Hz (armónico superior)")
    
    # 4. Energía de vacío
    print("\n4. ENERGÍA DE VACÍO E_vac(R_Ψ)")
    print("-" * 70)
    
    # Parámetros típicos
    alpha = 1.0
    beta = -0.5
    gamma = 0.1
    delta = 0.5
    
    energia = EnergiaVacio(alpha, beta, gamma, delta)
    print(f"   α = {alpha}, β = {beta}, γ = {gamma}, δ = {delta}")
    print(f"   ζ'(1/2) = {energia.zeta_prime_half:.6f}")
    print(f"   Λ = {energia.Lambda}")
    
    # Verificar coercividad
    print("\n5. PROPIEDADES MATEMÁTICAS")
    print("-" * 70)
    coerciva = energia.es_coerciva()
    print(f"   E_vac es coerciva: {coerciva}")
    
    # Encontrar mínimos
    print("\n6. BÚSQUEDA DE MÍNIMOS")
    print("-" * 70)
    minimos = energia.encontrar_minimos(R_min=0.5, R_max=50.0, n_celdas=4)
    print(f"   Encontrados {len(minimos)} mínimos:")
    
    for i, (R_min, E_min) in enumerate(minimos, 1):
        estab = energia.estabilidad_minimo(R_min)
        print(f"\n   Mínimo {i}:")
        print(f"     R_min = {R_min:.4f}")
        print(f"     E_min = {E_min:.6f}")
        print(f"     d²E/dR² = {estab['d2E_dR2']:.6f}")
        print(f"     Estable: {estab['estable']}")
    
    print("\n" + "=" * 70)
    print("GENERANDO VISUALIZACIONES...")
    print("=" * 70)
    
    # Generar gráficos
    import os
    results_dir = REPO_ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    output_file = results_dir / "simetria_discreta_analisis.png"
    
    generar_graficos(energia, R_min=0.5, R_max=50.0, output_file=str(output_file))
    
    return energia, minimos


if __name__ == "__main__":
    energia, minimos = ejemplo_uso()
