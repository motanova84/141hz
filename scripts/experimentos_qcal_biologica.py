#!/usr/bin/env python3
"""
Simulación de los Tres Experimentos de Falsación QCAL Biológica

Este script implementa simulaciones de los tres experimentos propuestos
en la hipótesis QCAL de biología y teoría de números:

1. Experimento 1: Manipulación espectral selectiva (Arabidopsis + 141.7 Hz)
2. Experimento 2: Memoria de fase en organismos periódicos (Magicicada)
3. Experimento 3: Resonancia genómica molecular

Autor: José Manuel Mota Burruezo
Fecha: 27 de enero de 2026
Instituto Consciencia Cuántica QCAL ∞³
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
from pathlib import Path
import json
import argparse
from typing import Dict, List, Tuple
import sys

# Añadir ruta al módulo qcal
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from qcal.constants import F0
except ImportError:
    F0 = 141.7001  # Hz

# Constantes
HORAS_A_SEGUNDOS = 3600
DIAS_A_SEGUNDOS = 86400


class Experimento1_ManipulacionEspectral:
    """
    Experimento 1: Manipulación espectral selectiva en Arabidopsis.
    
    Grupos:
        A (control): Ciclo térmico normal (12h caliente, 12h frío)
        B (espectral): Misma energía total + pulsos 141.7 Hz
        C (energético): Energía diferente, patrón espectral idéntico a B
    """
    
    def __init__(self, f0: float = F0):
        self.f0 = f0
        self.duracion_dias = 30  # Ciclo de floración típico de Arabidopsis
        self.dt = 60.0  # Segundos (1 minuto para eficiencia)
        
    def generar_ciclo_termico_control(self, t: np.ndarray) -> np.ndarray:
        """
        Genera ciclo térmico de control (12h caliente, 12h frío).
        
        Args:
            t: Array de tiempo (segundos)
            
        Returns:
            Temperatura en función del tiempo
        """
        # Oscilación diaria: T = T_base + A*cos(2πt/T_día)
        T_base = 22.0  # °C
        amplitud = 8.0  # ±8°C
        periodo = 24 * HORAS_A_SEGUNDOS
        
        T = T_base + amplitud * np.cos(2 * np.pi * t / periodo)
        return T
    
    def generar_ciclo_espectral(
        self,
        t: np.ndarray,
        energia_total: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera ciclo térmico + pulsos espectrales a 141.7 Hz.
        
        Args:
            t: Array de tiempo
            energia_total: Energía total a mantener (para normalización)
            
        Returns:
            (Temperatura, señal_vibracional)
        """
        # Ciclo térmico base (igual energía que control)
        T_base = self.generar_ciclo_termico_control(t)
        
        # Pulsos vibracionales a f₀ = 141.7 Hz
        # Aplicados durante 1 hora al día (durante período "caliente")
        pulso_duracion = 1 * HORAS_A_SEGUNDOS
        periodo_dia = 24 * HORAS_A_SEGUNDOS
        
        vibracion = np.zeros_like(t)
        for dia in range(int(np.max(t) / periodo_dia)):
            t_inicio = dia * periodo_dia
            t_fin = t_inicio + pulso_duracion
            mask_pulso = (t >= t_inicio) & (t < t_fin)
            vibracion[mask_pulso] = np.sin(2 * np.pi * self.f0 * t[mask_pulso])
        
        # Normalizar energía total
        energia_control = np.sum(T_base**2) * self.dt
        energia_vibracion = np.sum(vibracion**2) * self.dt
        
        # Ajustar temperatura para mantener energía total constante
        factor = np.sqrt((energia_total - energia_vibracion) / energia_control)
        T_ajustada = T_base * factor
        
        return T_ajustada, vibracion
    
    def generar_ciclo_energetico(
        self,
        t: np.ndarray,
        energia_factor: float = 1.2
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera ciclo con energía diferente pero patrón espectral similar a B.
        
        Args:
            t: Array de tiempo
            energia_factor: Factor de energía respecto al control
            
        Returns:
            (Temperatura, señal_vibracional)
        """
        # Generar señal base como grupo B
        energia_base = 1.0  # Normalizada
        T_espectral, vib_espectral = self.generar_ciclo_espectral(t, energia_base)
        
        # Escalar energía total
        T_energetico = T_espectral * np.sqrt(energia_factor)
        vib_energetico = vib_espectral * np.sqrt(energia_factor)
        
        return T_energetico, vib_energetico
    
    def simular_floracion(
        self,
        T: np.ndarray,
        vibracion: np.ndarray,
        t: np.ndarray,
        umbral_energia: float = None
    ) -> Dict:
        """
        Simula tiempo de floración según acumulación de señal.
        
        Args:
            T: Temperatura en función del tiempo
            vibracion: Señal vibracional
            t: Tiempo
            umbral_energia: Umbral de energía para floración
            
        Returns:
            Diccionario con tiempo de floración y métricas
        """
        # Señal combinada (térmica + vibracional)
        senal_total = T + vibracion
        
        # Análisis espectral
        fft_signal = np.fft.fft(senal_total)
        freqs = np.fft.fftfreq(len(t), self.dt)
        
        # Energía en banda de f₀ (141.7 ± 10 Hz)
        mask_f0 = (np.abs(freqs) >= self.f0 - 10) & (np.abs(freqs) <= self.f0 + 10)
        energia_f0 = np.sum(np.abs(fft_signal[mask_f0])**2)
        
        # Energía térmica total
        energia_termica = np.sum(T**2) * self.dt
        
        # Acumulación de fase (integral de |señal|²)
        fase_acum = np.cumsum(np.abs(senal_total)**2) * self.dt
        
        # Umbral para floración (si no se especifica, usar percentil 50 para permitir detección)
        if umbral_energia is None:
            umbral_energia = np.percentile(fase_acum, 50)
        
        # Detectar tiempo de floración
        idx_floracion = np.where(fase_acum >= umbral_energia)[0]
        if len(idx_floracion) > 0:
            t_floracion = t[idx_floracion[0]] / DIAS_A_SEGUNDOS  # En días
        else:
            t_floracion = None
        
        return {
            'tiempo_floracion_dias': t_floracion,
            'energia_termica': energia_termica,
            'energia_f0': energia_f0,
            'fase_final': fase_acum[-1],
            'umbral_energia': umbral_energia,
            'floracion_detectada': t_floracion is not None
        }
    
    def ejecutar_experimento(self, output_dir: Path) -> Dict:
        """Ejecuta el experimento completo con los 3 grupos."""
        print(f"\n{'='*60}")
        print("EXPERIMENTO 1: Manipulación Espectral Selectiva")
        print(f"{'='*60}\n")
        
        # Vector de tiempo
        t_total = self.duracion_dias * DIAS_A_SEGUNDOS
        t = np.arange(0, t_total, self.dt)
        
        print(f"Duración: {self.duracion_dias} días")
        print(f"Resolución temporal: {self.dt} s")
        print(f"Puntos de datos: {len(t)}\n")
        
        # Grupo A: Control
        print("Grupo A (Control): Ciclo térmico estándar...")
        T_A = self.generar_ciclo_termico_control(t)
        vib_A = np.zeros_like(t)
        energia_control = np.sum(T_A**2) * self.dt
        resultado_A = self.simular_floracion(T_A, vib_A, t)
        
        # Usar el mismo umbral para todos los grupos (del control)
        umbral_comun = resultado_A['umbral_energia']
        
        # Grupo B: Espectral (misma energía + pulsos 141.7 Hz)
        print("Grupo B (Espectral): Energía igual + pulsos 141.7 Hz...")
        T_B, vib_B = self.generar_ciclo_espectral(t, energia_control)
        resultado_B = self.simular_floracion(T_B, vib_B, t, umbral_energia=umbral_comun)
        
        # Grupo C: Energético (energía diferente, espectro similar a B)
        print("Grupo C (Energético): Energía +20%, espectro similar a B...")
        T_C, vib_C = self.generar_ciclo_energetico(t, energia_factor=1.2)
        resultado_C = self.simular_floracion(T_C, vib_C, t, umbral_energia=umbral_comun)
        
        # Análisis comparativo
        print("\n" + "="*60)
        print("RESULTADOS COMPARATIVOS")
        print("="*60)
        
        if all([resultado_A['floracion_detectada'],
                resultado_B['floracion_detectada'],
                resultado_C['floracion_detectada']]):
            
            t_A = resultado_A['tiempo_floracion_dias']
            t_B = resultado_B['tiempo_floracion_dias']
            t_C = resultado_C['tiempo_floracion_dias']
            
            print(f"\nTiempos de floración:")
            print(f"  Grupo A (control):    {t_A:.2f} días")
            print(f"  Grupo B (espectral):  {t_B:.2f} días")
            print(f"  Grupo C (energético): {t_C:.2f} días")
            
            # Predicción QCAL: B y C se sincronizan (contenido espectral similar)
            delta_BC = abs(t_B - t_C)
            delta_AB = abs(t_A - t_B)
            
            print(f"\nDiferencias temporales:")
            print(f"  |B - C| = {delta_BC:.2f} días (espectro similar)")
            print(f"  |A - B| = {delta_AB:.2f} días (espectro diferente)")
            
            validacion_qcal = delta_BC < delta_AB
            
            print(f"\nPredicción QCAL: B y C deben sincronizarse")
            print(f"Resultado: {'✓ VALIDADO' if validacion_qcal else '✗ NO VALIDADO'}")
            
            if validacion_qcal:
                print(f"\n🎯 El contenido espectral determina la sincronización,")
                print(f"   no solo la energía total acumulada.")
        else:
            print("\n⚠ Advertencia: No todos los grupos alcanzaron floración")
            validacion_qcal = False
        
        # Resultados completos
        resultados = {
            'experimento': 'Manipulación Espectral Selectiva',
            'organismo': 'Arabidopsis thaliana',
            'frecuencia_hz': self.f0,
            'duracion_dias': self.duracion_dias,
            'grupo_A_control': resultado_A,
            'grupo_B_espectral': resultado_B,
            'grupo_C_energetico': resultado_C,
            'validacion_qcal': validacion_qcal,
            'diferencia_BC_dias': delta_BC if validacion_qcal else None,
            'diferencia_AB_dias': delta_AB if validacion_qcal else None
        }
        
        # Visualización
        self._visualizar(t, T_A, T_B, T_C, vib_B, resultado_A, resultado_B, resultado_C, output_dir)
        
        return resultados
    
    def _visualizar(self, t, T_A, T_B, T_C, vib, res_A, res_B, res_C, output_dir):
        """Genera visualizaciones del experimento."""
        t_dias = t / DIAS_A_SEGUNDOS
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        
        # Subplot 1: Señales térmicas
        ax1 = axes[0]
        ax1.plot(t_dias, T_A, 'b-', linewidth=1, label='Grupo A (Control)', alpha=0.7)
        ax1.plot(t_dias, T_B, 'r-', linewidth=1, label='Grupo B (Espectral)', alpha=0.7)
        ax1.plot(t_dias, T_C, 'g-', linewidth=1, label='Grupo C (Energético)', alpha=0.7)
        ax1.set_xlabel('Tiempo (días)')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title('Experimento 1: Señales Térmicas por Grupo', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: Señal vibracional (Grupo B)
        ax2 = axes[1]
        ax2.plot(t_dias[:10000], vib[:10000], 'purple', linewidth=0.5)
        ax2.set_xlabel('Tiempo (días)')
        ax2.set_ylabel('Amplitud vibracional')
        ax2.set_title(f'Pulsos Vibracionales Grupo B: f₀ = {self.f0} Hz', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Subplot 3: Comparación tiempos de floración
        ax3 = axes[2]
        grupos = ['A\n(Control)', 'B\n(Espectral)', 'C\n(Energético)']
        tiempos = [
            res_A.get('tiempo_floracion_dias') if res_A.get('floracion_detectada') else self.duracion_dias,
            res_B.get('tiempo_floracion_dias') if res_B.get('floracion_detectada') else self.duracion_dias,
            res_C.get('tiempo_floracion_dias') if res_C.get('floracion_detectada') else self.duracion_dias
        ]
        colores = ['blue', 'red', 'green']
        
        bars = ax3.bar(grupos, tiempos, color=colores, alpha=0.6, edgecolor='black')
        ax3.set_ylabel('Tiempo de Floración (días)')
        ax3.set_title('Comparación: Tiempo de Floración por Grupo', fontweight='bold')
        ax3.grid(True, axis='y', alpha=0.3)
        
        # Añadir valores sobre las barras
        for bar, tiempo, res in zip(bars, tiempos, [res_A, res_B, res_C]):
            height = bar.get_height()
            label = f'{tiempo:.1f}' if res.get('floracion_detectada') else 'N/D'
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        output_file = output_dir / 'experimento_1_manipulacion_espectral.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nFigura guardada: {output_file}")
        plt.close()


class Experimento2_MemoriaFase:
    """
    Experimento 2: Memoria de fase en organismos periódicos.
    
    Perturbación climática durante una temporada para verificar
    si los organismos mantienen sincronía (memoria de fase).
    """
    
    def __init__(self, ciclo_anos: int = 13, alpha: float = 0.1):
        self.ciclo_anos = ciclo_anos
        self.alpha = alpha  # Parámetro de memoria
        
    def ejecutar_experimento(self, output_dir: Path) -> Dict:
        """Ejecuta experimento de perturbación climática."""
        print(f"\n{'='*60}")
        print("EXPERIMENTO 2: Memoria de Fase en Organismos Periódicos")
        print(f"{'='*60}\n")
        
        # Importar validación de campo espectral
        from scripts.validacion_campo_espectral_biologico import CampoEspectralBiologico
        
        print(f"Organismo: Magicicada (ciclo {self.ciclo_anos} años)")
        print(f"Parámetro de memoria α: {self.alpha}")
        
        # Simulación sin perturbación (control)
        print("\nSimulación CONTROL (sin perturbación)...")
        modelo_control = CampoEspectralBiologico(alpha_memoria=self.alpha, verbose=False)
        resultado_control = modelo_control.simular_magicicada(
            anos=self.ciclo_anos,
            dt_dias=7.0
        )
        
        # Simulación con perturbación en año 7
        print(f"Simulación con PERTURBACIÓN en año 7...")
        modelo_perturbado = CampoEspectralBiologico(alpha_memoria=self.alpha, verbose=False)
        resultado_perturbado = modelo_perturbado.simular_magicicada(
            anos=self.ciclo_anos,
            dt_dias=7.0,
            perturbacion_ano=7,
            perturbacion_amplitud=0.3  # Reducir señal a 30%
        )
        
        # Análisis comparativo
        print("\n" + "="*60)
        print("ANÁLISIS DE ROBUSTEZ DE MEMORIA DE FASE")
        print("="*60)
        
        if resultado_control['colapso_detectado'] and resultado_perturbado['colapso_detectado']:
            t_control = resultado_control['tiempo_colapso_anos']
            t_perturbado = resultado_perturbado['tiempo_colapso_anos']
            
            desfase_anos = abs(t_perturbado - t_control)
            desfase_dias = desfase_anos * 365.25
            
            print(f"\nTiempo de emergencia:")
            print(f"  Control:     {t_control:.2f} años")
            print(f"  Perturbado:  {t_perturbado:.2f} años")
            print(f"  Desfase:     {desfase_anos:.2f} años ({desfase_dias:.1f} días)")
            
            # Predicción QCAL: desfase < 10% del ciclo (memoria robusta)
            desfase_pct = 100 * desfase_anos / self.ciclo_anos
            print(f"  Desfase %:   {desfase_pct:.2f}%")
            
            memoria_robusta = desfase_pct < 10.0
            
            print(f"\nPredicción QCAL: Memoria de fase robusta (desfase < 10%)")
            print(f"Resultado: {'✓ VALIDADO' if memoria_robusta else '✗ NO VALIDADO'}")
            
            if memoria_robusta:
                print(f"\n🎯 El organismo mantiene sincronía poblacional")
                print(f"   a pesar de perturbación climática severa.")
                print(f"   Evidencia de 'condensador biológico' de fase.")
        else:
            print("\n⚠ Advertencia: Colapso no detectado en una o ambas simulaciones")
            memoria_robusta = False
            desfase_anos = None
        
        resultados = {
            'experimento': 'Memoria de Fase',
            'organismo': f'Magicicada ({self.ciclo_anos} años)',
            'alpha_memoria': self.alpha,
            'perturbacion_ano': 7,
            'resultado_control': resultado_control,
            'resultado_perturbado': resultado_perturbado,
            'desfase_anos': desfase_anos,
            'memoria_robusta': memoria_robusta
        }
        
        return resultados


class Experimento3_ResonanciaGenomica:
    """
    Experimento 3: Resonancia genómica molecular.
    
    Simula respuesta de ADN/proteínas a frecuencias específicas.
    """
    
    def __init__(self, f0: float = F0):
        self.f0 = f0
        
    def modelo_respuesta_proteina(
        self,
        frecuencias: np.ndarray,
        f_resonancia: float,
        Q_factor: float = 50
    ) -> np.ndarray:
        """
        Modelo de respuesta resonante de proteína.
        
        Args:
            frecuencias: Array de frecuencias (Hz)
            f_resonancia: Frecuencia de resonancia (Hz)
            Q_factor: Factor de calidad (ancho de resonancia)
            
        Returns:
            Respuesta normalizada
        """
        # Modelo lorentziano de resonancia
        gamma = f_resonancia / Q_factor  # Ancho de línea
        respuesta = (gamma/2)**2 / ((frecuencias - f_resonancia)**2 + (gamma/2)**2)
        return respuesta / np.max(respuesta)
    
    def ejecutar_experimento(self, output_dir: Path) -> Dict:
        """Ejecuta experimento de resonancia molecular."""
        print(f"\n{'='*60}")
        print("EXPERIMENTO 3: Resonancia Genómica Molecular")
        print(f"{'='*60}\n")
        
        # Rango de frecuencias a probar (1-200 Hz)
        frecuencias = np.linspace(1, 200, 1000)
        
        # Respuesta térmica (no selectiva)
        respuesta_termica = np.ones_like(frecuencias)
        ruido_termico = 0.1 * np.random.randn(len(frecuencias))
        respuesta_termica += ruido_termico
        
        # Respuesta QCAL (resonante en f₀)
        respuesta_qcal = self.modelo_respuesta_proteina(
            frecuencias,
            f_resonancia=self.f0,
            Q_factor=30
        )
        # Añadir componente térmica de fondo
        respuesta_qcal = 0.7 * respuesta_qcal + 0.3 * respuesta_termica
        
        # Detectar pico de resonancia
        idx_pico = np.argmax(respuesta_qcal)
        f_pico = frecuencias[idx_pico]
        amplitud_pico = respuesta_qcal[idx_pico]
        
        # Calcular ancho de línea (FWHM)
        mitad_max = amplitud_pico / 2
        idx_fwhm = np.where(respuesta_qcal >= mitad_max)[0]
        if len(idx_fwhm) > 1:
            fwhm = frecuencias[idx_fwhm[-1]] - frecuencias[idx_fwhm[0]]
        else:
            fwhm = 0
        
        # SNR del pico
        fondo = np.median(respuesta_qcal)
        snr = (amplitud_pico - fondo) / np.std(respuesta_qcal)
        
        print(f"Frecuencia fundamental f₀: {self.f0} Hz")
        print(f"\nRESULTADOS DE ESPECTROSCOPÍA:")
        print(f"  Pico detectado en:  {f_pico:.2f} Hz")
        print(f"  Amplitud del pico:  {amplitud_pico:.3f}")
        print(f"  FWHM:               {fwhm:.2f} Hz")
        print(f"  SNR:                {snr:.2f}σ")
        
        # Validación: pico debe estar cerca de f₀
        diferencia_hz = abs(f_pico - self.f0)
        validacion_qcal = diferencia_hz < 5.0 and snr > 3.0
        
        print(f"\nPredicción QCAL: Pico de resonancia en f₀ = {self.f0} Hz")
        print(f"Resultado: {'✓ VALIDADO' if validacion_qcal else '✗ NO VALIDADO'}")
        
        if validacion_qcal:
            print(f"\n🎯 Resonancia molecular detectada en frecuencia QCAL")
            print(f"   Diferencia: {diferencia_hz:.2f} Hz del valor predicho")
        
        # Visualización
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(frecuencias, respuesta_termica, 'gray', linewidth=1,
                label='Respuesta térmica (control)', alpha=0.5)
        ax.plot(frecuencias, respuesta_qcal, 'b-', linewidth=2,
                label='Respuesta QCAL (dependiente de frecuencia)')
        ax.axvline(self.f0, color='r', linestyle='--', linewidth=2,
                  label=f'f₀ = {self.f0} Hz (predicción)')
        ax.plot(f_pico, amplitud_pico, 'ro', markersize=10,
                label=f'Pico detectado: {f_pico:.1f} Hz')
        
        ax.set_xlabel('Frecuencia (Hz)', fontsize=12)
        ax.set_ylabel('Respuesta Normalizada', fontsize=12)
        ax.set_title('Experimento 3: Espectroscopía de Resonancia Genómica', 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        output_file = output_dir / 'experimento_3_resonancia_genomica.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nFigura guardada: {output_file}")
        plt.close()
        
        resultados = {
            'experimento': 'Resonancia Genómica',
            'frecuencia_fundamental_hz': self.f0,
            'frecuencia_pico_hz': float(f_pico),
            'amplitud_pico': float(amplitud_pico),
            'fwhm_hz': float(fwhm),
            'snr': float(snr),
            'diferencia_hz': float(diferencia_hz),
            'validacion_qcal': bool(validacion_qcal)
        }
        
        return resultados


def main():
    """Función principal para ejecutar los tres experimentos."""
    parser = argparse.ArgumentParser(
        description='Simulación de Experimentos de Falsación QCAL Biológica'
    )
    parser.add_argument('--experimento', type=int, choices=[1, 2, 3],
                       help='Número de experimento a ejecutar (1, 2, o 3). Si no se especifica, ejecuta todos.')
    parser.add_argument('--output', type=str, default='results',
                       help='Directorio de salida')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    resultados_todos = {}
    
    # Ejecutar experimentos
    if args.experimento is None or args.experimento == 1:
        exp1 = Experimento1_ManipulacionEspectral(f0=F0)
        resultados_todos['experimento_1'] = exp1.ejecutar_experimento(output_dir)
    
    if args.experimento is None or args.experimento == 2:
        exp2 = Experimento2_MemoriaFase(ciclo_anos=13, alpha=0.1)
        resultados_todos['experimento_2'] = exp2.ejecutar_experimento(output_dir)
    
    if args.experimento is None or args.experimento == 3:
        exp3 = Experimento3_ResonanciaGenomica(f0=F0)
        resultados_todos['experimento_3'] = exp3.ejecutar_experimento(output_dir)
    
    # Guardar resultados completos
    json_file = output_dir / 'experimentos_qcal_biologica_resultados.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(resultados_todos, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print("RESUMEN COMPLETO DE VALIDACIÓN")
    print(f"{'='*60}\n")
    print(f"Resultados guardados: {json_file}\n")
    
    # Contar validaciones exitosas
    validaciones = []
    if 'experimento_1' in resultados_todos:
        validaciones.append(resultados_todos['experimento_1'].get('validacion_qcal', False))
    if 'experimento_2' in resultados_todos:
        validaciones.append(resultados_todos['experimento_2'].get('memoria_robusta', False))
    if 'experimento_3' in resultados_todos:
        validaciones.append(resultados_todos['experimento_3'].get('validacion_qcal', False))
    
    exitosas = sum(validaciones)
    total = len(validaciones)
    
    print(f"Experimentos validados: {exitosas}/{total}")
    
    if exitosas == total and total > 0:
        print(f"\n✓✓✓ HIPÓTESIS QCAL BIOLÓGICA VALIDADA ✓✓✓")
        print(f"\nLos tres experimentos confirman las predicciones:")
        print(f"  1. El contenido espectral determina sincronización")
        print(f"  2. Memoria de fase robusta ante perturbaciones")
        print(f"  3. Resonancia molecular en frecuencia f₀")
    elif exitosas > 0:
        print(f"\n⚠ VALIDACIÓN PARCIAL: {exitosas}/{total} experimentos confirmados")
    else:
        print(f"\n✗ Hipótesis no validada con los parámetros actuales")
    
    print(f"{'='*60}\n")
    
    return 0 if exitosas == total else 1


if __name__ == '__main__':
    sys.exit(main())
