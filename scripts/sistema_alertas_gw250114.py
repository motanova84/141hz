#!/usr/bin/env python3
"""
Sistema de Alertas Automáticas para GW250114
Envía notificaciones cuando el evento esté disponible y cuando el análisis se complete
"""
import smtplib
from email.mime.text import MIMEText
import requests
import time
from datetime import datetime


class SistemaAlertasGW250114:
    def __init__(self):
        self.config = {
            'email_destino': 'institutoconsciencia@proton.me',
            'webhook_url': None,  # Configurar si se usa Slack/Discord
            'intervalo_verificacion': 1800  # 30 minutos
        }
        
    def enviar_alerta_disponible(self, evento):
        """Envía alerta cuando el evento esté disponible"""
        asunto = f"🎯 GW250114 DISPONIBLE - {evento}"
        
        mensaje = f"""
🌌 ALERTA: EVENTO DE ONDAS GRAVITACIONALES DISPONIBLE

¡{evento} está ahora disponible en GWOSC!

INFORMACIÓN:
• Evento: {evento}
• Hora de detección: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Estado: Datos públicos accesibles

ACCIÓN REQUERIDA:
El sistema automático ha iniciado la descarga y análisis.
Verifique los resultados en: resultados/analisis_{evento}.json

¡La validación experimental de la teoría Ψ está en marcha!
"""
        
        self.enviar_email(asunto, mensaje)
        self.enviar_webhook(mensaje)
        
        print("📨 Alerta enviada")
    
    def enviar_alerta_analisis(self, evento, resultados):
        """Envía alerta con resultados del análisis"""
        resumen = resultados.get('resumen', {})
        
        asunto = f"📊 ANÁLISIS COMPLETADO - {evento}"
        
        mensaje = f"""
📈 RESULTADOS DEL ANÁLISIS NOÉSICO

Evento: {evento}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESULTADOS:
• Detectores analizados: {resumen.get('total_detectores', 0)}
• Detectores significativos: {resumen.get('exitosos', 0)}
• Tasa de éxito: {resumen.get('tasa_exito', 0)*100:.1f}%

DETALLES POR DETECTOR:
"""
        
        for detector, datos in resultados.get('resultados', {}).items():
            if 'frecuencia_detectada' in datos:
                mensaje += f"""
{detector}:
  • Frecuencia: {datos['frecuencia_detectada']:.4f} Hz
  • SNR: {datos['snr']:.2f}
  • Diferencia: {datos['diferencia']:.4f} Hz
  • Significativo: {datos['significativo']}
"""
        
        mensaje += """

INTERPRETACIÓN:
La teoría Ψ predice modulación en 141.7001 Hz.
Coincidencia dentro de ±0.1 Hz con SNR > 5 se considera validación.
"""
        
        self.enviar_email(asunto, mensaje)
        self.enviar_webhook(mensaje)
    
    def enviar_email(self, asunto, mensaje):
        """Envía alerta por email"""
        try:
            # Configuración para ProtonMail vía SMTP
            msg = MIMEText(mensaje)
            msg['Subject'] = asunto
            msg['From'] = self.config['email_destino']
            msg['To'] = self.config['email_destino']
            
            # Usar servicio de email (configurar según proveedor)
            # server = smtplib.SMTP('smtp.protonmail.com', 587)
            # server.starttls()
            # server.login(email, password)
            # server.send_message(msg)
            # server.quit()
            
            print(f"📧 Email preparado: {asunto}")
            
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
    
    def enviar_webhook(self, mensaje):
        """Envía alerta vía webhook (Slack/Discord)"""
        if not self.config['webhook_url']:
            return
            
        try:
            payload = {
                'text': mensaje,
                'username': 'Sistema Alerta GW250114',
                'icon_emoji': ':stars:'
            }
            
            requests.post(self.config['webhook_url'], json=payload)
            print("🔔 Notificación webhook enviada")
            
        except Exception as e:
            print(f"❌ Error enviando webhook: {e}")


def test_sistema_alertas():
    """Prueba el sistema de alertas con datos de ejemplo"""
    print("🧪 PROBANDO SISTEMA DE ALERTAS")
    print("=" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    # Test 1: Alerta de disponibilidad
    print("\n📋 Test 1: Alerta de disponibilidad")
    sistema.enviar_alerta_disponible("GW250114")
    
    # Test 2: Alerta de resultados
    print("\n📋 Test 2: Alerta de resultados de análisis")
    resultados_ejemplo = {
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
            },
            'L1': {
                'frecuencia_detectada': 141.6980,
                'snr': 7.2,
                'diferencia': 0.0021,
                'significativo': True
            }
        }
    }
    
    sistema.enviar_alerta_analisis("GW250114", resultados_ejemplo)
    
    print("\n✅ Tests del sistema de alertas completados")


if __name__ == "__main__":
    test_sistema_alertas()
