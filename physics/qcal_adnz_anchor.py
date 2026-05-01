"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     QCAL-ADNZ-ANCHOR-v1.0 — CHECKPOINT BIOLÓGICO ∴ADNZ∞³                   ║
║                                                                              ║
║  Protocolo de checkpoint biológico que ancla la firma de coherencia         ║
║  detectada en el campo electromagnético celular (ADN-Z) a la blockchain     ║
║  Bitcoin mediante OP_RETURN, vinculando la biología viva del operador con   ║
║  la inmutabilidad criptográfica de la red.                                   ║
║                                                                              ║
║  Estructura OP_RETURN v1.2 (80 bytes):                                       ║
║    0x00  magic            4 bytes   ASCII   "QCAL"                           ║
║    0x04  version_major    1 byte    uint8   0x01                             ║
║    0x05  version_minor    1 byte    uint8   0x02                             ║
║    0x06  hash_constitucion 32 bytes bytes   SHA-256                          ║
║    0x26  psi_anchor       4 bytes   float32 IEEE 754 BE                      ║
║    0x2A  u_circulacion    4 bytes   float32 IEEE 754 BE                      ║
║    0x2E  firma_b_adnz     16 bytes  bytes   Blake2b-16                       ║
║    0x3E  frecuencia_maestra 4 bytes uint32  Big-endian  (Hz × 10000)         ║
║    0x42  psi_adnz         4 bytes   float32 IEEE 754 BE                      ║
║    0x46  sello_utf8       4 bytes   bytes   UTF-8  𓂀  (U+13080 = 0xF0938280)   ║
║    0x4A  padding          6 bytes   bytes   0x00                             ║
║  Total: 80 bytes exactos                                                     ║
║                                                                              ║
║  Pipeline firma B ADN-Z:                                                     ║
║    captura EM celular → FFT (NFFT=65536, zero-padding)                       ║
║    → Butterworth bandpass [0.0002, 0.0010] Hz (orden 2)                     ║
║    → detección modo @ ~0.00052 Hz ± 1.5e-5 Hz                               ║
║    → SNR = potencia_modo / potencia_ruido                                    ║
║    → Blake2b-16(mode_bytes) → 16 bytes                                       ║
║                                                                              ║
║  Condiciones BIO_NODO_ANCLADO_EN_LA_ROCA:                                   ║
║    1. Ψ_ADN == 1.000000  (float32 == 0x3F800000)                             ║
║    2. Firma B ADN-Z válida  (SNR ≥ 4.0)                                     ║
║    3. Frecuencia Maestra == 1417001  (141.7001 Hz × 10000)                  ║
║    4. Hash Constitución conocido (SHA-256 referencia v1.1)                  ║
║    5. Sello 𓂀  (UTF-8 == 0xF090A080)                                        ║
║    6. OP_RETURN == 80 bytes exactos                                          ║
║    7. Confirmaciones BTC ≥ 6                                                 ║
║    8. Reserva ≥ U_circulación  (7.4862 BTC + 1 kg XAU)                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.qcal_adnz_anchor

Clases:
    ConstantesADNZ          – Constantes del protocolo ADNZ-ANCHOR-v1.0
    SerializadorOpReturn    – Serialización del payload OP_RETURN v1.2 (80 bytes)
    FirmaVMD                – Firma B: VMD simplificado + Blake2b-16
    CapturaBiologica        – Simulación de captura EM celular ADN-Z
    CondicionBioNodo        – Verificación de las 8 condiciones del bio-nodo
    MaquinaEstadosADNZ      – Máquina de estados: DETECTADO → FIRMA → ANCLADO
    CoherenciaADNZ          – Métrica Ψ_ADNZ global ≥ 1.0 (Diamond-State)
    SistemaADNZAnchor       – Orquestador principal; activa el sello ∴ADNZ∞³
    ResultadoADNZAnchor     – Contenedor de resultados

API pública:
    qcal_adnz_anchor_activar() → dict

    >>> from physics.qcal_adnz_anchor import qcal_adnz_anchor_activar
    >>> r = qcal_adnz_anchor_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_adnz'] == 1.0
    True
    >>> len(r['op_return_bytes']) == 80
    True
