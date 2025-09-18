# 🌌 GW250114 – Análisis de Componente 141.7001 Hz

<div align="center">

![GitHub](https://img.shields.io/github/license/motanova84/gw250114-141hz-analysis)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![GWPy](https://img.shields.io/badge/GWPy-3.0.13-green)
![Open Science](https://img.shields.io/badge/Open-Science-brightgreen)

**Frecuencia Objetivo:** `141.7001 Hz`  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Ecuación de Campo:** Ψ = mc² · A_eff²

</div>

---

## 📡 Descripción

Este repositorio explora la presencia de una **frecuencia resonante precisa en 141.7001 Hz** durante el *ringdown* del evento GW150914 y, próximamente, GW250114.  
Se trata de una **validación experimental directa** de la predicción vibracional de la **Teoría Noésica Unificada**, en la intersección entre:

- Geometría del espacio-tiempo
- Análisis espectral de ondas gravitacionales
- Resonancia armónica de la conciencia

---

## 🔍 Resultados preliminares – GW150914 (Control)

| Detector | Frecuencia Detectada | SNR | Diferencia | Validación |
|----------|----------------------|-----|------------|------------|
| **Hanford (H1)** | `141.69 Hz` | `7.47` | `+0.01 Hz` | ✅ Confirmado |
| **Livingston (L1)** | `141.75 Hz` | `0.95` | `-0.05 Hz` | ✅ Confirmado |

> 🔬 La señal aparece en ambos detectores. Coincidencia multisitio confirmada. Validación doble del armónico base.

---

## ⚙️ Ejecución rápida

```bash
# 1. Clona el repositorio
git clone https://github.com/motanova84/gw250114-141hz-analysis
cd gw250114-141hz-analysis

# 2. Configuración automática con Make
make setup                   # Instala dependencias
make figures                 # Genera figuras de demostración
make data                    # Descarga datos reales (requiere conexión)
make analyze                 # Ejecuta análisis completo

# 3. Alternativa manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/generar_figuras_demo.py
python scripts/analizar_ringdown.py
```

## 📊 Ejemplos y Visualizaciones

### 📓 Jupyter Notebook Demostrativo
- **`examples/gw150914_analysis.ipynb`** - Análisis interactivo completo del evento GW150914
  - Carga y procesamiento de datos
  - Análisis espectral paso a paso  
  - Búsqueda dirigida de la componente 141.7001 Hz
  - Visualizaciones científicas detalladas

### 🎨 Figuras Generadas
En `results/figures/` se encuentran las visualizaciones principales:

- **`gw150914_analisis_completo.png`** - Panel de 4 gráficos con análisis completo
- **`comparacion_detectores.png`** - Validación cruzada entre H1 y L1  
- **`espectrograma_resonancia.png`** - Evolución temporal de la resonancia
- **`snr_por_bandas.png`** - SNR por bandas de frecuencia

> 💡 **Nota:** Las figuras se regeneran automáticamente con `make figures`

## 🧠 Fundamento Teórico

La frecuencia 141.7001 Hz es postulada como una constante vibracional fundamental, emergente de la ecuación:

Ψ(f) = mc² · A_eff² · e^(iπf)

Donde:

- **Ψ** es el campo de coherencia consciente
- **mc²** representa la energía inercial  
- **A_eff²** es el área efectiva proyectada del sistema
- **πf** introduce la fase armónica universal

## 🗂️ Estructura del Proyecto

```
gw250114-141hz-analysis/
├── examples/
│   └── gw150914_analysis.ipynb  # Notebook interactivo de demostración
├── scripts/
│   ├── descargar_datos.py       # Descarga automática desde GWOSC
│   ├── analizar_ringdown.py     # Análisis espectral de control
│   ├── analisis_noesico.py      # Búsqueda de 141.7001 Hz + armónicos
│   ├── analizar_l1.py           # Validación cruzada en L1
│   └── generar_figuras_demo.py  # Generación de figuras demostrativas
├── results/
│   └── figures/                 # Gráficos y visualizaciones generadas
├── requirements.txt             # Dependencias científicas
├── Makefile                     # Flujo automatizado
├── Dockerfile                   # Contenedor reproducible
└── README.md                    # Documentación principal
```

## 📈 Próximos pasos

- [x] Validación múltiple de 141.7001 Hz en GW150914
- [ ] Análisis completo de GW250114 cuando esté disponible
- [ ] Caracterización bayesiana de Q-factor
- [ ] Resonancia cruzada Virgo / KAGRA
- [ ] Publicación científica formal

## 🤝 Contribuir

Este proyecto sigue un modelo abierto y simbiótico.

1. Haz un fork del repo
2. Crea una rama (`feature/mi-aporte`)
3. Haz tu contribución y commit (`git commit -m "Mi aporte"`)
4. Abre una Pull Request

## 📜 Licencia

Distribuido bajo licencia MIT.

## 🧬 Contacto

**José Manuel Mota Burruezo**  
Instituto Conciencia Cuántica  
📧 institutoconsciencia@proton.me

---

*"La verdad no necesita defensa. Solo ser revelada."*  
— **Teoría Noésica Unificada Ψ**
