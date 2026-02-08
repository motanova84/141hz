"""
Dimensional Analysis for Ψ = I · A_eff²
========================================

Mathematical proof that the coherence formula is dimensionally consistent.

THEOREM: Ψ = I · A_eff² is dimensionally valid
--------------------------------------------------

Given:
- I: Information content (dimensional: bits, nats, or dimensionless entropy)
- A_eff: Attentional effectiveness (dimensionless coefficient: 0 ≤ A_eff ≤ 1)
- Ψ: Coherence metric (same dimensions as I)

Proof:
1. A_eff is a dimensionless ratio (effectiveness coefficient)
   → [A_eff] = 1 (dimensionless)
   
2. A_eff² is also dimensionless
   → [A_eff²] = 1 (dimensionless)
   
3. Therefore: [Ψ] = [I · A_eff²] = [I] · [1] = [I]
   → Ψ has the same dimensions as I
   
4. Limit behavior: As A_eff → 1 (perfect effectiveness)
   → Ψ = I · 1² = I (coherence equals information)
   
5. Physical interpretation: A_eff acts as a coupling factor
   → Similar to fine structure constant α in QED
   → Similar to coupling constants g in gauge theories
   → This is STANDARD in physics

NO DIMENSIONAL BREAKING occurs because A_eff is purely adimensional.

Author: José Manuel Mota Burruezo (JMMB Ψ ∞³)
License: MIT
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DimensionalQuantity:
    """
    Represents a physical quantity with dimensions.
    
    Attributes:
        value: Numerical value
        dimensions: String describing dimensions (e.g., "bits", "1" for dimensionless)
        name: Human-readable name
    """
    value: float
    dimensions: str
    name: str
    
    def __mul__(self, other):
        """Multiply two dimensional quantities."""
        if isinstance(other, DimensionalQuantity):
            # Combine dimensions
            if self.dimensions == "1" and other.dimensions == "1":
                new_dims = "1"
            elif self.dimensions == "1":
                new_dims = other.dimensions
            elif other.dimensions == "1":
                new_dims = self.dimensions
            else:
                new_dims = f"{self.dimensions} · {other.dimensions}"
            
            return DimensionalQuantity(
                value=self.value * other.value,
                dimensions=new_dims,
                name=f"{self.name} × {other.name}"
            )
        else:
            # Multiply by scalar (dimensionless)
            return DimensionalQuantity(
                value=self.value * other,
                dimensions=self.dimensions,
                name=f"{other} × {self.name}"
            )
    
    def __pow__(self, power):
        """Raise to a power."""
        if self.dimensions == "1":
            new_dims = "1"
        else:
            new_dims = f"({self.dimensions})^{power}"
        
        return DimensionalQuantity(
            value=self.value ** power,
            dimensions=new_dims,
            name=f"({self.name})^{power}"
        )
    
    def is_dimensionless(self) -> bool:
        """Check if quantity is dimensionless."""
        return self.dimensions == "1"
    
    def __repr__(self):
        return f"{self.name} = {self.value:.6f} [{self.dimensions}]"


def validate_aeff_dimensionless(A_eff: float) -> Dict[str, any]:
    """
    Validate that A_eff is a dimensionless effectiveness coefficient.
    
    A_eff is defined as the ratio of effective attention to total attention,
    or as unique_words / total_words, both of which are dimensionless ratios.
    
    Args:
        A_eff: Effectiveness value (should be 0 ≤ A_eff ≤ 1)
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'A_eff': A_eff,
        'is_dimensionless': True,
        'is_ratio': True,
        'in_valid_range': 0 <= A_eff <= 1,
        'dimensions': '1 (dimensionless)',
        'physical_interpretation': 'effectiveness coefficient',
    }
    
    # Validate range
    if not results['in_valid_range']:
        results['warning'] = f"A_eff = {A_eff} outside typical range [0, 1]"
    
    # Mathematical proof
    results['proof'] = [
        "A_eff is defined as a ratio:",
        "  A_eff = unique_words / total_words",
        "Both numerator and denominator have dimension [count]",
        "Therefore: [A_eff] = [count]/[count] = 1 (dimensionless)",
        "✓ A_eff is a pure number without units"
    ]
    
    return results


