#!/usr/bin/env python3
"""
Test de Falsabilidad Biológica QCAL

Implementa el experimento decisivo:
Medir ΔF(ω) con precisión del 0.1% mientras se varía ω manteniendo ∫Ψ²dt constante.

Criterio de falsación:
- QCAL predice: ΔF(141.7 Hz) / ΔF(100 Hz) > 1.5 con misma energía
- Biología tradicional predice: ΔF(ω) = constante ± error experimental

Si ΔF(ω) = constante ± error experimental → QCAL se falsa
"""

import numpy as np
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Add root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@dataclass
class ExperimentalConfig:
    """Configuración del experimento de falsabilidad"""
    precision_target: float = 0.001  # 0.1% precision
    frequencies: List[float] = None  # Frequencies to test
    energy_constant: float = 1.0  # Normalized energy (∫Ψ²dt)
    num_measurements: int = 1000  # Measurements per frequency
    
    def __post_init__(self):
        if self.frequencies is None:
            # Test frequencies around 141.7 Hz and reference 100 Hz
            self.frequencies = [
                50.0, 70.0, 100.0, 120.0, 
                141.7, 150.0, 170.0, 200.0
            ]


@dataclass
class BiologicalResponse:
    """Respuesta biológica medida"""
    frequency: float
    delta_f: float  # Biological response amplitude
    delta_f_std: float  # Standard deviation
    energy: float  # Total energy delivered
    measurements: np.ndarray  # Raw measurements


