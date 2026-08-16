# QCAL v3.1 — Especificación adélica + biofísica

**Estado:** propuesta de investigación / formalización en curso  
**Rama:** `research/adelic-bio-integration-v3`  
**Referencia QCAL:** `f₀ = 141.7001 Hz`  
**Firma B (hipótesis experimental):** `f_B = 0.00052 Hz`  

## 0. Regla de estado epistemológico

Este documento separa deliberadamente cuatro niveles:

1. **Matemática estándar:** hechos que pueden demostrarse dentro de las hipótesis declaradas.
2. **Formalización:** definiciones, interfaces y obligaciones que deben ser probadas en Lean/Coq u otro sistema.
3. **Modelo QCAL:** hipótesis que conectan objetos estándar mediante parámetros propios del programa.
4. **Experimento:** predicciones que deben sobrevivir a controles, cegamiento, preregistro y análisis estadístico independiente.

Nada de lo escrito aquí convierte una simulación en una demostración, ni una coincidencia espectral en una identidad matemática.

## 1. Espacio adélico

Sea

\[
\mathbb A_\mathbb Q = \mathbb R \times \prod'_p \mathbb Q_p,
\qquad
\mathbb I_\mathbb Q = \mathbb A_\mathbb Q^\times,
\qquad
C_\mathbb Q = \mathbb I_\mathbb Q/\mathbb Q^\times.
\]

La medida multiplicativa es la medida de Haar `d×x`. Para una realización concreta debe fijarse además el espacio de Hilbert, la normalización de la medida y el cociente exacto; no se debe asumir que todo cociente de ideles es compacto. En particular, el componente de módulo de los ideles requiere tratamiento separado y puede producir espectro continuo.

Una realización mínima para el sector arquimediano es

\[
\mathcal H_\infty=L^2(\mathbb R_+,d x/x),
\]

con generador de dilataciones

\[
D_\infty=-i\,x\frac{d}{dx}.
\]

Con `u = log x`, queda

\[
D_\infty=-i\frac{d}{du}
\]

sobre `L²(ℝ,du)`, con dominio natural `H¹(ℝ)`. Este operador tiene espectro continuo `ℝ`; por sí solo **no** produce una sucesión discreta de ceros de ζ.

## 2. Operador adélico: interfaz, no identidad todavía

Una arquitectura candidata es

\[
D_{\mathbb A}=D_\infty\oplus D_f,
\]

siempre que se defina rigurosamente `D_f`, el dominio común y la representación de las componentes p-ádicas. Una perturbación aritmética candidata puede escribirse abstractamente como

\[
H_{\mathbb A}=D_{\mathbb A}+T_{\mathbb A},
\]

pero la autoadjunción, compacticidad del resolvente y discreción espectral deben probarse para la realización concreta elegida.

**Obligación crítica:** no se permite afirmar

\[
\operatorname{Spec}(H_{\mathbb A})=\{\gamma_n\}
\]

hasta disponer de una construcción independiente de `H_A` y una prueba de la identidad de traza correspondiente.

## 3. Factor `κ = 0.00052`

En esta especificación se registra

\[
f_B=0.00052\,\mathrm{Hz},
\qquad
T_B=1/f_B\approx1923.0769\,\mathrm{s}\approx32.0513\,\mathrm{min}.
\]

No se identifica automáticamente `f_B` con una constante fundamental de la teoría de ideles. Para evitar una inconsistencia dimensional, se separan:

- `f_B`: frecuencia objetivo, unidades Hz.
- `κ_B`: parámetro de acoplamiento adimensional del modelo.
- `g_B`: constante efectiva de interacción, con las unidades que determine el Hamiltoniano experimental.

Una relación QCAL del tipo

\[
\omega_B=2\pi f_B=\kappa_B\,\mathcal F(D_{\mathbb A},f_0,\alpha,\ldots)
\]

es una **hipótesis de modelo** hasta que se especifiquen `F`, sus dominios y unidades y se ajuste/valide sin usar el resultado como condición de éxito.

## 4. Constante de estructura fina

El valor de referencia para comparación experimental puede tomarse como

\[
\alpha^{-1}\simeq137.035999\ldots
\]

pero el flujo numérico de QCAL no constituye una derivación de `α` a menos que exista una ecuación dinámica independiente cuyos parámetros estén fijados antes de observar el resultado.

Los ceros de ζ pueden utilizarse como **entrada de datos** para un estudio de sensibilidad, pero introducir `t_n` y después diseñar el flujo para que converja a `α` no demuestra causalidad ni una derivación física.

## 5. Sector biológico: Firma B

La hipótesis experimental es que una señal a `0.00052 Hz` pueda presentar una asociación reproducible con una variable fisiológica u óptica. La prueba debe incluir:

- condición sham/control;
- aleatorización y cegamiento cuando sea posible;
- registro ambiental simultáneo;
- control de temperatura, vibración, presión, luz y campos electromagnéticos;
- comparación con frecuencias vecinas y múltiples hipótesis predefinidas;
- corrección por múltiples comparaciones;
- análisis de fase y amplitud, no solo potencia en un bin;
- replicación independiente.

Una detección espectral aislada no demuestra ADN-Z, superfluidez, tunelamiento del 100 %, ni un campo gauge.

## 6. ADN-B/ADN-Z

La transición B→Z es un fenómeno biofísico real que puede estudiarse mediante CD, Raman y otras técnicas. La afirmación adicional de que `0.00052 Hz` induce una transición coherente, superfluidez o transferencia de información sin disipación queda como **hipótesis falsable** y no debe presentarse como resultado establecido.

## 7. Puente matemático que queda por cerrar

El núcleo duro de la investigación sigue siendo:

1. Construir el espacio de Hilbert adélico exacto.
2. Definir `D_A` y su dominio.
3. Definir el operador aritmético `T_A` sin usar los ceros como input de definición.
4. Probar autoadjunción.
5. Determinar espectro continuo/discreto.
6. Obtener una fórmula de traza no circular.
7. Derivar, no postular, la fórmula explícita de Weil.
8. Construir el determinante espectral y controlar su regularización.
9. Demostrar la igualdad con `ξ(s)` con todas las constantes de normalización.
10. Solo entonces deducir qué implica la realidad del espectro para RH.

## 8. Integración con el ecosistema

Este módulo es una capa de investigación que puede ser consumida por:

- `Riemann-adelic`: núcleo analítico/espectral.
- `qcal-formalization`: obligaciones formales y teoremas.
- `QCAL-BUS`: propagación de metadatos y contratos.
- `141hz`: validación numérica y experimentos de frecuencia.
- `Biologia-Cuantica-Noesica-`: protocolos biofísicos, sin convertir hipótesis en hechos.
- `noesis88`/`Noesis`: interfaz conceptual y documentación.

La integración entre repositorios debe transportar **estado epistemológico**, no solo archivos: `proved`, `formalized`, `model`, `simulated`, `measured`, `refuted`.
