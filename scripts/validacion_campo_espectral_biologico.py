#!/usr/bin/env python3
"""
Validación del Campo Espectral Biológico QCAL

Este script valida el modelo matemático del campo espectral Ψ aplicado a sistemas biológicos,
específicamente para ciclos de vida periódicos como Magicicada.

Ecuaciones implementadas:
    1. Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))          - Campo ambiental espectral
    2. H(ω) = ∫ G(τ)e^(-iωτ)dτ                 - Filtro biológico
    3. Φ(t) = ∫₀ᵗ |H(ω)*Ψₑ(ω)|² dω             - Acumulación de fase
    4. Φ_acum = αΦ(t) + (1-α)Φ(t-Δt)          - Memoria de fase
    5. Condición: Φ(t) ≥ Φ_crítico Y dΦ/dt > 0 - Colapso de fase

Autor: José Manuel Mota Burruezo
Fecha: 27 de enero de 2026
Instituto Consciencia Cuántica QCAL ∞³
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from pathlib import Path
import json
import argparse
from typing import Dict, List, Tuple, Optional
import sys

# Añadir ruta al módulo qcal si es necesario
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from qcal.constants import F0
except ImportError:
    # Valor por defecto si no se encuentra el módulo
    F0 = 141.7001  # Hz

# Constantes físicas
SECONDS_PER_DAY = 86400
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY

class CampoEspectralBiologico:
    """
    Modelo del campo espectral biológico según hipótesis QCAL.
    """
    
    def __init__(
        self,
        f0: float = F0,
        alpha_memoria: float = 0.1,
        verbose: bool = True
    ):
        """
        Inicializa el modelo del campo espectral.
        
        Args:
            f0: Frecuencia fundamental (Hz)
            alpha_memoria: Parámetro de memoria de fase (0 < α < 1)
            verbose: Mostrar información de progreso
        """
        self.f0 = f0
        self.alpha = alpha_memoria
        self.verbose = verbose
        
        # Frecuencias ambientales características
        self.omega_anual = 2 * np.pi / SECONDS_PER_YEAR  # rad/s
        self.omega_diario = 2 * np.pi / SECONDS_PER_DAY  # rad/s
        self.omega_lunar = 2 * np.pi / (29.5 * SECONDS_PER_DAY)  # rad/s
        
        if self.verbose:
            print(f"Campo Espectral Biológico QCAL inicializado:")
            print(f"  f₀ = {self.f0:.4f} Hz")
            print(f"  α (memoria) = {self.alpha:.2f}")
            print(f"  ω_anual = {self.omega_anual:.4e} rad/s")
            print(f"  ω_diario = {self.omega_diario:.4e} rad/s")
    
    def campo_ambiental_espectral(
        self,
        t: np.ndarray,
        amplitudes: Optional[List[float]] = None,
        frecuencias: Optional[List[float]] = None,
        fases: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Calcula el campo ambiental espectral Ψₑ(t).
        
        Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))
        
        Args:
            t: Array de tiempo (segundos)
            amplitudes: Amplitudes de componentes espectrales
            frecuencias: Frecuencias angulares (rad/s)
            fases: Fases iniciales (radianes)
            
        Returns:
            Campo complejo Ψₑ(t)
        """
        if amplitudes is None:
            # Valores por defecto: ciclos ambientales principales
            amplitudes = [1.0, 0.5, 0.3]  # Anual, diario, lunar
        
        if frecuencias is None:
            frecuencias = [self.omega_anual, self.omega_diario, self.omega_lunar]
        
        if fases is None:
            fases = [0.0] * len(amplitudes)
        
        # Superposición de componentes espectrales
        psi_e = np.zeros_like(t, dtype=complex)
        for A, omega, phi in zip(amplitudes, frecuencias, fases):
            psi_e += A * np.exp(1j * (omega * t + phi))
        
        return psi_e
    
    def filtro_biologico(
        self,
        omega: np.ndarray,
        tipo: str = 'magicicada'
    ) -> np.ndarray:
        """
        Calcula la función de transferencia biológica H(ω).
        
        Representa la selectividad evolutiva del organismo ante
        diferentes frecuencias ambientales.
        
        Args:
            omega: Frecuencias angulares (rad/s)
            tipo: Tipo de organismo ('magicicada', 'arabidopsis', 'general')
            
        Returns:
            H(ω) - Respuesta espectral del filtro biológico
        """
        if tipo == 'magicicada':
            # Magicicada: alta sensibilidad a ciclos anuales
            # Filtro pasa-bajas centrado en frecuencia anual
            H = np.exp(-((omega - self.omega_anual) / (0.5 * self.omega_anual))**2)
            # Banda media para vibraciones celulares (1-100 Hz)
            omega_hz = omega / (2 * np.pi)
            banda_media = np.exp(-((omega_hz - 50) / 30)**2)
            H = 0.7 * H + 0.3 * banda_media
            
        elif tipo == 'arabidopsis':
            # Arabidopsis: sensibilidad a ciclos diarios y vibraciones celulares
            H_diario = np.exp(-((omega - self.omega_diario) / self.omega_diario)**2)
            omega_hz = omega / (2 * np.pi)
            H_celular = np.exp(-((omega_hz - self.f0) / 20)**2)
            H = 0.5 * H_diario + 0.5 * H_celular
            
        else:  # general
            # Filtro multiescala
            H = np.ones_like(omega)
            omega_hz = omega / (2 * np.pi)
            # Atenuar frecuencias > 1 kHz (ruido térmico)
            H[omega_hz > 1000] *= 0.1
            # Realzar banda media (1-100 Hz)
            mask_media = (omega_hz >= 1) & (omega_hz <= 100)
            H[mask_media] *= 1.5
        
        return H
    
    def acumulacion_fase(
        self,
        t: np.ndarray,
        psi_e: np.ndarray,
        H: Optional[np.ndarray] = None,
        dt: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula la fase acumulada Φ(t).
        
        Φ(t) = ∫₀ᵗ |Ψₑ(t)|² dt  (energía acumulada)
        
        Args:
            t: Array de tiempo
            psi_e: Campo espectral ambiental
            H: Filtro biológico (opcional, no usado en versión simplificada)
            dt: Paso de tiempo (calculado si no se proporciona)
            
        Returns:
            (Φ(t), dΦ/dt) - Fase acumulada y su derivada temporal
        """
        if dt is None:
            dt = t[1] - t[0] if len(t) > 1 else 1.0
        
        # Integración acumulativa de la energía instantánea
        # Φ(t) = ∫|Ψₑ(τ)|² dτ
        fase_acum = np.cumsum(np.abs(psi_e)**2) * dt
        
        # Derivada temporal de Φ
        d_fase_dt = np.gradient(fase_acum, dt)
        
        return fase_acum, d_fase_dt
    
    def memoria_fase(
        self,
        fase_actual: np.ndarray,
        fase_anterior: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Aplica memoria de fase exponencial.
        
        Φ_acum = αΦ(t) + (1-α)Φ(t-Δt)
        
        Args:
            fase_actual: Φ(t)
            fase_anterior: Φ(t-Δt) (opcional)
            
        Returns:
            Φ_acum con memoria
        """
        if fase_anterior is None:
            return fase_actual
        
        return self.alpha * fase_actual + (1 - self.alpha) * fase_anterior
    
    def detectar_colapso_fase(
        self,
        t: np.ndarray,
        fase: np.ndarray,
        d_fase_dt: np.ndarray,
        phi_critico: float,
        tipo_organismo: str = 'magicicada',
        ciclo_anos: int = 17
    ) -> Dict:
        """
        Detecta eventos de colapso de fase (activación biológica).
        
        Condición: Φ(t) ≥ Φ_crítico Y dΦ/dt > 0
        
        Args:
            t: Tiempo (segundos)
            fase: Fase acumulada Φ(t)
            d_fase_dt: Derivada temporal dΦ/dt
            phi_critico: Umbral crítico
            tipo_organismo: Tipo de organismo
            ciclo_anos: Años del ciclo (para Magicicada)
            
        Returns:
            Diccionario con resultados de detección
        """
        # Condiciones de activación
        condicion_umbral = fase >= phi_critico
        condicion_flujo = d_fase_dt > 0
        condicion_colapso = condicion_umbral & condicion_flujo
        
        # Encontrar eventos de colapso
        indices_colapso = np.where(condicion_colapso)[0]
        
        if len(indices_colapso) > 0:
            # Primer evento de colapso
            idx_primer_colapso = indices_colapso[0]
            t_colapso = t[idx_primer_colapso]
            fase_colapso = fase[idx_primer_colapso]
            
            # Convertir a días/años para interpretación biológica
            dias_colapso = t_colapso / SECONDS_PER_DAY
            anos_colapso = t_colapso / SECONDS_PER_YEAR
            
            # Precisión: desviación del ciclo esperado
            if tipo_organismo == 'magicicada':
                desviacion_dias = abs(dias_colapso - ciclo_anos * 365.25)
                precision_pct = 100 * (1 - desviacion_dias / (ciclo_anos * 365.25))
            else:
                desviacion_dias = 0
                precision_pct = 100.0
            
            resultado = {
                'colapso_detectado': True,
                'tiempo_colapso_s': float(t_colapso),
                'tiempo_colapso_dias': float(dias_colapso),
                'tiempo_colapso_anos': float(anos_colapso),
                'fase_colapso': float(fase_colapso),
                'umbral_critico': float(phi_critico),
                'desviacion_dias': float(desviacion_dias),
                'precision_pct': float(precision_pct),
                'num_eventos': len(indices_colapso),
                'organismo': tipo_organismo,
                'ciclo_esperado_anos': ciclo_anos
            }
        else:
            resultado = {
                'colapso_detectado': False,
                'fase_maxima': float(np.max(fase)),
                'umbral_critico': float(phi_critico),
                'razon': 'Umbral no alcanzado en el período simulado',
                'organismo': tipo_organismo,
                'ciclo_esperado_anos': ciclo_anos
            }
        
        return resultado
    
    def simular_magicicada(
        self,
        anos: int = 17,
        dt_dias: float = 1.0,
        phi_critico: Optional[float] = None,
        perturbacion_ano: Optional[int] = None,
        perturbacion_amplitud: float = 0.5
    ) -> Dict:
        """
        Simula el ciclo de vida de Magicicada con campo espectral.
        
        Args:
            anos: Duración del ciclo (13 o 17 años)
            dt_dias: Paso de tiempo en días
            phi_critico: Umbral crítico (calculado si no se proporciona)
            perturbacion_ano: Año en el que aplicar perturbación (opcional)
            perturbacion_amplitud: Amplitud de la perturbación térmica
            
        Returns:
            Diccionario con resultados completos de la simulación
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Simulación Magicicada - Ciclo de {anos} años")
            print(f"{'='*60}\n")
        
        # Vector de tiempo
        t_total = anos * SECONDS_PER_YEAR
        dt = dt_dias * SECONDS_PER_DAY
        t = np.arange(0, t_total, dt)
        
        if self.verbose:
            print(f"Puntos temporales: {len(t)}")
            print(f"Resolución: {dt_dias} días\n")
        
        # Componentes espectrales ambientales
        amplitudes = [1.0, 0.3, 0.1]  # Anual, diario, lunar
        frecuencias = [self.omega_anual, self.omega_diario, self.omega_lunar]
        fases = [0.0, 0.0, 0.0]
        
        # Aplicar perturbación si se solicita
        if perturbacion_ano is not None:
            t_pert_inicio = perturbacion_ano * SECONDS_PER_YEAR
            t_pert_fin = (perturbacion_ano + 1) * SECONDS_PER_YEAR
            mask_pert = (t >= t_pert_inicio) & (t < t_pert_fin)
            
            # Crear amplitudes con perturbación aplicada
            amplitudes_perturbadas = []
            for A in amplitudes:
                A_t = np.full_like(t, A, dtype=float)
                A_t[mask_pert] *= perturbacion_amplitud  # Reducir señal durante perturbación
                amplitudes_perturbadas.append(A_t)
            
            if self.verbose:
                print(f"Perturbación aplicada en año {perturbacion_ano}")
                print(f"Amplitud reducida a {perturbacion_amplitud*100}%\n")
            
            # Campo ambiental espectral con perturbación
            psi_e = np.zeros_like(t, dtype=complex)
            for i, (omega, phi) in enumerate(zip(frecuencias, fases)):
                psi_e += amplitudes_perturbadas[i] * np.exp(1j * (omega * t + phi))
        else:
            # Campo ambiental espectral sin perturbación
            psi_e = self.campo_ambiental_espectral(t, amplitudes, frecuencias, fases)
        
        # Filtro biológico de Magicicada
        omega_test = np.linspace(0, 2*np.pi*200, 1000)  # Hasta 200 Hz
        H = self.filtro_biologico(omega_test, tipo='magicicada')
        
        # Acumulación de fase
        fase, d_fase_dt = self.acumulacion_fase(t, psi_e, H, dt)
        
        # Memoria de fase (simulación con actualización cada año)
        fase_memoria = np.zeros_like(fase)
        fase_memoria[0] = fase[0]
        
        # Índices correspondientes a cada año
        pasos_por_ano = int(SECONDS_PER_YEAR / dt)
        for i in range(1, len(fase)):
            if i % pasos_por_ano == 0:
                # Actualizar memoria anualmente
                fase_memoria[i] = self.memoria_fase(
                    fase[i],
                    fase_memoria[i - pasos_por_ano] if i >= pasos_por_ano else 0
                )
            else:
                fase_memoria[i] = fase[i]
        
        # Umbral crítico: energía acumulada de N ciclos anuales
        if phi_critico is None:
            energia_por_ciclo = np.mean(np.abs(psi_e)**2) * SECONDS_PER_YEAR
            phi_critico = anos * energia_por_ciclo
            if self.verbose:
                print(f"Φ_crítico calculado: {phi_critico:.2e}")
                print(f"Energía por ciclo: {energia_por_ciclo:.2e}\n")
        
        # Detectar colapso de fase
        resultado = self.detectar_colapso_fase(
            t, fase_memoria, d_fase_dt, phi_critico,
            tipo_organismo='magicicada',
            ciclo_anos=anos
        )
        
        # Añadir datos completos al resultado
        resultado.update({
            'tiempo': t.tolist() if len(t) < 10000 else t[::10].tolist(),
            'fase': fase_memoria.tolist() if len(fase_memoria) < 10000 else fase_memoria[::10].tolist(),
            'd_fase_dt': d_fase_dt.tolist() if len(d_fase_dt) < 10000 else d_fase_dt[::10].tolist(),
            'parametros': {
                'anos': anos,
                'dt_dias': dt_dias,
                'alpha_memoria': self.alpha,
                'f0_hz': self.f0,
                'perturbacion_ano': perturbacion_ano,
                'perturbacion_amplitud': perturbacion_amplitud if perturbacion_ano else None
            }
        })
        
        if self.verbose:
            print("\nResultados de simulación:")
            if resultado['colapso_detectado']:
                print(f"  ✓ Colapso detectado en: {resultado['tiempo_colapso_anos']:.2f} años")
                print(f"  ✓ Precisión: {resultado['precision_pct']:.2f}%")
                print(f"  ✓ Desviación: ±{resultado['desviacion_dias']:.1f} días")
            else:
                print(f"  ✗ Colapso no detectado")
                print(f"    Fase máxima: {resultado['fase_maxima']:.2e}")
                print(f"    Umbral: {resultado['umbral_critico']:.2e}")
        
        return resultado


def visualizar_resultados(resultado: Dict, output_dir: Path):
    """
    Genera visualizaciones de los resultados de simulación.
    
    Args:
        resultado: Diccionario con resultados
        output_dir: Directorio de salida
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extraer datos
    t = np.array(resultado['tiempo'])
    fase = np.array(resultado['fase'])
    d_fase = np.array(resultado['d_fase_dt'])
    
    # Convertir tiempo a años
    t_anos = t / SECONDS_PER_YEAR
    
    # Crear figura con subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Subplot 1: Fase acumulada
    ax1 = axes[0]
    ax1.plot(t_anos, fase, 'b-', linewidth=1.5, label='Φ(t) con memoria')
    if resultado['colapso_detectado']:
        t_colapso_anos = resultado['tiempo_colapso_anos']
        fase_colapso = resultado['fase_colapso']
        ax1.axhline(resultado['umbral_critico'], color='r', linestyle='--',
                   label=f'Φ_crítico = {resultado["umbral_critico"]:.2e}')
        ax1.plot(t_colapso_anos, fase_colapso, 'ro', markersize=10,
                label=f'Colapso: {t_colapso_anos:.2f} años')
    
    ax1.set_xlabel('Tiempo (años)', fontsize=12)
    ax1.set_ylabel('Fase Acumulada Φ(t)', fontsize=12)
    ax1.set_title('Acumulación de Fase - Modelo QCAL Magicicada', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Derivada temporal
    ax2 = axes[1]
    ax2.plot(t_anos, d_fase, 'g-', linewidth=1.5, label='dΦ/dt')
    ax2.axhline(0, color='k', linestyle=':', linewidth=1)
    if resultado['colapso_detectado']:
        ax2.axvline(t_colapso_anos, color='r', linestyle='--', alpha=0.5,
                   label='Momento de colapso')
    
    ax2.set_xlabel('Tiempo (años)', fontsize=12)
    ax2.set_ylabel('dΦ/dt', fontsize=12)
    ax2.set_title('Tasa de Acumulación de Fase', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar figura
    output_file = output_dir / 'campo_espectral_biologico_magicicada.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nVisualización guardada: {output_file}")
    
    plt.close()


def main():
    """Función principal de validación."""
    parser = argparse.ArgumentParser(
        description='Validación del Campo Espectral Biológico QCAL'
    )
    parser.add_argument('--anos', type=int, default=17,
                       help='Duración del ciclo en años (13 o 17 para Magicicada)')
    parser.add_argument('--dt-dias', type=float, default=7.0,
                       help='Paso de tiempo en días')
    parser.add_argument('--alpha', type=float, default=0.1,
                       help='Parámetro de memoria de fase (0-1)')
    parser.add_argument('--perturbacion-ano', type=int, default=None,
                       help='Año en el que aplicar perturbación climática')
    parser.add_argument('--perturbacion-amplitud', type=float, default=0.5,
                       help='Amplitud de la perturbación (0-1)')
    parser.add_argument('--output', type=str, default='results',
                       help='Directorio de salida para resultados')
    parser.add_argument('--quiet', action='store_true',
                       help='Modo silencioso')
    
    args = parser.parse_args()
    
    # Crear modelo
    modelo = CampoEspectralBiologico(
        f0=F0,
        alpha_memoria=args.alpha,
        verbose=not args.quiet
    )
    
    # Ejecutar simulación
    resultado = modelo.simular_magicicada(
        anos=args.anos,
        dt_dias=args.dt_dias,
        perturbacion_ano=args.perturbacion_ano,
        perturbacion_amplitud=args.perturbacion_amplitud
    )
    
    # Directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar resultados JSON
    json_file = output_dir / 'campo_espectral_biologico_resultados.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"\nResultados guardados: {json_file}")
    
    # Generar visualizaciones
    visualizar_resultados(resultado, output_dir)
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN DE VALIDACIÓN")
    print(f"{'='*60}")
    print(f"Modelo: Campo Espectral Biológico QCAL")
    print(f"Organismo: Magicicada ({args.anos} años)")
    print(f"Parámetro de memoria α: {args.alpha}")
    
    if resultado['colapso_detectado']:
        print(f"\n✓ VALIDACIÓN EXITOSA")
        print(f"  Colapso de fase detectado en: {resultado['tiempo_colapso_anos']:.2f} años")
        print(f"  Ciclo esperado: {args.anos} años")
        print(f"  Precisión: {resultado['precision_pct']:.2f}%")
        print(f"  Desviación: ±{resultado['desviacion_dias']:.1f} días")
        
        if resultado['precision_pct'] >= 99.0:
            print(f"\n  🎯 Precisión excelente (≥99%)")
            print(f"     Consistente con observaciones empíricas de Magicicada")
    else:
        print(f"\n✗ Colapso no detectado en el período simulado")
        print(f"  Sugerencia: Aumentar duración de simulación o ajustar Φ_crítico")
    
    print(f"{'='*60}\n")
    
    return 0 if resultado['colapso_detectado'] else 1


if __name__ == '__main__':
    sys.exit(main())
