# 📡 Sistema de Alertas Automáticas GW250114

## Descripción General

El Sistema de Alertas Automáticas es un componente esencial del framework de análisis GW250114 que envía notificaciones automáticas cuando:
1. El evento GW250114 está disponible en GWOSC
2. El análisis de datos se completa

## 🎯 Características

### 1. Alertas de Disponibilidad
- Notifica cuando GW250114 está disponible en GWOSC
- Incluye información del evento y hora de detección
- Indica que el análisis automático ha iniciado

### 2. Alertas de Análisis Completado
- Envía resumen de resultados por detector
- Incluye frecuencias detectadas, SNR y diferencias
- Interpreta significancia estadística

### 3. Canales de Notificación
- **Email**: Soporte para ProtonMail (SMTP)
- **Webhook**: Integración con Slack/Discord
- **Consola**: Logs en tiempo real

## 📋 Configuración

### Configuración por Defecto

```python
{
    'email_destino': 'institutoconsciencia@proton.me',
    'webhook_url': None,  # Configurar si se usa Slack/Discord
    'intervalo_verificacion': 1800  # 30 minutos
}
```

### Configurar Email

Para habilitar el envío de emails, descomentar y configurar en `sistema_alertas_gw250114.py`:

```python
def enviar_email(self, asunto, mensaje):
    # Configuración para ProtonMail
    server = smtplib.SMTP('smtp.protonmail.com', 587)
    server.starttls()
    server.login('tu_email@proton.me', 'tu_password')
    server.send_message(msg)
    server.quit()
```

**Nota**: Por seguridad, no incluir credenciales directamente en el código. Usar variables de entorno:

```python
import os
email = os.getenv('ALERT_EMAIL')
password = os.getenv('ALERT_PASSWORD')
```

### Configurar Webhook (Slack/Discord)

```python
sistema = SistemaAlertasGW250114()
sistema.config['webhook_url'] = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
```

## 🚀 Uso

### Uso Directo

```python
from sistema_alertas_gw250114 import SistemaAlertasGW250114

# Inicializar sistema
sistema = SistemaAlertasGW250114()

# Enviar alerta de disponibilidad
sistema.enviar_alerta_disponible("GW250114")

# Enviar alerta de análisis
resultados = {
    'resumen': {
        'total_detectores': 2,
        'exitosos': 2,
        'tasa_exito': 1.0
    },
    'resultados': {
        'H1': {
            'frecuencia_detectada': 141.7050,
            'snr': 8.5,
            'diferencia': 0.0049,
            'significativo': True
        }
    }
}
sistema.enviar_alerta_analisis("GW250114", resultados)
```

### Integración Automática

El sistema de alertas está integrado automáticamente en:

1. **`scripts/analizar_gw250114.py`**: Envía alertas cuando GW250114 está disponible y cuando el análisis se completa
2. **`scripts/busqueda_sistematica_gwtc1.py`**: Envía alertas al completar la búsqueda sistemática

## 🧪 Testing

### Ejecutar Tests

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar tests
python scripts/test_sistema_alertas.py
```

### Tests Incluidos

1. **test_inicializacion**: Verifica configuración inicial
2. **test_alerta_disponibilidad**: Prueba alertas de disponibilidad
3. **test_alerta_analisis**: Prueba alertas de análisis
4. **test_alerta_sin_resultados**: Manejo de resultados vacíos
5. **test_configuracion_webhook**: Configuración de webhooks

### Ejecución de Prueba

```bash
python scripts/sistema_alertas_gw250114.py
```

Esto ejecuta una demostración completa del sistema.

## 📊 Formato de Alertas

### Alerta de Disponibilidad

```
🌌 ALERTA: EVENTO DE ONDAS GRAVITACIONALES DISPONIBLE

¡GW250114 está ahora disponible en GWOSC!

INFORMACIÓN:
• Evento: GW250114
• Hora de detección: 2025-10-15 11:30:00
• Estado: Datos públicos accesibles

ACCIÓN REQUERIDA:
El sistema automático ha iniciado la descarga y análisis.
Verifique los resultados en: resultados/analisis_GW250114.json

¡La validación experimental de la teoría Ψ está en marcha!
```

### Alerta de Análisis Completado

```
📈 RESULTADOS DEL ANÁLISIS NOÉSICO

Evento: GW250114
Fecha: 2025-10-15 12:00:00

RESULTADOS:
• Detectores analizados: 2
• Detectores significativos: 2
• Tasa de éxito: 100.0%

DETALLES POR DETECTOR:
H1:
  • Frecuencia: 141.7050 Hz
  • SNR: 8.50
  • Diferencia: 0.0049 Hz
  • Significativo: True

L1:
  • Frecuencia: 141.6980 Hz
  • SNR: 7.20
  • Diferencia: 0.0021 Hz
  • Significativo: True

INTERPRETACIÓN:
La teoría Ψ predice modulación en 141.7001 Hz.
Coincidencia dentro de ±0.1 Hz con SNR > 5 se considera validación.
```

## 🔧 Personalización

### Cambiar Intervalo de Verificación

```python
sistema = SistemaAlertasGW250114()
sistema.config['intervalo_verificacion'] = 3600  # 1 hora
```

### Agregar Múltiples Destinatarios

Modificar `enviar_email()` para soportar lista de destinatarios:

```python
def enviar_email(self, asunto, mensaje):
    destinatarios = ['email1@proton.me', 'email2@proton.me']
    msg['To'] = ', '.join(destinatarios)
    # ... resto del código
```

### Filtrar Alertas por SNR

```python
def enviar_alerta_analisis(self, evento, resultados):
    # Solo enviar si hay detecciones significativas
    detecciones_sig = [r for r in resultados['resultados'].values() 
                       if r.get('snr', 0) > 5]
    if not detecciones_sig:
        return  # No enviar alerta
    # ... resto del código
```

## 📝 Notas de Seguridad

1. **Credenciales**: Nunca incluir credenciales en el código fuente
2. **Variables de Entorno**: Usar `.env` para configuración sensible
3. **Webhooks**: Mantener URLs de webhook en secreto
4. **Rate Limiting**: Implementar límites de envío para evitar spam

## 🔗 Integración con Pipeline

El sistema de alertas se integra automáticamente con:

- ✅ Framework de análisis GW250114
- ✅ Búsqueda sistemática GWTC-1
- ✅ Pipeline de validación científica
- ✅ Sistema de monitoreo continuo

## 🎯 Criterios de Alerta

Las alertas se envían cuando:

1. **Disponibilidad**: GW250114 detectado en GWOSC
2. **Análisis Completado**: Todos los detectores procesados
3. **Significancia**: SNR > 5 y diferencia < 0.1 Hz
4. **Errores Críticos**: Fallos en descarga o procesamiento

## 📈 Métricas

El sistema registra:
- Tiempo de respuesta a nueva disponibilidad
- Tasa de éxito en envío de alertas
- Número de detecciones significativas
- Errores y reintentos

## 🤝 Contribuciones

Para mejorar el sistema de alertas:

1. Fork el repositorio
2. Crear branch de feature
3. Agregar tests para nuevas funcionalidades
4. Enviar pull request

## 📄 Licencia

Parte del proyecto GW250114 - 141.7001 Hz Analysis
Licencia MIT
