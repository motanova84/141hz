#!/usr/bin/env python3
"""
ORQUESTADOR DE VALIDACIÓN RESILIENTE

Sistema orquestador que ejecuta todas las validaciones del proyecto,
utilizando el Agente Autónomo 141Hz para auto-recuperación en caso de fallos.

El orquestador:
- Descubre automáticamente scripts de validación
- Ejecuta cada validación con el agente autónomo
- Agrega resultados en un reporte consolidado
- Genera alertas y notificaciones
- Mantiene coherencia con la frecuencia 141Hz

Autor: Sistema de Orquestación Coherente 141Hz
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any
import subprocess

# Importar agente autónomo
from agente_autonomo_141hz import AgenteAutonomo141Hz, FrecuenciaCoherente141Hz


# Crear directorio de logs si no existe
Path('logs').mkdir(exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [ORQUESTADOR] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/orquestador_validacion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DescubridorValidaciones:
    """
    Descubre automáticamente scripts de validación en el repositorio.
    """
    
    PATRONES_VALIDACION = [
        'validate_*.py',
        'validacion_*.py',
        'verificacion_*.py',
        'test_*.py'
    ]
    
    EXCLUIR = [
        'test_dashboard.py',  # Tests de UI, no de validación científica
        '__init__.py',
        'agente_autonomo_141hz.py',
        'orquestador_validacion.py'
    ]
    
    def __init__(self, raiz: Path = None):
        self.raiz = raiz or Path('.')
        
    def descubrir(self) -> List[Dict[str, Any]]:
        """
        Descubre scripts de validación en el repositorio.
        
        Returns:
            Lista de diccionarios con información de cada script
        """
        logger.info("🔍 Descubriendo scripts de validación...")
        
        validaciones = []
        
        # Buscar en raíz
        for patron in self.PATRONES_VALIDACION:
            for script in self.raiz.glob(patron):
                if script.name not in self.EXCLUIR and script.is_file():
                    validaciones.append(self._analizar_script(script))
        
        # Buscar en subdirectorios
        for directorio in ['scripts', 'tests', 'src']:
            dir_path = self.raiz / directorio
            if dir_path.exists():
                for patron in self.PATRONES_VALIDACION:
                    for script in dir_path.glob(patron):
                        if script.name not in self.EXCLUIR and script.is_file():
                            validaciones.append(self._analizar_script(script))
        
        logger.info(f"✓ Encontrados {len(validaciones)} scripts de validación")
        
        return validaciones
    
    def _analizar_script(self, script: Path) -> Dict[str, Any]:
        """Analiza un script y extrae metadatos"""
        info = {
            'path': str(script),
            'nombre': script.name,
            'tipo': self._determinar_tipo(script.name),
            'prioridad': self._determinar_prioridad(script.name),
            'args_recomendados': self._determinar_args(script.name)
        }
        
        # Intentar extraer docstring
        try:
            with open(script, 'r', encoding='utf-8') as f:
                contenido = f.read()
                if '"""' in contenido:
                    inicio = contenido.find('"""') + 3
                    fin = contenido.find('"""', inicio)
                    if fin > inicio:
                        info['descripcion'] = contenido[inicio:fin].strip()[:200]
        except Exception:
            pass
        
        return info
    
    def _determinar_tipo(self, nombre: str) -> str:
        """Determina el tipo de validación"""
        if 'validate' in nombre or 'validacion' in nombre:
            return 'validacion_cientifica'
        elif 'verificacion' in nombre:
            return 'verificacion_sistema'
        elif 'test' in nombre:
            return 'test_unitario'
        return 'desconocido'
    
    def _determinar_prioridad(self, nombre: str) -> int:
        """Determina prioridad de ejecución (menor = más prioritario)"""
        # Validaciones core tienen mayor prioridad
        if 'coronacion' in nombre or 'v5' in nombre:
            return 1
        elif 'validate' in nombre or 'validacion' in nombre:
            return 2
        elif 'verificacion' in nombre:
            return 3
        else:
            return 4
    
    def _determinar_args(self, nombre: str) -> List[str]:
        """Determina argumentos recomendados para el script"""
        # Argumentos específicos para scripts conocidos
        if 'coronacion' in nombre or 'validate' in nombre:
            return ['--precision', '30']
        return []


