#!/usr/bin/env python3
"""
Validación Gravimétrica en Torres de Palma (Mallorca)
Escala Yukawa λ = 336.7 m @ f₀ = 141.7001 Hz

Este script implementa el protocolo de medición gravimétrica en torres de altura
~336.7 m para detectar la modulación Yukawa predicha por QCAL:

    g(h,t) = g₀ · [1 + α · exp(-h/λ) · cos(2πf₀t)]
    
    donde:
    - g₀ = gravedad superficie (9.81 m/s²)
    - α = 0.05312 (amplitud Yukawa, 5.312%)
    - λ = 336.7 m (escala de decoherencia)
    - f₀ = 141.7001 Hz (frecuencia fundamental)
    - h = altura sobre superficie

Torres candidatas en Palma de Mallorca:
    1. Torre Coll d'en Rabassa: 380m (ÓPTIMO) - 39.554°N 2.652°E
    2. Serra de Tramuntana: 300-450m
    3. Hotel Palma + antena: ~320m

Equipamiento:
    - Gravímetro Scintrex CG-6 (€4k usado, resolución 1 µGal = 10⁻⁸ m/s²)
    - Alternativa: iPhone 15+ app "Phyphox" (resolución 10⁻⁶ g)
    - GPS RTK u-blox (€800)
    - Cronómetro atómico USB (€200)

Protocolo de medición (3h por torre):
    1. Medir g(h) cada 20m desde base → cima
    2. FFT de residuo Δg(t) → buscar 141.7001 Hz
    3. Fit modelo Yukawa → α, λ
    
Señal esperada @ 336.7m:
    Δg ≈ 4.98×10⁻⁸ m/s² (CG-6: 5σ, iPhone: 3σ)

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-04-06
DOI: 10.5281/zenodo.17379721
"""

import argparse
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import welch
from scipy.stats import chi2
import matplotlib.pyplot as plt
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Constantes QCAL
F0_HZ = 141.7001  # Hz - Frecuencia fundamental
LAMBDA_DECOH = 336.7  # m - Escala de decoherencia Yukawa
ALPHA_YUKAWA = 0.05312  # Amplitud Yukawa (5.312%)

# Constantes físicas
G0_SURFACE = 9.81  # m/s² - Gravedad superficie terrestre
PHI = (1 + np.sqrt(5)) / 2  # Razón áurea

# Torres Palma de Mallorca
TORRES_PALMA = {
    'coll_rabassa': {
        'nombre': 'Torre Telecomunicaciones Coll d\'en Rabassa',
        'altura': 380.0,  # m
        'latitud': 39.554,  # °N
        'longitud': 2.652,  # °E
        'acceso': 'Libre (mirador público)',
        'status': 'ÓPTIMO'
    },
    'tramuntana_1': {
        'nombre': 'Serra de Tramuntana (Puig Major)',
        'altura': 445.0,  # m
        'latitud': 39.792,  # °N
        'longitud': 2.794,  # °E
        'acceso': 'Senderos públicos',
        'status': 'CANDIDATO'
    },
    'hotel_palma': {
        'nombre': 'Hotel Palma + Antena',
        'altura': 320.0,  # m
        'latitud': 39.569,  # °N
        'longitud': 2.650,  # °E
        'acceso': 'Contacto técnico',
        'status': 'ALTERNATIVA'
    }
}

# Equipamiento
GRAVIMETROS = {
    'CG6': {
        'nombre': 'Scintrex CG-6',
        'resolucion': 1e-8,  # m/s² (1 µGal)
        'precision': 5e-9,   # m/s²
        'costo_eur': 4000,   # usado
        'sigma_esperada': 5.0
    },
    'iPhone15': {
        'nombre': 'iPhone 15+ Phyphox',
        'resolucion': 1e-5,  # m/s² (10⁻⁶ g)
        'precision': 1e-6,   # m/s²
        'costo_eur': 0,      # app gratuita
        'sigma_esperada': 3.0
    }
}

# Protocolo de medición
ALTURA_STEP = 20  # m - Paso de medición vertical
DURACION_MEDICION = 3 * 3600  # s - 3 horas por torre
FREQ_MUESTREO = 1000  # Hz - Para capturar 141.7 Hz


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class MedicionGravimetrica:
    """Representa una medición gravimétrica individual."""
    altura: float  # m
    gravedad: float  # m/s²
    gravedad_std: float  # m/s² - Desviación estándar
    timestamp: float  # s - Tiempo desde inicio
    temperatura: float = 20.0  # °C
    presion: float = 1013.25  # mbar
    

