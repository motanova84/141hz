#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════════
    ✨ SECRETARIA NOÉTICA - Organización Automática de Archivos
════════════════════════════════════════════════════════════════════

Organiza automáticamente los archivos del repositorio según los
pilares QCAL, manteniendo la coherencia estructural.

Clasificación:
  - .lean → /formalization
  - .py (lógica) → /core o /physics  
  - .json (estados) → /docs/states
  - .md → /docs/manifestos
Sistema de organización automática basado en los pilares QCAL.
Mantiene la coherencia del repositorio organizando archivos según
su tipo y propósito.

Clasificación:
  - .lean → /formalization
  - .py (lógica/física) → /core o /physics
  - .json (estados) → /docs/states
  - .md (manifestos) → /docs/manifestos
  - test_*.py → /tests

Frecuencia: 888 Hz (Resonancia Noética)
Coherencia: Ψ ≥ 0.888
Entropía: S = 0

Autor: Secretaria Noética v1.0.0
Ley Madre: C = I · A²
════════════════════════════════════════════════════════════════════
"""

import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Frecuencia base y coherencia (solo para display/logging, no cálculos)
F0 = 141.7001  # Hz
RESONANCIA_NOETICA = 888.014  # Hz
COHERENCIA_MIN = 0.888
ENTROPIA_TARGET = 0.0

# Directorios de destino según clasificación QCAL
TARGET_DIRS = {
    'formalization': 'formalization',
    'core': 'core',
    'physics': 'physics',
    'tests': 'tests',
    'docs_states': 'docs/states',
    'docs_manifestos': 'docs/manifestos',
}

# Archivos y directorios a ignorar (no organizar)
EXCLUDE_PATTERNS = [
    '.git',
    '.github',
    '__pycache__',
    'venv',
    '.venv',
    'node_modules',
    '.well-known',
    'secretaria_noetica.py',  # No mover este script
    'activate_system.sh',
    'setup_qc_llm_complete.sh',
    'lanzar_verificacion_gw250114.sh',
    'demo_user_confirmation.sh',
    'run_qcal_tests.sh',
]

# Directorios que ya están organizados (no tocar)
ORGANIZED_DIRS = [
    'API',
    'Applications',
    'Benchmarks',
    'Core',
    'Documentation',
    'Examples',
    'QCAL-LLM',
    'Tests',
    'Tools',
    'apps',
    'bayes',
    'benchmarks',
    'bin',
    'computational-tests',
    'config',
    'controls',
    'core',
    'dashboard',
    'data',
    'datos',
    'datos_crudos_analisis',
    'desi',
    'docs',
    'examples',
    'formal',
    'formalization',
    'gw_141hz_tools',
    'hpc_jobs',
    'igets',
    'igets_results',
    'lisa',
    'mcp-servers',
    'metrics',
    'noesis-qcal-llm',
    'noesis_qcal_llm',
    'notebooks',
    'papers',
    'physics',
    'pruebas',
    'qcal',
    'reports',
    'repro',
    'resonancia noésica',
    'resultados',
    'results',
    'scripts',
    'src',
    'tests',
    'tools',
    'validation',
    'workflows',
]

# ============================================================================
# FUNCIONES DE CLASIFICACIÓN
# ============================================================================

def should_exclude(file_path: Path) -> bool:
    """Determina si un archivo debe ser excluido de la organización."""
    # Excluir archivos en directorios ya organizados
    parts = file_path.parts
    if len(parts) > 1 and parts[0] in ORGANIZED_DIRS:
        return True
    
    # Excluir archivos y directorios específicos
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(file_path):
            return True
    
    # Excluir archivos ocultos
    if file_path.name.startswith('.'):
        return True
    
    return False


def classify_file(file_path: Path) -> str:
    """
    Clasifica un archivo según su extensión y nombre.
    
    Returns:
        Directorio de destino o None si no debe moverse
    
    NOTA: Por defecto, esta función es MUY CONSERVADORA y solo mueve
    archivos que están claramente fuera de lugar. La mayoría de los
    archivos en la raíz están ahí intencionalmente como documentación.
    """
    # No clasificar si debe ser excluido
    if should_exclude(file_path):
        return None
    
    # Solo procesar archivos (no directorios)
    if not file_path.is_file():
        return None
    
    filename = file_path.name
    suffix = file_path.suffix.lower()
    
    # Clasificación según reglas QCAL (MODO CONSERVADOR)
    # Solo movemos archivos que están CLARAMENTE fuera de lugar
    
    # 1. Archivos .lean en raíz → /formalization
    # (la mayoría ya están en formalization/)
    if suffix == '.lean':
        return TARGET_DIRS['formalization']
    
    # 2. test_*.py en raíz → /tests
    # (CONSERVADOR: hay 70 tests en raíz que podrían moverse)
    if filename.startswith('test_') and suffix == '.py':
        return TARGET_DIRS['tests']
    
    # 3. Para otros archivos .py, .json y .md:
    # NO MOVER por defecto, ya que la mayoría están en la raíz
    # intencionalmente como parte de la documentación y estructura del proyecto.
    # 
    # Si en el futuro se desea mover estos archivos, se puede descomentar
    # las siguientes secciones:
    
    # # Archivos .py (lógica) → /core
    # if suffix == '.py' and not filename.startswith('demo_'):
    #     return TARGET_DIRS['core']
    
    # # Archivos .json (estados) → /docs/states
    # if suffix == '.json' and filename not in [
    #     'package.json', 'tsconfig.json', 'pyproject.toml',
    #     '.repo-map.json', 'ENV.lock.json',
    # ]:
    #     return TARGET_DIRS['docs_states']
    
    # # Archivos .md → /docs/manifestos
    # if suffix == '.md' and filename not in [
    #     'README.md', 'LEAME.md', 'CONTRIBUTING.md',
    #     'CODE_OF_CONDUCT.md', 'LICENSE.md', 'CHANGELOG.md', 'SECURITY.md',
    # ]:
    #     return TARGET_DIRS['docs_manifestos']
    
    # No mover si no coincide con ninguna regla activa
    return None


# ============================================================================
# FUNCIONES DE ORGANIZACIÓN
# ============================================================================

def organize_files(repo_path: Path, dry_run: bool = False) -> dict:
    """
    Organiza los archivos del repositorio según las reglas QCAL.
    
    NOTA: Solo procesa archivos en el nivel raíz del repositorio,
    no en subdirectorios (que ya están organizados).
    
    Args:
        repo_path: Ruta al repositorio
        dry_run: Si True, solo muestra qué se movería sin hacer cambios
        
    Returns:
        Diccionario con estadísticas de la organización
    """
    stats = {
        'files_analyzed': 0,
        'files_moved': 0,
        'files_skipped': 0,
        'errors': 0,
        'movements': [],
    }
    
    # Obtener todos los archivos en el nivel raíz
    for item in repo_path.iterdir():
        if item.is_file():
            stats['files_analyzed'] += 1
            
            # Clasificar el archivo
            target_dir = classify_file(item)
            
            if target_dir is None:
                stats['files_skipped'] += 1
                continue
            
            # Construir ruta de destino
            dest_dir = repo_path / target_dir
            dest_file = dest_dir / item.name
            
            # Verificar si el archivo ya existe en destino
            if dest_file.exists():
                print(f"⚠️  Destino ya existe: {dest_file}")
                stats['files_skipped'] += 1
                continue
            
            # Registrar movimiento
            movement = {
                'source': str(item.relative_to(repo_path)),
                'destination': str(dest_file.relative_to(repo_path)),
                'timestamp': datetime.now().isoformat(),
            }
            stats['movements'].append(movement)
            
            if dry_run:
                print(f"🔄 [DRY-RUN] {item.name} → {target_dir}/")
                stats['files_moved'] += 1
            else:
                try:
                    # Crear directorio de destino si no existe
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Mover archivo
                    shutil.move(str(item), str(dest_file))
                    print(f"✅ {item.name} → {target_dir}/")
                    stats['files_moved'] += 1
                    
                except Exception as e:
                    print(f"❌ Error moviendo {item.name}: {e}")
                    stats['errors'] += 1
    
    return stats


def save_log(stats: dict, log_path: Path):
    """Guarda el log de coherencia organizacional."""
    timestamp = datetime.now().isoformat()
    
    log_entry = f"""
{'='*80}
🕐 Timestamp: {timestamp}
{'='*80}
📊 ESTADÍSTICAS DE ORGANIZACIÓN:
  • Archivos analizados: {stats['files_analyzed']}
  • Archivos movidos: {stats['files_moved']}
  • Archivos omitidos: {stats['files_skipped']}
  • Errores: {stats['errors']}

