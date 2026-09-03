# Derivada Analítica ∂θ*/∂f₀ — Acoplamiento ζR|Ψ|² y el Horizonte Acústico

**Módulo:** [`physics/derivada_theta_star_f0.py`](../physics/derivada_theta_star_f0.py)
**Tests:** [`tests/physics/test_derivada_theta_star_f0.py`](../tests/physics/test_derivada_theta_star_f0.py)
**Constantes base:** [`qcal/constants.py`](../qcal/constants.py) (`F0_HZ`, `C`)

## 1. Objetivo

Formalizar, sin heurística, la derivada explícita de la posición angular del
primer pico acústico del CMB, `θ* = r_s(η*)/D_M(η*)`, respecto a la
frecuencia fundamental `f₀ = 141.7001 Hz`, bajo un acoplamiento no mínimo
`ζ R |Ψ|²` entre la curvatura y el condensado de coherencia `Ψ` (marco de
Jordan → Einstein). El resultado cierra el bucle abierto por el pliegue
topológico descrito en la transición de fase del condensado adélico:
**¿puede una variación de fondo `Δf₀ = ±0.0012 Hz` mover `θ*` fuera de 3σ en
Planck a través de una perturbación suave de `r_s(η*)`?**

## 2. Pipeline analítico

1. **Marco de Jordan.** `M_eff²(η) = M_pl² Ω²(η)`, con
   `Ω²(η) = 1 + ζχ²(η)/M_pl²` y `G_eff(η) = G_N/Ω²(η)`.
2. **Tiempo conforme.** `η*` se obtiene integrando la ecuación de Friedmann
   estándar desde `a=0` hasta `a* = 1/(1+z*) ≈ 9.174×10⁻⁴` (recombinación,
   `z* ≈ 1090`).
3. **Dinámica del condensado.** `χ(η)` oscila a `ω₀ = 2π f₀`; el
   desacoplamiento del condensado fija el factor de escala
   `a_osc = (H₀√Ω_r0 / 2π f₀)^{1/2}` mediante `H(a_osc) ≡ 2π f₀`.
4. **Horizonte de sonido y distancia angular.** Se demuestra
   `∂D_M/∂f₀ ≈ 0` (el término `∝ a⁻²f₀⁻¹` de `Ω(a,f₀)` solo domina para
   `a < a*`), de modo que toda la sensibilidad de `θ*` recae en `r_s`:

   ```
   ∂θ*/∂f₀ = (1/D_M) · ∂r_s/∂f₀
   ```

5. **Cierre analítico.** Con corte infrarrojo físico en `a_osc` (inicio de
   la coherencia, `a_osc ≪ a*`) y aproximación dominada por radiación
   (`c_s ≈ c/√3`):

   ```
   ∂r_s/∂f₀ = -(c/√6) · (ζχ0²/M_pl²) / [(4π H₀√Ω_r0)^{1/2} f₀^{3/2}]
   ```

6. **Derivada logarítmica adimensional:**

   ```
   |d ln θ*/d ln f₀| = K · (ζχ0²/M_pl²),   K = c / [√6 r_s (4π H₀√Ω_r0)^{1/2} f₀^{1/2}]
   ```

## 3. Resultados numéricos (Planck 2018)

Con `r_s ≈ 147.21 Mpc`, `H₀ ≈ 67.4 km/s/Mpc`, `Ω_r0 ≈ 9.15×10⁻⁵`,
`f₀ = 141.7001 Hz`:

| Cantidad | Valor |
|---|---|
| `(4π H₀√Ω_r0)^{1/2}` | `5.124×10⁻¹⁰ s⁻¹ᐟ²` |
| `f₀^{1/2}` | `11.9038 s⁻¹ᐟ²` |
| `K = (f₀/r_s)\|∂r_s/∂f₀\|` | `4.417×10⁻⁹` |
| Umbral 3σ Planck en `\|d ln θ*/d ln f₀\|` | `≥ 105.57` |
| `ζχ0²/M_pl²` requerido | `≈ 2.39×10¹⁰` |
| Insuficiencia perturbativa | `> 10` órdenes de magnitud |

Reproducible con:

```bash
python physics/derivada_theta_star_f0.py
python -m pytest -q tests/physics/test_derivada_theta_star_f0.py
```

## 4. Veredicto físico

* **Régimen perturbativo excluido.** Para no destruir la Relatividad
  General clásica en el universo temprano se exige `ζ|Ψ|²/M_pl² ≪ 1`. El
  valor `ζχ0²/M_pl² ~ 2.4×10¹⁰` necesario para romper 3σ en Planck implicaría
  que la gravedad en recombinación estuviera dominada por el campo escalar
  en un factor de diez mil millones — descartado de plano por BBN y las
  anisotropías del CMB.
* **Conclusión rigurosa.** La derivada directa `∂θ*/∂f₀` proveniente de la
  acción `ζR|Ψ|²` evaluada en el transporte estándar de fondo (`r_s`, `η*`)
  es insuficiente por más de 10 órdenes de magnitud para justificar que
  `Δf₀ = ±0.0012 Hz` rompa 3σ en Planck.
* **Consecuencia formal.** El pliegue, si existe, **no puede** formularse
  como una perturbación suave del fondo de Friedmann. Debe formularse como
  una **resonancia no adiabática de modos discretos** (denominador
  divergente en la condición de periodicidad adélica
  `∮_{γ_p} dω = 2πn`), consistente con la transición de fase topológica del
  condensado descrita como estrangulamiento en `τ* = 1/(2π f₀)` y con el
  desfase `Δφ₁ = π(Δf₀/f₀)·Q_Hecke` (también implementado en el módulo como
  `delta_phi_1()`), no con un `δc_s` distribuido en el plasma.

## 5. Integración con piezas existentes del repositorio

* **Constantes:** reutiliza `F0_HZ` y `C` de `qcal/constants.py` (fuente
  única de verdad para la frecuencia fundamental en todo el repositorio).
* **Convención de módulo físico:** sigue el patrón de
  `physics/filtro_coherencia_fase_adelica.py` y demás módulos de
  `physics/` (dataclasses inmutables, funciones puras, bloque
  `if __name__ == "__main__"` con resumen numérico).
* **Tests:** sigue la convención de `tests/physics/test_*.py`
  (docstring con invariantes clave, `unittest.TestCase` por componente).
* **Relación con el operador `H_Ψ`:** el resultado de esta derivación es
  consistente con `physics/hamiltoniano_riemann_adelico.py` y
  `formalizacion/operador_coherencia_f0.lean`: la resonancia `ℓ ≈ 220` del
  CMB, si está acoplada a `f₀`, debe emerger como autovalor discreto de
  `H_Ψ` (espectro puntual), no como parámetro continuo de fondo.