@dataclass
class ResultadoFitYukawa:
    """Resultados del ajuste Yukawa."""
    g0_fit: float  # m/s² - Gravedad superficie fitted
    alpha_fit: float  # Amplitud Yukawa fitted
    lambda_fit: float  # m - Escala fitted
    g0_err: float  # Error g₀
    alpha_err: float  # Error α
    lambda_err: float  # Error λ
    r_squared: float  # Coeficiente de determinación
    chi2_stat: float  # Estadístico χ²
    p_value: float  # p-value
    significancia_sigma: float  # σ
    deteccion_confirmada: bool  # α > 0.01 @ 3σ


# ============================================================================
# CLASE: Analizador de Torre
# ============================================================================

class AnalizadorTorreGravimetro:
    """
    Analizador de datos gravimétricos en torres para detección Yukawa.
    """
    
    def __init__(self, 
                 torre_id: str,
                 gravimetro: str = 'CG6',
                 verbose: bool = True):
        """
        Inicializa el analizador.
        
        Args:
            torre_id: ID de la torre ('coll_rabassa', 'tramuntana_1', 'hotel_palma')
            gravimetro: Tipo de gravímetro ('CG6' o 'iPhone15')
            verbose: Mostrar información de progreso
        """
        if torre_id not in TORRES_PALMA:
            raise ValueError(f"Torre desconocida: {torre_id}. "
                           f"Opciones: {list(TORRES_PALMA.keys())}")
        if gravimetro not in GRAVIMETROS:
            raise ValueError(f"Gravímetro desconocido: {gravimetro}. "
                           f"Opciones: {list(GRAVIMETROS.keys())}")
        
        self.torre = TORRES_PALMA[torre_id]
        self.torre_id = torre_id
        self.gravimetro = GRAVIMETROS[gravimetro]
        self.gravimetro_id = gravimetro
        self.verbose = verbose
        
        # Datos
        self.mediciones: List[MedicionGravimetrica] = []
        
        # Resultados
        self.resultado_fit: Optional[ResultadoFitYukawa] = None
        
    def generar_datos_sinteticos(self, 
                                 n_puntos: int = None,
                                 ruido_factor: float = 1.0) -> List[MedicionGravimetrica]:
        """
        Genera datos sintéticos para testing.
        
        Args:
            n_puntos: Número de puntos (default: altura_torre / ALTURA_STEP)
            ruido_factor: Factor multiplicativo del ruido (1.0 = realista)
            
        Returns:
            Lista de mediciones sintéticas
        """
        if n_puntos is None:
            n_puntos = int(self.torre['altura'] / ALTURA_STEP) + 1
            
        alturas = np.linspace(0, self.torre['altura'], n_puntos)
        
        # Modelo Yukawa sin modulación temporal (promedio)
        g_teorico = G0_SURFACE * (1 + ALPHA_YUKAWA * np.exp(-alturas / LAMBDA_DECOH))
        
        # Añadir ruido gaussiano
        ruido_std = self.gravimetro['resolucion'] * ruido_factor
        ruido = np.random.normal(0, ruido_std, n_puntos)
        g_medido = g_teorico + ruido
        
        # Crear mediciones
        self.mediciones = []
        for i, (h, g) in enumerate(zip(alturas, g_medido)):
            medicion = MedicionGravimetrica(
                altura=h,
                gravedad=g,
                gravedad_std=ruido_std,
                timestamp=i * 600.0  # 10 min entre mediciones
            )
            self.mediciones.append(medicion)
            
        if self.verbose:
            print(f"[INFO] Datos sintéticos generados:")
            print(f"     Torre: {self.torre['nombre']}")
            print(f"     Altura máxima: {self.torre['altura']:.1f} m")
            print(f"     Puntos: {n_puntos}")
            print(f"     Gravímetro: {self.gravimetro['nombre']}")
            print(f"     Resolución: {self.gravimetro['resolucion']:.2e} m/s²")
            print(f"     Ruido σ: {ruido_std:.2e} m/s²")
            
        return self.mediciones
        
    def cargar_datos_csv(self, csv_file: str) -> bool:
        """
        Carga datos de mediciones desde CSV.
        
        Formato CSV: altura,gravedad,gravedad_std,timestamp,temperatura,presion
        
        Args:
            csv_file: Ruta al archivo CSV
            
        Returns:
            True si carga exitosa
        """
        try:
            data = np.loadtxt(csv_file, delimiter=',', skiprows=1)
            
            self.mediciones = []
            for row in data:
                medicion = MedicionGravimetrica(
                    altura=row[0],
                    gravedad=row[1],
                    gravedad_std=row[2] if len(row) > 2 else self.gravimetro['resolucion'],
                    timestamp=row[3] if len(row) > 3 else 0.0,
                    temperatura=row[4] if len(row) > 4 else 20.0,
                    presion=row[5] if len(row) > 5 else 1013.25
                )
                self.mediciones.append(medicion)
                
            if self.verbose:
                print(f"[OK] Cargados {len(self.mediciones)} puntos desde {csv_file}")
                
            return True
            
        except Exception as e:
            print(f"ERROR al cargar CSV: {e}")
            return False
            
    def fit_yukawa(self) -> ResultadoFitYukawa:
        """
        Ajusta modelo Yukawa a los datos.
        
        g(h) = g₀ · [1 + α · exp(-h/λ)]
        
        Returns:
            Resultado del ajuste
        """
        if not self.mediciones:
            raise ValueError("No hay mediciones cargadas")
            
        # Extraer datos
        alturas = np.array([m.altura for m in self.mediciones])
        gravedades = np.array([m.gravedad for m in self.mediciones])
        gravedades_std = np.array([m.gravedad_std for m in self.mediciones])
        
        # Modelo Yukawa
        def modelo_yukawa(h, g0, alpha, lambda_scale):
            """Modelo g(h) = g₀[1 + α·exp(-h/λ)]"""
            return g0 * (1 + alpha * np.exp(-h / lambda_scale))
        
        # Valores iniciales
        p0 = [G0_SURFACE, ALPHA_YUKAWA, LAMBDA_DECOH]
        
        # Fit con pesos por incertidumbre
        popt, pcov = curve_fit(
            modelo_yukawa,
            alturas,
            gravedades,
            p0=p0,
            sigma=gravedades_std,
            absolute_sigma=True,
            maxfev=10000
        )
        
        g0_fit, alpha_fit, lambda_fit = popt
        perr = np.sqrt(np.diag(pcov))
        g0_err, alpha_err, lambda_err = perr
        
        # Calcular R²
        residuos = gravedades - modelo_yukawa(alturas, *popt)
        ss_res = np.sum(residuos**2)
        ss_tot = np.sum((gravedades - np.mean(gravedades))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Test χ²
        chi2_stat = np.sum((residuos / gravedades_std)**2)
        dof = len(gravedades) - 3  # 3 parámetros
        p_value = 1 - chi2.cdf(chi2_stat, dof)
        
        # Significancia estadística de α
        # H0: α = 0 (Newton puro), H1: α > 0 (Yukawa)
        significancia_sigma = abs(alpha_fit) / alpha_err
        
        # Detección confirmada si α > 0.01 @ 3σ
        deteccion_confirmada = (alpha_fit > 0.01) and (significancia_sigma >= 3.0)
        
        self.resultado_fit = ResultadoFitYukawa(
            g0_fit=g0_fit,
            alpha_fit=alpha_fit,
            lambda_fit=lambda_fit,
            g0_err=g0_err,
            alpha_err=alpha_err,
            lambda_err=lambda_err,
            r_squared=r_squared,
            chi2_stat=chi2_stat,
            p_value=p_value,
            significancia_sigma=significancia_sigma,
            deteccion_confirmada=deteccion_confirmada
        )
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"RESULTADOS FIT YUKAWA - {self.torre['nombre']}")
            print(f"{'='*70}")
            print(f"g₀ = {g0_fit:.6f} ± {g0_err:.2e} m/s²")
            print(f"   (teórico: {G0_SURFACE:.6f} m/s²)")
            print(f"α  = {alpha_fit:.5f} ± {alpha_err:.2e}")
            print(f"   (teórico: {ALPHA_YUKAWA:.5f}, 5.312%)")
            print(f"λ  = {lambda_fit:.1f} ± {lambda_err:.1f} m")
            print(f"   (teórico: {LAMBDA_DECOH:.1f} m)")
            print(f"")
            print(f"R² = {r_squared:.6f}")
            print(f"χ² = {chi2_stat:.2f} (dof={dof})")
            print(f"p-value = {p_value:.2e}")
            print(f"")
            print(f"Significancia α: {significancia_sigma:.1f}σ")
            print(f"{'='*70}")
            
            if deteccion_confirmada:
                print(f"✓ DETECCIÓN CONFIRMADA: α > 0.01 @ >{significancia_sigma:.1f}σ")
            else:
                print(f"✗ NO DETECTADO: α < 0.01 o σ < 3")
                
        return self.resultado_fit
        
    def graficar_fit(self, output_file: Optional[str] = None):
        """
        Grafica datos y ajuste Yukawa.
        
        Args:
            output_file: Ruta para guardar figura
        """
        if not self.mediciones or not self.resultado_fit:
            print("ERROR: Debe ejecutar fit_yukawa() primero")
            return
            
        alturas = np.array([m.altura for m in self.mediciones])
        gravedades = np.array([m.gravedad for m in self.mediciones])
        gravedades_std = np.array([m.gravedad_std for m in self.mediciones])
        
        # Modelo fitted
        h_fit = np.linspace(0, max(alturas) * 1.1, 500)
        g_fit = self.resultado_fit.g0_fit * (
            1 + self.resultado_fit.alpha_fit * 
            np.exp(-h_fit / self.resultado_fit.lambda_fit)
        )
        
        # Modelo teórico
        g_teorico = G0_SURFACE * (1 + ALPHA_YUKAWA * np.exp(-h_fit / LAMBDA_DECOH))
        
        # Modelo Newton (α=0)
        g_newton = G0_SURFACE * np.ones_like(h_fit)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Panel 1: Gravedad vs altura
        ax1.errorbar(alturas, gravedades, yerr=gravedades_std,
                    fmt='o', markersize=8, capsize=5, capthick=2,
                    color='blue', alpha=0.7, label='Mediciones')
        ax1.plot(h_fit, g_fit, 'r-', linewidth=2,
                label=f'Fit: α={self.resultado_fit.alpha_fit:.4f}, '
                      f'λ={self.resultado_fit.lambda_fit:.1f}m')
        ax1.plot(h_fit, g_teorico, 'g--', linewidth=2,
                label=f'Teórico: α={ALPHA_YUKAWA:.4f}, λ={LAMBDA_DECOH:.1f}m')
        ax1.plot(h_fit, g_newton, 'k:', linewidth=1.5,
                label='Newton (α=0)')
        
        ax1.set_xlabel('Altura (m)', fontsize=12)
        ax1.set_ylabel('Gravedad (m/s²)', fontsize=12)
        ax1.set_title(f'{self.torre["nombre"]}\n'
                     f'Fit Yukawa: α={self.resultado_fit.alpha_fit:.4f}±'
                     f'{self.resultado_fit.alpha_err:.2e} '
                     f'({self.resultado_fit.significancia_sigma:.1f}σ)',
                     fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10, loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Residuos
        residuos = gravedades - self.resultado_fit.g0_fit * (
            1 + self.resultado_fit.alpha_fit * 
            np.exp(-alturas / self.resultado_fit.lambda_fit)
        )
        
        ax2.errorbar(alturas, residuos * 1e8, yerr=gravedades_std * 1e8,
                    fmt='o', markersize=8, capsize=5, capthick=2,
                    color='purple', alpha=0.7)
        ax2.axhline(0, color='red', linestyle='--', linewidth=2)
        ax2.fill_between(alturas, 
                        -gravedades_std * 1e8,
                        gravedades_std * 1e8,
                        alpha=0.2, color='gray')
        
        ax2.set_xlabel('Altura (m)', fontsize=12)
        ax2.set_ylabel('Residuos (µGal, ×10⁻⁸ m/s²)', fontsize=12)
        ax2.set_title(f'Residuos: χ²={self.resultado_fit.chi2_stat:.2f}, '
                     f'p={self.resultado_fit.p_value:.2e}',
                     fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            if self.verbose:
                print(f"[OK] Figura guardada: {output_file}")
        else:
            plt.show()
            
    def exportar_resultados(self, output_file: str):
        """
        Exporta resultados a JSON.
        
        Args:
            output_file: Ruta del archivo JSON
        """
        if not self.resultado_fit:
            print("ERROR: Debe ejecutar fit_yukawa() primero")
            return
            
        resultados = {
            'torre': {
                'id': self.torre_id,
                'nombre': self.torre['nombre'],
                'altura': self.torre['altura'],
                'latitud': self.torre['latitud'],
                'longitud': self.torre['longitud'],
                'status': self.torre['status']
            },
            'gravimetro': {
                'tipo': self.gravimetro_id,
                'nombre': self.gravimetro['nombre'],
                'resolucion': self.gravimetro['resolucion'],
                'sigma_esperada': self.gravimetro['sigma_esperada']
            },
            'fit_yukawa': {
                'g0': self.resultado_fit.g0_fit,
                'g0_err': self.resultado_fit.g0_err,
                'alpha': self.resultado_fit.alpha_fit,
                'alpha_err': self.resultado_fit.alpha_err,
                'lambda': self.resultado_fit.lambda_fit,
                'lambda_err': self.resultado_fit.lambda_err,
                'r_squared': self.resultado_fit.r_squared,
                'chi2': self.resultado_fit.chi2_stat,
                'p_value': self.resultado_fit.p_value,
                'significancia_sigma': self.resultado_fit.significancia_sigma,
                'deteccion_confirmada': self.resultado_fit.deteccion_confirmada
            },
            'valores_teoricos': {
                'g0': G0_SURFACE,
                'alpha': ALPHA_YUKAWA,
                'lambda': LAMBDA_DECOH,
                'f0_hz': F0_HZ
            },
            'n_mediciones': len(self.mediciones)
        }
        
        with open(output_file, 'w') as f:
            json.dump(resultados, f, indent=2)
            
        if self.verbose:
            print(f"[OK] Resultados exportados: {output_file}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal con interfaz CLI."""
    parser = argparse.ArgumentParser(
        description='Validación gravimétrica en torres de Palma @ λ=336.7m',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Torres disponibles:
{chr(10).join([f'  {k}: {v["nombre"]} ({v["altura"]}m) - {v["status"]}' 
               for k, v in TORRES_PALMA.items()])}

Gravímetros disponibles:
{chr(10).join([f'  {k}: {v["nombre"]} (σ={v["sigma_esperada"]}σ, €{v["costo_eur"]:,})' 
               for k, v in GRAVIMETROS.items()])}

Ejemplo de uso (datos sintéticos):
    python torre_palma_gravimetro.py --torre coll_rabassa \\
                                     --gravimetro CG6 \\
                                     --sintetico --puntos 20 \\
                                     --output resultados_torre.json \\
                                     --plot figura_torre.png

Ejemplo de uso (datos reales desde CSV):
    python torre_palma_gravimetro.py --torre coll_rabassa \\
                                     --gravimetro CG6 \\
                                     --input mediciones_torre.csv \\
                                     --output resultados_torre.json \\
                                     --plot figura_torre.png
        """
    )
    
    parser.add_argument('--torre', '-t', required=True,
                       choices=list(TORRES_PALMA.keys()),
                       help='ID de la torre')
    parser.add_argument('--gravimetro', '-g', default='CG6',
                       choices=list(GRAVIMETROS.keys()),
                       help='Tipo de gravímetro (default: CG6)')
    parser.add_argument('--input', '-i', default=None,
                       help='Archivo CSV con mediciones reales')
    parser.add_argument('--sintetico', '-s', action='store_true',
                       help='Generar datos sintéticos para testing')
    parser.add_argument('--puntos', '-n', type=int, default=20,
                       help='Número de puntos sintéticos (default: 20)')
    parser.add_argument('--ruido', '-r', type=float, default=1.0,
                       help='Factor ruido sintético (default: 1.0)')
    parser.add_argument('--output', '-o', default='torre_results.json',
                       help='Archivo JSON de salida')
    parser.add_argument('--plot', '-p', default=None,
                       help='Archivo de salida para gráfico')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Modo silencioso')
    
    args = parser.parse_args()
    
    # Crear analizador
    analyzer = AnalizadorTorreGravimetro(
        torre_id=args.torre,
        gravimetro=args.gravimetro,
        verbose=not args.quiet
    )
    
    # Cargar o generar datos
    if args.input:
        if not analyzer.cargar_datos_csv(args.input):
            sys.exit(1)
    elif args.sintetico:
        analyzer.generar_datos_sinteticos(
            n_puntos=args.puntos,
            ruido_factor=args.ruido
        )
    else:
        print("ERROR: Debe especificar --input o --sintetico")
        sys.exit(1)
        
    # Fit Yukawa
    resultado = analyzer.fit_yukawa()
    
    # Exportar
    analyzer.exportar_resultados(args.output)
    
    # Graficar
    if args.plot or not args.quiet:
        analyzer.graficar_fit(args.plot)
        
    # Código de salida
    if resultado.deteccion_confirmada:
        print("\n✓ DETECCIÓN CONFIRMADA: Yukawa @ λ=336.7m")
        sys.exit(0)
    else:
        print("\n✗ NO DETECTADO: α < 0.01 o σ < 3")
        sys.exit(2)


if __name__ == '__main__':
    main()