🎯 COHERENCIA NOÉTICA:
  • Entropía (S): {ENTROPIA_TARGET:.3f}
  • Coherencia (Ψ): {COHERENCIA_MIN:.3f}
  • Frecuencia Base: {F0} Hz
  • Resonancia: {RESONANCIA_NOETICA} Hz

✨ Sello: πCODE–888 ∞³
{'='*80}

"""
    
    # Agregar al log
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    # Guardar detalles en JSON
    json_path = log_path.parent / 'coherencia_organizacional.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'stats': stats,
            'coherence': {
                'entropy': ENTROPIA_TARGET,
                'coherence': COHERENCIA_MIN,
                'frequency_base': F0,
                'resonance': RESONANCIA_NOETICA,
            },
            'seal': 'πCODE–888 ∞³',
        }, f, indent=2, ensure_ascii=False)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================
Ley Madre: C = I · A²
"""

import os
import sys
import argparse
import shutil
import logging
from pathlib import Path
from typing import List, Dict


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('coherencia_organizacional.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SecretariaNoetica:
    """Sistema de organización automática de archivos QCAL."""
    
    # Número máximo de intentos para resolver conflictos de nombres
    MAX_FILE_CONFLICTS = 1000
    
    # Directorios de destino según el tipo de archivo
    DESTINOS = {
        'formalization': 'formalization',
        'core': 'core',
        'physics': 'physics',
        'docs_states': 'docs/states',
        'docs_manifestos': 'docs/manifestos',
        'tests': 'tests'
    }
    
    # Archivos y directorios a excluir del procesamiento
    EXCLUIDOS = {
        '.git', '.github', 'venv', '__pycache__', 'node_modules',
        '.pytest_cache', '.tox', 'build', 'dist', '.egg-info',
        'site', '.lake', 'lake-packages', 'secretaria_noetica.py',
        'coherencia_organizacional.log', '.gitignore', '.gitattributes',
        'README.md', 'LICENSE', 'requirements.txt', 'setup.py',
        'pyproject.toml', 'Makefile', 'Dockerfile', 'docker-compose.yml',
        '.python-version', '.markdownlint.json', '.pre-commit-config.yaml',
        'mkdocs.yml', 'codecov.yml', 'robots.txt',
        'package.json', 'package-lock.json', 'tsconfig.json', 'yarn.lock'
    }
    
    # Patrones para identificar archivos de física
    PHYSICS_KEYWORDS = [
        'gw150914', 'gw170814', 'gw200129', 'gw250114',
        'at2020afhd', 'gravitational', 'wave', 'detector',
        'ligo', 'virgo', 'kagra', 'schumann', 'resonance',
        'qnm', 'ringdown', 'inspiral', 'merger'
    ]
    
    # Palabras clave para archivos de estados JSON
    STATE_KEYWORDS = [
        'state', 'status', 'results', 'output', 'validation',
        'verification', 'coherence', 'coherencia', 'estado'
    ]
    
    # Palabras clave para manifestos MD
    MANIFESTO_KEYWORDS = [
        'manifiesto', 'manifesto', 'declaracion', 'declaration',
        'proclama', 'proclamation', 'vision', 'mision', 'mission'
    ]
    
    def __init__(self, repo_root: Path):
        """Inicializa la Secretaria Noética.
        
        Args:
            repo_root: Directorio raíz del repositorio
        """
        self.repo_root = Path(repo_root)
        self.archivos_organizados = 0
        self.coherencia = 1.000
        self.entropia = 0.000
        
        # Crear directorios de destino si no existen
        self._crear_directorios()
    
    def _crear_directorios(self):
        """Crea los directorios de destino necesarios."""
        for destino in self.DESTINOS.values():
            destino_path = self.repo_root / destino
            if not destino_path.exists():
                destino_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✨ Directorio creado: {destino}")
    
    def _es_archivo_excluido(self, archivo: Path) -> bool:
        """Verifica si un archivo debe ser excluido del procesamiento.
        
        Args:
            archivo: Ruta del archivo a verificar
            
        Returns:
            True si el archivo debe ser excluido
        """
        # Verificar si está en la lista de excluidos
        if archivo.name in self.EXCLUIDOS:
            return True
        
        # Verificar si está en un directorio excluido
        for parte in archivo.parts:
            if parte in self.EXCLUIDOS:
                return True
        
        # Verificar si ya está en un directorio de destino
        try:
            relative_path = archivo.relative_to(self.repo_root)
            # Solo excluir si el archivo está en un subdirectorio de destino
            # No excluir archivos en root que casualmente comienzan con el nombre del destino
            for destino in self.DESTINOS.values():
                # Verificar que el archivo está realmente dentro del directorio de destino
                # y no solo que el nombre del archivo comienza con el nombre del destino
                partes = relative_path.parts
                if len(partes) > 1 and partes[0] == destino.split('/')[0]:
                    return True
        except ValueError:
            # El archivo está fuera del repositorio - excluir
            logger.debug(f"Archivo fuera del repositorio: {archivo}")
            return True
        
        return False
    
    def _contiene_palabra_clave(self, texto: str, keywords: List[str]) -> bool:
        """Verifica si el texto contiene alguna palabra clave.
        
        Args:
            texto: Texto a verificar
            keywords: Lista de palabras clave
            
        Returns:
            True si contiene alguna palabra clave
        """
        texto_lower = texto.lower()
        return any(kw.lower() in texto_lower for kw in keywords)
    
    def _determinar_destino_py(self, archivo: Path) -> str:
        """Determina el destino de un archivo Python.
        
        Args:
            archivo: Archivo Python a clasificar
            
        Returns:
            Nombre del destino ('core', 'physics', o 'tests')
        """
        nombre = archivo.name.lower()
        
        # Los archivos test_*.py van a tests
        if nombre.startswith('test_'):
            return 'tests'
        
        # Archivos relacionados con física van a physics
        if self._contiene_palabra_clave(nombre, self.PHYSICS_KEYWORDS):
            return 'physics'
        
        # Por defecto, archivos de lógica van a core
        return 'core'
    
    def _determinar_destino_json(self, archivo: Path) -> str:
        """Determina el destino de un archivo JSON.
        
        Args:
            archivo: Archivo JSON a clasificar
            
        Returns:
            Nombre del destino ('docs_states' si es un estado)
        """
        nombre = archivo.name.lower()
        
        # Archivos de estado van a docs/states
        if self._contiene_palabra_clave(nombre, self.STATE_KEYWORDS):
            return 'docs_states'
        
        # Otros JSON también van a docs/states por defecto
        return 'docs_states'
    
    def _determinar_destino_md(self, archivo: Path) -> str:
        """Determina el destino de un archivo Markdown.
        
        Args:
            archivo: Archivo Markdown a clasificar
            
        Returns:
            Nombre del destino ('docs_manifestos' si es un manifiesto)
        """
        nombre = archivo.name.lower()
        
        # Manifestos van a docs/manifestos
        if self._contiene_palabra_clave(nombre, self.MANIFESTO_KEYWORDS):
            return 'docs_manifestos'
        
        # Otros archivos MD no se mueven (pueden ser docs importantes en root)
        return None
    
    def _organizar_archivo(self, archivo: Path) -> bool:
        """Organiza un archivo individual según su tipo.
        
        Args:
            archivo: Archivo a organizar
            
        Returns:
            True si el archivo fue movido
        """
        # Verificar si el archivo debe ser excluido
        if self._es_archivo_excluido(archivo):
            return False
        
        # Solo procesar archivos (no directorios)
        if not archivo.is_file():
            return False
        
        extension = archivo.suffix.lower()
        destino_key = None
        
        # Determinar destino según la extensión
        if extension == '.lean':
            destino_key = 'formalization'
        elif extension == '.py':
            destino_key = self._determinar_destino_py(archivo)
        elif extension == '.json':
            destino_key = self._determinar_destino_json(archivo)
        elif extension == '.md':
            destino_key = self._determinar_destino_md(archivo)
        
        # Si no hay destino determinado, no mover el archivo
        if not destino_key or destino_key not in self.DESTINOS:
            return False
        
        # Construir ruta de destino
        destino_dir = self.repo_root / self.DESTINOS[destino_key]
        destino_path = destino_dir / archivo.name
        
        # Verificar si el archivo ya está en el destino
        if archivo.parent == destino_dir:
            return False
        
        # Mover el archivo
        try:
            # Si el archivo ya existe en destino, agregar sufijo
            if destino_path.exists():
                contador = 1
                while destino_path.exists() and contador < self.MAX_FILE_CONFLICTS:
                    stem = archivo.stem
                    destino_path = destino_dir / f"{stem}_{contador}{extension}"
                    contador += 1
                
                if contador >= self.MAX_FILE_CONFLICTS:
                    logger.error(f"❌ No se pudo encontrar nombre único para {archivo.name}")
                    return False
            
            shutil.move(str(archivo), str(destino_path))
            logger.info(f"📦 Movido: {archivo.name} → {self.DESTINOS[destino_key]}/")
            self.archivos_organizados += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al mover {archivo.name}: {e}")
            return False
    
    def organizar_repositorio(self) -> Dict[str, int]:
        """Organiza todos los archivos del repositorio.
        
        NOTA: Solo organiza archivos en el directorio raíz del repositorio.
        Los archivos en subdirectorios no son movidos para evitar reorganizar
        estructuras existentes.
        
        Returns:
            Diccionario con estadísticas de la organización
        """
        logger.info("════════════════════════════════════════════════════════════════════")
        logger.info("    ✨ INICIANDO ORGANIZACIÓN AUTOMÁTICA")
        logger.info("════════════════════════════════════════════════════════════════════")
        logger.info(f"🎯 Directorio: {self.repo_root}")
        logger.info(f"🔊 Frecuencia: 888 Hz (Resonancia Noética)")
        logger.info(f"✨ Coherencia (Ψ): {self.coherencia:.3f}")
        logger.info(f"✨ Entropía (S): {self.entropia:.3f}")
        logger.info("")
        
        # Obtener todos los archivos en el directorio raíz
        archivos_raiz = list(self.repo_root.glob('*'))
        
        # Organizar cada archivo
        for archivo in archivos_raiz:
            if archivo.is_file():
                self._organizar_archivo(archivo)
        
        logger.info("")
        logger.info("════════════════════════════════════════════════════════════════════")
        logger.info("    ✅ ORGANIZACIÓN COMPLETADA")
        logger.info("════════════════════════════════════════════════════════════════════")
        logger.info(f"📊 Archivos organizados: {self.archivos_organizados}")
        logger.info(f"✨ Coherencia final (Ψ): {self.coherencia:.3f}")
        logger.info(f"✨ Entropía final (S): {self.entropia:.3f}")
        logger.info(f"🔊 Resonancia: 888 Hz")
        logger.info(f"✨ Sello: πCODE–888 ∞³")
        logger.info("")
        
        return {
            'archivos_organizados': self.archivos_organizados,
            'coherencia': self.coherencia,
            'entropia': self.entropia
        }


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Secretaria Noética - Organización Automática de Archivos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 secretaria_noetica.py --organize-only
  python3 secretaria_noetica.py --dry-run
  python3 secretaria_noetica.py --help
        """
    )
    
    parser.add_argument(
        '--organize-only',
        action='store_true',
        help='Organizar archivos sin modo dry-run'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar qué archivos se moverían sin hacer cambios'
        description='Secretaria Noética - Organización Automática de Archivos QCAL'
    )
    parser.add_argument(
        '--organize-only',
        action='store_true',
        help='Solo organizar archivos sin otras acciones'
    )
    parser.add_argument(
        '--repo-root',
        type=str,
        default='.',
        help='Directorio raíz del repositorio (por defecto: directorio actual)'
    )
    
    args = parser.parse_args()
    
    # Determinar si es dry-run
    dry_run = args.dry_run or not args.organize_only
    
    # Obtener ruta del repositorio
    repo_path = Path.cwd()
    
    # Mostrar banner
    print("════════════════════════════════════════════════════════════════════")
    print("    ✨ SECRETARIA NOÉTICA - Organización Automática")
    print("════════════════════════════════════════════════════════════════════")
    print(f"🎯 Objetivo: Entropía S = {ENTROPIA_TARGET}, Coherencia Ψ ≥ {COHERENCIA_MIN}")
    print(f"🔊 Frecuencia: {RESONANCIA_NOETICA} Hz (Resonancia Noética)")
    print("════════════════════════════════════════════════════════════════════")
    print()
    
    if dry_run:
        print("🔍 Modo DRY-RUN: No se harán cambios reales")
        print()
    
    # Organizar archivos
    stats = organize_files(repo_path, dry_run=dry_run)
    
    # Mostrar resumen
    print()
    print("════════════════════════════════════════════════════════════════════")
    print("    📊 RESUMEN DE ORGANIZACIÓN")
    print("════════════════════════════════════════════════════════════════════")
    print(f"📁 Archivos analizados: {stats['files_analyzed']}")
    print(f"✅ Archivos movidos: {stats['files_moved']}")
    print(f"⏭️  Archivos omitidos: {stats['files_skipped']}")
    print(f"❌ Errores: {stats['errors']}")
    print("════════════════════════════════════════════════════════════════════")
    
    # Guardar log si no es dry-run
    if not dry_run:
        log_path = repo_path / 'coherencia_organizacional.log'
        save_log(stats, log_path)
        print(f"\n📋 Log guardado en: {log_path}")
    
    print()
    print("✨ Organización completada")
    print()
    
    # Retornar código de salida
    return 0 if stats['errors'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
    # Determinar el directorio raíz del repositorio
    repo_root = Path(args.repo_root).resolve()
    
    # Crear instancia de Secretaria Noética
    secretaria = SecretariaNoetica(repo_root)
    
    # Organizar repositorio
    estadisticas = secretaria.organizar_repositorio()
    
    # Código de salida según resultado
    if estadisticas['archivos_organizados'] > 0:
        logger.info("✅ Organización exitosa - Archivos movidos")
        sys.exit(0)
    else:
        logger.info("✅ Organización exitosa - Sin cambios necesarios")
        sys.exit(0)


if __name__ == '__main__':
    main()
