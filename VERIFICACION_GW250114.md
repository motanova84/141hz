# Sistema de Verificación Inmediata GW250114

Este directorio contiene el sistema de verificación y monitoreo automático para el evento GW250114.

## Archivos

### `lanzar_verificacion_gw250114.sh`
Script principal de lanzamiento que:
- Crea directorios necesarios (data/raw, resultados, scripts, dashboard)
- Ejecuta verificación inmediata de disponibilidad de GW250114
- Opcionalmente inicia monitoreo continuo en segundo plano
- Proporciona instrucciones de control y estado

### `scripts/verificador_gw250114.py`
Script Python que verifica la disponibilidad de GW250114 en GWOSC:
- Verifica conectividad con catálogo GWOSC
- Busca el evento GW250114 en el catálogo público
- Retorna exit code 0 si está disponible, 1 si no
- Soporta modo de monitoreo continuo (--continuo)

## Uso

### Verificación Inmediata

```bash
./lanzar_verificacion_gw250114.sh
```

Este comando:
1. Crea la estructura de directorios necesaria
2. Verifica si GW250114 está disponible
3. Si no está disponible, pregunta si desea iniciar monitoreo continuo

### Verificación Automática (sin prompt)

```bash
./lanzar_verificacion_gw250114.sh --auto
```

Inicia automáticamente el monitoreo continuo sin preguntar.

### Monitoreo Continuo Manual

```bash
# Iniciar en segundo plano
nohup python scripts/verificador_gw250114.py --continuo > monitoreo_gw250114.log 2>&1 &

# Ver logs en tiempo real
tail -f monitoreo_gw250114.log

# Detener monitoreo
pkill -f verificador_gw250114.py
```

## Comportamiento

### Cuando GW250114 NO está disponible:
- Exit code: 1
- Mensaje: "❌ GW250114 NO DISPONIBLE AÚN"
- En modo continuo: verifica cada hora

### Cuando GW250114 está disponible:
- Exit code: 0
- Mensaje: "✅ GW250114 DISPONIBLE - Listo para análisis"
- Crea archivo: `GW250114_DISPONIBLE.txt`
- Indica comando para ejecutar análisis: `python scripts/analizar_gw250114.py`

## Directorios Creados

```
gw250114-141hz-analysis/
├── data/
│   └── raw/          # Datos crudos descargados
├── resultados/       # Resultados de análisis
├── dashboard/        # Visualizaciones y reportes
└── scripts/          # Scripts de análisis (ya existe)
```

## Archivos de Monitoreo

- `monitoreo_gw250114.log` - Logs del monitoreo continuo
- `monitoreo_gw250114.pid` - PID del proceso de monitoreo
- `GW250114_DISPONIBLE.txt` - Archivo de alerta cuando está disponible

## Integración

El sistema está diseñado para integrarse con:
- `scripts/analizar_gw250114.py` - Framework de análisis principal
- `scripts/validar_gw150914.py` - Metodología validada en GW150914
- Sistema de validación completo existente

## Requisitos

- Python 3.7+
- GWPy >= 3.0.0
- Conexión a internet (para acceder a GWOSC)

## Notas

- GW250114 es un evento objetivo hipotético
- El sistema detectará automáticamente cuando esté disponible en GWOSC
- La verificación usa GW150914 como test de conectividad
- El monitoreo continuo verifica cada hora por defecto
