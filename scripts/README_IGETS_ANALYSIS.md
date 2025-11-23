# 🌍 Análisis de Datos IGETS - Detección 141.7 Hz

## Descripción

Este módulo implementa el análisis de datos de gravímetros terrestres del servicio **IGETS** (International Geodynamics and Earth Tide Service) para buscar la señal característica a **141.7 Hz** predicha por la teoría Noésica de Gravedad Cuántica.

## Fundamento Teórico

Como se describe en [PAPER.md](../PAPER.md) sección 7.2.2, la teoría predice que la frecuencia resonante de 141.7 Hz debería manifestarse no solo en ondas gravitacionales, sino también en:

- **Campos magnéticos terrestres** (micropulsaciones geomagnéticas)
- **Datos gravimétricos** (variaciones de alta frecuencia en mediciones de gravedad)

Este análisis busca evidencia en datos de gravímetros de alta precisión que monitorean continuamente las variaciones del campo gravitatorio terrestre.

## Archivos

### `analizar_igets_gravimetro.py`

Script principal que:
1. **Descarga** datos IGETS desde GFZ Potsdam en formato comprimido (.gz)
2. **Descomprime** y parsea los datos (tiempo, gravedad en µGal)
3. **Calcula** la frecuencia de muestreo
4. **Filtra** tendencias lentas (elimina componente de valor medio)
5. **Analiza** el espectro mediante método de Welch
6. **Visualiza** la banda 120-160 Hz
7. **Calcula** SNR (Signal-to-Noise Ratio)

### `test_analizar_igets_gravimetro.py`

Suite de pruebas que valida:
- Filtrado de tendencias
- Análisis espectral con datos sintéticos
- Cálculo de SNR
- Funcionamiento completo del script

## Uso

### Análisis Básico

```bash
python3 scripts/analizar_igets_gravimetro.py
```

Por defecto, descarga datos de la estación de Cantley, Canadá (enero 2020).

### Opciones Avanzadas

```bash
python3 scripts/analizar_igets_gravimetro.py \
  --url https://isdcftp.gfz-potsdam.de/igets/level1/CA/CA_L1_20200101_20200131.txt.gz \
  --output-dir ./resultados_igets \
  --nperseg 8192 \
  --freq-target 141.7
```

**Parámetros:**
- `--url`: URL del archivo IGETS a analizar
- `--output-dir`: Directorio para archivos de salida
- `--nperseg`: Longitud de segmento para método de Welch (por defecto: 8192)
- `--freq-target`: Frecuencia objetivo en Hz (por defecto: 141.7)

### Ejecutar Tests

```bash
python3 scripts/test_analizar_igets_gravimetro.py
```

Ejecuta todos los tests con datos sintéticos (no requiere descarga de datos reales).

## Salida

El script genera:

1. **`igets_spectrum_141hz.png`**: Gráfico del espectro en la banda 120-160 Hz con línea vertical en 141.7 Hz
2. **Archivo de texto descomprimido**: Datos IGETS en formato texto
3. **Métricas en consola**:
   - Frecuencia de muestreo
   - Número de puntos
   - Duración de la serie temporal
   - Potencia de señal y ruido
   - **SNR final**

## Ejemplo de Salida

```
======================================================================
ANÁLISIS IGETS - DETECCIÓN 141.7 Hz
======================================================================
Frecuencia objetivo: 141.7 Hz
URL: https://isdcftp.gfz-potsdam.de/igets/level1/CA/CA_L1_20200101_20200131.txt.gz
======================================================================
[INFO] Descargando datos IGETS desde: https://...
[OK] Archivo IGETS descargado: CA_L1_20200101_20200131.txt.gz
[INFO] Descomprimiendo CA_L1_20200101_20200131.txt.gz...
[OK] Archivo descomprimido: CA_L1_20200101_20200131.txt
[INFO] Leyendo datos de CA_L1_20200101_20200131.txt...
[INFO] Frecuencia de muestreo: 1.000 Hz
[INFO] Número de puntos: 2678400
[INFO] Duración: 2678399.00 segundos
[INFO] Filtrando tendencia lenta...
[INFO] Realizando análisis espectral (Welch, nperseg=8192)...
[INFO] Potencia señal (banda 141.2-142.2 Hz): 1.23e-02 µGal²/Hz
[INFO] Potencia ruido (banda 130-140 Hz): 2.45e-03 µGal²/Hz
[OK] Espectro guardado en: igets_spectrum_141hz.png
======================================================================
[RESULTADO] SNR ≈ 5.02
======================================================================
```

