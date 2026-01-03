# KAGRA K1: Validación Pendiente - Run O4

## 🎯 Por qué KAGRA es importante

KAGRA (K1) es crucial para validar si 141.7 Hz es una frecuencia física universal o un artefacto instrumental:

### 1. Detector Independiente
- **Ubicación:** Japón (Kamioka)
- **Operador:** Instituto Nacional de Ciencias Naturales de Japón
- **Diseño completamente independiente de LIGO**

### 2. Diseño Único
- **Subterráneo:** 200 metros bajo tierra (reducción de ruido sísmico)
- **Criogénico:** Espejos enfriados a 20K (reducción de ruido térmico)
- **Geometría diferente:** Brazos de 3 km (vs. 4 km de LIGO)

### 3. Orientación Única
- **Geometría del detector:** Diferente a H1/L1
- **Respuesta angular:** Complementaria a LIGO
- **Ubicación geográfica:** Red global de detección

## 🔬 Predicción Científica

Si 141.7 Hz es una frecuencia física universal (como predice Ψ = I × A²_eff):
- ✅ **DEBE aparecer en KAGRA K1** en eventos de fusión BBH
- ✅ **DEBE tener coherencia con H1/L1** cuando detecta simultáneamente
- ✅ **DEBE mostrar el mismo patrón de ringdown**

Si 141.7 Hz es un artefacto instrumental de LIGO:
- ❌ **NO aparecerá en KAGRA K1**
- ❌ **NO habrá coherencia con H1/L1**
- ❌ **Diferentes patrones de ruido instrumental**

## 📊 Estado Actual: Run O4

### Información del Run
- **Run O4 comenzó:** Abril 2023 (aprox.)
- **Estado:** En curso / Recientemente finalizado
- **Datos públicos:** TBD (típicamente 18 meses después del run)

### Política de Datos LIGO/Virgo/KAGRA
GWOSC (Gravitational Wave Open Science Center) libera datos en fases:
1. **Eventos significativos:** ~6 meses después de detección
2. **Catálogo completo:** ~18 meses después del run
3. **Datos de strain continuos:** Progresivamente

### Próximos Pasos
Cuando los datos estén disponibles:

```bash
# Analizar segmento específico
python scripts/analizar_kagra_k1.py --run O4 --segment START-END

# Buscar automáticamente datos disponibles
python scripts/analizar_kagra_k1.py --search-available --run O4
```

## 🌐 Análisis Comparativo Mientras Tanto

Mientras esperamos datos de KAGRA O4, podemos:

### 1. Análisis de Sensibilidad
Comparar sensibilidad teórica LIGO vs. KAGRA en 141.7 Hz:
```bash
python scripts/comparar_ligo_vs_kagra_sensibilidad.py
```

### 2. Análisis de Runs Previos
Si hay datos de runs anteriores (O3), analizarlos:
```bash
python scripts/analizar_kagra_k1.py --run O3
```

### 3. Simulaciones
Simular respuesta esperada de KAGRA a señales con 141.7 Hz:
```bash
python scripts/simular_respuesta_kagra_141hz.py
```

## 📚 Referencias

### Diseño de KAGRA
- KAGRA Collaboration, "KAGRA: 2.5 generation interferometric gravitational wave detector"
- Nature Astronomy 3, 35-40 (2019)

### Sensibilidad y Ruido
- KAGRA Collaboration, "Overview of KAGRA: Detector design and construction history"
- arXiv:2005.05574

### Datos Abiertos
- GWOSC: https://gwosc.org
- KAGRA Data Release: https://gwcenter.icrr.u-tokyo.ac.jp/en/

## 🔔 Notificaciones

Para recibir notificaciones cuando los datos estén disponibles:
1. Suscribirse a GWOSC announcements: https://gwosc.org/news/
2. Seguir @KAGRA_PR en Twitter/X
3. Revisar periódicamente: https://gwosc.org/eventapi/

---

**Última actualización:** 2025-11-05 23:24 UTC
**Estado:** ESPERANDO DATOS O4
**Importancia:** CRÍTICA para validación independiente
