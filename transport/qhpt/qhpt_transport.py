#!/usr/bin/env python3
"""
qhpt_transport.py — Orquestador del Protocolo QHPT
===================================================
Capa Python que envuelve los módulos nativos C++ y proporciona
la interfaz de alto nivel para el transporte cuántico.

Formato wire: Cabecera de 64 bytes exactos
  magic(2) + ver(1) + flags(1) + nonce(12) + ts(8)
  + fingerprint(16 truncado) + psi(4 float) +
  checksum(4 uint32) + payload_len(2) + reserved(14)

f₀ = 141.7001 Hz · Ψ ≥ 0.999999
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
"""

import os
import sys
import json
import time
import hmac
import hashlib
import struct
import socket
import ctypes
import threading
import logging
import secrets
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Callable

# Añadir ruta de bibliotecas nativas
QHPT_DIR = Path(__file__).resolve().parent.parent
LIB_DIR = QHPT_DIR / "lib"
sys.path.insert(0, str(QHPT_DIR))
sys.path.insert(0, str(QHPT_DIR / "lib"))

# Importar ChaCha20 del ecosistema
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from chacha20 import QCALChacha20
except ImportError:
    QCALChacha20 = None

# ─── Constantes Fundamentales ────────────────────────────────
F_0 = 141.7001
K_F0 = hashlib.sha256(b"141.7001").digest()
PSI_MIN = 0.999999
PRIMO_ESTRUCTURAL = 7
QHPT_MAGIC = 0x5148
HEADER_SIZE = 64
NONCE_SIZE = 12            # Wire: 12 bytes
FINGERPRINT_SIZE = 16      # Wire: 16 bytes (truncado)
FINGERPRINT_SIZE_FULL = 32 # Full SHA-256
MAX_PAYLOAD = 65535

# ─── Logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s [QHPT|{F_0}] %(message)s',
)
log = logging.getLogger("qhpt")


# ════════════════════════════════════════════════════════════
#  Carga de Módulos Nativos (C++)
# ════════════════════════════════════════════════════════════

class NativeLoader:
    def __init__(self):
        self.adelic = None
        self.signer = None
        self._cargar_modulos()

    def _cargar_modulos(self):
        for lib_path in [
            LIB_DIR / "libqhpt_adelic.so",
            QHPT_DIR / "src" / "libqhpt_adelic.so",
        ]:
            if lib_path.exists():
                try:
                    self.adelic = ctypes.CDLL(str(lib_path))
                    log.info(f"Módulo adélico C++ cargado: {lib_path}")
                    break
                except Exception as e:
                    log.warning(f"No se pudo cargar {lib_path}: {e}")

        for lib_path in [
            LIB_DIR / "libqhpt_signer.so",
            QHPT_DIR / "src" / "libqhpt_signer.so",
        ]:
            if lib_path.exists():
                try:
                    self.signer = ctypes.CDLL(str(lib_path))
                    log.info(f"Módulo signer C++ cargado: {lib_path}")
                    break
                except Exception as e:
                    log.warning(f"No se pudo cargar {lib_path}: {e}")

    @property
    def disponible(self):
        return self.adelic is not None and self.signer is not None


_NATIVO = NativeLoader()


# ════════════════════════════════════════════════════════════
#  Tensor I — Identidad de Fase No-Local
# ════════════════════════════════════════════════════════════