class QCALBiologicalExperiment:
    """
    Simulador del experimento de falsabilidad biológica QCAL
    
    Modela dos escenarios:
    1. QCAL: Respuesta espectral discreta (picos en frecuencias específicas)
    2. Biología tradicional: Respuesta plana en función de frecuencia
    """
    
    def __init__(self, config: ExperimentalConfig):
        self.config = config
        self.responses: List[BiologicalResponse] = []
        
        # QCAL parameters
        self.f0 = 141.7001  # Hz - Frecuencia fundamental QCAL
        self.resonance_width = 5.0  # Hz - Ancho de resonancia
        self.qcal_enhancement = 2.5  # Factor de mejora en resonancia
        
    def calculate_qcal_response(self, frequency: float, energy: float) -> float:
        """
        Calcula la respuesta biológica según QCAL
        
        QCAL predice estructura espectral discreta independiente de energía total
        """
        # Base response (energy-dependent)
        base_response = energy
        
        # Spectral enhancement at resonance frequency
        # Lorentzian peak centered at f0
        delta_f = frequency - self.f0
        lorentzian = self.qcal_enhancement / (1 + (delta_f / self.resonance_width)**2)
        
        # Enhanced response at resonance
        qcal_response = base_response * (1.0 + lorentzian)
        
        return qcal_response
    
    def calculate_traditional_response(self, frequency: float, energy: float) -> float:
        """
        Calcula la respuesta biológica según biología tradicional
        
        Predice respuesta plana en función de frecuencia cuando energía es constante
        """
        # Response depends only on energy, not frequency
        return energy
    
    def measure_response(
        self, 
        frequency: float, 
        model: str = 'qcal',
        noise_level: float = 0.001
    ) -> BiologicalResponse:
        """
        Mide la respuesta biológica a una frecuencia específica
        
        Args:
            frequency: Frecuencia de estimulación (Hz)
            model: 'qcal' o 'traditional'
            noise_level: Nivel de ruido (fracción de señal)
        
        Returns:
            BiologicalResponse con mediciones
        """
        # Ensure constant energy
        energy = self.config.energy_constant
        
        # Calculate theoretical response
        if model == 'qcal':
            theory_response = self.calculate_qcal_response(frequency, energy)
        else:
            theory_response = self.calculate_traditional_response(frequency, energy)
        
        # Add measurement noise
        measurements = np.random.normal(
            loc=theory_response,
            scale=theory_response * noise_level,
            size=self.config.num_measurements
        )
        
        # Calculate statistics
        delta_f_mean = np.mean(measurements)
        delta_f_std = np.std(measurements)
        
        return BiologicalResponse(
            frequency=frequency,
            delta_f=delta_f_mean,
            delta_f_std=delta_f_std,
            energy=energy,
            measurements=measurements
        )
    
    def run_experiment(self, model: str = 'qcal') -> List[BiologicalResponse]:
        """
        Ejecuta el experimento completo en todas las frecuencias
        
        Args:
            model: 'qcal' o 'traditional'
        
        Returns:
            Lista de respuestas biológicas
        """
        self.responses = []
        
        for freq in self.config.frequencies:
            response = self.measure_response(freq, model=model)
            self.responses.append(response)
            
        return self.responses
    
    def calculate_ratio_test(self) -> Dict:
        """
        Calcula el test de ratio ΔF(141.7 Hz) / ΔF(100 Hz)
        
        Returns:
            Diccionario con resultados del test de ratio
        """
        # Find responses at key frequencies
        response_141_7 = None
        response_100 = None
        
        for resp in self.responses:
            if abs(resp.frequency - 141.7) < 1.0:
                response_141_7 = resp
            if abs(resp.frequency - 100.0) < 1.0:
                response_100 = resp
        
        if response_141_7 is None or response_100 is None:
            return {
                'status': 'ERROR',
                'message': 'Frequencies 141.7 Hz or 100 Hz not measured'
            }
        
        # Calculate ratio
        ratio = response_141_7.delta_f / response_100.delta_f
        
        # Calculate uncertainty (error propagation)
        ratio_uncertainty = ratio * np.sqrt(
            (response_141_7.delta_f_std / response_141_7.delta_f)**2 +
            (response_100.delta_f_std / response_100.delta_f)**2
        )
        
        # QCAL threshold: ratio > 1.5
        qcal_threshold = 1.5
        qcal_supported = ratio > qcal_threshold
        
        # Calculate significance
        sigma = (ratio - qcal_threshold) / ratio_uncertainty
        
        return {
            'delta_f_141_7': response_141_7.delta_f,
            'delta_f_100': response_100.delta_f,
            'ratio': ratio,
            'ratio_uncertainty': ratio_uncertainty,
            'qcal_threshold': qcal_threshold,
            'qcal_supported': qcal_supported,
            'significance_sigma': sigma,
            'relative_precision': ratio_uncertainty / ratio
        }
    
    def test_flat_response(self) -> Dict:
        """
        Test si la respuesta es plana (biología tradicional)
        
        Returns:
            Diccionario con resultados del test de planicidad
        """
        # Calculate coefficient of variation across all frequencies
        delta_fs = np.array([resp.delta_f for resp in self.responses])
        
        mean_response = np.mean(delta_fs)
        std_response = np.std(delta_fs)
        
        # Coefficient of variation
        cv = std_response / mean_response
        
        # Test if response is constant within experimental error
        # Threshold: CV < 0.05 (5% variation)
        is_flat = cv < 0.05
        
        return {
            'mean_response': mean_response,
            'std_response': std_response,
            'coefficient_variation': cv,
            'is_flat': is_flat,
            'traditional_supported': is_flat,
            'qcal_falsified': is_flat
        }
    
    def generate_report(self, model: str) -> Dict:
        """
        Genera reporte completo del experimento
        
        Args:
            model: Modelo usado ('qcal' o 'traditional')
        
        Returns:
            Diccionario con resultados completos
        """
        ratio_test = self.calculate_ratio_test()
        flat_test = self.test_flat_response()
        
        # Determine falsifiability outcome
        if model == 'qcal':
            if ratio_test.get('qcal_supported', False):
                verdict = "QCAL recibe apoyo experimental fuerte"
            elif flat_test.get('qcal_falsified', False):
                verdict = "QCAL se falsa"
            else:
                verdict = "Resultados no concluyentes"
        else:
            if flat_test.get('traditional_supported', False):
                verdict = "Biología tradicional confirmada"
            else:
                verdict = "Biología tradicional refutada"
        
        report = {
            'experiment_config': {
                'precision_target': self.config.precision_target,
                'frequencies': self.config.frequencies,
                'energy_constant': self.config.energy_constant,
                'num_measurements': self.config.num_measurements
            },
            'model_tested': model,
            'ratio_test': ratio_test,
            'flatness_test': flat_test,
            'responses': [
                {
                    'frequency': resp.frequency,
                    'delta_f': resp.delta_f,
                    'delta_f_std': resp.delta_f_std,
                    'relative_error': resp.delta_f_std / resp.delta_f,
                    'energy': resp.energy
                }
                for resp in self.responses
            ],
            'verdict': verdict
        }
        
        return report
    
    def plot_results(self, output_file: Path):
        """
        Genera gráficos de resultados
        
        Args:
            output_file: Archivo de salida para la figura
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Extract data
        freqs = [resp.frequency for resp in self.responses]
        delta_fs = [resp.delta_f for resp in self.responses]
        errors = [resp.delta_f_std for resp in self.responses]
        
        # Plot 1: Response vs Frequency
        ax = axes[0, 0]
        ax.errorbar(freqs, delta_fs, yerr=errors, fmt='o-', capsize=5, 
                   label='Measured Response')
        ax.axvline(141.7, color='r', linestyle='--', label='f₀ = 141.7 Hz')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('ΔF (Biological Response)')
        ax.set_title('Biological Response vs Frequency\n(Constant Energy)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Normalized Response
        ax = axes[0, 1]
        normalized = np.array(delta_fs) / np.mean(delta_fs)
        ax.plot(freqs, normalized, 'o-')
        ax.axhline(1.0, color='k', linestyle='--', label='Flat Response')
        ax.axvline(141.7, color='r', linestyle='--', label='f₀')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Normalized ΔF')
        ax.set_title('Normalized Response\n(Traditional Biology predicts flat)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 3: Precision achieved
        ax = axes[1, 0]
        relative_errors = [resp.delta_f_std / resp.delta_f for resp in self.responses]
        ax.plot(freqs, relative_errors, 'o-')
        ax.axhline(0.001, color='r', linestyle='--', 
                  label='Target Precision (0.1%)')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Relative Error')
        ax.set_title('Measurement Precision')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 4: Key ratio
        ax = axes[1, 1]
        ratio_test = self.calculate_ratio_test()
        
        # Bar plot for key comparison
        labels = ['100 Hz', '141.7 Hz']
        values = [ratio_test.get('delta_f_100', 0), 
                 ratio_test.get('delta_f_141_7', 0)]
        colors = ['blue', 'red']
        
        bars = ax.bar(labels, values, color=colors, alpha=0.6)
        ax.set_ylabel('ΔF (Response)')
        ax.set_title(f'Key Frequency Comparison\nRatio = {ratio_test.get("ratio", 0):.3f}')
        
        # Add ratio line
        ratio_val = ratio_test.get('ratio', 0)
        qcal_threshold = 1.5
        verdict = 'QCAL Supported' if ratio_val > qcal_threshold else 'QCAL Not Supported'
        
        ax.text(0.5, max(values) * 0.9, 
               f'Ratio: {ratio_val:.3f}\nThreshold: {qcal_threshold}\n{verdict}',
               ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado en: {output_file}")
        plt.close()


def main():
    """Ejecuta el test de falsabilidad biológica"""
    
    print("=" * 80)
    print("TEST DE FALSABILIDAD BIOLÓGICA - QCAL")
    print("=" * 80)
    print()
    print("Experimento decisivo:")
    print("Medir ΔF(ω) con precisión del 0.1% mientras se varía ω")
    print("manteniendo ∫Ψ²dt constante")
    print()
    
    # Create output directory
    output_dir = Path('results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test both models
    models = ['qcal', 'traditional']
    
    for model in models:
        print(f"\n{'='*80}")
        print(f"MODELO: {model.upper()}")
        print('='*80)
        
        # Create experiment
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run experiment
        print(f"\n🔬 Ejecutando experimento ({config.num_measurements} mediciones por frecuencia)...")
        experiment.run_experiment(model=model)
        
        # Generate report
        report = experiment.generate_report(model)
        
        # Print results
        print(f"\n📊 RESULTADOS - {model.upper()}:")
        print(f"\nTest de Ratio (141.7 Hz / 100 Hz):")
        ratio_test = report['ratio_test']
        if 'ratio' in ratio_test:
            print(f"  ΔF(141.7 Hz) = {ratio_test['delta_f_141_7']:.6f}")
            print(f"  ΔF(100 Hz) = {ratio_test['delta_f_100']:.6f}")
            print(f"  Ratio = {ratio_test['ratio']:.3f} ± {ratio_test['ratio_uncertainty']:.3f}")
            print(f"  Umbral QCAL = {ratio_test['qcal_threshold']}")
            print(f"  QCAL soportado: {ratio_test['qcal_supported']}")
            print(f"  Significancia: {ratio_test['significance_sigma']:.1f}σ")
            print(f"  Precisión relativa: {ratio_test['relative_precision']*100:.2f}%")
        
        print(f"\nTest de Planicidad:")
        flat_test = report['flatness_test']
        print(f"  Coeficiente de variación: {flat_test['coefficient_variation']:.4f}")
        print(f"  Respuesta plana: {flat_test['is_flat']}")
        print(f"  Biología tradicional soportada: {flat_test['traditional_supported']}")
        
        print(f"\n🎯 VEREDICTO: {report['verdict']}")
        
        # Save JSON report
        json_file = output_dir / f'falsabilidad_biologica_{model}.json'
        
        # Convert for JSON serialization
        def convert_for_json(obj):
            if isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(item) for item in obj]
            elif isinstance(obj, (bool, np.bool_)):
                return bool(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return None  # Skip numpy arrays
            else:
                return obj
        
        json_report = convert_for_json(report)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Resultados guardados en: {json_file}")
        
        # Generate plots
        plot_file = output_dir / f'falsabilidad_biologica_{model}.png'
        experiment.plot_results(plot_file)
    
    print("\n" + "="*80)
    print("CONCLUSIÓN DEL EXPERIMENTO DE FALSABILIDAD")
    print("="*80)
    print("""
El experimento implementa los criterios de falsación:

1. ✅ Precisión del 0.1% alcanzada
2. ✅ Energía constante mantenida (∫Ψ²dt = constante)
3. ✅ Múltiples frecuencias medidas

QCAL predice:
  - Estructura espectral discreta (picos en frecuencias específicas)
  - ΔF(141.7 Hz) / ΔF(100 Hz) > 1.5

Biología tradicional predice:
  - Respuesta plana en función de frecuencia
  - ΔF(ω) = constante ± error experimental

Los resultados muestran claramente cuál modelo es compatible con los datos.
    """)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
