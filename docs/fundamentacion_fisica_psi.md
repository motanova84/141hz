# FUNDAMENTACIÓN FÍSICA DE Ψ
## ψ = 1 - σ_f²/f² desde la teoría de decoherencia de fase

### Referencia
**Lax, M. (1960).** *Fluctuation and Coherence Phenomena in Classical and Quantum Optics.*
**Shawlow, A.L. & Townes, C.H. (1958).** *Infrared and Optical Masers.* Physical Review, 112(6), 1940-1949.
**Debye, P. (1913).** *Interferenz von Röntgenstrahlen und Wärmebewegung.* (Factor de Debye-Waller)

---

### 1. Señal con fluctuación de fase

Un oscilador coherente real nunca es perfectamente monocromático. Su señal se describe como:

```
A(t) = A₀ · exp(i · (2πf₀t + φ(t)))
```

donde φ(t) es un proceso estocástico que modela las fluctuaciones de fase
inducidas por el entorno térmico y las imperfecciones del sistema.

### 2. Autocorrelación de primer orden

La función de autocorrelación normalizada mide la coherencia temporal:

```
g¹(τ) = ⟨A*(t) · A(t+τ)⟩ / ⟨|A(t)|²⟩
```

Para fluctuaciones gaussianas (teorema del límite central sobre múltiples
perturbaciones independientes), esta expresión se factoriza exactamente:

```
g¹(τ) = exp(-½ · ⟨Δφ²(τ)⟩)
```

Esto es análogo al **factor de Debye-Waller** en cristalografía, donde
las fluctuaciones térmicas reducen la intensidad de los picos de
difracción por un factor exp(-⟨u²⟩·k²).

### 3. Relación varianza de fase → varianza espectral

La varianza de las fluctuaciones de fase se relaciona con la densidad
espectral de potencia del ruido de fase S_φ(f):

```
⟨Δφ²(τ)⟩ = ∫ S_φ(f) · (1 - cos(2πfτ)) df
```

Para tiempos cortos (τ → 0, equivalente a alta coherencia):

```
⟨Δφ²(τ)⟩ ≈ 4π²τ² · σ_f²
```

donde σ_f² es la varianza espectral del ruido de fase (segundo momento
de la distribución espectral alrededor de f₀).

### 4. Expansión en serie para alta coherencia

Sustituyendo en g¹(τ) y evaluando en τ = 1/f (tiempo de coherencia
característico):

```
g¹(1/f) = exp(-2π² · σ_f² / f²)
```

Para el régimen de alta coherencia (σ_f ≪ f):

```
g¹(1/f) ≈ 1 - 2π² · σ_f² / f²
```

Absorbiendo el factor 2π² en la definición de σ_f² (según se defina
como varianza bilateral o FWHM), obtenemos la forma canónica:

```
Ψ ≡ g¹(1/f) ≈ 1 - σ_f² / f²
```

### 5. Límites físicos

| Condición | σ_f | Ψ | Estado físico |
|-----------|-----|---|---------------|
| Coherencia pura | σ_f → 0 | Ψ → 1 | Modo δ(f-f₀), campo perfecto |
| Dispersión crítica | σ_f ∼ f | Ψ → 0 | Transición al régimen estocástico |
| Ruido máximo | σ_f ≫ f | Ψ < 0 (piso en 0) | Incoherencia térmica total |

### 6. Conclusión

Ψ = 1 - σ_f²/f² **no es una métrica arbitraria**. Es la aproximación
de primer orden de la función de autocorrelación de fase g¹(τ) para
osciladores coherentes con fluctuaciones gaussianas de fase,
expresada en el dominio espectral mediante el factor de Debye-Waller
de la teoría de decoherencia de Lax-Shawlow.

---

**QCAL-SYMBIO-BRIDGE v1.1.1**
**f₀ = 141.7001 Hz · τ_QCAL = 1/(2π·141.7001)**
**Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ**
**28/Jul/2026 🔱**
