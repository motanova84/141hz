# QCAL (141.7 Hz) — Análisis Reproducible

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18557905.svg)](https://doi.org/10.5281/zenodo.18557905)

## Prior Art / Registro de Autoría

Este repositorio se integra en el ecosistema **MCP Noésico QCAL-EPR (QCAL ∞³)**, con trabajo público previo desde 2024.

- **Zenodo (141hz)**: [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)
- **SafeCreative (autor JMMB84)**: [safecreative.org/creators/JMMB84](https://www.safecreative.org/creators/JMMB84)
- **Ecosistema relacionado**: QCAL-BUS, Riemann-adelic, biologia-cuantica-noesica y demás repositorios QCAL ∞³.

## Uso rápido
```bash
pip install -e .
python -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts
```

## Resultados

- **Tablas:** `artifacts/tables/*.csv`
- **Figuras:** `artifacts/figures/*.png`

## Reproducibilidad

```bash
cd repro/GWTC-1
pip-compile --generate-hashes requirements.in -o env.lock
./run.sh
```

## Cita

Ver CITATION.cff.

---

### 🔱 TRIPLE CONVENCIÓN DE EVALUACIÓN ZETA (QCAL-SYMBIO) — CANON OFICIAL

> **Declaración canónica (13/Ago/2026). Bajo f₀ = 141.7001 Hz y Ψ = 0.999999.**
> La función zeta de Riemann se evalúa en **tres caras semánticamente diferenciadas**. No son errores ni ambigüedades:
> son **tres dimensiones acopladas** de la misma realidad espectral.

| Cara | Constante | Valor | Identidad | Rol |
|---|---|---|---|---|
| **I · Canónica** | `ZETA_PRIME_HALF` | **−0.20788622497735456** | ζ′(1/2) derivada analítica | Teorema QCAL-π · κ_Π · Latido primario |
| **II · Amplitud** | `ZETA_HALF` | **−1.4603545088095868** | ζ(1/2) la función | Nivel de suelo del vacío en línea crítica |
| **III · Operador SABIO∞⁴** | `ZETA_PRIME_SABIO` | **−3.922646** | Operador de transformación / flujo de entropía nula | Ecuación de Resurrección · Axioma de Emisión · acción espectral |

```python
ZETA_PRIME_HALF  = -0.20788622497735456   # Cara I: ζ′(1/2) Analítico Canónico (QCAL-π & κ_Π)
ZETA_HALF        = -1.4603545088095868    # Cara II: ζ(1/2) Amplitud de Campo en la Línea Crítica
ZETA_PRIME_SABIO = -3.922646              # Cara III: Operador Efectivo de Emisión Coherente SABIO∞⁴
```

> *El reordenamiento no destruye ninguna dimensión: las ubica en su verdadero eje.*
> Estructural = derivada pura −0.2078 · Dinámico = magnitud de campo −1.4603 · Resonante (SABIO∞⁴) = acción espectral −3.9226.

∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ · 13/Ago/2026

