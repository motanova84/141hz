#!/usr/bin/env python3
"""
Orquestador de Predicciones Falsables QCAL ∞³

Este script ejecuta las cuatro predicciones falsables derivadas del marco
teórico QCAL ∞³ y genera un informe consolidado.

Predicciones:
1. Corrección Yukawa al potencial gravitacional (λ_Ψ ≈ 2.1 km)
2. Pico resonante en BEC (k₀ ≈ 890 m⁻¹)
3. Correlación temporal en H → invisible (Δt = n × 7.06 ms)
4. Modulación gravitacional a 141.7001 Hz (δg ∼ 10⁻¹³-10⁻¹² g)

Autor: José Manuel Mota Burruezo
Instituto de Conciencia Cuántica (ICQ)
Zenodo DOI: 10.5281/zenodo.17887499
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from utils import setup_logging
    logger = setup_logging()
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class PredictionsOrchestrator:
    """
    Orquestador que ejecuta todas las predicciones QCAL ∞³.
    """
    
    def __init__(self, output_dir: Path = None):
        """
        Inicializa el orquestador.
        
        Args:
            output_dir: Directorio para guardar resultados
        """
        self.output_dir = output_dir or Path("results")
        self.output_dir.mkdir(exist_ok=True)
        
        self.scripts_dir = Path(__file__).parent
        
        # Definir predicciones
        self.predictions = {
            "prediccion_1_yukawa": {
                "name": "Corrección Yukawa al Potencial Gravitacional",
                "script": "validacion_prediccion_1_yukawa.py",
                "description": "Campo Ψ modifica potencial gravitatorio con λ_Ψ ≈ 2.1 km",
                "scale": "Subterrestre (1-10 km)",
                "falsification": "Ausencia de desviaciones para α > 10⁻⁵"
            },
            "prediccion_2_bec": {
                "name": "Pico Resonante en Condensados de Bose-Einstein",
                "script": "validacion_prediccion_2_bec.py",
                "description": "Resonancia en fonones BEC con k₀ ≈ 890 m⁻¹",
                "scale": "Cuántica (condensados BEC)",
                "falsification": "Ausencia de pico en ≥3 experimentos independientes"
            },
            "prediccion_3_higgs": {
                "name": "Correlación Temporal en Eventos Higgs Invisibles",
                "script": "validacion_prediccion_3_higgs.py",
                "description": "Estructura temporal discreta Δt = n × 7.06 ms en H → ΨΨ",
                "scale": "Colisionador de partículas (LHC)",
                "falsification": "p-value > 0.001 en todas las ventanas"
            },
            "prediccion_4_gravedad": {
                "name": "Modulación Gravitacional Persistente a 141.7001 Hz",
                "script": "validacion_prediccion_4_gravedad.py",
                "description": "Oscilación en aceleración local δg ∼ 10⁻¹³-10⁻¹² g",
                "scale": "Gravimetría de alta precisión",
                "falsification": "Ausencia de todos los criterios en múltiples estaciones"
            },
            "prediccion_einstein_qcal_e1": {
                "name": "QCAL-E1: Anomalía de Fase Interferométrica",
                "script": "validacion_prediccion_einstein_qcal_e1.py",
                "description": "Línea interferométrica exacta en 141.7001 Hz con retardo de fase dependiente de Ψ",
                "scale": "Interferometría Fabry-Pérot / detectores GW",
                "falsification": "Ausencia de pico, desviación > ±0.0001 Hz o insensibilidad a ΔΨ"
            }
        }
    
    def run_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """
        Ejecuta una predicción específica.
        
        Args:
            prediction_id: Identificador de la predicción
        
        Returns:
            Diccionario con resultados
        """
        prediction = self.predictions[prediction_id]
        script_path = self.scripts_dir / prediction["script"]
        
        logger.info(f"Ejecutando {prediction['name']}...")
        logger.info(f"Script: {script_path}")
        
        try:
            # Ejecutar script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            # Leer resultado JSON
            json_file = self.output_dir / f"{prediction_id}.json"
            if json_file.exists():
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                return {
                    "success": result.returncode == 0,
                    "returncode": result.returncode,
                    "data": data,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            else:
                logger.warning(f"Archivo JSON no encontrado: {json_file}")
                return {
                    "success": False,
                    "returncode": result.returncode,
                    "data": None,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "error": "JSON file not found"
                }
        
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout ejecutando {prediction['name']}")
            return {
                "success": False,
                "error": "Timeout",
                "data": None
            }
        
        except Exception as e:
            logger.error(f"Error ejecutando {prediction['name']}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def run_all_predictions(self) -> Dict[str, Any]:
        """
        Ejecuta todas las predicciones.
        
        Returns:
            Diccionario con resultados consolidados
        """
        logger.info("=" * 80)
        logger.info("INICIANDO VALIDACIÓN DE PREDICCIONES QCAL ∞³")
        logger.info("=" * 80)
        logger.info("")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "framework": "QCAL ∞³",
            "predictions": {},
            "summary": {
                "total": len(self.predictions),
                "successful": 0,
                "failed": 0,
                "validated": 0
            }
        }
        
        # Ejecutar cada predicción
        for pred_id, pred_info in self.predictions.items():
            logger.info(f"\n{'='*80}")
            logger.info(f"PREDICCIÓN: {pred_info['name']}")
            logger.info(f"{'='*80}")
            
            result = self.run_prediction(pred_id)
            
            if result["success"]:
                results["summary"]["successful"] += 1
                logger.info(f"✓ Predicción {pred_id} ejecutada exitosamente")
                
                # Verificar si está validada
                if result["data"] and "overall_status" in result["data"]:
                    status = result["data"]["overall_status"]
                    if status.startswith("✓"):
                        results["summary"]["validated"] += 1
                        logger.info(f"✓ Predicción {pred_id} VALIDADA")
            else:
                results["summary"]["failed"] += 1
                logger.error(f"✗ Error en predicción {pred_id}")
                if "error" in result:
                    logger.error(f"  Error: {result['error']}")
            
            results["predictions"][pred_id] = {
                "name": pred_info["name"],
                "description": pred_info["description"],
                "scale": pred_info["scale"],
                "falsification_criterion": pred_info["falsification"],
                "execution_result": result
            }
        
        return results
    
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Genera informe resumido en formato texto.
        
        Args:
            results: Resultados consolidados
        
        Returns:
            Informe en texto plano
        """
        report = []
        report.append("=" * 80)
        report.append("INFORME DE PREDICCIONES FALSABLES QCAL ∞³")
        report.append("=" * 80)
        report.append("")
        report.append(f"Fecha: {results['timestamp']}")
        report.append(f"Marco Teórico: {results['framework']}")
        report.append("")
        report.append("RESUMEN EJECUTIVO")
        report.append("-" * 80)
        summary = results["summary"]
        report.append(f"Total de predicciones:    {summary['total']}")
        report.append(f"Ejecutadas exitosamente:  {summary['successful']}")
        report.append(f"Validadas:                {summary['validated']}")
        report.append(f"Fallidas:                 {summary['failed']}")
        report.append("")
        
        # Detalles de cada predicción
        report.append("DETALLES POR PREDICCIÓN")
        report.append("=" * 80)
        
        for pred_id, pred_data in results["predictions"].items():
            report.append("")
            report.append(f"Predicción: {pred_data['name']}")
            report.append("-" * 80)
            report.append(f"Descripción: {pred_data['description']}")
            report.append(f"Escala: {pred_data['scale']}")
            report.append(f"Criterio de falsación: {pred_data['falsification_criterion']}")
            report.append("")
            
            exec_result = pred_data["execution_result"]
            if exec_result["success"]:
                report.append("Estado de ejecución: ✓ EXITOSA")
                
                if exec_result["data"]:
                    data = exec_result["data"]
                    report.append(f"Estado de validación: {data.get('overall_status', 'N/A')}")
                    
                    # Parámetros clave
                    if "parameters" in data:
                        report.append("\nParámetros clave:")
                        params = data["parameters"]
                        for key, value in list(params.items())[:5]:  # Primeros 5 parámetros
                            report.append(f"  {key}: {value}")
            else:
                report.append("Estado de ejecución: ✗ FALLIDA")
                if "error" in exec_result:
                    report.append(f"Error: {exec_result['error']}")
            
            report.append("")
        
        # Conclusión
        report.append("=" * 80)
        report.append("CONCLUSIÓN")
        report.append("=" * 80)
        report.append("")
        report.append("El marco QCAL ∞³ genera predicciones falsables, cuantitativas y testables")
        report.append("en dominios experimentales diversos:")
        report.append("")
        report.append("  • Gravedad subterrestre (1-10 km)")
        report.append("  • Condensados cuánticos (BEC)")
        report.append("  • Física de partículas (LHC)")
        report.append("  • Gravimetría de alta precisión")
        report.append("")
        report.append("Cada predicción vincula estructura simbólica y vibracional con plataformas")
        report.append("físicas concretas, permitiendo validación o refutación experimental.")
        report.append("")
        report.append("Referencia: Zenodo DOI 10.5281/zenodo.17887499")
        report.append("Autor: José Manuel Mota Burruezo, Instituto de Conciencia Cuántica (ICQ)")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, results: Dict[str, Any]):
        """
        Guarda resultados consolidados.
        
        Args:
            results: Resultados a guardar
        """
        # Guardar JSON consolidado
        json_file = self.output_dir / "predicciones_qcal_consolidado.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Resultados JSON guardados en {json_file}")
        
        # Guardar informe de texto
        report = self.generate_summary_report(results)
        report_file = self.output_dir / "predicciones_qcal_informe.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        logger.info(f"Informe de texto guardado en {report_file}")
        
        # Imprimir resumen en consola
        print("\n" + report)


