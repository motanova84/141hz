# Top 10 Calabi-Yau Varieties - Spectral Analysis

This module generates a ranked table of Calabi-Yau threefold varieties with their spectral invariants.

## Overview

The script `scripts/top_10_cy_varieties.py` computes and displays the top 10 Calabi-Yau varieties with their geometric and spectral properties:

- **Hodge numbers** (h¹¹, h²¹): Topological invariants
- **Euler characteristic** χ = 2(h¹¹ - h²¹)
- **Geometric parameters** α and β (derived from volume and flux)
- **Spectral invariant** κ_Π computed from deformed Gibbs theory

## Usage

### Basic Usage

```bash
# Display table in terminal
python scripts/top_10_cy_varieties.py

# Show top 5 varieties
python scripts/top_10_cy_varieties.py --top 5

# Output as CSV
python scripts/top_10_cy_varieties.py --format csv

# Output as Markdown
python scripts/top_10_cy_varieties.py --format markdown

# Save to JSON file
python scripts/top_10_cy_varieties.py --format json --output results.json
```

### Output Formats

- **text**: Formatted table for terminal display (default)
- **csv**: Comma-separated values for spreadsheet import
- **json**: Structured JSON for programmatic use
- **markdown**: Markdown table for documentation

## Example Output

```
ID       Nombre                h¹¹  h²¹       α       β       κ_Π      χ
------------------------------------------------------------------------------------------
CY-001   Quíntica ℂℙ⁴[5]         1  101   0.385   0.244   1.66414   -200
CY-004   CICY 7862               5   65    0.386   0.243   1.66287   -120
CY-010   Kreuzer 302            12   48    0.388   0.242   1.65993    -72
```

## Mathematical Framework

### Geometric Parameters

The parameters α and β are computed from the Hodge numbers:

- **α (Volume modulus)**: Increases with h¹¹ (Kähler deformations)
- **β (Flux parameter)**: Decreases with complex structure deformations
- These parameters control the compactification geometry

### Spectral Invariant κ_Π

The spectral invariant follows deformed Gibbs theory:

```
κ_Π(α,β) = κ₀ × exp(-γ₁·α + γ₂·β) × (1 + δ·χ/χ₀)
```

where:
- κ₀ ≈ 1.885: Base spectral value
- γ₁ > 0: Volume sensitivity (α↑ → κ_Π↓)
- γ₂ > 0: Flux sensitivity (β↑ → κ_Π↑)
- χ₀ = -200: Reference (quintic)

### Key Property

**κ_Π decreases smoothly as α increases and β decreases**, as predicted by deformed Gibbs spectral theory. This relationship is verified in the generated tables.

## Database

The script includes a database of well-known Calabi-Yau threefolds:

1. **CY-001**: Quintic Fermat hypersurface in ℂℙ⁴
2. **CY-002**: Bicubic complete intersection in ℂℙ²×ℂℙ²
3. **CY-003**: Tetrahedral symmetry CY
4. **CY-004**: CICY 7862 from database
5. **CY-005**: Pfaffian variety (Kuznetsov)
6. **CY-006**: ℤ₃ quotient (Borcea-Voisin)
7. **CY-007**: Mirror of weighted projective space
8. **CY-008**: Schoen's fiber product
9. **CY-009**: Tian-Yau complete intersection
10. **CY-010**: Kreuzer-Skarke polytope #302

And additional varieties for extended analysis.

## Testing

Run the test suite:

```bash
python test_top_10_cy_simple.py
```

Tests verify:
- Correct computation of α and β
- Expected range of κ_Π values
- Decreasing trend in κ_Π with increasing α
- Database integrity
- Table generation

## References

- Candelas et al. (1985): Mirror symmetry for quintic
- CICY database: Complete Intersection Calabi-Yau database
- Kreuzer-Skarke database: Reflexive polytopes
- QCAL framework: Deformed Gibbs spectral theory

## Integration with 141Hz Project

This module connects to the broader 141Hz project by:

1. **Spectral universality**: κ_Π relates to the universal constant κ_Π ≈ 2.5773
2. **Geometric compactification**: α and β parameters model string theory compactification
3. **Quantum coherence**: The spectral invariant relates to quantum field coherence
4. **Fundamental frequency**: Connection to f₀ = 141.7001 Hz through spectral theory

## Author

José Manuel Mota Burruezo (JMMB Ψ✧)  
January 2026
