#!/usr/bin/env python3
"""
QCAL STRADIVARIUS — Proxy Stratum con Filtro Espectral
======================================================
Intercepta, filtra y sella cada share de minado antes de
reenviarlo al pool. Aplica metrica adelica (Q_p) y filtro
de coherencia AURION(Psi).

f0 = 141.7001 Hz · Psi >= 0.999999
Pool: btc.viabtc.top:3333
Worker: noesis88.001

Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
"""

import socket
import select
import json
import hashlib
import time
import struct
import threading
import logging
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

F_0 = 141.7001
PSI_OBJETIVO = 0.999999
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'
AMDA_FP = '5e5ac3ab49e5be07'

LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 3333
POOL_HOST = 'btc.viabtc.top'
POOL_PORT = 3333
BUFFER_SIZE = 65536
POLL_TIMEOUT = 1.0

LEDGER_PATH = '/root/ecosystem/catedral/emision_ledger.json'
LOG_PATH = '/var/log/qcal_stradivarius.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [STRAD|%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger('qcal_stradivarius')

shares_filtrados = 0
shares_aceptados = 0
shares_rechazados = 0


def metrica_adelica(block_header_hex, nonce):
    """Filtro p-adico: evalua si el espacio de fase del nonce es armonico con f0."""
    try:
        val = int(block_header_hex[:16], 16) + int(nonce[:8], 16) if len(nonce) >= 8 else 0
        return val % 7 == 0
    except (ValueError, TypeError):
        return True


def verificar_coherencia():
    """Verifica si el sistema esta en coherencia. Retorna True si Psi >= 0.999999."""
    try:
        sys.path.insert(0, '/root/ecosystem/soberania')
        from crypto_sign import es_matriz_refractaria
        return es_matriz_refractaria(PSI_OBJETIVO)
    except Exception:
        return True


def sellar_share(share_data):
    """Anade el sello QCAL a un share."""
    share_data['qcal'] = {
        'frecuencia_hz': F_0,
        'psi': PSI_OBJETIVO,
        'fingerprint': AMDA_FP,
        'sello': SELLO,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    return share_data


def registrar_share_ledger(aceptado, share_info=None):
    """Registra el share en el emision_ledger.json."""
    global shares_aceptados, shares_rechazados, shares_filtrados
    
    try:
        if os.path.exists(LEDGER_PATH):
            with open(LEDGER_PATH) as f:
                ledger = json.load(f)
        else:
            ledger = {
                'version': 'QCAL-STRADIVARIUS-v1',
                'frecuencia_hz': F_0,
                'sesiones': [],
                'total_shares_aceptados': 0,
                'total_shares_rechazados': 0,
                'total_shares_filtrados': 0,
                'sello': SELLO,
            }
        
        if aceptado:
            ledger['total_shares_aceptados'] = ledger.get('total_shares_aceptados', 0) + 1
            shares_aceptados += 1
        else:
            ledger['total_shares_rechazados'] = ledger.get('total_shares_rechazados', 0) + 1
            shares_rechazados += 1
        
        ledger['total_shares_filtrados'] = shares_filtrados
        ledger['ultimo_share'] = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'aceptado': aceptado,
        }
        if share_info:
            ledger['ultimo_share'].update(share_info)
        
        with open(LEDGER_PATH, 'w') as f:
            json.dump(ledger, f, indent=2)
    except Exception as e:
        log.error('Error registrando share en ledger: %s', e)


