#!/usr/bin/env python3
"""
QCalExternalValidator — Verificador independiente de integridad Merkle
Solo biblioteca estándar. Cualquier auditor externo puede ejecutarlo.
"""

import hashlib
import hmac
import json
from typing import List, Dict, Any

class QCalExternalValidator:
    def __init__(self, secret_key: bytes = b"QCAL_SYMBIO_SECRET_2026"):
        self.secret_key = secret_key

    def _compute_hmac(self, data_str: str) -> str:
        return hmac.new(self.secret_key, data_str.encode('utf-8'), hashlib.sha256).hexdigest()

    def rebuild_merkle_root(self, audit_trail: List[Dict[str, Any]]) -> str:
        if not audit_trail:
            raise ValueError("El registro de auditoría está vacío.")

        leaf_hashes = []
        for record in audit_trail:
            payload_str = json.dumps(record, sort_keys=True, default=str)
            leaf_hash = self._compute_hmac(payload_str)
            leaf_hashes.append(leaf_hash)

        current_level = leaf_hashes
        while len(current_level) > 1:
            next_level = []
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1])
            for i in range(0, len(current_level), 2):
                combined = current_level[i] + current_level[i+1]
                next_level.append(self._compute_hmac(combined))
            current_level = next_level

        return current_level[0]
