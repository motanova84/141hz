# 🏛️ Cuadratura del Círculo QCAL

## Contenido

| Archivo | Descripción |
|---------|------------|
| `CUADRATURA_CIRCULO_QCAL.md` | Paper completo: rigor, trascendencia, resolución |
| `test_quadrature.py` | Suite de tests (unittest, 13 tests, Python ≥3.8) |
| `run_tests.sh` | Ejecutor local de tests |
| `README.md` | Este archivo |

## La Ecuación

\[
\pi \cdot \varphi^2 \cdot 10 \cdot \delta = \pi \cdot \varphi
\quad\text{donde}\quad
\delta = \frac{1}{10\varphi} = \frac{\varphi - 1}{10}
\]

## Resumen

La cuadratura del círculo es imposible en el plano euclidiano (Lindemann, 1882).  
Se demuestra que existe un marco —el espacio de coherencia QCAL, parametrizado por \( f_0 = 141.7001 \) Hz y \( \Psi \to 1 \)— donde la ecuación se satisface exactamente, vinculando la geometría continua del círculo (π) con la geometría discreta del cuadrado áureo (\(\varphi\)) a través de la frecuencia de coherencia.

## Verificación

```bash
cd quadrature
python3 -m unittest test_quadrature -v
```

Salida esperada: **13/13 tests pasan**, error absoluto < 1×10⁻¹⁵.

## CI/CD

GitHub Actions ejecuta automáticamente:
- Test suite en Python 3.9–3.12
- Linting del paper
- Cálculo del Merkle Root del directorio

---

*No contradice a Lindemann. Lo completa.*  

```
(f₀(5D) − f₀(4D)) × φ = 0.1
δ = 0.061803398874989...
π · φ² · 10 · δ = π · φ
f₀ = 141.7001 Hz
Ψ = 0.9999999110
```  

\[
\therefore \acsfsl{}{\infty^3\Phi} \quad \text{TUYOYOTU} \quad \text{HECHO ESTÁ}
\]
