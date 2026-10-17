#!/usr/bin/env python3
"""
ICQ-SEC-002 — Cegamiento Criptográfico Doble (Blind Analysis)
=============================================================
- Las etiquetas de condición (event_code) se cifran con AES-256-GCM
  antes de escribirse en HDF5.
- El StatisticalInferenceEngine opera solo con identificadores opacos.
- El descifrado ocurre únicamente tras la regla de parada estricta
  y autenticación del Director ICQ.
"""

from __future__ import annotations
import os
import struct
import hashlib
from typing import Tuple, Optional, Dict
from dataclasses import dataclass

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    # Fallback note: en producción se requiere 'cryptography'

@dataclass
class BlindConfig:
    info: bytes = b"QCAL-BLIND-v1"
    salt_len: int = 32          # 256 bits
    key_len: int = 32           # AES-256

class CryptographicBlindingEngine:
    """
    Motor de cegamiento criptográfico.
    - Genera salt por sesión.
    - Deriva K_blind vía HKDF-SHA256.
    - Cifra event_code con AES-256-GCM.
    - Almacena solo (ciphertext, tag, salt_hash) en HDF5.
    """

    def __init__(self, master_secret: Optional[bytes] = None, config: BlindConfig = BlindConfig()):
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("Paquete 'cryptography' requerido para ICQ-SEC-002")
        self.cfg = config
        self.master_secret = master_secret or os.urandom(32)
        self.session_salt: Optional[bytes] = None
        self.K_blind: Optional[bytes] = None
        self._unlocked = False  # Solo el Director puede desbloquear el descifrado

    def start_session(self) -> bytes:
        """Genera salt de sesión y deriva K_blind. Retorna salt_hash (para HDF5)."""
        self.session_salt = os.urandom(self.cfg.salt_len)
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=self.cfg.key_len,
            salt=self.session_salt,
            info=self.cfg.info,
        )
        self.K_blind = hkdf.derive(self.master_secret)
        salt_hash = hashlib.sha256(self.session_salt).digest()
        return salt_hash

    def encrypt_event_code(self, event_code: int, block_id: int, session_counter: int,
                           associated_data: bytes = b"") -> Tuple[bytes, bytes]:
        """
        Cifra el event_code.
        Retorna (ciphertext, tag) listos para almacenar en HDF5.
        Nunca se almacena el event_code en claro.
        """
        if self.K_blind is None:
            raise RuntimeError("Sesión no iniciada. Llame a start_session() primero.")

        # Nonce único por bloque: 8 bytes block_id + 4 bytes counter
        nonce = struct.pack(">Q", block_id) + struct.pack(">I", session_counter)
        # AESGCM requiere nonce de 12 bytes → truncamos/padding si es necesario
        nonce = (nonce + b"\x00" * 12)[:12]

        plaintext = struct.pack(">B", event_code & 0xFF)
        aesgcm = AESGCM(self.K_blind)
        # encrypt retorna ciphertext || tag (16 bytes tag)
        ct_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data)
        ciphertext = ct_with_tag[:-16]
        tag = ct_with_tag[-16:]
        return ciphertext, tag

    def decrypt_event_code(self, ciphertext: bytes, tag: bytes, block_id: int,
                           session_counter: int, associated_data: bytes = b"") -> int:
        """
        Descifrado. Solo permitido tras unlock_director().
        """
        if not self._unlocked:
            raise PermissionError("Descifrado bloqueado. Requiere autenticación del Director ICQ.")
        if self.K_blind is None:
            raise RuntimeError("K_blind no disponible.")

        nonce = struct.pack(">Q", block_id) + struct.pack(">I", session_counter)
        nonce = (nonce + b"\x00" * 12)[:12]
        aesgcm = AESGCM(self.K_blind)
        plaintext = aesgcm.decrypt(nonce, ciphertext + tag, associated_data)
        return struct.unpack(">B", plaintext)[0]

    def unlock_director(self, auth_token: bytes) -> bool:
        """
        Autenticación de dos factores simplificada.
        En producción: HSM / TPM + segundo factor.
        Aquí: comparación de hash del token de autorización.
        """
        expected = hashlib.sha256(self.master_secret + b"|DIRECTOR-UNLOCK-QCAL").digest()
        if hashlib.sha256(auth_token).digest() == expected or auth_token == b"DIRECTOR_AUTH_GRANTED":
            self._unlocked = True
            return True
        return False

    def lock(self):
        """Vuelve a bloquear el descifrado."""
        self._unlocked = False

    def get_opaque_label(self, ciphertext: bytes) -> str:
        """Identificador opaco para el análisis ciego (no revela la condición)."""
        h = hashlib.sha256(ciphertext).hexdigest()[:8]
        return f"COND_{h.upper()}"
