#!/usr/bin/env python3
"""
Calabi-Yau Varieties Database

This module provides access to 150 authentic Calabi-Yau three-fold varieties
with their Hodge numbers (h¹¹, h²¹) from the Kreuzer-Skarke and CICY databases.

The Hodge numbers are topological invariants that characterize the geometry
of Calabi-Yau manifolds, which are fundamental in string theory compactification.

References:
- Kreuzer-Skarke database: hep.itp.tuwien.ac.at
- CICY database: Candelas & He
- Literature: Altman et al.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∞³)
Date: January 2026
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class CalabiYauVariety:
    """
    Represents a single Calabi-Yau three-fold variety with its Hodge numbers.
    
    Attributes:
        id: Unique identifier (1-150)
        h11: First Hodge number h^{1,1} (number of Kähler moduli)
        h21: Second Hodge number h^{2,1} (number of complex structure moduli)
    """
    
    def __init__(self, id: int, h11: int, h21: int):
        self.id = id
        self.h11 = h11
        self.h21 = h21
    
    @property
    def euler_characteristic(self) -> int:
        """
        Compute the Euler characteristic χ = 2(h^{1,1} - h^{2,1})
        
        Returns:
            Euler characteristic
        """
        return 2 * (self.h11 - self.h21)
    
    @property
    def hodge_numbers(self) -> Tuple[int, int]:
        """
        Return the Hodge numbers as a tuple (h¹¹, h²¹)
        
        Returns:
            Tuple of (h11, h21)
        """
        return (self.h11, self.h21)
    
    def __repr__(self) -> str:
        return f"CalabiYauVariety(id={self.id}, h11={self.h11}, h21={self.h21})"
    
    def __str__(self) -> str:
        return f"CY#{self.id}: (h¹¹={self.h11}, h²¹={self.h21}, χ={self.euler_characteristic})"


class CalabiYauDatabase:
    """
    Database of 150 Calabi-Yau three-fold varieties.
    
    This class provides methods to load, query, and export the varieties
    from the Kreuzer-Skarke and CICY databases.
    """
    
    def __init__(self, data_file: Optional[Path] = None):
        """
        Initialize the database.
        
        Args:
            data_file: Path to JSON data file. If None, uses default location.
        """
        if data_file is None:
            data_file = Path(__file__).parent / "calabi_yau_varieties_150.json"
        
        self.data_file = Path(data_file)
        self.varieties: List[CalabiYauVariety] = []
        self.metadata: Dict = {}
        self._load_data()
    
    def _load_data(self):
        """Load varieties from JSON file."""
        if not self.data_file.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_file}")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.metadata = data.get('metadata', {})
        
        for variety_data in data.get('varieties', []):
            variety = CalabiYauVariety(
                id=variety_data['id'],
                h11=variety_data['h11'],
                h21=variety_data['h21']
            )
            self.varieties.append(variety)
    
    def get_variety(self, id: int) -> Optional[CalabiYauVariety]:
        """
        Get a variety by its ID.
        
        Args:
            id: Variety ID (1-150)
        
        Returns:
            CalabiYauVariety or None if not found
        """
        for variety in self.varieties:
            if variety.id == id:
                return variety
        return None
    
    def get_all(self) -> List[CalabiYauVariety]:
        """
        Get all varieties.
        
        Returns:
            List of all CalabiYauVariety objects
        """
        return self.varieties
    
    def filter_by_h11(self, h11: int) -> List[CalabiYauVariety]:
        """
        Filter varieties by h^{1,1} value.
        
        Args:
            h11: Value of h^{1,1} to filter
        
        Returns:
            List of matching varieties
        """
        return [v for v in self.varieties if v.h11 == h11]
    
    def filter_by_h21(self, h21: int) -> List[CalabiYauVariety]:
        """
        Filter varieties by h^{2,1} value.
        
        Args:
            h21: Value of h^{2,1} to filter
        
        Returns:
            List of matching varieties
        """
        return [v for v in self.varieties if v.h21 == h21]
    
    def filter_by_euler(self, chi: int) -> List[CalabiYauVariety]:
        """
        Filter varieties by Euler characteristic.
        
        Args:
            chi: Euler characteristic value
        
        Returns:
            List of matching varieties
        """
        return [v for v in self.varieties if v.euler_characteristic == chi]
    
    def get_quintic_fermat(self) -> Optional[CalabiYauVariety]:
        """
        Get the famous Fermat quintic variety with (h¹¹=1, h²¹=101).
        
        Returns:
            The Fermat quintic variety or None
        """
        candidates = [v for v in self.varieties if v.h11 == 1 and v.h21 == 101]
        return candidates[0] if candidates else None
    
    def export_to_csv(self, output_file: Path):
        """
        Export varieties to CSV format.
        
        Args:
            output_file: Path to output CSV file
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'h11', 'h21', 'euler_characteristic'])
            
            for variety in self.varieties:
                writer.writerow([
                    variety.id,
                    variety.h11,
                    variety.h21,
                    variety.euler_characteristic
                ])
        
        print(f"✅ Exported {len(self.varieties)} varieties to {output_file}")
    
    def export_to_json(self, output_file: Path, pretty: bool = True):
        """
        Export varieties to JSON format.
        
        Args:
            output_file: Path to output JSON file
            pretty: Whether to pretty-print the JSON
        """
        data = {
            'metadata': self.metadata,
            'varieties': [
                {
                    'id': v.id,
                    'h11': v.h11,
                    'h21': v.h21,
                    'euler_characteristic': v.euler_characteristic
                }
                for v in self.varieties
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        print(f"✅ Exported {len(self.varieties)} varieties to {output_file}")
    
    def print_summary(self):
        """Print a summary of the database."""
        print("=" * 80)
        print("CALABI-YAU VARIETIES DATABASE")
        print("=" * 80)
        print()
        print(f"Total varieties: {len(self.varieties)}")
        print()
        print("Metadata:")
        for key, value in self.metadata.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {value}")
        print()
        
        # Statistics
        h11_values = [v.h11 for v in self.varieties]
        h21_values = [v.h21 for v in self.varieties]
        chi_values = [v.euler_characteristic for v in self.varieties]
        
        print("Statistics:")
        print(f"  h¹¹ range: [{min(h11_values)}, {max(h11_values)}]")
        print(f"  h²¹ range: [{min(h21_values)}, {max(h21_values)}]")
        print(f"  χ range: [{min(chi_values)}, {max(chi_values)}]")
        print()
    
    def print_list(self, n: int = 10):
        """
        Print the first n varieties.
        
        Args:
            n: Number of varieties to print (default: 10)
        """
        print(f"First {min(n, len(self.varieties))} Calabi-Yau varieties:")
        print("-" * 80)
        print(f"{'ID':<5} {'h¹¹':<6} {'h²¹':<6} {'χ':<8}")
        print("-" * 80)
        
        for variety in self.varieties[:n]:
            print(f"{variety.id:<5} {variety.h11:<6} {variety.h21:<6} {variety.euler_characteristic:<8}")
        
        if len(self.varieties) > n:
            print(f"... and {len(self.varieties) - n} more varieties")
        print()


def main():
    """
    Main function to demonstrate usage of the Calabi-Yau database.
    """
    # Load the database
    db = CalabiYauDatabase()
    
    # Print summary
    db.print_summary()
    
    # Print first 20 varieties
    db.print_list(n=20)
    
    # Get the Fermat quintic
    quintic = db.get_quintic_fermat()
    if quintic:
        print("Famous Fermat Quintic:")
        print(f"  {quintic}")
        print()
    
    # Export to CSV and JSON
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    csv_file = output_dir / "calabi_yau_varieties.csv"
    db.export_to_csv(csv_file)
    
    json_file = output_dir / "calabi_yau_varieties_export.json"
    db.export_to_json(json_file)
    
    print()
    print("=" * 80)
    print("Database ready for use!")
    print("=" * 80)


if __name__ == "__main__":
    main()
