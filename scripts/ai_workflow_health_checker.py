#!/usr/bin/env python3
"""
AI Workflow Health Checker
Automated AI collaborator for verifying and diagnosing workflow health.

This script analyzes GitHub Actions workflows to ensure they are configured
correctly and can pass successfully (show green badges).

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple


class WorkflowHealthChecker:
    """Automated AI collaborator for workflow health verification"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.workflows_dir = self.repo_root / ".github" / "workflows"
        self.scripts_dir = self.repo_root / "scripts"
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def check_all_workflows(self) -> Dict:
        """Run comprehensive health check on all workflows"""
        print("🤖 AI WORKFLOW HEALTH CHECKER")
        print("=" * 70)
        print("Analyzing workflows for badge status optimization...")
        print()
        
        results = {
            "total_workflows": 0,
            "healthy_workflows": 0,
            "workflows_with_issues": 0,
            "issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        if not self.workflows_dir.exists():
            print(f"❌ Workflows directory not found: {self.workflows_dir}")
            return results
        
        workflow_files = list(self.workflows_dir.glob("*.yml")) + \
                        list(self.workflows_dir.glob("*.yaml"))
        
        results["total_workflows"] = len(workflow_files)
        
        for workflow_file in workflow_files:
            print(f"\n📋 Checking: {workflow_file.name}")
            print("-" * 70)
            
            workflow_health = self.check_workflow_file(workflow_file)
            
            if workflow_health["issues"]:
                results["workflows_with_issues"] += 1
                results["issues"].extend(workflow_health["issues"])
                for issue in workflow_health["issues"]:
                    print(f"  ❌ ISSUE: {issue}")
            else:
                results["healthy_workflows"] += 1
                print(f"  ✅ No critical issues found")
            
            if workflow_health["warnings"]:
                results["warnings"].extend(workflow_health["warnings"])
                for warning in workflow_health["warnings"]:
                    print(f"  ⚠️  WARNING: {warning}")
            
            if workflow_health["recommendations"]:
                results["recommendations"].extend(workflow_health["recommendations"])
                for rec in workflow_health["recommendations"]:
                    print(f"  💡 RECOMMENDATION: {rec}")
        
        self._print_summary(results)
        return results
    
    def check_workflow_file(self, workflow_file: Path) -> Dict:
        """Check a single workflow file for issues"""
        issues = []
        warnings = []
        recommendations = []
        
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow = yaml.safe_load(f)
            
            if not workflow:
                issues.append(f"{workflow_file.name}: Empty or invalid YAML")
                return {"issues": issues, "warnings": warnings, "recommendations": recommendations}
            
            # Check for required fields (YAML parses 'on' as True/boolean)
            # In YAML, 'on' is a reserved keyword that gets parsed as boolean True
            if True not in workflow and 'on' not in workflow:
                issues.append(f"{workflow_file.name}: Missing 'on' trigger configuration")
            
            if 'jobs' not in workflow:
                issues.append(f"{workflow_file.name}: Missing 'jobs' section")
                return {"issues": issues, "warnings": warnings, "recommendations": recommendations}
            
            # Check each job
            for job_name, job_config in workflow['jobs'].items():
                job_issues = self._check_job(workflow_file.name, job_name, job_config)
                issues.extend(job_issues["issues"])
                warnings.extend(job_issues["warnings"])
                recommendations.extend(job_issues["recommendations"])
            
            # Check for script references
            script_issues = self._check_script_references(workflow_file.name, workflow)
            issues.extend(script_issues["issues"])
            warnings.extend(script_issues["warnings"])
            
            # Check Python version consistency
            python_issues = self._check_python_versions(workflow_file.name, workflow)
            warnings.extend(python_issues["warnings"])
            recommendations.extend(python_issues["recommendations"])
            
        except yaml.YAMLError as e:
            issues.append(f"{workflow_file.name}: YAML parsing error - {e}")
        except Exception as e:
            issues.append(f"{workflow_file.name}: Unexpected error - {e}")
        
        return {"issues": issues, "warnings": warnings, "recommendations": recommendations}
    
    def _check_job(self, workflow_name: str, job_name: str, job_config: Dict) -> Dict:
        """Check a single job configuration"""
        issues = []
        warnings = []
        recommendations = []
        
        if not isinstance(job_config, dict):
            issues.append(f"{workflow_name}/{job_name}: Invalid job configuration")
            return {"issues": issues, "warnings": warnings, "recommendations": recommendations}
        
        # Check for runs-on
        if 'runs-on' not in job_config:
            issues.append(f"{workflow_name}/{job_name}: Missing 'runs-on' field")
        
        # Check steps
        if 'steps' not in job_config:
            warnings.append(f"{workflow_name}/{job_name}: No steps defined")
        else:
            steps = job_config['steps']
            if not steps:
                warnings.append(f"{workflow_name}/{job_name}: Empty steps list")
            
            # Check for Python setup in workflows that need it
            has_python_setup = any(
                step.get('uses', '').startswith('actions/setup-python')
                for step in steps if isinstance(step, dict)
            )
            
            # Check for actual Python command usage (not just mentions in echo/comments)
            has_python_commands = False
            for step in steps:
                if not isinstance(step, dict):
                    continue
                run_command = step.get('run', '')
                if not run_command:
                    continue
                
                # Split into lines and check each line
                import re
                for line in str(run_command).split('\n'):
                    line = line.strip()
                    # Skip comments and echo statements (with any amount of leading whitespace)
                    if re.match(r'^\s*#', line) or re.match(r'^\s*echo\s+', line):
                        continue
                    # Check for actual python/pip commands using word boundaries
                    if re.search(r'\b(python3?|pip)\b', line):
                        has_python_commands = True
                        break
                if has_python_commands:
                    break
            
            if has_python_commands and not has_python_setup:
                issues.append(
                    f"{workflow_name}/{job_name}: Uses Python but missing setup-python action"
                )
            
            # Check for dependency installation
            if has_python_setup and not any(
                'pip install -r requirements.txt' in str(step.get('run', ''))
                for step in steps if isinstance(step, dict)
            ):
                warnings.append(
                    f"{workflow_name}/{job_name}: Has Python setup but doesn't install requirements.txt"
                )
            
            # Recommend caching for pip
            if has_python_setup and not any(
                'actions/cache' in step.get('uses', '')
                for step in steps if isinstance(step, dict)
            ):
                recommendations.append(
                    f"{workflow_name}/{job_name}: Consider adding pip caching for faster builds"
                )
        
        return {"issues": issues, "warnings": warnings, "recommendations": recommendations}
    
    def _check_script_references(self, workflow_name: str, workflow: Dict) -> Dict:
        """Check if referenced scripts exist"""
        issues = []
        warnings = []
        
        jobs = workflow.get('jobs', {})
        
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                continue
                
            steps = job_config.get('steps', [])
            
            for step in steps:
                if not isinstance(step, dict):
                    continue
                
                run_command = step.get('run', '')
                if not run_command:
                    continue
                
                # Check for Python script references
                if 'python' in run_command.lower():
                    # Extract script names (simple pattern matching)
                    import re
                    script_patterns = re.findall(r'python3?\s+(\S+\.py)', run_command)
                    
                    for script_path in script_patterns:
                        # Skip if path contains shell variable expansion
                        if '${' in script_path or '${{' in script_path or '$(' in script_path:
                            continue
                        
                        # Remove leading ./ or scripts/
                        script_path = script_path.replace('./', '')
                        
                        # Check if file exists
                        full_path = self.repo_root / script_path
                        
                        if not full_path.exists():
                            # Try in scripts directory
                            alt_path = self.scripts_dir / Path(script_path).name
                            if not alt_path.exists():
                                issues.append(
                                    f"{workflow_name}: Referenced script not found: {script_path}"
                                )
        
        return {"issues": issues, "warnings": warnings}
    
    def _check_python_versions(self, workflow_name: str, workflow: Dict) -> Dict:
        """Check Python version consistency"""
        warnings = []
        recommendations = []
        
        jobs = workflow.get('jobs', {})
        python_versions = set()
        
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                continue
                
            steps = job_config.get('steps', [])
            
            for step in steps:
                if not isinstance(step, dict):
                    continue
                
                if step.get('uses', '').startswith('actions/setup-python'):
                    with_config = step.get('with', {})
                    version = with_config.get('python-version', '')
                    if version:
                        python_versions.add(str(version))
        
        if len(python_versions) > 1:
            warnings.append(
                f"{workflow_name}: Multiple Python versions used: {', '.join(python_versions)}. "
                "Consider standardizing to Python 3.11 or 3.12."
            )
        elif python_versions:
            version = list(python_versions)[0]
            if version not in ['3.11', '3.12', '3.11+', '3.12+']:
                recommendations.append(
                    f"{workflow_name}: Consider upgrading to Python 3.11 or 3.12 "
                    f"(currently using {version})"
                )
        
        return {"warnings": warnings, "recommendations": recommendations}
    
    def _print_summary(self, results: Dict):
        """Print summary of health check results"""
        print("\n" + "=" * 70)
        print("📊 WORKFLOW HEALTH SUMMARY")
        print("=" * 70)
        
        print(f"\nTotal workflows analyzed: {results['total_workflows']}")
        print(f"✅ Healthy workflows: {results['healthy_workflows']}")
        print(f"⚠️  Workflows with issues: {results['workflows_with_issues']}")
        
        if results['issues']:
            print(f"\n❌ Critical Issues Found: {len(results['issues'])}")
            for issue in results['issues'][:10]:  # Show first 10
                print(f"   • {issue}")
            if len(results['issues']) > 10:
                print(f"   ... and {len(results['issues']) - 10} more")
        
        if results['warnings']:
            print(f"\n⚠️  Warnings: {len(results['warnings'])}")
            for warning in results['warnings'][:5]:  # Show first 5
                print(f"   • {warning}")
            if len(results['warnings']) > 5:
                print(f"   ... and {len(results['warnings']) - 5} more")
        
        if results['recommendations']:
            print(f"\n💡 Recommendations: {len(results['recommendations'])}")
            for rec in results['recommendations'][:5]:  # Show first 5
                print(f"   • {rec}")
            if len(results['recommendations']) > 5:
                print(f"   ... and {len(results['recommendations']) - 5} more")
        
        print("\n" + "=" * 70)
        
        if results['workflows_with_issues'] == 0:
            print("🎉 All workflows are healthy! Badges should show GREEN ✅")
        else:
            print("🔧 Fix the issues above to ensure badges show GREEN ✅")
        
        print("=" * 70)
    
    def generate_report(self, output_file: Path) -> bool:
        """Generate detailed JSON report"""
        results = self.check_all_workflows()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Detailed report saved to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False


def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    
    checker = WorkflowHealthChecker(repo_root)
    results = checker.check_all_workflows()
    
    # Save report
    report_file = repo_root / "results" / "workflow_health_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    checker.generate_report(report_file)
    
    # Exit with error code if there are issues
    if results['workflows_with_issues'] > 0:
        print("\n⚠️  Exiting with error code due to workflow issues")
        return 1
    
    print("\n✅ All workflows are healthy!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