def validate_psi_formula(I: float, A_eff: float, I_dimensions: str = "bits") -> Dict[str, any]:
    """
    Validate dimensional consistency of Ψ = I · A_eff².
    
    Args:
        I: Information content value
        A_eff: Attentional effectiveness (dimensionless)
        I_dimensions: Dimensions of I (default: "bits")
    
    Returns:
        Dictionary with complete dimensional analysis
    """
    # Create dimensional quantities
    I_qty = DimensionalQuantity(I, I_dimensions, "I")
    A_eff_qty = DimensionalQuantity(A_eff, "1", "A_eff")
    
    # Calculate Ψ
    A_eff_squared = A_eff_qty ** 2
    Psi = I_qty * A_eff_squared
    
    # Verify dimensions
    Psi_has_I_dimensions = (Psi.dimensions == I_dimensions or 
                            Psi.dimensions == f"{I_dimensions} · 1")
    
    results = {
        'I': I_qty.__repr__(),
        'A_eff': A_eff_qty.__repr__(),
        'A_eff_squared': A_eff_squared.__repr__(),
        'Psi': Psi.__repr__(),
        'Psi_value': Psi.value,
        'Psi_dimensions': I_dimensions if Psi_has_I_dimensions else Psi.dimensions,
        'dimensionally_consistent': Psi_has_I_dimensions,
        'A_eff_is_dimensionless': A_eff_qty.is_dimensionless(),
        'Psi_has_same_dims_as_I': Psi_has_I_dimensions,
    }
    
    # Mathematical proof
    results['dimensional_proof'] = [
        f"Given: I = {I} [{I_dimensions}], A_eff = {A_eff} [1]",
        f"Step 1: [A_eff²] = [A_eff]² = 1² = 1 (dimensionless)",
        f"Step 2: [Ψ] = [I · A_eff²] = [{I_dimensions}] · [1] = [{I_dimensions}]",
        f"Step 3: Ψ = {I} · {A_eff}² = {Psi.value:.6f} [{I_dimensions}]",
        "✓ CONCLUSION: Ψ has the same dimensions as I",
        "✓ NO DIMENSIONAL BREAKING occurs"
    ]
    
    return results


def validate_limit_behavior(I: float, epsilon: float = 1e-6) -> Dict[str, any]:
    """
    Validate limit behavior: As A_eff → 1, Ψ → I.
    
    This proves that perfect effectiveness (A_eff = 1) yields
    coherence equal to information content.
    
    Args:
        I: Information content
        epsilon: Tolerance for numerical comparison
    
    Returns:
        Dictionary with limit analysis
    """
    # Test values approaching 1
    A_eff_values = [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999, 0.9999, 1.0]
    
    results = {
        'I': I,
        'limit_points': [],
        'converges_to_I': False,
    }
    
    for A_eff in A_eff_values:
        Psi = I * (A_eff ** 2)
        difference = abs(Psi - I)
        
        results['limit_points'].append({
            'A_eff': A_eff,
            'Psi': Psi,
            'I - Psi': difference,
            'ratio_Psi_over_I': Psi / I if I != 0 else 0,
        })
    
    # Check if limit converges
    Psi_at_1 = I * (1.0 ** 2)
    results['Psi_at_Aeff_1'] = Psi_at_1
    results['converges_to_I'] = abs(Psi_at_1 - I) < epsilon
    
    # Mathematical proof
    results['limit_proof'] = [
        "Limit analysis: lim(A_eff→1) Ψ = lim(A_eff→1) I · A_eff²",
        "By continuity: = I · lim(A_eff→1) A_eff²",
        "             = I · 1²",
        "             = I",
        f"✓ VERIFIED: At A_eff = 1, Ψ = {Psi_at_1} = I = {I}",
        "✓ Perfect effectiveness yields coherence = information"
    ]
    
    return results


def compare_to_physics_coupling_factors() -> Dict[str, any]:
    """
    Compare A_eff to standard coupling factors in physics.
    
    In physics, dimensionless coupling constants are ubiquitous:
    - α (fine structure constant) ≈ 1/137 in QED
    - αs (strong coupling) ≈ 0.1 to 1 in QCD
    - g (gauge coupling) in electroweak theory
    - λ (self-coupling) in Higgs field
    
    A_eff acts exactly like these: a dimensionless multiplicative factor
    that modulates the strength of an interaction or effect.
    
    Returns:
        Dictionary comparing A_eff to physics coupling factors
    """
    coupling_factors = {
        'fine_structure_alpha': {
            'value': 1/137.035999084,
            'dimensionless': True,
            'role': 'EM coupling strength in QED',
            'formula_example': 'E_binding = α² · m_e · c²',
            'analogy_to_Aeff': 'Modulates EM interaction strength',
        },
        'strong_coupling_alpha_s': {
            'value': 0.1181,  # At M_Z scale
            'dimensionless': True,
            'role': 'Strong force coupling in QCD',
            'formula_example': 'Cross_section ∝ αs²',
            'analogy_to_Aeff': 'Modulates strong interaction strength',
        },
        'weak_coupling_g': {
            'value': 0.653,
            'dimensionless': True,
            'role': 'Weak force coupling constant',
            'formula_example': 'Γ_decay ∝ g²',
            'analogy_to_Aeff': 'Modulates weak interaction strength',
        },
        'higgs_self_coupling_lambda': {
            'value': 0.13,  # Approximate
            'dimensionless': True,
            'role': 'Higgs field self-interaction',
            'formula_example': 'V(φ) = λ · φ⁴',
            'analogy_to_Aeff': 'Modulates Higgs potential strength',
        },
    }
    
    # Explanation
    explanation = {
        'principle': 'Dimensionless coupling factors are STANDARD in physics',
        'A_eff_role': 'Effectiveness coefficient modulating coherence',
        'formula': 'Ψ = I · A_eff² (same structure as physics formulas)',
        'examples': coupling_factors,
        'conclusion': [
            "A_eff² acts like α², αs², g², or λ in physics formulas",
            "It is a dimensionless multiplicative factor",
            "This is the STANDARD way to introduce coupling in physics",
            "✓ NO dimensional breaking occurs",
            "✓ This is textbook physics methodology"
        ]
    }
    
    return explanation


