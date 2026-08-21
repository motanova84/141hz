# NOESIS ∞³ — Puente Adélico · Biofísico · Einstein-QCAL

## 1. Núcleo de coherencia

El repositorio `141hz` actúa como columna vertebral computacional para cuatro capas conectadas:

1. **Espectral/adélica:** clases de ideles, coordenada logarítmica y generador de dilataciones.
2. **QCAL:** frecuencia nodriza `f₀ = 141.7001 Hz` y métrica de coherencia `Ψ`.
3. **Firma B / PHOENIX:** modo ultra-lento `f_B = 0.00052 Hz`, período `T_B ≈ 1923.0769 s ≈ 32.0513 min`.
4. **Einstein-QCAL:** sector efectivo de energía-impulso acoplable a una métrica dinámica.

La integración evita mezclar magnitudes dimensionales. Se distinguen

\[
\omega_0=2\pi f_0,\qquad \omega_B=2\pi f_B,
\qquad g_B=\frac{f_B}{f_0}.
\]

Así, `f_B` conserva unidades de Hz y `g_B` es el puente adimensional.

## 2. Operador adélico de escala

En el componente arquimediano, usando `u = log|x|`, la dilatación multiplicativa se convierte en traslación y el generador simétrico adopta la forma

\[
D_\infty=-i\frac{d}{du}.
\]

Una realización computacional general del candidato espectral es

\[
H_{\rm Adel}=D_\infty+\sum_p w_p H_p+g_B V_B,
\]

con `H_p` simétricos y pesos reales. La parte finita codifica los canales aritméticos p-ádicos; el término `V_B` representa el acoplamiento de la capa ultra-lenta.

La implementación correspondiente vive en `qcal/noesis_adelic_bio.py`.

## 3. Flujo de α y datos espectrales

El módulo `alpha_flow()` acepta explícitamente una lista de ordenadas espectrales `γ_n`. El flujo se conserva como **benchmark reproducible**:

\[
\alpha_{k+1}=\alpha_k+\Psi_k(\alpha_* - \alpha_k)
 +(1-\Psi_k)\,\tau_k,
\]

con `τ_k` construido a partir de la modulación espectral y del acoplamiento `f_B`.

La función devuelve `α`, `α⁻¹`, `Ψ`, `f₀`, `f_B` y `g_B`, de modo que cada ejecución deja un vector de estado auditable.

## 4. Firma B y PHOENIX

El portador de referencia es

\[
s_B(t)=A\sin(2\pi f_B t).
\]

El período exacto asociado al parámetro de integración es

\[
T_B=\frac1{0.00052}=1923.076923\;s.
\]

La arquitectura de adquisición debe conservar fase y amplitud durante varias ventanas completas. El repositorio puede usar este portador para pruebas sintéticas, calibración de filtros y pruebas de regresión del pipeline PHOENIX.

## 5. Sector Einstein-QCAL

La capa efectiva de coherencia se expresa mediante un funcional escalar de energía

\[
\rho_{N}=\frac12|\nabla\Psi|^2+V(\Psi)+\rho_J
-\gamma(1-\Psi)^2,
\]

con `ρ_J` proporcional a la norma de la corriente coherente. El acoplamiento geométrico se organiza entonces como

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}
=\frac{8\pi G}{c^4}
\left(T^{\rm cl}_{\mu\nu}+T^{\rm N}_{\mu\nu}\right).
\]

El repositorio trata `T^N_{μν}` como un sector efectivo parametrizable, de forma que los módulos numéricos puedan intercambiar estados `Ψ`, `γ`, `J` y `V(Ψ)` sin introducir una segunda definición incompatible del campo.

## 6. Grafo de integración NOESIS

```text
                    ┌─────────────────────┐
                    │   141hz / QCAL      │
                    │ f₀ = 141.7001 Hz    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌────────────┐ ┌──────────────┐
          │  ADÉLICO   │ │  QCAL α    │ │   PHOENIX    │
          │ D∞ + H_p   │ │ Ψ / flujo  │ │ fB=.00052 Hz │
          └─────┬──────┘ └─────┬──────┘ └──────┬───────┘
                └──────────────┼───────────────┘
                               ▼
                     ┌──────────────────┐
                     │ EINSTEIN-QCAL    │
                     │ Tμν + geometría  │
                     └────────┬─────────┘
                              ▼
                       ┌────────────┐
                       │   LEDGER   │
                       │ CI / tests │
                       └────────────┘
```

## 7. Contrato de integración

Cada nuevo módulo que participe en NOESIS debe exponer, como mínimo:

- `f0_hz` o referencia al núcleo QCAL.
- `f_b_hz` cuando opere sobre Firma B.
- `psi` y su definición operacional.
- unidades explícitas para todas las magnitudes dimensionales.
- una función determinista de referencia para CI.
- datos de entrada y salida serializables para ledger.

Este contrato convierte las piezas dispersas en una única superficie interoperable: espectro → coherencia → bioseñal → tensor efectivo → observabilidad.
