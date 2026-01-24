#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════════
    ✨ SECRETARIA NOÉTICA - Organización Automática de Archivos
════════════════════════════════════════════════════════════════════

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
        'mkdocs.yml', 'codecov.yml', 'vercel.json', 'robots.txt',
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
            for destino in self.DESTINOS.values():
                if str(relative_path).startswith(destino):
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
                max_intentos = 1000  # Evitar bucles infinitos
                while destino_path.exists() and contador < max_intentos:
                    stem = archivo.stem
                    destino_path = destino_dir / f"{stem}_{contador}{extension}"
                    contador += 1
                
                if contador >= max_intentos:
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