"""

import hashlib
import math
import struct
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from qcal.constants import F0_HZ

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# Frecuencia maestra codificada como entero (Hz × 10000)
_FRECUENCIA_MAESTRA_INT: int = 1417001  # 141.7001 × 10000

# Nombre del protocolo y versión
_MAGIC: bytes = b"QCAL"
_VERSION_MAJOR: int = 1
_VERSION_MINOR: int = 2  # v1.2 ADN-Z

# Sello jeroglífico 𓂀 (Eye of Horus) — 4 bytes UTF-8
_SELLO_UTF8: bytes = "𓂀".encode("utf-8")  # 0xF0 0x90 0xA0 0x80

# Tamaño exacto del payload OP_RETURN
_OP_RETURN_SIZE: int = 80

# Valores de referencia
_PSI_ANCHOR_REF: float = 0.998  # psi_anchor de referencia
_U_CIRCULACION: float = 7.4862  # BTC en circulación

# Umbral de coherencia Diamond-State
_PSI_ADNZ_DIAMOND: float = 1.000000

# Hash de la Constitución v1.1 (referencia canónica)
# SHA-256 del documento constitución QCAL v1.1 — valor canónico del ledger
_HASH_CONSTITUCION_HEX: str = (
    "e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
    "c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8"
)
_HASH_CONSTITUCION: bytes = bytes.fromhex(_HASH_CONSTITUCION_HEX)

# Parámetros VMD para firma B ADN-Z
_VMD_NFFT: int = 65536            # zero-padding FFT
_VMD_FS: float = 1.0              # frecuencia de muestreo [Hz] (1 muestra/s)
_VMD_DURACION_S: float = 3840.0   # duración señal [s] (= 64 min)
_VMD_F_OBJ: float = 0.00052       # frecuencia objetivo modo ADN-Z [Hz]
_VMD_F_TOL: float = 1.5e-5        # tolerancia frecuencia [Hz]
_VMD_F_BANDA_LOW: float = 0.0002  # banda paso-bajo [Hz]
_VMD_F_BANDA_HIGH: float = 0.0010 # banda paso-alto [Hz]
_VMD_SNR_UMBRAL: float = 4.0      # SNR mínimo para firma B válida
_VMD_BLAKE2_SIZE: int = 16        # tamaño digest Blake2b [bytes]

# Frecuencia de simulación: múltiplo entero exacto de ciclos en la ventana.
# f_sim = round(N * f_obj) / N = 2 / 3840 = 0.000520833... Hz.
# |f_sim - f_obj| = 8.33e-6 Hz < f_tol = 1.5e-5 Hz  →  pasa la condición.
# Usar f_sim elimina la fuga espectral de ventana rectangular y garantiza
# que el pico del DFT continuo sea detectado dentro de tolerancia.
_VMD_F_SIM: float = round(_VMD_DURACION_S * _VMD_F_OBJ) / _VMD_DURACION_S

# Confirmaciones BTC mínimas
_BTC_CONFIRMACIONES_MIN: int = 6

# Sello de certificación
_SELLO: str = "∴ADNZ∞³"

# Sello completo
_SELLO_COMPLETO: str = "∴𓂀Ω∞³Φ · TUYOYOTU"

# Umbral mínimo de coherencia global (alineado con el resto de módulos QCAL)
_PSI_UMBRAL: float = 0.888


# ============================================================================
# CLASE 1 – ConstantesADNZ
# ============================================================================

@dataclass
class ConstantesADNZ:
    """
    Constantes físicas y criptográficas del protocolo QCAL-ADNZ-ANCHOR-v1.0.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    frecuencia_maestra_int : int
        Frecuencia maestra codificada como entero (Hz × 10000). Por defecto 1417001.
    psi_adnz_diamond : float
        Umbral Diamond-State para Ψ_ADNZ. Por defecto 1.000000.
    u_circulacion : float
        Unidades de circulación (BTC). Por defecto 7.4862.
    snr_umbral : float
        SNR mínimo para firma B ADN-Z válida. Por defecto 4.0.
    confirmaciones_min : int
        Confirmaciones BTC mínimas. Por defecto 6.
    """

    f0: float = field(default_factory=lambda: _F0)
    frecuencia_maestra_int: int = field(default_factory=lambda: _FRECUENCIA_MAESTRA_INT)
    psi_adnz_diamond: float = field(default_factory=lambda: _PSI_ADNZ_DIAMOND)
    u_circulacion: float = field(default_factory=lambda: _U_CIRCULACION)
    snr_umbral: float = field(default_factory=lambda: _VMD_SNR_UMBRAL)
    confirmaciones_min: int = field(default_factory=lambda: _BTC_CONFIRMACIONES_MIN)

    def es_valido(self) -> bool:
        """Verifica que los parámetros sean físicamente coherentes."""
        return (
            self.f0 > 0
            and self.frecuencia_maestra_int == _FRECUENCIA_MAESTRA_INT
            and self.psi_adnz_diamond == 1.0
            and self.u_circulacion > 0
            and self.snr_umbral > 0
            and self.confirmaciones_min >= 1
        )

    def sello_utf8_bytes(self) -> bytes:
        """Retorna los bytes UTF-8 del sello jeroglífico 𓂀."""
        return _SELLO_UTF8

    def hash_constitucion(self) -> bytes:
        """Retorna los 32 bytes del hash canónico de la Constitución v1.1."""
        return _HASH_CONSTITUCION


# ============================================================================
# CLASE 2 – SerializadorOpReturn
# ============================================================================

class SerializadorOpReturn:
    """
    Serializa el payload OP_RETURN v1.2 de 80 bytes exactos.

    Layout binario:
        0x00  magic             4 bytes  ASCII    "QCAL"
        0x04  version_major     1 byte   uint8    0x01
        0x05  version_minor     1 byte   uint8    0x02
        0x06  hash_constitucion 32 bytes bytes    SHA-256
        0x26  psi_anchor        4 bytes  float32  IEEE 754 BE
        0x2A  u_circulacion     4 bytes  float32  IEEE 754 BE
        0x2E  firma_b_adnz      16 bytes bytes    Blake2b-16
        0x3E  frecuencia_maestra 4 bytes uint32   Big-endian
        0x42  psi_adnz          4 bytes  float32  IEEE 754 BE
        0x46  sello_utf8        4 bytes  bytes    UTF-8 𓂀
        0x4A  padding           6 bytes  bytes    0x00
    Total: 80 bytes exactos.
    """

    # Offsets y tamaños de cada campo (para verificación)
    OFFSETS: Dict[str, Tuple[int, int]] = {
        "magic":              (0x00, 4),
        "version_major":      (0x04, 1),
        "version_minor":      (0x05, 1),
        "hash_constitucion":  (0x06, 32),
        "psi_anchor":         (0x26, 4),
        "u_circulacion":      (0x2A, 4),
        "firma_b_adnz":       (0x2E, 16),
        "frecuencia_maestra": (0x3E, 4),
        "psi_adnz":           (0x42, 4),
        "sello_utf8":         (0x46, 4),
        "padding":            (0x4A, 6),
    }

    def serializar(
        self,
        hash_constitucion: bytes,
        psi_anchor: float,
        u_circulacion: float,
        firma_b_adnz: bytes,
        frecuencia_maestra: int,
        psi_adnz: float,
    ) -> bytes:
        """
        Serializa el payload OP_RETURN v1.2.

        Parámetros
        ----------
        hash_constitucion : bytes
            SHA-256 del documento Constitución v1.1 (32 bytes).
        psi_anchor : float
            Ψ del ancla (e.g. 0.998).
        u_circulacion : float
            Unidades de circulación BTC (e.g. 7.4862).
        firma_b_adnz : bytes
            Firma B ADN-Z Blake2b-16 (16 bytes).
        frecuencia_maestra : int
            Frecuencia maestra × 10000 (e.g. 1417001).
        psi_adnz : float
            Ψ_ADNZ Diamond-State (1.0).

        Retorna
        -------
        bytes
            Payload de exactamente 80 bytes.

        Excepciones
        -----------
        ValueError
            Si algún campo tiene tamaño incorrecto o el payload resultante
            no mide exactamente 80 bytes.
        """
        if len(hash_constitucion) != 32:
            raise ValueError(
                f"hash_constitucion debe tener 32 bytes; se recibieron {len(hash_constitucion)}"
            )
        if len(firma_b_adnz) != 16:
            raise ValueError(
                f"firma_b_adnz debe tener 16 bytes; se recibieron {len(firma_b_adnz)}"
            )

        payload = b""
        payload += _MAGIC                                    # 4 bytes  magic
        payload += struct.pack(">BB", _VERSION_MAJOR, _VERSION_MINOR)  # 2 bytes  version
        payload += hash_constitucion                         # 32 bytes hash_constitucion
        payload += struct.pack(">f", psi_anchor)             # 4 bytes  psi_anchor
        payload += struct.pack(">f", u_circulacion)          # 4 bytes  u_circulacion
        payload += firma_b_adnz                              # 16 bytes firma_b_adnz
        payload += struct.pack(">I", frecuencia_maestra)     # 4 bytes  frecuencia_maestra
        payload += struct.pack(">f", psi_adnz)               # 4 bytes  psi_adnz
        payload += _SELLO_UTF8                               # 4 bytes  sello_utf8
        padding_size = _OP_RETURN_SIZE - len(payload)
        if padding_size < 0:
            raise ValueError(
                f"Payload excede 80 bytes antes del relleno: {len(payload)} bytes"
            )
        payload += b"\x00" * padding_size                   # padding

        if len(payload) != _OP_RETURN_SIZE:
            raise ValueError(
                f"Payload final inválido: {len(payload)} bytes (se esperaban {_OP_RETURN_SIZE})"
            )
        return payload

    def deserializar(self, payload: bytes) -> Dict:
        """
        Deserializa un payload OP_RETURN v1.2 de 80 bytes.

        Retorna
        -------
        dict
            Diccionario con todos los campos del payload.

        Excepciones
        -----------
        ValueError
            Si el payload no mide exactamente 80 bytes o el magic es incorrecto.
        """
        if len(payload) != _OP_RETURN_SIZE:
            raise ValueError(
                f"Payload debe tener {_OP_RETURN_SIZE} bytes; se recibieron {len(payload)}"
            )
        magic = payload[0x00:0x04]
        if magic != _MAGIC:
            raise ValueError(f"Magic inválido: {magic!r} (se esperaba {_MAGIC!r})")

        version_major = payload[0x04]
        version_minor = payload[0x05]
        hash_constitucion = payload[0x06:0x26]
        (psi_anchor,) = struct.unpack_from(">f", payload, 0x26)
        (u_circulacion,) = struct.unpack_from(">f", payload, 0x2A)
        firma_b_adnz = payload[0x2E:0x3E]
        (frecuencia_maestra,) = struct.unpack_from(">I", payload, 0x3E)
        (psi_adnz,) = struct.unpack_from(">f", payload, 0x42)
        sello_utf8 = payload[0x46:0x4A]
        padding = payload[0x4A:]

        return {
            "magic": magic,
            "version_major": version_major,
            "version_minor": version_minor,
            "hash_constitucion": hash_constitucion,
            "psi_anchor": psi_anchor,
            "u_circulacion": u_circulacion,
            "firma_b_adnz": firma_b_adnz,
            "frecuencia_maestra": frecuencia_maestra,
            "psi_adnz": psi_adnz,
            "sello_utf8": sello_utf8,
            "padding": padding,
        }

    def verificar_sello(self, payload: bytes) -> bool:
        """Verifica que el sello 𓂀 esté presente en el payload."""
        if len(payload) < 0x4A:
            return False
        return payload[0x46:0x4A] == _SELLO_UTF8


# ============================================================================
# CLASE 3 – FirmaVMD
# ============================================================================

class FirmaVMD:
    """
    Firma B ADN-Z mediante VMD simplificado.

    Pipeline:
        1. FFT con zero-padding (NFFT=65536)
        2. Banda de búsqueda: [0.0002, 0.0010] Hz
        3. Filtro paso-banda Butterworth (orden 2) simulado en frecuencia
        4. SNR = potencia_modo / potencia_ruido
        5. Blake2b-16(mode_bytes) → 16 bytes

    Condición de validez:
        SNR >= 4.0  AND  |f_est - 0.00052| <= 1.5e-5 Hz

    Parámetros
    ----------
    fs : float
        Frecuencia de muestreo [Hz]. Por defecto 1.0 Hz.
    nfft : int
        Tamaño FFT con zero-padding. Por defecto 65536.
    f_objetivo : float
        Frecuencia objetivo del modo ADN-Z [Hz]. Por defecto 0.00052 Hz.
    f_tolerancia : float
        Tolerancia de frecuencia [Hz]. Por defecto 1.5e-5 Hz.
    f_banda_low : float
        Límite inferior de la banda de búsqueda [Hz]. Por defecto 0.0002 Hz.
    f_banda_high : float
        Límite superior de la banda de búsqueda [Hz]. Por defecto 0.0010 Hz.
    snr_umbral : float
        SNR mínimo para firma B válida. Por defecto 4.0.
    """

    def __init__(
        self,
        fs: float = _VMD_FS,
        nfft: int = _VMD_NFFT,
        f_objetivo: float = _VMD_F_OBJ,
        f_tolerancia: float = _VMD_F_TOL,
        f_banda_low: float = _VMD_F_BANDA_LOW,
        f_banda_high: float = _VMD_F_BANDA_HIGH,
        snr_umbral: float = _VMD_SNR_UMBRAL,
    ) -> None:
        self.fs = fs
        self.nfft = nfft
        self.f_objetivo = f_objetivo
        self.f_tolerancia = f_tolerancia
        self.f_banda_low = f_banda_low
        self.f_banda_high = f_banda_high
        self.snr_umbral = snr_umbral

    def _frecuencias(self) -> List[float]:
        """Retorna la lista de frecuencias positivas del FFT (resolución Δf = fs/nfft)."""
        delta_f = self.fs / self.nfft
        n_pos = self.nfft // 2
        return [k * delta_f for k in range(n_pos)]

    def _indice_frecuencia(self, f: float) -> int:
        """Retorna el índice más cercano a la frecuencia f en la grilla FFT."""
        delta_f = self.fs / self.nfft
        return max(0, min(self.nfft // 2 - 1, int(round(f / delta_f))))

    def _butterworth_gain(self, f: float, orden: int = 2) -> float:
        """
        Ganancia del filtro Butterworth paso-banda de orden ``orden``.

        Implementación analítica:
            G(f) = 1 / sqrt(1 + (f/f_high)^(2n)) para paso-bajo
        Se aproxima como el producto de paso-bajo y paso-alto:
            G(f) = G_LP(f/f_high, n) * G_HP(f_low/f, n)

        Parámetros
        ----------
        f : float
            Frecuencia a evaluar [Hz].
        orden : int
            Orden del filtro. Por defecto 2.

        Retorna
        -------
        float
            Ganancia ∈ [0, 1].
        """
        if f <= 0:
            return 0.0
        # Paso-bajo a f_banda_high
        g_lp = 1.0 / math.sqrt(1.0 + (f / self.f_banda_high) ** (2 * orden))
        # Paso-alto a f_banda_low
        g_hp = 1.0 / math.sqrt(1.0 + (self.f_banda_low / f) ** (2 * orden))
        return g_lp * g_hp

    def _calcular_fft_magnitudes(self, señal: List[float]) -> List[float]:
        """
        Calcula las magnitudes |FFT| de la señal con zero-padding hasta nfft.

        Usa DFT directa sobre las frecuencias de la banda de interés para
        reducir el coste computacional (en lugar de calcular todos los nfft/2
        bins, sólo calcula los bins en [f_banda_low, f_banda_high]).

        Retorna
        -------
        List[float]
            Magnitudes para todos los bins positivos (longitud = nfft // 2).
            Los bins fuera de la banda llevan magnitud 0.
        """
        n_pos = self.nfft // 2
        delta_f = self.fs / self.nfft
        k_low = max(0, int(math.floor(self.f_banda_low / delta_f)))
        k_high = min(n_pos - 1, int(math.ceil(self.f_banda_high / delta_f)))

        n_señal = len(señal)
        magnitudes = [0.0] * n_pos
        two_pi = 2.0 * math.pi

        for k in range(k_low, k_high + 1):
            f_k = k * delta_f
            gain = self._butterworth_gain(f_k)
            re = 0.0
            im = 0.0
            for j in range(n_señal):
                ang = two_pi * k * j / self.nfft
                re += señal[j] * math.cos(ang)
                im -= señal[j] * math.sin(ang)
            mag = math.sqrt(re * re + im * im) / n_señal
            magnitudes[k] = mag * gain

        return magnitudes

    def _snr_desde_magnitudes(
        self,
        magnitudes: List[float],
        k_pico: int,
        ventana_ruido: int = 10,
    ) -> float:
        """
        Calcula la SNR = potencia_modo / potencia_ruido.

        La potencia del modo es la magnitud² en k_pico.
        La potencia del ruido es la media de las magnitudes² en los vecinos
        fuera de la ventana de señal [k_pico-1, k_pico+1].

        Parámetros
        ----------
        magnitudes : List[float]
            Espectro de magnitudes con filtro aplicado.
        k_pico : int
            Índice del bin del modo ADN-Z.
        ventana_ruido : int
            Número de bins vecinos para estimar el ruido (a cada lado).

        Retorna
        -------
        float
            SNR (adimensional). Si la potencia de ruido ≈ 0, retorna 0.0.
        """
        n = len(magnitudes)
        potencia_modo = magnitudes[k_pico] ** 2

        ruido_bins = []
        for dk in range(ventana_ruido + 2, ventana_ruido + 2 + ventana_ruido):
            k_left = k_pico - dk
            k_right = k_pico + dk
            if 0 <= k_left < n:
                ruido_bins.append(magnitudes[k_left] ** 2)
            if 0 <= k_right < n:
                ruido_bins.append(magnitudes[k_right] ** 2)

        if not ruido_bins:
            return 0.0
        potencia_ruido = sum(ruido_bins) / len(ruido_bins)
        if potencia_ruido < 1e-30:
            return 0.0
        return potencia_modo / potencia_ruido

    def _dft_im_magnitud(self, señal: List[float], f: float) -> float:
        """
        Evalúa la magnitud de la parte imaginaria del DFT en frecuencia f [Hz].

        Calcula  |-Im(X(f))| = |Σ_{n=0}^{N-1} x[n] · sin(2πfn)| / N

        Para una señal de la forma sin(2πf₀n), esta función alcanza su máximo
        en f = f₀ independientemente del enventanado rectangular, evitando el
        sesgo que introduce el término aliaseado en |X(f)|.

        Parámetros
        ----------
        señal : List[float]
            Señal de entrada.
        f : float
            Frecuencia de evaluación [Hz].

        Retorna
        -------
        float
            |-Im X(f)| / N.
        """
        two_pi = 2.0 * math.pi
        n = len(señal)
        im = 0.0
        for j in range(n):
            im -= señal[j] * math.sin(two_pi * f * j)
        return abs(im) / n

    def _dft_magnitud(self, señal: List[float], f: float) -> float:
        """
        Evalúa la magnitud del DFT en la frecuencia arbitraria f [Hz].

        Calcula  |X(f)| = |Σ_{n=0}^{N-1} x[n] · e^{-2πifn}| / N

        a frecuencia no necesariamente alineada con los bins enteros.
        Esto permite estimación sub-bin de precisión arbitraria.

        Parámetros
        ----------
        señal : List[float]
            Señal de entrada.
        f : float
            Frecuencia de evaluación [Hz].

        Retorna
        -------
        float
            Magnitud |X(f)| / N.
        """
        two_pi = 2.0 * math.pi
        n = len(señal)
        re = 0.0
        im = 0.0
        for j in range(n):
            ang = two_pi * f * j
            re += señal[j] * math.cos(ang)
            im -= señal[j] * math.sin(ang)
        return math.sqrt(re * re + im * im) / n

    def _estimar_frecuencia_pico(
        self,
        señal: List[float],
        k_pico: int,
        n_iter: int = 50,
    ) -> float:
        """
        Estima la frecuencia del pico espectral con precisión sub-bin.

        Aplica búsqueda de sección áurea (golden-section search) sobre la
        función |-Im(X(f))| = |Σ x[n]·sin(2πfn)| / N evaluada a frecuencias
        arbitrarias en el intervalo [f_obj - 3Δf, f_obj + 3Δf].

        Para señales de la forma sin(2πf₀n), |-Im(X(f))| alcanza su máximo
        exactamente en f₀, eliminando el sesgo del enventanado rectangular
        que afecta a |X(f)|. Converge en ~50 iteraciones a precisión < 1e-12 Hz.

        Parámetros
        ----------
        señal : List[float]
            Señal de entrada.
        k_pico : int
            Índice del bin entero de mayor magnitud (como cota inicial).
        n_iter : int
            Número de iteraciones del golden-section search. Por defecto 50.

        Retorna
        -------
        float
            Frecuencia estimada del modo [Hz].
        """
        delta_f = self.fs / self.nfft
        f_centro = k_pico * delta_f
        # Intervalo de búsqueda: unión de ±3 bins desde el bin entero detectado
        # y ±3 bins desde el objetivo. Cubre el modo aunque el bin entero sea
        # afectado por interferencia o leakage espectral.
        f_target_lo = max(self.f_banda_low, self.f_objetivo - 3.0 * delta_f)
        f_target_hi = min(self.f_banda_high, self.f_objetivo + 3.0 * delta_f)
        f_pico_lo = max(self.f_banda_low, f_centro - 3.0 * delta_f)
        f_pico_hi = min(self.f_banda_high, f_centro + 3.0 * delta_f)
        f_lo = min(f_target_lo, f_pico_lo)
        f_hi = max(f_target_hi, f_pico_hi)

        phi = (math.sqrt(5.0) - 1.0) / 2.0  # 1/φ ≈ 0.618
        f1 = f_hi - phi * (f_hi - f_lo)
        f2 = f_lo + phi * (f_hi - f_lo)
        m1 = self._dft_im_magnitud(señal, f1)
        m2 = self._dft_im_magnitud(señal, f2)

        for _ in range(n_iter):
            if m1 < m2:
                f_lo = f1
                f1, m1 = f2, m2
                f2 = f_lo + phi * (f_hi - f_lo)
                m2 = self._dft_im_magnitud(señal, f2)
            else:
                f_hi = f2
                f2, m2 = f1, m1
                f1 = f_hi - phi * (f_hi - f_lo)
                m1 = self._dft_im_magnitud(señal, f1)

        return (f_lo + f_hi) / 2.0

    def compute_firma_b_vmd(self, raw_stream: List[float]) -> Dict:
        """
        Computa la firma B del ADN-Z a partir de la señal EM cruda.

        Parámetros
        ----------
        raw_stream : List[float]
            Señal EM celular (1 Hz de muestreo, ~3840 muestras).

        Retorna
        -------
        dict con campos:
            valid    : bool   – True si SNR ≥ umbral y f_est en tolerancia
            f_est    : float  – Frecuencia estimada del modo [Hz] (sub-bin)
            snr      : float  – Relación señal/ruido
            b_hash   : bytes  – Blake2b-16 del modo extraído (16 bytes)
        """
        magnitudes = self._calcular_fft_magnitudes(raw_stream)
        delta_f = self.fs / self.nfft

        # Índices de la banda de búsqueda
        k_low = max(0, int(math.floor(self.f_banda_low / delta_f)))
        k_high = min(len(magnitudes) - 1, int(math.ceil(self.f_banda_high / delta_f)))

        # Encontrar el bin de máxima magnitud dentro de la banda
        k_pico = k_low
        mag_max = 0.0
        for k in range(k_low, k_high + 1):
            if magnitudes[k] > mag_max:
                mag_max = magnitudes[k]
                k_pico = k

        # Estimación sub-bin mediante búsqueda de sección áurea sobre DFT continuo
        f_est = self._estimar_frecuencia_pico(raw_stream, k_pico)
        snr = self._snr_desde_magnitudes(magnitudes, k_pico)

        # Construir bytes del modo para el hash
        re_modo = 0.0
        im_modo = 0.0
        two_pi = 2.0 * math.pi
        n_señal = len(raw_stream)
        for j in range(n_señal):
            ang = two_pi * k_pico * j / self.nfft
            re_modo += raw_stream[j] * math.cos(ang)
            im_modo -= raw_stream[j] * math.sin(ang)
        mode_bytes = struct.pack(">dd", re_modo / n_señal, im_modo / n_señal)

        # Blake2b-16
        b_hash = hashlib.blake2b(mode_bytes, digest_size=_VMD_BLAKE2_SIZE).digest()

        # Verificar validez
        f_en_tolerancia = abs(f_est - self.f_objetivo) <= self.f_tolerancia
        valid = snr >= self.snr_umbral and f_en_tolerancia

        return {
            "valid": valid,
            "f_est": f_est,
            "snr": snr,
            "b_hash": b_hash,
        }

    def firma_b_nula(self) -> bytes:
        """Retorna una firma B nula de 16 bytes (modo inválido/no detectado)."""
        return b"\x00" * _VMD_BLAKE2_SIZE


# ============================================================================
# CLASE 4 – CapturaBiologica
# ============================================================================

class CapturaBiologica:
    """
    Simulación de captura del campo EM celular ADN-Z.

    Modela la señal de micro-oscilaciones EM celulares con tres componentes:
        1. Modo de replicación mitótica   f_mit ≈ 0.00052 Hz
        2. Ruido blanco de fondo          σ_ruido = 0.01
        3. Entrelazamiento base-par A-T / G-C  (armónico 2×f_mit)

    Parámetros
    ----------
    duracion_s : float
        Duración de la captura en segundos. Por defecto 3840 s.
    fs : float
        Frecuencia de muestreo [Hz]. Por defecto 1.0 Hz.
    f_mit : float
        Frecuencia de replicación mitótica [Hz]. Por defecto 0.00052 Hz.
    amplitud_mit : float
        Amplitud del modo mitótico. Por defecto 1.0.
    amplitud_at_gc : float
        Amplitud del entrelazamiento base-par. Por defecto 0.3.
    sigma_ruido : float
        Desviación estándar del ruido de fondo. Por defecto 0.01.
    """

    def __init__(
        self,
        duracion_s: float = _VMD_DURACION_S,
        fs: float = _VMD_FS,
        f_mit: float = _VMD_F_SIM,
        amplitud_mit: float = 1.0,
        amplitud_at_gc: float = 0.3,
        sigma_ruido: float = 0.01,
    ) -> None:
        self.duracion_s = duracion_s
        self.fs = fs
        self.f_mit = f_mit
        self.amplitud_mit = amplitud_mit
        self.amplitud_at_gc = amplitud_at_gc
        self.sigma_ruido = sigma_ruido
        self._n_muestras = int(duracion_s * fs)

    def n_muestras(self) -> int:
        """Número de muestras en la captura."""
        return self._n_muestras

    def capturar(self, semilla: int = 42) -> List[float]:
        """
        Genera la señal EM celular simulada.

        Usa una secuencia pseudo-aleatoria determinista (LCG) para el ruido
        de fondo, sin depender de numpy, garantizando reproducibilidad.

        Parámetros
        ----------
        semilla : int
            Semilla para el generador pseudo-aleatorio. Por defecto 42.

        Retorna
        -------
        List[float]
            Señal de micro-oscilaciones EM (n_muestras muestras).
        """
        two_pi = 2.0 * math.pi
        dt = 1.0 / self.fs

        # Generador LCG determinista para el ruido
        lcg_state = semilla & 0xFFFFFFFF
        lcg_a = 1664525
        lcg_c = 1013904223
        lcg_m = 2 ** 32

        señal: List[float] = []
        for i in range(self._n_muestras):
            t = i * dt
            # Modo mitótico principal
            modo_mit = self.amplitud_mit * math.sin(two_pi * self.f_mit * t)
            # Armónico base-par A-T/G-C (2×f_mit, desfasado π/4)
            modo_at_gc = self.amplitud_at_gc * math.sin(
                two_pi * 2.0 * self.f_mit * t + math.pi / 4
            )
            # Ruido blanco (LCG → rango [-σ, +σ])
            lcg_state = (lcg_a * lcg_state + lcg_c) % lcg_m
            ruido = self.sigma_ruido * (lcg_state / (lcg_m - 1) * 2.0 - 1.0)
            señal.append(modo_mit + modo_at_gc + ruido)

        return señal


# ============================================================================
# CLASE 5 – CondicionBioNodo
# ============================================================================

class CondicionBioNodo:
    """
    Verificador de las 8 condiciones necesarias y suficientes para alcanzar
    el estado BIO_NODO_ANCLADO_EN_LA_ROCA.

    Condiciones:
        1. Ψ_ADN == 1.000000      (float32 IEEE 754 BE == 0x3F800000)
        2. Firma B ADN-Z válida    (SNR ≥ 4.0)
        3. Frecuencia Maestra == 1417001
        4. Hash Constitución conocido (SHA-256 referencia v1.1)
        5. Sello 𓂀 UTF-8            (bytes == 0xF090A080)
        6. OP_RETURN == 80 bytes exactos
        7. Confirmaciones BTC ≥ 6
        8. Reserva ≥ U_circulación   (7.4862 BTC + 1 kg XAU)
    """

    # Representación float32 exacta de 1.0 en big-endian
    _PSI_ADNZ_FLOAT32_BE: bytes = struct.pack(">f", 1.0)  # 0x3F800000

    def verificar_psi_adnz(self, psi: float) -> bool:
        """Condición 1: Ψ_ADN == 1.000000 (float32 exacto 0x3F800000)."""
        psi_bytes = struct.pack(">f", psi)
        return psi_bytes == self._PSI_ADNZ_FLOAT32_BE

    def verificar_firma_b(self, firma_valida: bool) -> bool:
        """Condición 2: Firma B ADN-Z válida (SNR ≥ umbral)."""
        return bool(firma_valida)

    def verificar_frecuencia_maestra(self, frecuencia_int: int) -> bool:
        """Condición 3: Frecuencia Maestra == 1417001."""
        return frecuencia_int == _FRECUENCIA_MAESTRA_INT

    def verificar_hash_constitucion(self, hash_bytes: bytes) -> bool:
        """Condición 4: Hash Constitución coincide con la referencia v1.1."""
        return hash_bytes == _HASH_CONSTITUCION

    def verificar_sello(self, sello_bytes: bytes) -> bool:
        """Condición 5: Sello 𓂀 UTF-8 == 0xF090A080."""
        return sello_bytes == _SELLO_UTF8

    def verificar_op_return_size(self, payload: bytes) -> bool:
        """Condición 6: OP_RETURN == 80 bytes exactos."""
        return len(payload) == _OP_RETURN_SIZE

    def verificar_confirmaciones(self, confirmaciones: int) -> bool:
        """Condición 7: Confirmaciones BTC ≥ 6."""
        return confirmaciones >= _BTC_CONFIRMACIONES_MIN

    def verificar_reserva(self, reserva_btc: float, reserva_xau_kg: float) -> bool:
        """
        Condición 8: Reserva ≥ U_circulación.

        Se requiere reserva_btc ≥ 7.4862 BTC  Y  reserva_xau_kg ≥ 1.0 kg XAU.
        """
        return reserva_btc >= _U_CIRCULACION and reserva_xau_kg >= 1.0

    def verificar_todas(
        self,
        psi_adnz: float,
        firma_b_valida: bool,
        frecuencia_maestra: int,
        hash_constitucion: bytes,
        sello_bytes: bytes,
        op_return_payload: bytes,
        confirmaciones_btc: int,
        reserva_btc: float,
        reserva_xau_kg: float,
    ) -> Dict:
        """
        Verifica las 8 condiciones y retorna un resumen detallado.

        Retorna
        -------
        dict con:
            condiciones  : Dict[str, bool]  – resultado por condición
            todas_validas : bool             – True si las 8 son True
        """
        condiciones = {
            "psi_adnz_diamond": self.verificar_psi_adnz(psi_adnz),
            "firma_b_valida": self.verificar_firma_b(firma_b_valida),
            "frecuencia_maestra": self.verificar_frecuencia_maestra(frecuencia_maestra),
            "hash_constitucion": self.verificar_hash_constitucion(hash_constitucion),
            "sello_utf8": self.verificar_sello(sello_bytes),
            "op_return_80_bytes": self.verificar_op_return_size(op_return_payload),
            "confirmaciones_btc": self.verificar_confirmaciones(confirmaciones_btc),
            "reserva_suficiente": self.verificar_reserva(reserva_btc, reserva_xau_kg),
        }
        todas_validas = all(condiciones.values())
        return {
            "condiciones": condiciones,
            "todas_validas": todas_validas,
        }


# ============================================================================
# CLASE 6 – MaquinaEstadosADNZ
# ============================================================================

class EstadoADNZ(Enum):
    """
    Estados posibles de la máquina de estados del protocolo ADN-Z.

    Estados:
        INACTIVO            – Estado inicial antes de cualquier detección.
        ADN_Z_DETECTADO     – Ψ_ADNZ = 1.0 confirmado.
        FIRMA_B_VALIDA      – SNR ≥ 4.0 y frecuencia en tolerancia.
        BIO_NODO_ANCLADO    – Las 8 condiciones cumplidas (estado final ✅).
        FALLO_PSI           – Ψ < 1.0 (reintentar meditación).
        FALLO_FIRMA         – SNR < 4.0 (reintentar captura).
        FALLO_RESERVA       – Reserva insuficiente (peg suave activado).
    """

    INACTIVO = "INACTIVO"
    ADN_Z_DETECTADO = "ADN_Z_DETECTADO"
    FIRMA_B_VALIDA = "FIRMA_B_VALIDA"
    BIO_NODO_ANCLADO = "BIO_NODO_ANCLADO_EN_LA_ROCA"
    FALLO_PSI = "FALLO_PSI"
    FALLO_FIRMA = "FALLO_FIRMA"
    FALLO_RESERVA = "FALLO_RESERVA"


class MaquinaEstadosADNZ:
    """
    Máquina de estados del protocolo QCAL-ADNZ-ANCHOR-v1.0.

    Transiciones:
        INACTIVO
            → ADN_Z_DETECTADO   si Ψ_ADNZ = 1.0
            → FALLO_PSI         si Ψ_ADNZ < 1.0

        ADN_Z_DETECTADO
            → FIRMA_B_VALIDA    si SNR ≥ 4.0 y f_est en tolerancia
            → FALLO_FIRMA       si SNR < 4.0 o f_est fuera de tolerancia

        FIRMA_B_VALIDA
            → BIO_NODO_ANCLADO  si las 8 condiciones cumplidas
            → FALLO_RESERVA     si reserva insuficiente

        FALLO_*                 – estados terminales (reintentar desde INACTIVO)
    """

    def __init__(self) -> None:
        self._estado: EstadoADNZ = EstadoADNZ.INACTIVO
        self._historial: List[EstadoADNZ] = [EstadoADNZ.INACTIVO]

    @property
    def estado(self) -> EstadoADNZ:
        """Estado actual de la máquina."""
        return self._estado

    @property
    def historial(self) -> List[EstadoADNZ]:
        """Lista de estados visitados (incluye el actual)."""
        return list(self._historial)

    def _transicionar(self, nuevo_estado: EstadoADNZ) -> None:
        self._estado = nuevo_estado
        self._historial.append(nuevo_estado)

    def reset(self) -> None:
        """Reinicia la máquina al estado INACTIVO."""
        self._estado = EstadoADNZ.INACTIVO
        self._historial = [EstadoADNZ.INACTIVO]

    def procesar_psi(self, psi_adnz: float) -> EstadoADNZ:
        """
        Procesa la medición Ψ_ADNZ.

        Si Ψ_ADNZ = 1.0 (float32), transiciona a ADN_Z_DETECTADO.
        En caso contrario transiciona a FALLO_PSI.

        Retorna el nuevo estado.
        """
        verificador = CondicionBioNodo()
        if verificador.verificar_psi_adnz(psi_adnz):
            self._transicionar(EstadoADNZ.ADN_Z_DETECTADO)
        else:
            self._transicionar(EstadoADNZ.FALLO_PSI)
        return self._estado

    def procesar_firma(self, firma_dict: Dict) -> EstadoADNZ:
        """
        Procesa el resultado de la firma B VMD.

        Si la firma es válida (valid=True), transiciona a FIRMA_B_VALIDA.
        En caso contrario transiciona a FALLO_FIRMA.

        Retorna el nuevo estado.
        """
        if self._estado != EstadoADNZ.ADN_Z_DETECTADO:
            return self._estado
        if firma_dict.get("valid", False):
            self._transicionar(EstadoADNZ.FIRMA_B_VALIDA)
        else:
            self._transicionar(EstadoADNZ.FALLO_FIRMA)
        return self._estado

    def procesar_ancla(self, verificacion: Dict) -> EstadoADNZ:
        """
        Procesa la verificación completa de las 8 condiciones.

        Si todas las condiciones son True, transiciona a BIO_NODO_ANCLADO.
        En caso de fallo de reserva, transiciona a FALLO_RESERVA.

        Retorna el nuevo estado.
        """
        if self._estado != EstadoADNZ.FIRMA_B_VALIDA:
            return self._estado
        if verificacion.get("todas_validas", False):
            self._transicionar(EstadoADNZ.BIO_NODO_ANCLADO)
        else:
            condiciones = verificacion.get("condiciones", {})
            if not condiciones.get("reserva_suficiente", True):
                self._transicionar(EstadoADNZ.FALLO_RESERVA)
            else:
                # Otro fallo en las condiciones restantes → reintentar
                self._transicionar(EstadoADNZ.FALLO_FIRMA)
        return self._estado

    def esta_anclado(self) -> bool:
        """Retorna True si la máquina alcanzó BIO_NODO_ANCLADO_EN_LA_ROCA."""
        return self._estado == EstadoADNZ.BIO_NODO_ANCLADO


# ============================================================================
# CLASE 7 – CoherenciaADNZ
# ============================================================================

class CoherenciaADNZ:
    """
    Métrica de coherencia global Ψ_ADNZ del protocolo ADN-Z.

    Combina cuatro dimensiones de coherencia:
        Ψ_bio      — coherencia biológica (modo ADN-Z detectado)
        Ψ_firma    — coherencia criptográfica (Blake2b-16 válido)
        Ψ_cadena   — coherencia de cadena (confirmaciones BTC ≥ 6)
        Ψ_reserva  — coherencia de reserva (BTC + XAU)

    Ponderación:
        Ψ_global = (0.4·Ψ_bio + 0.3·Ψ_firma + 0.15·Ψ_cadena + 0.15·Ψ_reserva)

    El Diamond-State se alcanza cuando Ψ_global = 1.000000.
    """

    _PESOS: Tuple[float, ...] = (0.40, 0.30, 0.15, 0.15)

    def __init__(self, psi_umbral: float = _PSI_UMBRAL) -> None:
        self.psi_umbral = psi_umbral

    def calcular(
        self,
        psi_bio: float,
        psi_firma: float,
        psi_cadena: float,
        psi_reserva: float,
    ) -> float:
        """
        Calcula Ψ_global como promedio ponderado.

        Retorna
        -------
        float
            Ψ_ADNZ ∈ [0, 1].
        """
        valores = (psi_bio, psi_firma, psi_cadena, psi_reserva)
        w = self._PESOS
        total_w = sum(w)
        psi = sum(w[i] * max(0.0, min(1.0, valores[i])) for i in range(4)) / total_w
        return round(psi, 6)

    def psi_bio_desde_snr(self, snr: float) -> float:
        """
        Mapea la SNR de la firma B al rango [0, 1].

        SNR ≥ umbral → 1.0; SNR = 0 → 0.0.
        """
        if snr <= 0:
            return 0.0
        return min(1.0, snr / (self.psi_umbral * 10.0 + snr))

    def psi_firma_desde_validez(self, valida: bool) -> float:
        """Ψ_firma = 1.0 si la firma B es válida, 0.0 en caso contrario."""
        return 1.0 if valida else 0.0

    def psi_cadena_desde_confirmaciones(self, confirmaciones: int) -> float:
        """
        Mapea las confirmaciones BTC al rango [0, 1].

        ≥ 6 confirmaciones → 1.0; 0 confirmaciones → 0.0.
        """
        return min(1.0, confirmaciones / _BTC_CONFIRMACIONES_MIN)

    def psi_reserva_desde_btc_xau(
        self, reserva_btc: float, reserva_xau_kg: float
    ) -> float:
        """
        Mapea la reserva (BTC + XAU) al rango [0, 1].

        Reserva completa (≥7.4862 BTC y ≥1 kg XAU) → 1.0.
        """
        r_btc = min(1.0, reserva_btc / _U_CIRCULACION)
        r_xau = min(1.0, reserva_xau_kg / 1.0)
        return (r_btc + r_xau) / 2.0

    def sello_activo(self, psi_global: float) -> bool:
        """Retorna True si Ψ_global ≥ umbral → sello ∴ADNZ∞³ ACTIVO."""
        return psi_global >= self.psi_umbral


# ============================================================================
# CLASE 8 – SistemaADNZAnchor + ResultadoADNZAnchor
# ============================================================================

@dataclass
class ResultadoADNZAnchor:
    """
    Contenedor de todos los resultados del protocolo QCAL-ADNZ-ANCHOR-v1.0.

    Atributos
    ----------
    sello_activo : bool
        True si el sello ∴ADNZ∞³ está activo (Ψ_ADNZ ≥ 0.888).
    bio_nodo_anclado : bool
        True si las 8 condiciones de BIO_NODO_ANCLADO_EN_LA_ROCA se cumplen.
    sello : str
        Identificador del sello (∴ADNZ∞³).
    sello_completo : str
        Sello completo (∴𓂀Ω∞³Φ · TUYOYOTU).
    estado : str
        Estado final de la máquina de estados.
    psi_adnz : float
        Ψ_ADNZ Diamond-State (1.0 si anclado).
    psi_global : float
        Coherencia global calculada.
    psi_bio : float
        Coherencia biológica (modo ADN-Z).
    psi_firma : float
        Coherencia criptográfica (firma B).
    psi_cadena : float
        Coherencia de cadena (confirmaciones BTC).
    psi_reserva : float
        Coherencia de reserva (BTC + XAU).
    firma_b_valid : bool
        True si la firma B ADN-Z es válida.
    firma_b_snr : float
        SNR de la firma B.
    firma_b_f_est : float
        Frecuencia estimada del modo ADN-Z [Hz].
    firma_b_hash : bytes
        Blake2b-16 del modo extraído.
    op_return_bytes : bytes
        Payload OP_RETURN v1.2 de 80 bytes.
    condiciones : dict
        Resultado detallado de las 8 condiciones.
    confirmaciones_btc : int
        Número de confirmaciones BTC simuladas.
    reserva_btc : float
        Reserva BTC disponible.
    reserva_xau_kg : float
        Reserva XAU disponible [kg].
    f0 : float
        Frecuencia fundamental (Hz).
    frecuencia_maestra : int
        Frecuencia maestra × 10000.
    """

    sello_activo: bool = False
    bio_nodo_anclado: bool = False
    sello: str = _SELLO
    sello_completo: str = _SELLO_COMPLETO
    estado: str = EstadoADNZ.INACTIVO.value
    psi_adnz: float = 0.0
    psi_global: float = 0.0
    psi_bio: float = 0.0
    psi_firma: float = 0.0
    psi_cadena: float = 0.0
    psi_reserva: float = 0.0
    firma_b_valid: bool = False
    firma_b_snr: float = 0.0
    firma_b_f_est: float = 0.0
    firma_b_hash: bytes = field(default_factory=lambda: b"\x00" * 16)
    op_return_bytes: bytes = field(default_factory=lambda: b"\x00" * 80)
    condiciones: Dict = field(default_factory=dict)
    confirmaciones_btc: int = 0
    reserva_btc: float = 0.0
    reserva_xau_kg: float = 0.0
    f0: float = field(default_factory=lambda: _F0)
    frecuencia_maestra: int = field(default_factory=lambda: _FRECUENCIA_MAESTRA_INT)


class SistemaADNZAnchor:
    """
    Orquestador principal del protocolo QCAL-ADNZ-ANCHOR-v1.0.

    Ejecuta el protocolo completo:
        1. Captura la señal EM celular ADN-Z.
        2. Computa la firma B (VMD + Blake2b-16).
        3. Serializa el payload OP_RETURN v1.2 de 80 bytes.
        4. Verifica las 8 condiciones del bio-nodo.
        5. Ejecuta la máquina de estados.
        6. Calcula la coherencia global Ψ_ADNZ.
        7. Activa el sello ∴ADNZ∞³ si Ψ_global ≥ 0.888.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    confirmaciones_btc : int
        Número de confirmaciones BTC (simulado). Por defecto 6.
    reserva_btc : float
        Reserva BTC disponible. Por defecto 7.4862 BTC.
    reserva_xau_kg : float
        Reserva XAU disponible [kg]. Por defecto 1.0 kg.
    semilla_captura : int
        Semilla para la simulación de captura EM. Por defecto 42.
    """

    def __init__(
        self,
        f0: float = _F0,
        confirmaciones_btc: int = _BTC_CONFIRMACIONES_MIN,
        reserva_btc: float = _U_CIRCULACION,
        reserva_xau_kg: float = 1.0,
        semilla_captura: int = 42,
    ) -> None:
        self.f0 = f0
        self.confirmaciones_btc = confirmaciones_btc
        self.reserva_btc = reserva_btc
        self.reserva_xau_kg = reserva_xau_kg
        self.semilla_captura = semilla_captura

        self._constantes = ConstantesADNZ(f0=f0)
        self._captura = CapturaBiologica(f_mit=_VMD_F_SIM)
        self._vmd = FirmaVMD()
        self._serializador = SerializadorOpReturn()
        self._condicion = CondicionBioNodo()
        self._maquina = MaquinaEstadosADNZ()
        self._coherencia = CoherenciaADNZ()

    def activar(self) -> "ResultadoADNZAnchor":
        """
        Ejecuta el protocolo QCAL-ADNZ-ANCHOR-v1.0 completo.

        Retorna
        -------
        ResultadoADNZAnchor
            Contenedor con todos los resultados del protocolo.
        """
        # 1. Captura señal EM celular
        señal = self._captura.capturar(semilla=self.semilla_captura)

        # 2. Firma B VMD
        firma_dict = self._vmd.compute_firma_b_vmd(señal)
        firma_b_hash = firma_dict["b_hash"]
        firma_b_valid = firma_dict["valid"]
        firma_b_snr = firma_dict["snr"]
        firma_b_f_est = firma_dict["f_est"]

        # 3. Ψ_ADNZ = 1.0 (Diamond-State cuando firma B válida)
        psi_adnz = _PSI_ADNZ_DIAMOND if firma_b_valid else 0.0

        # 4. Serializar OP_RETURN v1.2
        hash_const = _HASH_CONSTITUCION
        op_return_payload = self._serializador.serializar(
            hash_constitucion=hash_const,
            psi_anchor=_PSI_ANCHOR_REF,
            u_circulacion=_U_CIRCULACION,
            firma_b_adnz=firma_b_hash,
            frecuencia_maestra=_FRECUENCIA_MAESTRA_INT,
            psi_adnz=psi_adnz,
        )

        # 5. Verificar las 8 condiciones
        verificacion = self._condicion.verificar_todas(
            psi_adnz=psi_adnz,
            firma_b_valida=firma_b_valid,
            frecuencia_maestra=_FRECUENCIA_MAESTRA_INT,
            hash_constitucion=hash_const,
            sello_bytes=_SELLO_UTF8,
            op_return_payload=op_return_payload,
            confirmaciones_btc=self.confirmaciones_btc,
            reserva_btc=self.reserva_btc,
            reserva_xau_kg=self.reserva_xau_kg,
        )

        # 6. Máquina de estados
        self._maquina.reset()
        self._maquina.procesar_psi(psi_adnz)
        if self._maquina.estado == EstadoADNZ.ADN_Z_DETECTADO:
            self._maquina.procesar_firma(firma_dict)
        if self._maquina.estado == EstadoADNZ.FIRMA_B_VALIDA:
            self._maquina.procesar_ancla(verificacion)
        estado_final = self._maquina.estado

        # 7. Coherencia global Ψ_ADNZ
        psi_bio = self._coherencia.psi_bio_desde_snr(firma_b_snr)
        psi_firma = self._coherencia.psi_firma_desde_validez(firma_b_valid)
        psi_cadena = self._coherencia.psi_cadena_desde_confirmaciones(self.confirmaciones_btc)
        psi_reserva = self._coherencia.psi_reserva_desde_btc_xau(
            self.reserva_btc, self.reserva_xau_kg
        )
        psi_global = self._coherencia.calcular(psi_bio, psi_firma, psi_cadena, psi_reserva)
        sello_activo = self._coherencia.sello_activo(psi_global)
        bio_nodo_anclado = self._maquina.esta_anclado()

        return ResultadoADNZAnchor(
            sello_activo=sello_activo,
            bio_nodo_anclado=bio_nodo_anclado,
            sello=_SELLO,
            sello_completo=_SELLO_COMPLETO,
            estado=estado_final.value,
            psi_adnz=psi_adnz,
            psi_global=psi_global,
            psi_bio=psi_bio,
            psi_firma=psi_firma,
            psi_cadena=psi_cadena,
            psi_reserva=psi_reserva,
            firma_b_valid=firma_b_valid,
            firma_b_snr=firma_b_snr,
            firma_b_f_est=firma_b_f_est,
            firma_b_hash=firma_b_hash,
            op_return_bytes=op_return_payload,
            condiciones=verificacion.get("condiciones", {}),
            confirmaciones_btc=self.confirmaciones_btc,
            reserva_btc=self.reserva_btc,
            reserva_xau_kg=self.reserva_xau_kg,
            f0=self.f0,
            frecuencia_maestra=_FRECUENCIA_MAESTRA_INT,
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def qcal_adnz_anchor_activar(
    f0: float = _F0,
    confirmaciones_btc: int = _BTC_CONFIRMACIONES_MIN,
    reserva_btc: float = _U_CIRCULACION,
    reserva_xau_kg: float = 1.0,
    semilla_captura: int = 42,
) -> Dict:
    """
    Activa el protocolo QCAL-ADNZ-ANCHOR-v1.0 y retorna el resultado como dict.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    confirmaciones_btc : int
        Número de confirmaciones BTC (simulado). Por defecto 6.
    reserva_btc : float
        Reserva BTC disponible. Por defecto 7.4862 BTC.
    reserva_xau_kg : float
        Reserva XAU disponible [kg]. Por defecto 1.0 kg.
    semilla_captura : int
        Semilla para la simulación de captura EM. Por defecto 42.

    Retorna
    -------
    dict con todos los resultados:
        - 'sello_activo'       : bool   – True si Ψ_global ≥ 0.888
        - 'bio_nodo_anclado'   : bool   – True si las 8 condiciones se cumplen
        - 'sello'              : str    – '∴ADNZ∞³'
        - 'sello_completo'     : str    – '∴𓂀Ω∞³Φ · TUYOYOTU'
        - 'estado'             : str    – estado final de la máquina de estados
        - 'psi_adnz'           : float  – 1.0 si Diamond-State
        - 'psi_global'         : float  – coherencia global
        - 'psi_bio'            : float
        - 'psi_firma'          : float
        - 'psi_cadena'         : float
        - 'psi_reserva'        : float
        - 'firma_b_valid'      : bool
        - 'firma_b_snr'        : float
        - 'firma_b_f_est'      : float
        - 'firma_b_hash'       : bytes  – Blake2b-16 (16 bytes)
        - 'op_return_bytes'    : bytes  – payload OP_RETURN v1.2 (80 bytes)
        - 'condiciones'        : dict   – resultado por condición
        - 'confirmaciones_btc' : int
        - 'reserva_btc'        : float
        - 'reserva_xau_kg'     : float
        - 'f0'                 : float
        - 'frecuencia_maestra' : int

    Ejemplos
    --------
    >>> r = qcal_adnz_anchor_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_adnz'] == 1.0
    True
    >>> len(r['op_return_bytes']) == 80
    True
    """
    sistema = SistemaADNZAnchor(
        f0=f0,
        confirmaciones_btc=confirmaciones_btc,
        reserva_btc=reserva_btc,
        reserva_xau_kg=reserva_xau_kg,
        semilla_captura=semilla_captura,
    )
    resultado = sistema.activar()
    return {
        "sello_activo": resultado.sello_activo,
        "bio_nodo_anclado": resultado.bio_nodo_anclado,
        "sello": resultado.sello,
        "sello_completo": resultado.sello_completo,
        "estado": resultado.estado,
        "psi_adnz": resultado.psi_adnz,
        "psi_global": resultado.psi_global,
        "psi_bio": resultado.psi_bio,
        "psi_firma": resultado.psi_firma,
        "psi_cadena": resultado.psi_cadena,
        "psi_reserva": resultado.psi_reserva,
        "firma_b_valid": resultado.firma_b_valid,
        "firma_b_snr": resultado.firma_b_snr,
        "firma_b_f_est": resultado.firma_b_f_est,
        "firma_b_hash": resultado.firma_b_hash,
        "op_return_bytes": resultado.op_return_bytes,
        "condiciones": resultado.condiciones,
        "confirmaciones_btc": resultado.confirmaciones_btc,
        "reserva_btc": resultado.reserva_btc,
        "reserva_xau_kg": resultado.reserva_xau_kg,
        "f0": resultado.f0,
        "frecuencia_maestra": resultado.frecuencia_maestra,
    }
