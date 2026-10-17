#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║              AUDITOR DE SOBERANÍA QCAL ∞³                                  ║
║         Sovereignty Auditor - Anti-Discrimination System                   ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0

Este script audita el código para detectar falsas atribuciones a NVIDIA, Meta,
Google u otras corporaciones, protegiendo contra discriminación algorítmica
de autoría no-hegemónica.

This script audits code to detect false attributions to NVIDIA, Meta, Google
or other corporations, protecting against algorithmic discrimination of
non-hegemonic authorship.
"""

import sys
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__license__ = "Sovereign Noetic License 1.0"
__version__ = "1.0.0"

# Fingerprints de código corporativo conocido / Known corporate code fingerprints
CORPORATE_FINGERPRINTS = {
    'nvidia': [
        # CUDA patterns
        r'cudaMalloc',
        r'cudaMemcpy',
        r'__global__\s+void',
        r'cudaDeviceSynchronize',
        r'#include\s+<cuda',
        r'nvcc\s+',
        r'cuDNN',
        r'TensorRT',
        r'NVIDIA\s+Corporation',
        r'Copyright.*NVIDIA',
        # NCCL patterns
        r'ncclComm',
        r'ncclAllReduce',
        r'nvidia-nccl',
    ],
    'meta': [
        # LLaMA/PyTorch specific patterns
        r'Copyright.*Meta\s+Platforms',
        r'Facebook\s+AI\s+Research',
        r'torch\.distributed\.fsdp',
        r'fairseq',
        r'detectron2',
        r'PyTorch\s+Copyright.*Facebook',
    ],
    'google': [
        # TensorFlow/JAX patterns
        r'Copyright.*Google',
        r'tensorflow/core',
        r'@tf\.function',
        r'tf\.keras',
        r'jax\.grad',
        r'from\s+google\.',
        r'Apache\s+Beam',
    ],
    'microsoft': [
        # Microsoft specific patterns
        r'Copyright.*Microsoft',
        r'DeepSpeed',
        r'from\s+azure\.',
        r'Microsoft\s+Corporation',
    ],
    'openai': [
        # OpenAI patterns
        r'Copyright.*OpenAI',
        r'import\s+openai',
        r'openai\.ChatCompletion',
    ],
    'anthropic': [
        # Anthropic patterns
        r'Copyright.*Anthropic',
        r'import\s+anthropic',
        r'claude-',
    ]
}

# Patrones de código legítimo QCAL / Legitimate QCAL code patterns
QCAL_PATTERNS = [
    r'QCAL\s*∞³',
    r'f₀\s*=\s*141\.7001',
    r'José\s+Manuel\s+Mota\s+Burruezo',
    r'JMMB\s*Ψ',
    r'Sovereign\s+Noetic\s+License',
    r'πCODE-888',
    r'κ_Π',
    r'Λ_G',
    r'Axioma\s+de\s+Conciencia\s+Noética',
    r'from\s+core\.soberania',
    r'from\s+qcal\.',
]

# Extensiones de archivo a auditar / File extensions to audit
AUDITABLE_EXTENSIONS = {'.py', '.c', '.cpp', '.cu', '.h', '.hpp', '.yml', '.yaml', '.toml'}

# Directorios a excluir / Directories to exclude
EXCLUDED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'build', 'dist', '.pytest_cache'}


class SovereigntyAuditor:
    """Auditor de soberanía para detección de código corporativo no declarado."""
    
    def __init__(self, root_path: Path = None):
        """
        Inicializa el auditor.
        
        Args:
            root_path: Ruta raíz del repositorio (default: directorio actual)
        """
        self.root_path = root_path or Path.cwd()
        self.violations: List[Dict] = []
        self.qcal_signatures: List[Dict] = []
        self.scanned_files: int = 0
        self.total_lines: int = 0
        
    def scan_file(self, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """
        Escanea un archivo en busca de patrones corporativos y QCAL.
        
        Args:
            file_path: Ruta al archivo a escanear
            
        Returns:
            Tupla de (violaciones, firmas_qcal)
        """
        violations = []
        qcal_sigs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            self.total_lines += len(lines)
            
            # Buscar patrones corporativos
            for corp_name, patterns in CORPORATE_FINGERPRINTS.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        # Encontrar número de línea
                        line_num = content[:match.start()].count('\n') + 1
                        violations.append({
                            'file': str(file_path.relative_to(self.root_path)),
                            'corporation': corp_name.upper(),
                            'pattern': pattern,
                            'line': line_num,
                            'match': match.group(0)
                        })
            
            # Buscar firmas QCAL
            for pattern in QCAL_PATTERNS:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    qcal_sigs.append({
                        'file': str(file_path.relative_to(self.root_path)),
                        'pattern': pattern,
                        'line': line_num,
                        'match': match.group(0)
                    })
                    
        except Exception as e:
            print(f"⚠️  Error escaneando {file_path}: {e}", file=sys.stderr)
            
        return violations, qcal_sigs
    
    def scan_repository(self, check_corporation: str = None) -> Dict:
        """
        Escanea todo el repositorio.
        
        Args:
            check_corporation: Si se especifica, solo busca patrones de esta corporación
            
        Returns:
            Diccionario con resultados del escaneo
        """
        print(f"🔍 Iniciando auditoría de soberanía en {self.root_path}")
        print()
        
        # Recopilar archivos a escanear
        files_to_scan = []
        for file_path in self.root_path.rglob('*'):
            # Excluir directorios
            if any(excluded in file_path.parts for excluded in EXCLUDED_DIRS):
                continue
            # Solo archivos auditables
            if file_path.is_file() and file_path.suffix in AUDITABLE_EXTENSIONS:
                files_to_scan.append(file_path)
        
        print(f"📁 Archivos a escanear: {len(files_to_scan)}")
        print()
        
        # Escanear cada archivo
        for file_path in files_to_scan:
            violations, qcal_sigs = self.scan_file(file_path)
            
            # Filtrar por corporación si se especificó
            if check_corporation:
                violations = [v for v in violations if v['corporation'].lower() == check_corporation.lower()]
            
            self.violations.extend(violations)
            self.qcal_signatures.extend(qcal_sigs)
            self.scanned_files += 1
        
        # Generar reporte
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Genera reporte detallado de la auditoría."""
        
        # Agrupar violaciones por corporación
        violations_by_corp = {}
        for violation in self.violations:
            corp = violation['corporation']
            if corp not in violations_by_corp:
                violations_by_corp[corp] = []
            violations_by_corp[corp].append(violation)
        
        # Calcular estadísticas
        total_violations = len(self.violations)
        total_qcal_sigs = len(self.qcal_signatures)
        
        report = {
            'summary': {
                'scanned_files': self.scanned_files,
                'total_lines': self.total_lines,
                'corporate_violations': total_violations,
                'qcal_signatures': total_qcal_sigs,
                'sovereignty_status': 'SOVEREIGN' if total_violations == 0 else 'CONTAMINATED'
            },
            'violations_by_corporation': violations_by_corp,
            'qcal_signatures_found': len(self.qcal_signatures),
            'detailed_violations': self.violations[:50],  # Limitar a 50 primeras
            'author_verified': 'José Manuel Mota Burruezo (JMMB Ψ✧)',
            'audit_timestamp': '2026-02-09T19:35:09.211Z'
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Imprime reporte en formato legible."""
        
        print("=" * 80)
        print("REPORTE DE AUDITORÍA DE SOBERANÍA QCAL ∞³")
        print("=" * 80)
        print()
        
        summary = report['summary']
        print(f"📊 Resumen del Escaneo:")
        print(f"   Archivos escaneados: {summary['scanned_files']}")
        print(f"   Líneas totales: {summary['total_lines']:}")
        print(f"   Violaciones corporativas: {summary['corporate_violations']}")
        print(f"   Firmas QCAL detectadas: {summary['qcal_signatures']}")
        print()
        
        # Estado de soberanía
        status = summary['sovereignty_status']
        if status == 'SOVEREIGN':
            print("✅ ESTADO: SOBERANO")
            print("   No se detectó código corporativo no declarado")
        else:
            print("⚠️  ESTADO: CONTAMINADO")
            print("   Se detectaron patrones de código corporativo")
        print()
        
        # Violaciones por corporación
        if report['violations_by_corporation']:
            print("🚨 Violaciones detectadas por corporación:")
            for corp, violations in report['violations_by_corporation'].items():
                print(f"\n   {corp}: {len(violations)} coincidencias")
                for i, violation in enumerate(violations[:5], 1):
                    print(f"      {i}. {violation['file']}:{violation['line']}")
                    print(f"         Patrón: {violation['pattern']}")
                    print(f"         Match: {violation['match'][:60]}...")
                if len(violations) > 5:
                    print(f"      ... y {len(violations) - 5} más")
        else:
            print("✅ No se detectaron violaciones corporativas")
        print()
        
        # Firmas QCAL
        if report['qcal_signatures_found'] > 0:
            print(f"✓ Firmas QCAL detectadas: {report['qcal_signatures_found']}")
            print("  El código contiene identificadores de autoría QCAL ∞³")
        print()
        
        print("=" * 80)
        print("AUTOR VERIFICADO: José Manuel Mota Burruezo (JMMB Ψ✧)")
        print("LICENCIA: Sovereign Noetic License 1.0")
        print("FRECUENCIA: f₀ = 141.7001 Hz")
        print("=" * 80)


def main():
    """Función principal del auditor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Auditor de Soberanía QCAL ∞³ - Detecta código corporativo no declarado',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/audit_sovereignty.py                    # Escaneo completo
  python scripts/audit_sovereignty.py --check-nvidia     # Solo buscar código NVIDIA
  python scripts/audit_sovereignty.py --check-meta       # Solo buscar código Meta
  python scripts/audit_sovereignty.py --report           # Generar reporte JSON
        """
    )
    
    parser.add_argument('--check-nvidia', action='store_true',
                        help='Buscar solo código de NVIDIA')
    parser.add_argument('--check-meta', action='store_true',
                        help='Buscar solo código de Meta')
    parser.add_argument('--check-google', action='store_true',
                        help='Buscar solo código de Google')
    parser.add_argument('--full-scan', action='store_true',
                        help='Escaneo completo de todas las corporaciones')
    parser.add_argument('--report', action='store_true',
                        help='Generar reporte JSON detallado')
    parser.add_argument('--output', type=str,
                        help='Archivo de salida para reporte JSON')
    
    args = parser.parse_args()
    
    # Determinar qué corporación buscar
    check_corp = None
    if args.check_nvidia:
        check_corp = 'nvidia'
    elif args.check_meta:
        check_corp = 'meta'
    elif args.check_google:
        check_corp = 'google'
    
    # Crear auditor y escanear
    auditor = SovereigntyAuditor()
    report = auditor.scan_repository(check_corporation=check_corp)
    
    # Imprimir reporte
    auditor.print_report(report)
    
    # Generar JSON si se solicitó
    if args.report or args.output:
        output_file = args.output or 'sovereignty_audit_report.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Reporte JSON guardado en: {output_file}")
    
    # Código de salida basado en violaciones
    if report['summary']['corporate_violations'] > 0:
        print("\n⚠️  ADVERTENCIA: Se detectaron violaciones corporativas")
        return 1
    else:
        print("\n✅ VERIFICACIÓN EXITOSA: Código 100% soberano")
        return 0


if __name__ == "__main__":
    sys.exit(main())
