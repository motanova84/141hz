# VerificadorGW250114 - Documentación

## 📋 Descripción

La clase `VerificadorGW250114` implementa un sistema proactivo de verificación de disponibilidad del evento GW250114 en el catálogo GWOSC (Gravitational Wave Open Science Center), así como la búsqueda de eventos similares disponibles para análisis.

## 🚀 Uso Básico

### Ejemplo Simple

```python
from datetime import datetime
from scripts.analizar_gw250114 import VerificadorGW250114

# Crear verificador
verificador = VerificadorGW250114()

# Verificar disponibilidad del evento GW250114
estado_actual = verificador.verificar_disponibilidad_evento()

print(f"\n📅 FECHA ACTUAL: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🎯 ESTADO GW250114: {verificador.estado_actual}")

if verificador.estado_actual == "NO_DISPONIBLE":
    print("\n🔍 BUSCANDO EVENTOS SIMILARES DISPONIBLES...")
    verificador.verificar_eventos_similares()
```

### Ejecutar Demostración

```bash
# Usando Python directamente
python3 demo_verificador.py

# O usando el script de prueba
python3 scripts/test_verificador_gw250114.py
```

## 🔧 API de la Clase

### Constructor

```python
VerificadorGW250114()
```

Inicializa el verificador con un catálogo de eventos conocidos de GWOSC.

**Atributos:**
- `estado_actual`: Estado actual de la verificación (`None`, `"NO_DISPONIBLE"`, `"ERROR_CONEXION"`)
- `eventos_conocidos`: Diccionario de eventos conocidos con sus parámetros
- `eventos_similares`: Lista de eventos similares encontrados

### Métodos

#### verificar_disponibilidad_evento()

```python
def verificar_disponibilidad_evento(offline_mode=False)
```

Verifica si GW250114 está disponible en GWOSC.

**Parámetros:**
- `offline_mode` (bool): Si es True, asume modo offline y no intenta conectarse

**Retorna:**
- `bool`: True si está disponible, False en caso contrario

**Efectos secundarios:**
- Actualiza `self.estado_actual` con el estado de la verificación

#### verificar_eventos_similares()

```python
def verificar_eventos_similares(offline_mode=False)
```

Busca eventos similares disponibles en GWOSC que puedan servir para validar la metodología.

**Parámetros:**
- `offline_mode` (bool): Si es True, simula búsqueda sin conectarse a GWOSC

**Retorna:**
- `list`: Lista de diccionarios con información de eventos similares

**Formato de retorno:**
```python
[
    {
        'nombre': 'GW150914',
        'gps': 1126259462.423,
        'tipo': 'BBH',
        'masa_total': 65,
        'disponible': True
    },
    ...
]
```

## 📊 Eventos Conocidos

El verificador incluye los siguientes eventos del catálogo GWTC:

| Evento | Tipo | GPS Time | Masa Total (M☉) |
|--------|------|----------|-----------------|
| GW150914 | BBH | 1126259462.423 | 65 |
| GW151226 | BBH | 1135136350.6 | 22 |
| GW170104 | BBH | 1167559936.6 | 50 |
| GW170814 | BBH | 1186741861.5 | 56 |
| GW170823 | BBH | 1187008882.4 | 40 |
| GW170817 | BNS | 1187008882.4 | 2.8 |

**Tipos:**
- BBH: Binary Black Hole (Agujero Negro Binario)
- BNS: Binary Neutron Star (Estrella de Neutrones Binaria)

## 💡 Modo Offline

El verificador soporta un modo offline para demostraciones y pruebas sin conectividad a GWOSC:

```python
verificador = VerificadorGW250114()

# Verificación offline
verificador.verificar_disponibilidad_evento(offline_mode=True)
eventos = verificador.verificar_eventos_similares(offline_mode=True)

print(f"Eventos disponibles: {len([e for e in eventos if e['disponible']])}")
```

## 🎯 Casos de Uso

### 1. Monitoreo Automático

```python
import time
from scripts.analizar_gw250114 import VerificadorGW250114

def monitorear_gw250114(intervalo_horas=24):
    """Monitorear periódicamente la disponibilidad de GW250114"""
    while True:
        verificador = VerificadorGW250114()
        disponible = verificador.verificar_disponibilidad_evento()
        
        if disponible:
            print("¡GW250114 DISPONIBLE! Iniciando análisis...")
            # Iniciar análisis automático
            break
        
        print(f"Esperando {intervalo_horas}h para próxima verificación...")
        time.sleep(intervalo_horas * 3600)
```

### 2. Análisis de Eventos Alternativos

```python
verificador = VerificadorGW250114()
verificador.verificar_disponibilidad_evento()

if verificador.estado_actual == "NO_DISPONIBLE":
    eventos = verificador.verificar_eventos_similares()
    eventos_bbh = [e for e in eventos if e['disponible'] and e['tipo'] == 'BBH']
    
    print(f"\n✅ Eventos BBH disponibles para análisis: {len(eventos_bbh)}")
    for evento in eventos_bbh:
        print(f"   - {evento['nombre']}: {evento['masa_total']} M☉")
```

## 🔍 Troubleshooting

### Error de Conexión

Si obtiene errores de conexión:

```
❌ Error accediendo catálogo: HTTPSConnectionPool...
```

**Soluciones:**
1. Verificar conectividad a internet
2. Comprobar que gwosc.org está accesible
3. Usar modo offline para pruebas: `offline_mode=True`

### Eventos No Disponibles

Si no se encuentran eventos disponibles:

```
⚠️ No se encontraron eventos disponibles en este momento
```

**Posibles causas:**
1. Problema temporal de GWOSC
2. Sin conectividad a internet
3. Eventos no liberados públicamente aún

**Solución:**
- Intentar más tarde
- Verificar estado de GWOSC en https://gwosc.org/
- Usar modo offline para demostraciones

## 📚 Referencias

- [GWOSC - Gravitational Wave Open Science Center](https://gwosc.org/)
- [GWPy Documentation](https://gwpy.github.io/)
- [GWTC-1 Catalog](https://gwosc.org/eventapi/html/GWTC-1/)

## 🤝 Contribuir

Para reportar problemas o sugerir mejoras, por favor abrir un issue en el repositorio.
