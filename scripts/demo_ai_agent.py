#!/usr/bin/env python3
"""
Demo: AI Agent Project Creator
===============================

This script demonstrates the capabilities of the AI Project Creator Agent
by creating sample projects and showing the generated structure.

Usage:
    python scripts/demo_ai_agent.py

Author: AI Agent System
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def print_file_preview(file_path, lines=20):
    """Print preview of file content"""
    print(f"\n📄 File: {file_path}")
    print("-" * 70)
    
    try:
        with open(file_path, 'r') as f:
            content_lines = f.readlines()
            
        for i, line in enumerate(content_lines[:lines], 1):
            print(f"{i:3d} | {line.rstrip()}")
        
        if len(content_lines) > lines:
            print(f"... ({len(content_lines) - lines} more lines)")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    print("-" * 70)


def demo_event_analysis():
    """Demonstrate event analysis project creation"""
    from scripts.ai_agent_project_creator import AIProjectAgent
    
    print_section("DEMO 1: Event Analysis Project")
    
    print("Creating a sample event analysis project for GW250115...")
    print("This demonstrates automatic generation of:")
    print("  • Analysis script with data download and SNR calculation")
    print("  • Complete test suite")
    print("  • Documentation")
    print("  • CI/CD workflow")
    print("  • Makefile integration\n")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="ai_agent_demo_")
    print(f"🔧 Using temporary directory: {temp_dir}\n")
    
    try:
        # Create agent
        agent = AIProjectAgent()
        agent.root_dir = Path(temp_dir)
        
        # Create necessary directories
        (agent.root_dir / 'scripts').mkdir(parents=True)
        (agent.root_dir / '.github' / 'workflows').mkdir(parents=True)
        (agent.root_dir / 'docs').mkdir(parents=True)
        
        # Create minimal Makefile
        with open(agent.root_dir / 'Makefile', 'w') as f:
            f.write('# Demo Makefile\n\n# Show available targets\nhelp:\n\t@echo "Demo"\n')
        
        # Create project
        metadata = agent.create_project(
            'event',
            'GW250115',
            'Demonstration analysis of GW250115 binary black hole merger at 141.7001 Hz'
        )
        
        print("\n✅ Project created successfully!\n")
        
        # Show file structure
        print("📁 Generated File Structure:")
        print("-" * 70)
        
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{sub_indent}{file}')
        
        print("-" * 70)
        
        # Show preview of generated files
        print("\n📝 File Previews:")
        
        # Analysis script preview
        analysis_script = agent.root_dir / 'scripts' / 'analizar_gw250115.py'
        print_file_preview(analysis_script, lines=40)
        
        # Test script preview
        test_script = agent.root_dir / 'scripts' / 'test_gw250115.py'
        print_file_preview(test_script, lines=30)
        
        # Workflow preview
        workflow = agent.root_dir / '.github' / 'workflows' / 'gw250115.yml'
        print_file_preview(workflow, lines=30)
        
        # Documentation preview
        doc = agent.root_dir / 'docs' / 'GW250115_ANALYSIS.md'
        print_file_preview(doc, lines=30)
        
        # Makefile update
        makefile = agent.root_dir / 'Makefile'
        print_file_preview(makefile, lines=30)
        
        print("\n✅ Demo 1 Complete!")
        print(f"\n💡 Files remain in: {temp_dir}")
        print("   You can inspect them manually if desired.")
        
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()
    
    return temp_dir


def demo_validation_method():
    """Demonstrate validation method project creation"""
    from scripts.ai_agent_project_creator import AIProjectAgent
    
    print_section("DEMO 2: Validation Method Project")
    
    print("Creating a sample validation method project...")
    print("This demonstrates automatic generation of:")
    print("  • Validation script with high-precision calculations")
    print("  • CI/CD workflow with scheduled runs")
    print("  • Makefile integration\n")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="ai_agent_demo_val_")
    print(f"🔧 Using temporary directory: {temp_dir}\n")
    
    try:
        # Create agent
        agent = AIProjectAgent()
        agent.root_dir = Path(temp_dir)
        
        # Create necessary directories
        (agent.root_dir / 'scripts').mkdir(parents=True)
        (agent.root_dir / '.github' / 'workflows').mkdir(parents=True)
        
        # Create minimal Makefile
        with open(agent.root_dir / 'Makefile', 'w') as f:
            f.write('# Demo Makefile\n\n# Show available targets\nhelp:\n\t@echo "Demo"\n')
        
        # Create project
        metadata = agent.create_project(
            'validation',
            'harmonic_series',
            'Validation of harmonic frequency series f_n = f₀/π^(2n)'
        )
        
        print("\n✅ Project created successfully!\n")
        
        # Show file structure
        print("📁 Generated File Structure:")
        print("-" * 70)
        
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{sub_indent}{file}')
        
        print("-" * 70)
        
        # Show preview of generated files
        print("\n📝 File Previews:")
        
        # Validation script preview
        val_script = agent.root_dir / 'scripts' / 'validacion_harmonic_series.py'
        print_file_preview(val_script, lines=40)
        
        # Workflow preview
        workflow = agent.root_dir / '.github' / 'workflows' / 'harmonic_series.yml'
        print_file_preview(workflow, lines=30)
        
        print("\n✅ Demo 2 Complete!")
        print(f"\n💡 Files remain in: {temp_dir}")
        
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()
    
    return temp_dir


def demo_multiple_projects():
    """Demonstrate creating multiple projects"""
    from scripts.ai_agent_project_creator import AIProjectAgent
    
    print_section("DEMO 3: Multiple Projects Creation")
    
    print("Creating multiple projects to show batch operations...")
    print("This demonstrates:")
    print("  • Creating multiple projects in sequence")
    print("  • Project metadata tracking")
    print("  • Listing all created projects\n")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="ai_agent_demo_multi_")
    print(f"🔧 Using temporary directory: {temp_dir}\n")
    
    try:
        # Create agent
        agent = AIProjectAgent()
        agent.root_dir = Path(temp_dir)
        
        # Create necessary directories
        (agent.root_dir / 'scripts').mkdir(parents=True)
        (agent.root_dir / '.github' / 'workflows').mkdir(parents=True)
        (agent.root_dir / 'docs').mkdir(parents=True)
        
        # Create minimal Makefile
        with open(agent.root_dir / 'Makefile', 'w') as f:
            f.write('# Demo Makefile\n\n# Show available targets\nhelp:\n\t@echo "Demo"\n')
        
        # Define projects to create
        projects = [
            ('event', 'GW250115', 'Analysis of GW250115 event'),
            ('event', 'GW250116', 'Analysis of GW250116 event'),
            ('validation', 'coherence_check', 'Coherence validation across scales'),
            ('validation', 'frequency_stability', 'Frequency stability validation'),
        ]
        
        print(f"Creating {len(projects)} projects...\n")
        
        # Create projects
        for i, (ptype, name, desc) in enumerate(projects, 1):
            print(f"\n[{i}/{len(projects)}] Creating {ptype} project: {name}")
            metadata = agent.create_project(ptype, name, desc)
            print(f"    ✅ Created with {len(metadata['files'])} files")
        
        print("\n" + "="*70)
        print("All projects created successfully!")
        print("="*70)
        
        # List all projects
        print("\n📋 Project Summary:")
        print("-" * 70)
        
        all_projects = agent.list_projects()
        
        for i, project in enumerate(all_projects, 1):
            print(f"\n{i}. {project['name']}")
            print(f"   Type: {project['type']}")
            print(f"   Description: {project['description']}")
            print(f"   Files: {len(project['files'])}")
            print(f"   Created: {project['created_at']}")
        
        print("\n" + "-" * 70)
        
        # Show directory structure
        print("\n📁 Complete Directory Structure:")
        print("-" * 70)
        
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root)
            
            if level < 3:  # Limit depth for readability
                print(f'{indent}{folder_name}/')
                
                sub_indent = ' ' * 2 * (level + 1)
                for file in sorted(files):
                    print(f'{sub_indent}{file}')
        
        print("-" * 70)
        
        print("\n✅ Demo 3 Complete!")
        print(f"\n💡 Files remain in: {temp_dir}")
        
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()
    
    return temp_dir


def main():
    """Main demo function"""
    print("\n" + "="*70)
    print("  🤖 AI AGENT PROJECT CREATOR - DEMONSTRATION")
    print("="*70)
    
    print("\nThis demo showcases the AI Agent's ability to automatically")
    print("create and configure new analysis projects with full coherence")
    print("to the existing GW250114-141Hz framework.\n")
    
    print("The demo will:")
    print("  1. Create an event analysis project")
    print("  2. Create a validation method project")
    print("  3. Create multiple projects in batch")
    print("\nAll generated files will be created in temporary directories")
    print("that you can inspect after the demo completes.\n")
    
    input("Press Enter to continue...")
    
    # Run demos
    temp_dirs = []
    
    try:
        # Demo 1: Event analysis
        temp_dir1 = demo_event_analysis()
        temp_dirs.append(temp_dir1)
        
        input("\n\nPress Enter to continue to Demo 2...")
        
        # Demo 2: Validation method
        temp_dir2 = demo_validation_method()
        temp_dirs.append(temp_dir2)
        
        input("\n\nPress Enter to continue to Demo 3...")
        
        # Demo 3: Multiple projects
        temp_dir3 = demo_multiple_projects()
        temp_dirs.append(temp_dir3)
        
        # Final summary
        print_section("DEMO COMPLETE")
        
        print("All demonstrations completed successfully!")
        print("\n📁 Generated files are available in:")
        for i, temp_dir in enumerate(temp_dirs, 1):
            print(f"   Demo {i}: {temp_dir}")
        
        print("\n💡 To use the AI Agent in your project:")
        print("   python scripts/ai_agent_project_creator.py --type event --name GW250115 --description 'Your description'")
        
        print("\n📚 For more information:")
        print("   - Read: docs/AI_AGENT_PROJECT_CREATOR.md")
        print("   - Tests: python scripts/test_ai_agent_project_creator.py")
        print("   - Help: python scripts/ai_agent_project_creator.py --help")
        
        print("\n🎉 Thank you for exploring the AI Agent Project Creator!")
        
        # Ask about cleanup
        print("\n" + "="*70)
        cleanup = input("\nClean up temporary directories? (y/N): ").strip().lower()
        
        if cleanup == 'y':
            for temp_dir in temp_dirs:
                shutil.rmtree(temp_dir)
                print(f"   Removed: {temp_dir}")
            print("\n✅ Cleanup complete")
        else:
            print("\n💾 Temporary directories preserved for inspection")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
