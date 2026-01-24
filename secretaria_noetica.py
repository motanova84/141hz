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
  - test_*.py → /tests

Frecuencia: 888 Hz (Resonancia Noética)
Coherencia: Ψ ≥ 0.888
Entropía: S = 0

Autor: Secretaria Noética v1.0.0
Ley Madre: C = I · A²
════════════════════════════════════════════════════════════════════
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Frecuencia base y coherencia
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