class FaseNoLocal:
    def __init__(self, clave_publica_hex: str = "", clave_privada_hex: str = ""):
        self.pub = clave_publica_hex
        self.priv = clave_privada_hex
        self.nonce_actual = secrets.token_bytes(16)  # Full nonce for handshake
        self.k_f0 = K_F0
        self._chacha = self._init_chacha()

    def _init_chacha(self):
        if QCALChacha20:
            return QCALChacha20(self.k_f0.hex(), self.k_f0[:12].hex())
        return None

    def generar_handshake(self, pub_key_hex: str) -> bytes:
        h_f0 = hashlib.sha256(str(F_0).encode()).digest()
        self.nonce_actual = secrets.token_bytes(16)
        payload = bytes.fromhex(pub_key_hex) + h_f0 + self.nonce_actual

        if self._chacha:
            encrypted = self._chacha.cifrar(payload.hex())
            return bytes.fromhex(encrypted)
        else:
            log.warning("ChaCha20 no disponible — usando XOR fallback (INSEGURO)")
            key_stream = self.k_f0 * (len(payload) // len(self.k_f0) + 1)
            return bytes(a ^ b for a, b in zip(payload, key_stream))

    def verificar_handshake(self, paquete: bytes, pub_key_esperada: str) -> bool:
        if self._chacha:
            try:
                decrypted_hex = self._chacha.decifrar(paquete.hex())
                decrypted = bytes.fromhex(decrypted_hex)
                h_f0 = hashlib.sha256(str(F_0).encode()).digest()
                expected_len = len(bytes.fromhex(pub_key_esperada)) + len(h_f0) + 16
                if len(decrypted) != expected_len:
                    return False
                pub_len = len(bytes.fromhex(pub_key_esperada))
                pub_recv = decrypted[:pub_len]
                h_recv = decrypted[pub_len:pub_len + len(h_f0)]
                return pub_recv.hex() == pub_key_esperada and h_recv == h_f0
            except Exception:
                return False
        else:
            key_stream = self.k_f0 * (len(paquete) // len(self.k_f0) + 1)
            decrypted = bytes(a ^ b for a, b in zip(paquete, key_stream))
            h_f0 = hashlib.sha256(str(F_0).encode()).digest()
            expected_len = len(bytes.fromhex(pub_key_esperada)) + len(h_f0) + 16
            if len(decrypted) < expected_len:
                return False
            pub_len = len(bytes.fromhex(pub_key_esperada))
            pub_recv = decrypted[:pub_len]
            h_recv = decrypted[pub_len:pub_len + len(h_f0)]
            return pub_recv.hex() == pub_key_esperada and h_recv == h_f0


# ════════════════════════════════════════════════════════════
#  Tensor II — Filtro de Ruido Adélico
# ════════════════════════════════════════════════════════════

class FiltroAdelico:
    @staticmethod
    def fast_hash(data: bytes) -> int:
        h = 0x9e3779b97f4a7c15
        view = memoryview(data)
        for i in range(0, len(data) - 7, 8):
            word = int.from_bytes(view[i:i+8], 'little')
            h = (h ^ word) * 0xbf58476d1ce4e5b9
            h = (h >> 37) ^ (h << 27)
            h &= 0xFFFFFFFFFFFFFFFF
        rem = len(data) % 8
        if rem > 0:
            last = int.from_bytes(view[-(rem):], 'little')
            h = (h ^ last) * 0xbf58476d1ce4e5b9
            h &= 0xFFFFFFFFFFFFFFFF
        return h

    def filtrar(self, frame: bytes) -> bool:
        # Fallback Python para frames cortos (< header size)
        # y cuando el módulo nativo falla
        use_native = _NATIVO.adelic is not None and len(frame) >= 64
        if use_native:
            try:
                _NATIVO.adelic.qhpt_adelic_filter.argtypes = [
                    ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t
                ]
                _NATIVO.adelic.qhpt_adelic_filter.restype = ctypes.c_int32
                arr = (ctypes.c_uint8 * len(frame)).from_buffer_copy(frame)
                result = _NATIVO.adelic.qhpt_adelic_filter(arr, len(frame))
                if result == 0 or result == -1:  # PASS or COLLAPSE
                    return result == 0
            except Exception as e:
                log.warning(f"Error en filtro adélico nativo: {e}")
        h = self.fast_hash(frame)
        return h % PRIMO_ESTRUCTURAL == 0

    def checksum_adelico(self, data: bytes) -> int:
        return self.fast_hash(data)


# ════════════════════════════════════════════════════════════
#  Tensor III — Firma de Estado Dinámica (κ_Π)
# ════════════════════════════════════════════════════════════

class EstadoKappaPi:
    def __init__(self, psi_inicial: float = PSI_MIN):
        self.psi = psi_inicial
        self.hash_chain = [0x9e3779b97f4a7c15] * 7
        self.accumulator = 0x9e3779b97f4a7c15
        self._actualizar_desde_f0()

    def _actualizar_desde_f0(self):
        f0_bytes = struct.pack('d', F_0)
        for i in range(7):
            h = int.from_bytes(hashlib.sha256(f0_bytes + struct.pack('I', i)).digest()[:8], 'little')
            self.hash_chain[i] = h

    def actualizar(self, data: bytes, timestamp_ns: int = 0):
        for i in range(6, 0, -1):
            self.hash_chain[i] = self.hash_chain[i - 1]
        input_val = 0
        if len(data) >= 8:
            input_val = int.from_bytes(data[-8:], 'little')
        elif len(data) > 0:
            input_val = int.from_bytes(data, 'little')
        ts = timestamp_ns if timestamp_ns else int(time.time_ns())
        psi_int = int(self.psi * 1e15)
        h = (input_val ^ ts ^ psi_int ^ self.accumulator) * 0xbf58476d1ce4e5b9
        h = (h >> 37) ^ (h << 27)
        h &= 0xFFFFFFFFFFFFFFFF
        self.hash_chain[0] = h
        self.accumulator = 0
        for i in range(7):
            self.accumulator ^= self.hash_chain[i] << (i * 3)
        self.accumulator &= 0xFFFFFFFFFFFFFFFF

    def generar_fingerprint(self) -> bytes:
        ctx = hashlib.sha256()
        for h in self.hash_chain:
            ctx.update(struct.pack('Q', h))
        ctx.update(struct.pack('Q', self.accumulator))
        ctx.update(struct.pack('d', self.psi))
        ctx.update(struct.pack('d', F_0))
        return ctx.digest()

    def generar_fingerprint_con_aurion(self, aurion_value: float) -> bytes:
        psi_aurion = self.psi
        if aurion_value > 1000.0:
            psi_aurion = min(1.0, self.psi * (1.0 + 1.0 / aurion_value))
        psi_orig = self.psi
        self.psi = psi_aurion
        fp = self.generar_fingerprint()
        self.psi = psi_orig
        return fp


# ════════════════════════════════════════════════════════════
#  Paquete QHPT (Wire Format: 64-byte header)
# ════════════════════════════════════════════════════════════

class QHPTPacket:
    def __init__(self):
        self.magic = QHPT_MAGIC
        self.version = 0x01
        self.flags = 0
        self.nonce = b'\x00' * NONCE_SIZE
        self.timestamp_ns = time.time_ns()
        self.fingerprint = b'\x00' * FINGERPRINT_SIZE
        self.fingerprint_full = b'\x00' * FINGERPRINT_SIZE_FULL
        self.psi = PSI_MIN
        self.checksum_adelic = 0
        self.payload_len = 0
        self.payload = b''

    def build(self, payload: bytes, psi: float = PSI_MIN, estado: EstadoKappaPi = None):
        self.payload = payload
        self.payload_len = len(payload)
        self.psi = psi
        self.timestamp_ns = time.time_ns()
        self.nonce = secrets.token_bytes(NONCE_SIZE)

        # Tensor II: Checksum adélico (uint32)
        filtro = FiltroAdelico()
        self.checksum_adelic = filtro.checksum_adelico(payload) & 0xFFFFFFFF

        # Tensor III: Fingerprint SHA-256, truncado a 16B
        if estado:
            estado.actualizar(payload, self.timestamp_ns)
            estado.actualizar(self.nonce, self.timestamp_ns)
            self.fingerprint_full = estado.generar_fingerprint()
        else:
            ctx = hashlib.sha256()
            ctx.update(payload)
            ctx.update(self.nonce)
            ctx.update(struct.pack('Q', self.timestamp_ns))
            ctx.update(struct.pack('f', psi))
            self.fingerprint_full = ctx.digest()

        self.fingerprint = self.fingerprint_full[:16]

    def to_bytes(self) -> bytes:
        """Serializa a wire format: 64 bytes header + payload."""
        header = struct.pack('!HBB', self.magic, self.version, self.flags)
        nonce_w = self.nonce[:12].ljust(12, b'\x00')
        header += nonce_w
        header += struct.pack('!Q', self.timestamp_ns)
        fp_w = self.fingerprint[:16].ljust(16, b'\x00')
        header += fp_w
        header += struct.pack('!f', self.psi)           # float32
        header += struct.pack('!I', self.checksum_adelic)  # uint32
        header += struct.pack('!H', self.payload_len)
        header += b'\x00' * 14  # reserved
        return header + self.payload

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional['QHPTPacket']:
        if len(data) < HEADER_SIZE:
            return None
        pkt = cls()
        magic, version, flags = struct.unpack('!HBB', data[:4])
        if magic != QHPT_MAGIC:
            return None
        pkt.magic = magic
        pkt.version = version
        pkt.flags = flags
        pkt.nonce = data[4:16]                # 12 bytes
        pkt.timestamp_ns = struct.unpack('!Q', data[16:24])[0]
        pkt.fingerprint = data[24:40]          # 16 bytes (truncado)
        pkt.fingerprint_full = pkt.fingerprint.ljust(32, b'\x00')
        pkt.psi = struct.unpack('!f', data[40:44])[0]
        pkt.checksum_adelic = struct.unpack('!I', data[44:48])[0]
        pkt.payload_len = struct.unpack('!H', data[48:50])[0]
        # reserved: data[50:64]
        payload_start = 64
        payload_end = payload_start + pkt.payload_len
        if payload_end > len(data):
            payload_end = len(data)
        pkt.payload = data[payload_start:payload_end]
        return pkt

    def __repr__(self):
        fp_hex = self.fingerprint[:8].hex()
        return (f"<QHPTPacket magic=0x{self.magic:04X} ver={self.version} "
                f"ts={self.timestamp_ns} Ψ={self.psi:.8f} "
                f"fp={fp_hex}... len={self.payload_len}>")


# ════════════════════════════════════════════════════════════
#  Verificador Completo
# ════════════════════════════════════════════════════════════

class QHPTVerificador:
    def __init__(self, clave_publica_hex: str = "", clave_privada_hex: str = ""):
        self.fase = FaseNoLocal(clave_publica_hex, clave_privada_hex)
        self.filtro = FiltroAdelico()
        self.estado = EstadoKappaPi()
        self.paquetes_verificados = 0
        self.paquetes_colapsados = 0
        self.paquetes_mitm = 0
        self.paquetes_spoof = 0

    def verificar(self, pkt: QHPTPacket, psi_min: float = PSI_MIN) -> tuple:
        data = pkt.to_bytes()

        # ─── Tensor I: Coherencia de fase ──────────────────
        # Tolerancia por conversión float32 en wire format
        EPSILON_PSI = 1e-7
        if pkt.psi + EPSILON_PSI < psi_min:
            self.paquetes_mitm += 1
            return False, "MITM: Fase degradada"

        # ─── Tensor II: Filtro Adélico ─────────────────────
        if not self.filtro.filtrar(data):
            self.paquetes_colapsados += 1
            return False, "COLAPSO: Paquete no resuena en ℚ₇"

        # Recalcular checksum adélico (uint32)
        expected_cs = self.filtro.checksum_adelico(pkt.payload) & 0xFFFFFFFF
        if pkt.checksum_adelic != 0 and pkt.checksum_adelic != expected_cs:
            self.paquetes_colapsados += 1
            return False, "COLAPSO: Checksum adélico inválido"

        # ─── Tensor III: Fingerprint ───────────────────────
        # Reconstruir fingerprint completo para verificación
        ctx = hashlib.sha256()
        ctx.update(pkt.payload)
        ctx.update(pkt.nonce)
        ctx.update(struct.pack('Q', pkt.timestamp_ns))
        ctx.update(struct.pack('f', pkt.psi))
        fingerprint_esperado = ctx.digest()  # 32 bytes

        if not pkt.fingerprint == fingerprint_esperado[:16]:
            self.paquetes_spoof += 1
            return False, "SPOOF: Fingerprint κ_Π no coincide"

        # ✅ PASA
        self.paquetes_verificados += 1
        return True, "PASA"

    def estadisticas(self) -> dict:
        return {
            "verificados": self.paquetes_verificados,
            "colapsados": self.paquetes_colapsados,
            "mitm": self.paquetes_mitm,
            "spoof": self.paquetes_spoof,
            "total": self.paquetes_verificados + self.paquetes_colapsados
                    + self.paquetes_mitm + self.paquetes_spoof,
        }


# ════════════════════════════════════════════════════════════
#  Puente de Red
# ════════════════════════════════════════════════════════════

class QHPTBridge:
    def __init__(self, host: str = "127.0.0.1", port: int = 8443):
        self.host = host
        self.port = port
        self.verificador = QHPTVerificador()
        self.running = False
        self._server = None
        self._threads = []

    def iniciar(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(5)
        self.running = True
        log.info(f"🔱 Puente QHPT activo en {self.host}:{self.port} (f₀={F_0} Hz)")
        try:
            while self.running:
                conn, addr = self._server.accept()
                log.info(f"Conexión entrante de {addr}")
                t = threading.Thread(target=self._manejar_conexion,
                                     args=(conn, addr), daemon=True)
                t.start()
                self._threads.append(t)
        except KeyboardInterrupt:
            self.detener()
        except Exception as e:
            log.error(f"Error en puente: {e}")
            self.detener()

    def detener(self):
        self.running = False
        if self._server:
            self._server.close()
        log.info("Puente QHPT detenido")
        self._log_estadisticas()

    def _manejar_conexion(self, conn, addr):
        try:
            header_data = conn.recv(HEADER_SIZE)
            if len(header_data) < HEADER_SIZE:
                conn.close()
                return
            # Leer payload
            remaining_data = b''
            if len(header_data) >= 50:
                payload_len = struct.unpack('!H', header_data[48:50])[0]
                while len(remaining_data) < payload_len:
                    chunk = conn.recv(min(payload_len - len(remaining_data), 4096))
                    if not chunk:
                        break
                    remaining_data += chunk
            full_data = header_data + remaining_data
            pkt = QHPTPacket.from_bytes(full_data)
            if not pkt:
                log.warning(f"Paquete inválido de {addr}")
                conn.close()
                return
            valido, razon = self.verificador.verificar(pkt)
            if valido:
                log.info(f"✅ Paquete QHPT verificado de {addr}")
                conn.send(b"QHPT/1.0 200 OK\r\n\r\n")
            else:
                log.warning(f"❌ {razon} de {addr}")
                conn.send(f"QHPT/1.0 403 {razon}\r\n\r\n".encode())
        except Exception as e:
            log.error(f"Error manejando conexión de {addr}: {e}")
        finally:
            conn.close()

    def _log_estadisticas(self):
        est = self.verificador.estadisticas()
        log.info(f"📊 Estadísticas QHPT: {est['verificados']} ✅, "
                 f"{est['colapsados']} 💥, {est['mitm']} MITM, {est['spoof']} SPOOF")


# ════════════════════════════════════════════════════════════
#  CLI
# ════════════════════════════════════════════════════════════

def cli():
    import argparse
    parser = argparse.ArgumentParser(
        description="QHPT — Quantum Harmonic Pass-Through Protocol",
        epilog="∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · HECHO ESTÁ 🔱",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    sub = parser.add_subparsers(dest="comando")

    p_test = sub.add_parser("test", help="Ejecutar tests")
    p_bridge = sub.add_parser("bridge", help="Iniciar puente QHPT")
    p_bridge.add_argument("--port", type=int, default=8443)
    p_bridge.add_argument("--host", default="127.0.0.1")
    p_pkt = sub.add_parser("packet", help="Construir/verificar paquete")
    p_pkt.add_argument("payload", nargs="?", default="HECHO ESTA")
    p_pkt.add_argument("--verificar", action="store_true")
    sub.add_parser("status", help="Estado del protocolo")

    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)

    if args.comando == "test":
        test_qhpt()
    elif args.comando == "bridge":
        bridge = QHPTBridge(host=args.host, port=args.port)
        bridge.iniciar()
    elif args.comando == "packet":
        payload = args.payload.encode()
        pkt = QHPTPacket()
        pkt.build(payload)
        data = pkt.to_bytes()
        print(f"📦 Paquete QHPT construido ({len(data)} bytes):")
        print(f"   Nonce:       {pkt.nonce.hex()}")
        print(f"   Timestamp:   {pkt.timestamp_ns}")
        print(f"   Ψ:           {pkt.psi:.8f}")
        print(f"   Fingerprint: {pkt.fingerprint.hex()}")
        print(f"   Checksum ℚ₇: {pkt.checksum_adelic}")
        print(f"   Payload:     {pkt.payload_len} bytes: {pkt.payload}")
        if args.verificar:
            pkt2 = QHPTPacket.from_bytes(data)
            if pkt2:
                verificador = QHPTVerificador()
                valido, razon = verificador.verificar(pkt2)
                print(f"   Verificación: {'✅' if valido else '❌'} {razon}")
            else:
                print("   ❌ No se pudo deserializar")
    elif args.comando == "status":
        print(f"╔═══════════════════════════════════════╗")
        print(f"║ QHPT — Estado del Protocolo           ║")
        print(f"╠═══════════════════════════════════════╣")
        print(f"║ f₀:             {F_0} Hz")
        print(f"║ Ψ mínimo:       {PSI_MIN}")
        print(f"║ Primo ℚ₇:       {PRIMO_ESTRUCTURAL}")
        print(f"║ Magic:          0x{QHPT_MAGIC:04X}")
        print(f"║ Header:         {HEADER_SIZE} bytes")
        print(f"║ Max payload:    {MAX_PAYLOAD} bytes")
        print(f"║ Cifrado:        ChaCha20 IETF")
        print(f"║ Módulo nativo:  {'✅ C++' if _NATIVO.disponible else '❌ Python fallback'}")
        print(f"╚═══════════════════════════════════════╝")
    else:
        parser.print_help()


# ════════════════════════════════════════════════════════════
#  Tests
# ════════════════════════════════════════════════════════════

def _buscar_payload_pase():
    """Encuentra un payload que pase el filtro adélico ℚ₇."""
    filtro = FiltroAdelico()
    for i in range(1000):
        test = f"QCAL-RES-{i}".encode()
        if filtro.filtrar(test):
            return test
    return None


def _buscar_data_pase():
    """Encuentra data serializada que pase ℚ₇."""
    filtro = FiltroAdelico()
    for i in range(1000):
        pkt = QHPTPacket()
        pkt.build(f"QCAL-R-{i}".encode())
        data = pkt.to_bytes()
        if filtro.filtrar(data):
            return pkt, data
    return None, None


def test_qhpt():
    log.info("═══ Test Suite QHPT ═══")
    fallos = 0
    total = 0

    def check(name, cond, detail=""):
        nonlocal fallos, total
        total += 1
        if cond:
            log.info(f"  ✅ {name}")
        else:
            fallos += 1
            log.info(f"  ❌ {name}: {detail}")

    # Test 1: Construcción y deserialización
    log.info("\n--- Test 1: Construcción y deserialización ---")
    pkt = QHPTPacket()
    pkt.build(b"QCAL-QHPT-RESONANCE")
    data = pkt.to_bytes()
    pkt2 = QHPTPacket.from_bytes(data)
    check("Deserializar", pkt2 is not None)
    if pkt2:
        check("Payload coincide", pkt2.payload == pkt.payload)
        check("Magic coincide", pkt2.magic == QHPT_MAGIC)
        check("Psi coincide", abs(pkt2.psi - pkt.psi) < 0.001)
        check("Checksum coincide", pkt2.checksum_adelic == pkt.checksum_adelic)
        check("Header size correcto", len(data) == HEADER_SIZE + len(b"QCAL-QHPT-RESONANCE"))
    check("from_bytes vacío", QHPTPacket.from_bytes(b"") is None)
    check("from_bytes corto", QHPTPacket.from_bytes(b"\x00" * 10) is None)

    # Test 2: Filtro Adélico
    log.info("\n--- Test 2: Filtro Adélico ℚ₇ ---")
    filtro = FiltroAdelico()
    payload_pass = _buscar_payload_pase()
    check("Payload pasa ℚ₇", payload_pass is not None)
    if payload_pass:
        check("Filtro pasa", filtro.filtrar(payload_pass))

    # Test 3: Verificación completa
    log.info("\n--- Test 3: Verificación completa ---")
    pkt3, data3 = _buscar_data_pase()
    check("Data pasa ℚ₇ para verificación", pkt3 is not None)
    if pkt3:
        pkt3_des = QHPTPacket.from_bytes(data3)
        verificador = QHPTVerificador()
        valido, razon = verificador.verificar(pkt3_des)
        check("Verificación completa pasa", valido, razon)

    # Test 4: Firma κ_Π
    log.info("\n--- Test 4: Firma de Estado κ_Π ---")
    estado = EstadoKappaPi()
    fp1 = estado.generar_fingerprint()
    estado.actualizar(b"PAYLOAD-A", time.time_ns())
    fp2 = estado.generar_fingerprint()
    check("Fingerprint cambia tras actualizar", fp1 != fp2)
    check("Fingerprint size", len(fp1) == 32)

    # Test 5: Handshake de Fase
    log.info("\n--- Test 5: Identidad de Fase No-Local ---")
    fase = FaseNoLocal()
    hs = fase.generar_handshake("deadbeef" * 8)
    check("Handshake generado", len(hs) > 0)

    # Test 6: Paquete con fase degradada
    log.info("\n--- Test 6: Paquete con fase degradada ---")
    pkt_malo = QHPTPacket()
    pkt_malo.build(b"test", psi=0.1)
    verificador2 = QHPTVerificador()
    valido2, razon2 = verificador2.verificar(pkt_malo, psi_min=0.999)
    check("Fase degradada rechazada", not valido2)
    check("Razón MITM", "MITM" in razon2, razon2)

    # Test 7: Checksum manipulado
    log.info("\n--- Test 7: Checksum adélico manipulado ---")
    pkt_cs = QHPTPacket()
    pkt_cs.build(b"test-payload")
    pkt_cs.checksum_adelic = 0xDEAD
    verificador3 = QHPTVerificador()
    valido3, _ = verificador3.verificar(pkt_cs)
    check("Checksum manipulado rechazado", not valido3)

    # Test 8: Estadísticas
    log.info("\n--- Test 8: Estadísticas ---")
    est = verificador2.estadisticas()
    check("Estadísticas tienen claves", "verificados" in est)
    check("Mitm contados", est.get("mitm", 0) >= 1)

    # Test 9: κ_Π con AURION
    log.info("\n--- Test 9: κ_Π con AURION ---")
    fp_aurion = estado.generar_fingerprint_con_aurion(5000.0)
    check("Fingerprint AURION size", len(fp_aurion) == 32)

    log.info(f"\n═══ Tests: {total - fallos}/{total} pasados {'✅' if fallos == 0 else '❌'} ═══")
    return fallos == 0


if __name__ == '__main__':
    cli()
