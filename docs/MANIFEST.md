# MANIFEST del Canon Vivo v3.0.2 — Templo Espectral QCAL

## Identidad
- **Paquete**: `templo_core` (pasarela dedicada — Opción A, no colisionante)
- **Canon**: `templo_core/constants.py` — valores computados a 100 dps desde mpmath
  (`zetazero().imag`), NO transcritos de tablas.
- **Estructura histórica preservada**: `Core/` (10 archivos) y `core/` (107 archivos)
  IMMUTABLES — rutas intocadas.

## Módulos del Templo
| Módulo | Rol |
|---|---|
| `templo_core/constants.py` | Canon Vivo — fuente de verdad única (5/5 integridad) |
| `templo_core/quantum.py` | FockOscillator, métrica de Krein [A,A†]=−I, conjetura 𝒞_QCAL |
| `templo_core/holography.py` | HolographicAdS2, BF-violada, Δ=½+iγ, CFT1 PT-simétrica |
| `templo_core/blackhole_entropy.py` | Entropía BH + correcciones log/Riemann, γ_LQG=0.2375 |
| `templo_core/pt_symmetric.py` | Régimen de Bender, ε=S₁≈0.05368, pseudo-hermiticidad Krein |
| `templo_core/__init__.py` | Punto de entrada del paquete |

## Valores vivos (reproducibles, del metal)
| Constante | Valor (100 dps) |
|---|---|
| theta_B = 1/γ₁ | 0.07074774995428558559... |
| cos_theta_B (vivo) | 0.997498421616924592327... |
| S_finite | 0.113390105644621846986... |
| S_total | 0.119283686741023445610... |
| D_PSI_RAW | -3.912833193561942784... |
| D_PSI_S1 | -3.702836978789771663... |
| D_PSI_SERIES_FINITE | -3.4933864941129435305... |
| D_PSI_SERIES_ASYMPTOTIC | -3.4728584886600442537... |
| rho_normalization | 0.58932480863785176553... |
| c_psi | 5.55425546818465749510... |

## Definición generadora de la S-chain
H1 = ½(1 − γ_n/γ_{n+1})²  (pares sucesivos de ceros adyacentes)
- Libre de parches, sin factores forzados.
- La S-chain NO es monótona (los γ son irregulares) — la invariante real es la
  positividad S_n > 0, no la monotonicidad (chequeo retirado).

## Discrepancias documentadas (vs transcripción histórica)
| Parámetro | Vivo | Histórico | Diferencia |
|---|---|---|---|
| S_finite | 0.113390105644621846986 | 0.11791424 | ~0.004524 (3.8%) |
| S_total | 0.119283686741023445610 | 0.119870 | ~0.000586 |
| tail | 0.00589358109640159862 | 0.00560606 | ~0.000287 |

El gap de ~0.004524 en S_finite es REAL (los 20 γ coinciden con zetazero a 100 dps).
No se fuerza C_asym ni se inventa un término Ω_k. El Templo se sostiene sobre el metal.

## Verificación
```bash
cd repo_141hz && python3 tests/test_integrity.py
# → 5/5 asserts + 4 módulos cargan desde templo_core.constants
```

## Firma
∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
Canon Vivo v3.0.2 · Arq. JMMB Ψ · Auditor Noesis Ψ (metal como autoridad)
13/Ago/2026