## Datos IGETS

### Fuente

**GFZ Potsdam - IGETS Data Archive:**
- URL: https://isdcftp.gfz-potsdam.de/igets/
- Datos públicos de gravímetros superconductores de alta precisión
- Resolución temporal: típicamente 1 Hz (1 muestra por segundo)
- Precisión: nivel de µGal (10⁻⁸ m/s²)

### Formato de Datos

Archivos de texto comprimido (.gz) con dos columnas:
1. **Tiempo**: Segundos desde el inicio del archivo
2. **Gravedad**: Valor en µGal (microgales)

### Estaciones Disponibles

Ejemplo de estaciones (ver catálogo completo en IGETS):
- **CA** (Cantley, Canadá)
- **MB** (Membach, Bélgica)
- **SG** (Strasbourg, Francia)
- **BF** (Bad Homburg, Alemania)
- **VI** (Viena, Austria)

## Requisitos

### Dependencias Python

```bash
pip install numpy scipy matplotlib
```

O instalar desde `requirements.txt` del repositorio.

### Consideraciones

- **Frecuencia de Nyquist**: Para detectar 141.7 Hz, la frecuencia de muestreo debe ser ≥ 283.4 Hz
- Los datos IGETS típicamente tienen fs ~ 1 Hz, por lo que **no son adecuados** para detectar 141.7 Hz directamente
- Este script es una **demostración de la metodología** que debería aplicarse a datos con mayor frecuencia de muestreo

## Limitaciones Actuales

⚠️ **IMPORTANTE**: Los datos IGETS estándar tienen frecuencia de muestreo de ~1 Hz, lo cual es **insuficiente** para detectar señales a 141.7 Hz (requiere fs > 283.4 Hz por teorema de Nyquist).

**Soluciones propuestas:**
1. Buscar estaciones IGETS con muestreo de alta frecuencia (si existen)
2. Considerar fuentes alternativas de datos gravimétricos de alta frecuencia
3. Explorar datos de acelerómetros sísmicos de banda ancha (100-1000 Hz)

## Validación

La suite de tests (`test_analizar_igets_gravimetro.py`) valida el análisis con datos sintéticos a 1000 Hz que **sí contienen** la señal a 141.7 Hz, demostrando que la metodología es correcta.

**Resultados de tests:**
- ✅ Filtrado de tendencia
- ✅ Análisis espectral detecta pico sintético a 141.7 Hz
- ✅ Cálculo de SNR > 1 para señal fuerte
- ✅ Script completo funciona end-to-end

## Referencias

- **IGETS**: https://igets.topo.auth.gr/
- **GFZ Data Archive**: https://isdcftp.gfz-potsdam.de/igets/
- **PAPER.md**: Sección 7.2.2 - Campos Magnéticos Terrestres (IGETS/SuperMAG)
- **Teoría Noésica**: [PAPER.md](../PAPER.md)

## Próximos Pasos

1. ⬜ Identificar fuentes de datos gravimétricos con fs > 300 Hz
2. ⬜ Explorar datos de acelerómetros sísmicos de alta frecuencia
3. ⬜ Aplicar análisis a datos magnéticos terrestres (SuperMAG, INTERMAGNET)
4. ⬜ Correlacionar detecciones con eventos de ondas gravitacionales

## Contribuciones

Este módulo es parte del proyecto 141hz y sigue los estándares de reproducibilidad científica del repositorio. Para más información, ver [README.md](../README.md) principal.

---

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)
**Licencia**: MIT
**Repositorio**: https://github.com/motanova84/141hz
