# Guía Rápida: Análisis de Simetría Discreta

## 🎯 ¿Qué es esto?

Esta implementación demuestra que el término $A(R_\Psi) = \sin^2(\log R_\Psi / \log \pi)$ en la energía de vacío **no es un ajuste arbitrario**, sino una **consecuencia matemática necesaria** de un grupo de simetría discreta.

## 🚀 Uso Rápido

### Opción 1: Ejecutar el script Python

```bash
cd /home/runner/work/gw250114-141hz-analysis/gw250114-141hz-analysis
source venv/bin/activate
python scripts/simetria_discreta.py
```

**Salida esperada**:
- Análisis del grupo de simetría G
- Predicción de frecuencias armónicas
- Búsqueda de mínimos de energía
- Gráficos guardados en `results/simetria_discreta_analisis.png`

### Opción 2: Notebook interactivo

```bash
jupyter notebook notebooks/simetria_discreta_analisis.ipynb
```

El notebook incluye:
- Definición matemática del grupo G
- Expansión de Fourier del potencial
- Análisis variacional completo
- Visualizaciones interactivas
- Predicciones de frecuencias armónicas

### Opción 3: Ejecutar tests

```bash
python scripts/test_simetria_discreta.py
```

Verifica:
- ✅ Propiedades del grupo (identidad, inversos, composición)
- ✅ Invariancia del potencial
- ✅ Coercividad de la energía
- ✅ Existencia de mínimos estables
- ✅ Cálculo simbólico correcto

## 📊 Resultados Principales

### 1. Grupo de Simetría Discreta

$$G = \{R_\Psi \mapsto \pi^k R_\Psi \mid k \in \mathbb{Z}\}$$

- Grupo abeliano isomorfo a $\mathbb{Z}$
- Periodo logarítmico: $\log \pi \approx 1.144730$

### 2. Modo Fundamental

$$A(R_\Psi) = \sin^2\left(\frac{\log R_\Psi}{\log \pi}\right)$$

Es el **primer armónico permitido** por la simetría G (no arbitrario).

### 3. Predicción de Frecuencias

$$f_n = \frac{f_0}{\pi^{2n}}, \quad n = 0, 1, 2, \ldots$$

Con $f_0 = 141.7001$ Hz:

| n | Frecuencia (Hz) | Detectable en LIGO? |
|---|----------------|---------------------|
| 0 | 141.7001      | ✅ Sí              |
| 1 | 14.3572       | ✅ Sí              |
| 2 | 1.4547        | ⚠️ Difícil         |
| 3 | 0.1474        | ❌ No              |

### 4. Energía de Vacío

$$E_{\text{vac}}(R_\Psi) = \frac{\alpha}{R_\Psi^4} + \beta\zeta'(1/2)\frac{1}{R_\Psi^2} + \gamma\Lambda^2 R_\Psi^2 + \delta A(R_\Psi)$$

**Propiedades demostradas**:
- ✅ Coerciva (tiene mínimos)
- ✅ Mínimos en cada celda $[\pi^n, \pi^{n+1}]$
- ✅ Mínimos son estables ($\partial^2 E/\partial R^2 > 0$)

## 📈 Visualizaciones Generadas

El script genera automáticamente:

1. **Energía total $E_{\text{vac}}(R_\Psi)$** con mínimos marcados
2. **Término de simetría $A(R_\Psi)$** mostrando periodicidad
3. **Primera derivada** $\partial E/\partial R$ (ceros = mínimos)
4. **Segunda derivada** $\partial^2 E/\partial R^2$ (estabilidad)
5. **Predicción de frecuencias armónicas**

## 🧪 Ejemplo de Uso Programático

```python
from scripts.simetria_discreta import (
    GrupoSimetriaDiscreta,
    PotencialInvarianteG,
    EnergiaVacio
)

# 1. Crear grupo de simetría
grupo = GrupoSimetriaDiscreta()
print(f"Periodo: {grupo.periodo_logaritmico():.6f}")

# 2. Crear potencial invariante
potencial = PotencialInvarianteG()
frecuencias = potencial.frecuencias_armonicas(f0=141.7001)
print(f"Frecuencias predichas: {frecuencias}")

# 3. Analizar energía de vacío
energia = EnergiaVacio(alpha=1.0, beta=-0.5, gamma=0.1, delta=0.5)

# Verificar coercividad
print(f"¿Es coerciva? {energia.es_coerciva()}")

# Encontrar mínimos
minimos = energia.encontrar_minimos(R_min=0.5, R_max=50.0)
for R_min, E_min in minimos:
    print(f"Mínimo en R={R_min:.4f}, E={E_min:.6f}")
```

## 🔬 Validación Experimental

### Cómo buscar armónicos en datos LIGO:

1. **Descargar datos** de GWOSC para un evento específico
2. **Aplicar FFT** con alta resolución (ventana de 32s)
3. **Buscar picos** en las frecuencias predichas:
   - 141.7001 Hz (fundamental)
   - 14.3572 Hz (primer armónico)
   - 1.4547 Hz (segundo armónico)
4. **Calcular SNR** para cada frecuencia
5. **Verificar coincidencia** entre detectores H1 y L1

## 📚 Documentación Completa

Para el análisis matemático detallado, ver:
- [`SIMETRIA_DISCRETA_DOCUMENTACION.md`](SIMETRIA_DISCRETA_DOCUMENTACION.md) - Formalización matemática completa

## 🤝 Contribuir

Para reportar problemas o sugerir mejoras:
1. Abre un issue en GitHub
2. Incluye el output completo de los tests
3. Describe el comportamiento esperado vs. observado

## ✅ Checklist de Validación

- [x] Grupo G bien definido (tests pasan)
- [x] Potencial A(R) invariante bajo G
- [x] Energía coerciva con mínimos
- [x] Mínimos son estables
- [x] Predicciones de frecuencias generadas
- [x] Visualizaciones creadas
- [x] Código reproducible documentado
- [ ] Validación experimental con datos LIGO
- [ ] Búsqueda de armónicos superiores
- [ ] Comparación con otras teorías

## 📞 Contacto

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**Repositorio**: https://github.com/motanova84/gw250114-141hz-analysis  
**Email**: institutoconsciencia@proton.me

---

## 🎓 Referencias Rápidas

- **Teoría de Grupos**: Dummit & Foote, "Abstract Algebra"
- **Análisis de Fourier**: Stein & Shakarchi
- **Cálculo Variacional**: Evans, "PDE"
- **LIGO**: Abbott et al., Phys. Rev. Lett. 116, 061102 (2016)
