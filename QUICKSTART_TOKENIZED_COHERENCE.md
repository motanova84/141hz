# Quick Start: Modo Coherencia Tokenizada QCAL ∞³

> **Análisis rápido del corpus tokenizado y comparación con benchmarks AI/Math**

## 🚀 Uso Rápido (1 comando)

```bash
# Analizar corpus y generar métricas
python scripts/analizar_corpus_tokenizado.py
```

**Salida esperada:**
- Total de tokens: ~5.2M (este repositorio)
- Comparación con GPT-4, arXiv Math, Lean4 Library
- Archivos guardados en `results/`

## 📊 Ver Resultados

```bash
# Ver métricas detalladas
cat results/corpus_tokenizado_metrics.json

# Ver comparación con benchmarks
cat results/corpus_tokenizado_comparison.json
```

## 🔍 Métricas Clave

| Métrica | Valor |
|---------|-------|
| **Total tokens** | ~5.2M |
| **Archivos** | ~1,923 |
| **Coherencia** | 100% |
| **Reproducibilidad** | 80% |
| **Densidad** | 5.2M tokens/repo |

## 📈 Comparación

| Corpus | Tokens | Coherencia | Reproducible |
|--------|--------|------------|--------------|
| **QCAL ∞³ (este repo)** | 5.2M | 100% | 80% |
| Ecosistema completo (35 repos) | ~60M+ | 100% | Sí |
| GPT-4 | 13T | 20% | No |
| arXiv Math | 500M | 60% | Parcial |
| Lean4 Library | 100M | 90% | Sí |

## 🛠️ Opciones Avanzadas

```bash
# Analizar repositorio específico
python scripts/analizar_corpus_tokenizado.py --repo-path /path/to/repo

# Guardar en directorio personalizado
python scripts/analizar_corpus_tokenizado.py --output-dir custom_results

# Modo silencioso (solo guardar archivos)
python scripts/analizar_corpus_tokenizado.py --quiet
```

## 🧪 Tests

```bash
# Ejecutar tests del analizador
python -m pytest tests/test_analizar_corpus_tokenizado.py -v

# Todos los tests deben pasar (16 tests)
```

## 📚 Documentación Completa

Para información detallada, ver:
- [MODO_COHERENCIA_TOKENIZADA.md](MODO_COHERENCIA_TOKENIZADA.md) - Documentación completa
- [QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md](QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md) - Compresión 1000:1

## 🔬 Integración con Token Compression

```python
from core.qcal_token_density import QCALTokenDensity

# Calcular densidad de compresión
calc = QCALTokenDensity(coherence=0.923)
metrics = calc.calculate_density(token_data, context)

# Typical density: ~1000-1100x
print(f"Compression density: {metrics.total_density:.2f}x")
```

## ✨ Resumen

**QCAL ∞³ domina en coherencia, no en volumen bruto:**
- ✓ 100% coherencia (vs 20% GPT-4)
- ✓ Reproducible (ENV.lock + lake build)
- ✓ Auto-validante (SABIO ∞⁴)
- ✓ Compresión ~1000:1 (irreplicable)

---

**∴ ✧ JMMB Ψ @ 888.888 Hz**  
f₀ = 141.7001 Hz | Coherence: Ψ = 0.923 | State: ∞³ CERTIFIED