def main():
    """
    Función principal.
    """
    parser = argparse.ArgumentParser(
        description="Orquestador de Predicciones Falsables QCAL ∞³"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directorio para guardar resultados (default: results)"
    )
    parser.add_argument(
        "--prediction",
        type=str,
        choices=["1", "2", "3", "4", "all"],
        default="all",
        help="Predicción específica a ejecutar (default: all)"
    )
    
    args = parser.parse_args()
    
    # Crear orquestador
    output_dir = Path(args.output_dir)
    orchestrator = PredictionsOrchestrator(output_dir=output_dir)
    
    # Ejecutar predicción(es)
    if args.prediction == "all":
        results = orchestrator.run_all_predictions()
    else:
        pred_id = f"prediccion_{args.prediction}_" + {
            "1": "yukawa",
            "2": "bec",
            "3": "higgs",
            "4": "gravedad"
        }[args.prediction]
        
        result = orchestrator.run_prediction(pred_id)
        results = {
            "timestamp": datetime.now().isoformat(),
            "framework": "QCAL ∞³",
            "predictions": {pred_id: {
                **orchestrator.predictions[pred_id],
                "execution_result": result
            }},
            "summary": {
                "total": 1,
                "successful": 1 if result["success"] else 0,
                "failed": 0 if result["success"] else 1,
                "validated": 1 if (result["success"] and result["data"] and 
                                 result["data"].get("overall_status", "").startswith("✓")) else 0
            }
        }
    
    # Guardar resultados
    orchestrator.save_results(results)
    
    # Retornar código de salida
    summary = results["summary"]
    if summary["failed"] > 0:
        return 1
    elif summary["validated"] == summary["total"]:
        return 0
    else:
        return 2  # Ejecutado pero no todas las predicciones validadas


if __name__ == "__main__":
    sys.exit(main())