class OrquestadorValidacion:
    """
    Orquestador principal que coordina todas las validaciones.
    """
    
    def __init__(self, max_intentos_por_script: int = 5):
        self.max_intentos = max_intentos_por_script
        self.descubridor = DescubridorValidaciones()
        self.frecuencia = FrecuenciaCoherente141Hz()
        self.resultados = []
        
        # Crear directorios
        Path('logs').mkdir(exist_ok=True)
        Path('results').mkdir(exist_ok=True)
        
        logger.info("=" * 80)
        logger.info("🎼 ORQUESTADOR DE VALIDACIÓN RESILIENTE")
        logger.info("   Alineado con frecuencia coherente: 141.7001 Hz")
        logger.info("=" * 80)
    
    def ejecutar_todas(self, filtro_tipo: str = None) -> Dict[str, Any]:
        """
        Ejecuta todas las validaciones descubiertas.
        
        Args:
            filtro_tipo: Opcional, filtrar por tipo de validación
            
        Returns:
            Diccionario con resultados consolidados
        """
        # Descubrir validaciones
        validaciones = self.descubridor.descubrir()
        
        # Filtrar si es necesario
        if filtro_tipo:
            validaciones = [v for v in validaciones if v['tipo'] == filtro_tipo]
            logger.info(f"🔍 Filtrado por tipo: {filtro_tipo} ({len(validaciones)} scripts)")
        
        # Ordenar por prioridad
        validaciones.sort(key=lambda x: x['prioridad'])
        
        logger.info(f"\n📋 Ejecutando {len(validaciones)} validaciones...\n")
        
        # Ejecutar cada validación
        for i, validacion in enumerate(validaciones, 1):
            logger.info("")
            logger.info("=" * 80)
            logger.info(f"📊 VALIDACIÓN {i}/{len(validaciones)}: {validacion['nombre']}")
            logger.info("=" * 80)
            
            # Ejecutar con agente autónomo
            exito = self._ejecutar_con_agente(validacion)
            
            # Registrar resultado
            self.resultados.append({
                'validacion': validacion,
                'exito': exito,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            # Pausa coherente entre validaciones
            if i < len(validaciones):
                logger.info("⏸️  Pausa de coherencia cuántica...")
                self.frecuencia.pausa_coherente(ciclos=100)
        
        # Generar reporte consolidado
        return self._generar_reporte_consolidado()
    
    def _ejecutar_con_agente(self, validacion: Dict[str, Any]) -> bool:
        """
        Ejecuta una validación usando el agente autónomo.
        
        Args:
            validacion: Info de la validación
            
        Returns:
            True si la validación pasa
        """
        # Crear agente para esta validación
        agente = AgenteAutonomo141Hz(max_intentos=self.max_intentos)
        
        # Ejecutar ciclo de auto-recuperación
        exito = agente.ciclo_auto_recuperacion(
            validacion['path'],
            validacion.get('args_recomendados', [])
        )
        
        # Guardar reporte del agente
        nombre_base = Path(validacion['path']).stem
        reporte_path = f"results/agente_{nombre_base}_report.json"
        agente.generar_reporte(reporte_path)
        
        return exito
    
    def _generar_reporte_consolidado(self) -> Dict[str, Any]:
        """Genera reporte consolidado de todas las validaciones"""
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 GENERANDO REPORTE CONSOLIDADO")
        logger.info("=" * 80)
        
        total = len(self.resultados)
        exitosos = sum(1 for r in self.resultados if r['exito'])
        fallidos = total - exitosos
        tasa_exito = (exitosos / total * 100) if total > 0 else 0
        
        reporte = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'frecuencia_alineacion': self.frecuencia.FRECUENCIA_BASE,
            'resumen': {
                'total_validaciones': total,
                'exitosas': exitosos,
                'fallidas': fallidos,
                'tasa_exito': tasa_exito
            },
            'resultados_detallados': self.resultados,
            'estado_global': 'EXITOSO' if fallidos == 0 else 'PARCIAL' if exitosos > 0 else 'FALLIDO'
        }
        
        # Guardar reporte
        reporte_path = Path('results/orquestador_consolidado.json')
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        # Mostrar resumen
        logger.info("")
        logger.info("📊 RESUMEN DE EJECUCIÓN:")
        logger.info(f"   Total de validaciones: {total}")
        logger.info(f"   ✅ Exitosas: {exitosos}")
        logger.info(f"   ❌ Fallidas: {fallidos}")
        logger.info(f"   📈 Tasa de éxito: {tasa_exito:.1f}%")
        logger.info(f"   🎯 Estado global: {reporte['estado_global']}")
        logger.info("")
        logger.info(f"📄 Reporte guardado: {reporte_path}")
        
        # Mostrar validaciones fallidas
        if fallidos > 0:
            logger.warning("")
            logger.warning("⚠️  VALIDACIONES FALLIDAS:")
            for resultado in self.resultados:
                if not resultado['exito']:
                    logger.warning(f"   ❌ {resultado['validacion']['nombre']}")
        
        return reporte
    
    def ejecutar_validacion_unica(self, script_path: str, args: List[str] = None) -> bool:
        """
        Ejecuta una sola validación específica.
        
        Args:
            script_path: Ruta al script
            args: Argumentos opcionales
            
        Returns:
            True si la validación pasa
        """
        logger.info(f"🎯 Ejecutando validación única: {script_path}")
        
        agente = AgenteAutonomo141Hz(max_intentos=self.max_intentos)
        exito = agente.ciclo_auto_recuperacion(script_path, args or [])
        
        # Guardar reporte
        nombre_base = Path(script_path).stem
        agente.generar_reporte(f"results/agente_{nombre_base}_report.json")
        
        return exito


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Orquestador de Validación Resiliente - Sistema 141Hz"
    )
    parser.add_argument(
        '--script',
        help="Ejecutar un script específico en lugar de descubrir todos"
    )
    parser.add_argument(
        '--args',
        nargs='*',
        default=[],
        help="Argumentos para el script específico"
    )
    parser.add_argument(
        '--tipo',
        choices=['validacion_cientifica', 'verificacion_sistema', 'test_unitario'],
        help="Filtrar por tipo de validación"
    )
    parser.add_argument(
        '--max-intentos',
        type=int,
        default=5,
        help="Máximo intentos por validación (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Crear orquestador
    orquestador = OrquestadorValidacion(max_intentos_por_script=args.max_intentos)
    
    # Ejecutar
    if args.script:
        # Validación única
        exito = orquestador.ejecutar_validacion_unica(args.script, args.args)
        sys.exit(0 if exito else 1)
    else:
        # Todas las validaciones
        reporte = orquestador.ejecutar_todas(filtro_tipo=args.tipo)
        
        # Exit code basado en estado global
        estado = reporte['estado_global']
        if estado == 'EXITOSO':
            sys.exit(0)
        elif estado == 'PARCIAL':
            sys.exit(1)
        else:
            sys.exit(2)


if __name__ == '__main__':
    main()
