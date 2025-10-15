# 🏗️ Arquitectura del Dashboard GW250114

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USUARIO / CLIENTE                            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴──────────┐
                    │                      │
            ┌───────▼────────┐    ┌───────▼────────┐
            │   Web Browser  │    │  API Client    │
            │                │    │  (curl, etc)   │
            └───────┬────────┘    └───────┬────────┘
                    │                      │
                    │  HTTP GET            │  HTTP GET
                    │  /monitor-gw         │  /estado-gw250114
                    │                      │
                    └──────────┬───────────┘
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│                     FLASK APPLICATION                              │
│                  (dashboard/estado_gw250114.py)                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Route: /estado-gw250114                                 │    │
│  │  Method: GET                                             │    │
│  │  Returns: JSON                                           │    │
│  │  ┌────────────────────────────────────────────────────┐ │    │
│  │  │ {                                                  │ │    │
│  │  │   "evento": "GW250114",                            │ │    │
│  │  │   "disponible": true/false,                        │ │    │
│  │  │   "estado": "ANALIZADO" | "NO_DISPONIBLE",         │ │    │
│  │  │   "resultados": {...}                              │ │    │
│  │  │ }                                                  │ │    │
│  │  └────────────────────────────────────────────────────┘ │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Route: /monitor-gw                                      │    │
│  │  Method: GET                                             │    │
│  │  Returns: HTML                                           │    │
│  │  ┌────────────────────────────────────────────────────┐ │    │
│  │  │ • Auto-refresh cada 30 segundos                    │ │    │
│  │  │ • JavaScript fetch() a /estado-gw250114            │ │    │
│  │  │ • Diseño responsive                                │ │    │
│  │  │ • Indicadores visuales (verde/rojo)                │ │    │
│  │  └────────────────────────────────────────────────────┘ │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                    │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                 ┌───────────┴──────────┐
                 │  File System Check   │
                 └───────────┬──────────┘
                             │
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   SISTEMA DE ARCHIVOS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📁 resultados/                                                 │
│     └── analisis_GW250114.json  ◄── Generado por scripts       │
│                                     de análisis                 │
│                                                                 │
│  Estructura del JSON:                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ {                                                         │ │
│  │   "evento": "GW250114",                                   │ │
│  │   "detectores": {                                         │ │
│  │     "H1": {                                               │ │
│  │       "bayes_factor": 15.3,                               │ │
│  │       "p_value": 0.0075,                                  │ │
│  │       "snr": 12.4                                         │ │
│  │     },                                                    │ │
│  │     "L1": {...}                                           │ │
│  │   }                                                       │ │
│  │ }                                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### Escenario 1: Sin Resultados Disponibles

```
Usuario → Browser → GET /monitor-gw
                    ↓
                Flask app carga HTML
                    ↓
                Browser ejecuta JavaScript
                    ↓
                fetch('/estado-gw250114')
                    ↓
                Flask verifica archivo
                    ↓ (no existe)
                Retorna JSON: disponible=false
                    ↓
                JavaScript actualiza HTML
                    ↓
                Muestra: "⏳ GW250114 NO DISPONIBLE"
```

### Escenario 2: Con Resultados Disponibles

```
Usuario → Browser → GET /monitor-gw
                    ↓
                Flask app carga HTML
                    ↓
                Browser ejecuta JavaScript
                    ↓
                fetch('/estado-gw250114')
                    ↓
                Flask verifica archivo
                    ↓ (existe)
                Lee analisis_GW250114.json
                    ↓
                Retorna JSON: disponible=true + resultados
                    ↓
                JavaScript actualiza HTML
                    ↓
                Muestra: "🎯 GW250114 DISPONIBLE"
```

## Integración con Scripts de Análisis

```
┌──────────────────────────────────────────────────────────────┐
│  scripts/analizar_gw250114.py                                │
│                                                              │
│  1. Detecta disponibilidad de GW250114                       │
│  2. Ejecuta análisis (Bayes Factor, p-value, SNR)           │
│  3. Genera resultados/analisis_GW250114.json ◄─────────┐    │
│                                                         │    │
└─────────────────────────────────────────────────────────┼────┘
                                                          │
                                                          │
┌─────────────────────────────────────────────────────────┼────┐
│  dashboard/estado_gw250114.py                           │    │
│                                                         │    │
│  1. Escucha en puerto 5000                              │    │
│  2. Verifica existencia del archivo ────────────────────┘    │
│  3. Lee y muestra resultados                                 │
│  4. Auto-actualiza cada 30 segundos                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Tecnologías Utilizadas

- **Backend**: Flask 2.0+
- **Frontend**: HTML5 + JavaScript (Vanilla JS)
- **Styling**: CSS3 (embedded)
- **Data Format**: JSON
- **Communication**: REST API + AJAX (fetch)

## Características de Diseño

### Modular
- Flask app separada del resto del código
- Sin dependencias de templates externos
- Fácil de desplegar independientemente

### Resiliente
- Funciona sin resultados (modo "esperando")
- Búsqueda flexible de archivos
- Manejo de errores graceful

### Performante
- Lightweight (sin dependencias pesadas)
- Caché en frontend vía JavaScript
- Actualización incremental

### Extensible
- API REST para integración
- Formato JSON estándar
- Fácil de conectar con otros sistemas
