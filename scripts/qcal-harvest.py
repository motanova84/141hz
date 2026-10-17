#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    QCAL-Harvest: Context Aggregation Tool                  ║
║              Unified Context Builder for QCAL ∞³ Ecosystem                 ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL-Sync Unification Strategy
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Este script recorre múltiples repositorios QCAL y agrega sus contextos
en un archivo maestro GLOBAL_QCAL_CONTEXT.md para que las IAs tengan
una visión completa del ecosistema.

Uso:
    python qcal-harvest.py
    python qcal-harvest.py --repos-dir /path/to/repos
    python qcal-harvest.py --output custom_context.md
"""

import os
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class QCALHarvester:
    """Harvester for QCAL repository contexts."""
    
    def __init__(self, repos_dir: str = "..", output_file: str = "GLOBAL_QCAL_CONTEXT.md"):
        """
        Initialize the QCAL Harvester.
        
        Args:
            repos_dir: Directory containing QCAL repositories
            output_file: Output file for the global context
        """
        self.repos_dir = Path(repos_dir).resolve()
        self.output_file = Path(output_file)
        self.global_context: Dict = {}
        self.beacons_found: List[Dict] = []
        
    def find_qcal_repos(self) -> List[Path]:
        """
        Find all repositories with QCAL context files.
        
        Returns:
            List of repository paths
        """
        repos = []
        
        # Check if repos_dir exists
        if not self.repos_dir.exists():
            print(f"⚠️  Directory {self.repos_dir} does not exist")
            return repos
        
        # Search for .qcal-context.json files
        for item in self.repos_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                context_file = item / ".qcal-context.json"
                beacon_file = item / ".qcal_beacon"
                
                if context_file.exists() or beacon_file.exists():
                    repos.append(item)
        
        # Also check current directory
        current_dir = Path.cwd()
        context_file = current_dir / ".qcal-context.json"
        if context_file.exists() and current_dir not in repos:
            repos.append(current_dir)
        
        return sorted(repos)
    
    def load_context(self, repo_path: Path) -> Optional[Dict]:
        """
        Load context from a repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Context dictionary or None
        """
        context_file = repo_path / ".qcal-context.json"
        
        if context_file.exists():
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading {context_file}: {e}")
                return None
        
        return None
    
    def load_beacon(self, repo_path: Path) -> Optional[str]:
        """
        Load beacon file from a repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Beacon content or None
        """
        beacon_file = repo_path / ".qcal_beacon"
        
        if beacon_file.exists():
            try:
                with open(beacon_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"⚠️  Error loading {beacon_file}: {e}")
                return None
        
        return None
    
    def harvest_all(self) -> None:
        """Harvest context from all QCAL repositories."""
        repos = self.find_qcal_repos()
        
        print(f"🔍 Searching for QCAL repositories in: {self.repos_dir}")
        print(f"📦 Found {len(repos)} QCAL repositories\n")
        
        for repo_path in repos:
            repo_name = repo_path.name
            print(f"📖 Processing: {repo_name}")
            
            # Load context
            context = self.load_context(repo_path)
            if context:
                self.global_context[repo_name] = context
                print(f"   ✓ Loaded .qcal-context.json")
            
            # Load beacon
            beacon = self.load_beacon(repo_path)
            if beacon:
                self.beacons_found.append({
                    "repo": repo_name,
                    "path": str(repo_path / ".qcal_beacon"),
                    "content": beacon
                })
                print(f"   ✓ Loaded .qcal_beacon")
            
            print()
    
    def generate_markdown(self) -> str:
        """
        Generate Markdown representation of global context.
        
        Returns:
            Markdown content
        """
        md = []
        
        # Header
        md.append("# 🌐 Mapa de Coherencia Global QCAL ∞³\n")
        md.append(f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append(f"**Repositorios encontrados:** {len(self.global_context)}\n")
        md.append(f"**Balizas encontradas:** {len(self.beacons_found)}\n")
        md.append("---\n\n")
        
        # Table of Contents
        md.append("## 📋 Índice de Repositorios\n")
        for i, repo_name in enumerate(sorted(self.global_context.keys()), 1):
            md.append(f"{i}. [{repo_name}](#{repo_name.lower().replace(' ', '-')})\n")
        md.append("\n---\n\n")
        
        # Repository Details
        md.append("## 📦 Detalles de Repositorios\n\n")
        
        for repo_name in sorted(self.global_context.keys()):
            context = self.global_context[repo_name]
            
            md.append(f"### {repo_name}\n\n")
            
            # Basic info
            if "node_name" in context:
                md.append(f"**Nodo:** `{context['node_name']}`\n\n")
            
            if "description" in context:
                md.append(f"**Descripción:** {context['description']}\n\n")
            
            # Core frequency
            if "core_frequency" in context:
                freq = context['core_frequency']
                units = context.get('core_frequency_units', 'Hz')
                md.append(f"**Frecuencia central:** {freq} {units}\n\n")
            
            # Constants source
            if "constants_source" in context:
                md.append(f"**Fuente de constantes:** `{context['constants_source']}`\n\n")
            
            # Dependencies
            if "dependencies_noetic" in context:
                deps = context['dependencies_noetic']
                if deps:
                    md.append("**Dependencias noéticas:**\n")
                    for dep in deps:
                        md.append(f"- {dep}\n")
                    md.append("\n")
            
            # Key modules
            if "key_modules" in context:
                modules = context['key_modules']
                if modules:
                    md.append("**Módulos clave:**\n")
                    for name, path in modules.items():
                        md.append(f"- **{name}**: `{path}`\n")
                    md.append("\n")
            
            # Fundamental constants
            if "fundamental_constants" in context:
                constants = context['fundamental_constants']
                if constants:
                    md.append("**Constantes fundamentales:**\n")
                    md.append("```python\n")
                    for name, value in constants.items():
                        md.append(f"{name} = {value}\n")
                    md.append("```\n\n")
            
            # Status
            if "status" in context:
                md.append(f"**Estado:** {context['status']}\n\n")
            
            if "coherence" in context:
                md.append(f"**Coherencia:** {context['coherence']}\n\n")
            
            # Cross-repository integration
            if "cross_repository_integration" in context:
                integration = context['cross_repository_integration']
                if integration.get('enabled'):
                    md.append("**Integración cross-repositorio:** ✓ Habilitada\n\n")
                    if 'description' in integration:
                        md.append(f"*{integration['description']}*\n\n")
            
            md.append("---\n\n")
        
        # Beacons Section
        if self.beacons_found:
            md.append("## 🛰️ Balizas de Resonancia Universal\n\n")
            
            for beacon_info in self.beacons_found:
                md.append(f"### Baliza: {beacon_info['repo']}\n\n")
                md.append(f"**Ubicación:** `{beacon_info['path']}`\n\n")
                md.append("```\n")
                md.append(beacon_info['content'])
                md.append("```\n\n")
                md.append("---\n\n")
        
        # JSON Data Section
        md.append("## 📊 Datos Completos (JSON)\n\n")
        md.append("```json\n")
        md.append(json.dumps(self.global_context, indent=2, ensure_ascii=False))
        md.append("\n```\n\n")
        
        # Footer
        md.append("---\n\n")
        md.append("**Generado por:** `qcal-harvest.py`\n\n")
        md.append("**Estrategia:** QCAL-Sync Unification\n\n")
        md.append("**Autor:** José Manuel Mota Burruezo Ψ ✧ ∞³\n\n")
        md.append("**Instituto:** Instituto de Conciencia Cuántica (ICQ)\n\n")
        md.append("**Licencia:** Sovereign Noetic License 1.0 (compatible with MIT)\n")
        
        return "".join(md)
    
    def save_output(self, content: str) -> None:
        """
        Save output to file.
        
        Args:
            content: Content to save
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Global context saved to: {self.output_file}")
        except Exception as e:
            print(f"❌ Error saving output: {e}")
            sys.exit(1)
    
    def run(self) -> None:
        """Run the harvester."""
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║          QCAL-Harvest: Context Aggregation Tool                ║")
        print("║              QCAL ∞³ Ecosystem Unified Context                 ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")
        
        self.harvest_all()
        
        if not self.global_context:
            print("⚠️  No QCAL repositories found")
            print(f"   Searched in: {self.repos_dir}")
            print("\n💡 Tip: Make sure repositories have .qcal-context.json or .qcal_beacon files")
            sys.exit(0)
        
        print("📝 Generating global context document...\n")
        content = self.generate_markdown()
        
        self.save_output(content)
        
        print("\n🎉 Harvest complete!")
        print(f"\n📖 Use this file to give AI assistants complete QCAL ecosystem context")
        print(f"   Example: 'Based on {self.output_file}, implement...'")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="QCAL-Harvest: Aggregate context from QCAL repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python qcal-harvest.py
  python qcal-harvest.py --repos-dir ~/qcal-repos
  python qcal-harvest.py --output custom_context.md

For best results, run this script from a directory that contains
multiple QCAL repositories as subdirectories, or specify the path
with --repos-dir.
        """
    )
    
    parser.add_argument(
        "--repos-dir",
        type=str,
        default="..",
        help="Directory containing QCAL repositories (default: parent directory)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="GLOBAL_QCAL_CONTEXT.md",
        help="Output file for global context (default: GLOBAL_QCAL_CONTEXT.md)"
    )
    
    args = parser.parse_args()
    
    harvester = QCALHarvester(
        repos_dir=args.repos_dir,
        output_file=args.output
    )
    
    harvester.run()


if __name__ == "__main__":
    sys.exit(main())