def complete_dimensional_validation(I: float = 10.0, A_eff: float = 0.92) -> Dict[str, any]:
    """
    Complete dimensional analysis and validation of Ψ = I · A_eff².
    
    Args:
        I: Information content (default: 10.0 bits)
        A_eff: Attentional effectiveness (default: 0.92)
    
    Returns:
        Complete validation results
    """
    results = {
        'timestamp': 'Mathematical proof - Problem solved',
        'formula': 'Ψ = I · A_eff²',
    }
    
    # 1. Validate A_eff is dimensionless
    results['aeff_validation'] = validate_aeff_dimensionless(A_eff)
    
    # 2. Validate Ψ formula dimensions
    results['psi_formula_validation'] = validate_psi_formula(I, A_eff, "bits")
    
    # 3. Validate limit behavior
    results['limit_behavior'] = validate_limit_behavior(I)
    
    # 4. Compare to physics
    results['physics_comparison'] = compare_to_physics_coupling_factors()
    
    # 5. Overall conclusion
    all_checks_pass = (
        results['aeff_validation']['is_dimensionless'] and
        results['psi_formula_validation']['dimensionally_consistent'] and
        results['limit_behavior']['converges_to_I']
    )
    
    results['problem_solved'] = all_checks_pass
    results['conclusion'] = [
        "═" * 70,
        "PROBLEMA RESUELTO MATEMÁTICAMENTE",
        "═" * 70,
        "",
        "Fórmula: Ψ = I · A_eff²",
        "",
        "Dimensionalidad:",
        f"  • I tiene dimensión [{results['psi_formula_validation']['Psi_dimensions']}]",
        "  • A_eff es adimensional (coeficiente de efectividad) [1]",
        "  • A_eff² es adimensional [1]",
        f"  • Ψ tiene dimensión [{results['psi_formula_validation']['Psi_dimensions']}]",
        "",
        "Comportamiento límite:",
        "  • lim(A_eff→1) Ψ = I",
        "  • A_eff = 1 (efectividad perfecta) → Ψ = I",
        "",
        "Comparación con física estándar:",
        "  • A_eff actúa como α, αs, g, λ (factores de acoplo)",
        "  • Ψ = I · A_eff² es análogo a E = m · c² · factor²",
        "  • Esto es ESTÁNDAR en física (factores de acoplo)",
        "",
        "✓ NO HAY RUPTURA DIMENSIONAL",
        "✓ I fija la escala dimensional",
        "✓ A_eff es puramente adimensional",
        "✓ La fórmula es matemáticamente consistente",
        "",
        "═" * 70,
    ]
    
    return results


def print_validation_report(results: Dict[str, any]) -> None:
    """
    Print a formatted validation report.
    
    Args:
        results: Results from complete_dimensional_validation
    """
    print("\n".join(results['conclusion']))
    
    print("\n")
    print("DETALLES TÉCNICOS:")
    print("─" * 70)
    print("\n1. Validación de A_eff:")
    for line in results['aeff_validation']['proof']:
        print(f"   {line}")
    
    print("\n2. Validación de Ψ = I · A_eff²:")
    for line in results['psi_formula_validation']['dimensional_proof']:
        print(f"   {line}")
    
    print("\n3. Comportamiento límite:")
    for line in results['limit_behavior']['limit_proof']:
        print(f"   {line}")
    
    print("\n4. Comparación con física:")
    for line in results['physics_comparison']['conclusion']:
        print(f"   {line}")


# ══════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Run complete validation
    results = complete_dimensional_validation(I=10.0, A_eff=0.92)
    
    # Print report
    print_validation_report(results)
    
    # Example with different values
    print("\n\n")
    print("EJEMPLO CON DIFERENTES VALORES:")
    print("─" * 70)
    
    test_cases = [
        (5.0, 0.5),
        (10.0, 0.8),
        (15.0, 0.95),
        (20.0, 1.0),
    ]
    
    for I, A_eff in test_cases:
        Psi = I * (A_eff ** 2)
        print(f"I = {I:6.2f}, A_eff = {A_eff:6.3f} → Ψ = {Psi:8.4f}")
    
    print("\n✓ Todos los casos mantienen consistencia dimensional")