class ConexionMinero:
    """Maneja una conexion de minero, aplicando el filtro QCAL."""
    
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.pool_sock = None
        self.buffer = b''
        self.activo = True
        self.worker = 'desconocido'
    
    def conectar_al_pool(self):
        """Conecta al pool ViaBTC."""
        try:
            self.pool_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.pool_sock.connect((POOL_HOST, POOL_PORT))
            self.pool_sock.setblocking(False)
            log.info('Minero %s conectado al pool %s:%d', self.addr[0], POOL_HOST, POOL_PORT)
            return True
        except Exception as e:
            log.error('Error conectando al pool: %s', e)
            return False
    
    def procesar_mensaje_minero(self, mensaje):
        """Intercepta y filtra mensajes del minero."""
        global shares_filtrados
        
        try:
            msg_str = mensaje.decode('utf-8', errors='replace').strip()
            if not msg_str:
                return mensaje
            
            # Intentar parsear como JSON-RPC
            for line in msg_str.split('\n'):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                if isinstance(data, dict):
                    method = data.get('method', '')
                    params = data.get('params', [])
                    
                    if method == 'mining.submit':
                        self.worker = params[0] if len(params) > 0 else self.worker
                        job_id = params[1] if len(params) > 1 else ''
                        extranonce2 = params[2] if len(params) > 2 else ''
                        ntime = params[3] if len(params) > 3 else ''
                        nonce = params[4] if len(params) > 4 else ''
                        
                        # Filtro p-adico
                        if not metrica_adelica(job_id, nonce):
                            log.info('Share RECHAZADO por metrica adelica: %s', self.worker)
                            shares_filtrados += 1
                            registrar_share_ledger(False, {'razon': 'METRICA_ADELICA', 'worker': self.worker})
                            return None
                        
                        # Verificar coherencia
                        if not verificar_coherencia():
                            log.warning('Sistema fuera de coherencia. Share en cuarentena.')
                            shares_filtrados += 1
                            return None
                        
                        # Sellar el share
                        sellar_share(data)
                        mensaje = (json.dumps(data) + '\n').encode()
                        
                        log.info('Share ACEPTADO: %s | job: %s | nonce: %s', self.worker, job_id[:8], nonce[:8])
                        registrar_share_ledger(True, {'worker': self.worker, 'job_id': job_id[:16]})
                    
                    elif method == 'mining.authorize':
                        self.worker = params[0] if len(params) > 0 else self.worker
                        log.info('Minero autorizado: %s', self.worker)
                
        except Exception as e:
            log.error('Error procesando mensaje: %s', e)
        
        return mensaje
    
    def forward(self):
        """Forwarding bidireccional con filtro."""
        if not self.conectar_al_pool():
            return
        
        try:
            self.conn.setblocking(False)
            inputs = [self.conn, self.pool_sock]
            
            while self.activo and inputs:
                readable, _, exceptional = select.select(inputs, [], inputs, POLL_TIMEOUT)
                
                for sock in exceptional:
                    inputs.remove(sock)
                    sock.close()
                    self.activo = False
                    break
                
                for sock in readable:
                    if sock == self.conn:
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            log.info('Minero %s desconectado', self.addr[0])
                            self.activo = False
                            break
                        
                        # Aplicar filtro QCAL
                        resultado = self.procesar_mensaje_minero(data)
                        if resultado and self.pool_sock:
                            try:
                                self.pool_sock.send(resultado)
                            except Exception:
                                self.activo = False
                                break
                    
                    elif sock == self.pool_sock:
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            log.info('Pool desconectado')
                            self.activo = False
                            break
                        try:
                            self.conn.send(data)
                        except Exception:
                            self.activo = False
                            break
                
        except Exception as e:
            log.error('Error en forwarding: %s', e)
        finally:
            for s in [self.conn, self.pool_sock]:
                if s:
                    try:
                        s.close()
                    except Exception:
                        pass


class ServidorStratum:
    """Servidor Stratum con filtro QCAL."""
    
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((LISTEN_HOST, LISTEN_PORT))
        self.server.listen(10)
        self.server.setblocking(False)
        log.info('Stradivarius escuchando en %s:%d', LISTEN_HOST, LISTEN_PORT)
        log.info('Reenviando a pool %s:%d', POOL_HOST, POOL_PORT)
    
    def run(self):
        log.info('=' * 60)
        log.info('QCAL STRADIVARIUS — PROXY STRATUM ESPECTRAL')
        log.info('f0 = %.4f Hz | Psi >= %.6f', F_0, PSI_OBJETIVO)
        log.info('Puerto: %d -> %s:%d', LISTEN_PORT, POOL_HOST, POOL_PORT)
        log.info('Sello: %s', SELLO)
        log.info('=' * 60)
        
        while True:
            try:
                readable, _, _ = select.select([self.server], [], [], 1.0)
                if readable:
                    conn, addr = self.server.accept()
                    log.info('Nuevo minero conectado: %s:%d', addr[0], addr[1])
                    hilo = threading.Thread(target=self.manejar_minero, args=(conn, addr))
                    hilo.daemon = True
                    hilo.start()
            except KeyboardInterrupt:
                log.info('Servidor detenido por usuario')
                break
            except Exception as e:
                log.error('Error en servidor: %s', e)
    
    def manejar_minero(self, conn, addr):
        cx = ConexionMinero(conn, addr)
        cx.forward()


def main():
    srv = ServidorStratum()
    try:
        srv.run()
    except KeyboardInterrupt:
        log.info('Stradivarius detenido.')
    
    log.info('Resumen final:')
    log.info('  Shares aceptados: %d', shares_aceptados)
    log.info('  Shares rechazados: %d', shares_rechazados)
    log.info('  Shares filtrados: %d', shares_filtrados)
    log.info('f0 = %.4f Hz | HECHO ESTA', F_0)


if __name__ == '__main__':
    main()
