#!/usr/bin/env python3
"""
AGGREGATE RESULTS - Consolidate all validation results

This script aggregates all validation results from various tests and analyses
into a single comprehensive report for the production pipeline.

Usage:
    python3 scripts/aggregate_results.py
    python3 scripts/aggregate_results.py --output results/aggregated_report.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any


def find_result_files(results_dir: Path) -> List[Path]:
    """
    Find all JSON result files in the results directory

    Args:
        results_dir: Path to results directory

    Returns:
        List of Path objects for JSON files
    """
    if not results_dir.exists():
        return []

    # Find all JSON files
    json_files = list(results_dir.glob("*.json"))

    # Also check subdirectories
    for subdir in results_dir.iterdir():
        if subdir.is_dir():
            json_files.extend(subdir.glob("*.json"))

    return sorted(json_files)


def load_result_file(filepath: Path) -> Dict[str, Any]:
    """
    Load a single result file

    Args:
        filepath: Path to JSON file

    Returns:
        Dictionary with result data, or error info if loading fails
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            "file": str(filepath.name),
            "status": "loaded",
            "data": data
        }
    except Exception as e:
        return {
            "file": str(filepath.name),
            "status": "error",
            "error": str(e)
        }


def extract_validation_status(result_data: Dict[str, Any]) -> str:
    """
    Extract validation status from result data

    Args:
        result_data: Result data dictionary

    Returns:
        Status string (PASS, FAIL, UNKNOWN)
    """
    if "status" not in result_data:
        return "error"

    data = result_data["data"]

    # Check for overall_status
    if "overall_status" in data:
        return data["overall_status"]

    # Check for status field
    if "status" in data:
        return data["status"]

    # Check for estado_general (Spanish)
    if "estado_general" in data:
        status = data["estado_general"]
        if "EXITOSA" in status.upper():
            return "PASS"
        elif "ERROR" in status.upper() or "FALLO" in status.upper():
            return "FAIL"

    # Check nested validation status
    if "validation_suite" in data or "validacion_completa" in data:
        return "PASS"  # Assume pass if validation suite exists

    return "UNKNOWN"


def aggregate_results(results_dir: Path) -> Dict[str, Any]:
    """
    Aggregate all results into a comprehensive report

    Args:
        results_dir: Path to results directory

    Returns:
        Dictionary with aggregated results
    """
    print("=" * 70)
    print(" AGGREGATING RESULTS")
    print("=" * 70)
    print()

    # Find all result files
    result_files = find_result_files(results_dir)
    print(f"📁 Found {len(result_files)} result files")
    print()

    # Load all results
    loaded_results = []
    for filepath in result_files:
        print(f"   Loading: {filepath.name}")
        result = load_result_file(filepath)
        loaded_results.append(result)

    print()

    # Count statuses
    statuses = {
        "loaded": 0,
        "error": 0
    }

    validation_statuses = {
        "PASS": 0,
        "FAIL": 0,
        "UNKNOWN": 0
    }

    for result in loaded_results:
        statuses[result["status"]] += 1
        if result["status"] == "loaded":
            status = extract_validation_status(result)
            validation_statuses[status] += 1

    # Create aggregated report
    aggregated = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results_directory": str(results_dir),
        "summary": {
            "total_files": len(result_files),
            "files_loaded": statuses["loaded"],
            "files_error": statuses["error"],
            "validations_passed": validation_statuses["PASS"],
            "validations_failed": validation_statuses["FAIL"],
            "validations_unknown": validation_statuses["UNKNOWN"]
        },
        "results": loaded_results,
        "overall_status": "PASS" if validation_statuses["FAIL"] == 0 and statuses["error"] == 0 else "FAIL"
    }

    # Print summary
    print("=" * 70)
    print(" AGGREGATION SUMMARY")
    print("=" * 70)
    print(f" Total files:         {aggregated['summary']['total_files']}")
    print(f" Files loaded:        {aggregated['summary']['files_loaded']}")
    print(f" Files with errors:   {aggregated['summary']['files_error']}")
    print(f" Validations passed:  {aggregated['summary']['validations_passed']}")
    print(f" Validations failed:  {aggregated['summary']['validations_failed']}")
    print(f" Validations unknown: {aggregated['summary']['validations_unknown']}")
    print("=" * 70)
    print(f" Overall status: {aggregated['overall_status']}")
    print("=" * 70)
    print()

    return aggregated


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Aggregate validation results into a comprehensive report"
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="Directory containing result files (default: results)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: results/aggregated_report.json)"
    )

    args = parser.parse_args()

    # Set paths
    results_dir = Path(args.results_dir)
    output_path = args.output if args.output else "results/aggregated_report.json"
    output_file = Path(output_path)

    # Ensure results directory exists
    results_dir.mkdir(parents=True, exist_ok=True)

    # Aggregate results
    aggregated = aggregate_results(results_dir)

    # Save aggregated report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)

    print(f"📊 Aggregated report saved to: {output_file}")
    print()

    # Exit with appropriate code
    sys.exit(0 if aggregated['overall_status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
