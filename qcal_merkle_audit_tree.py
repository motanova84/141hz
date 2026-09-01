#!/usr/bin/env python3
"""
QCalMerkleAuditTree — Árbol de Merkle de Auditoría Dual
Registra de forma inmutable tanto bloques PASSED como VETOED.
Impide el p-hacking: eliminar un veto cambia la raíz.
"""

import hashlib
import hmac
import time
import json
import numpy as np
from typing import List, Dict, Tuple, Any, Optional

class MerkleAuditNode:
    def __init__(self, hash_value: str, metadata: Dict[str, Any]):
        self.hash_value = hash_value
        self.metadata = metadata

class QCalMerkleAuditTree:
    def __init__(self, secret_key: bytes = b"QCAL_SYMBIO_SECRET_2026"):
        self.secret_key = secret_key
        self.leaves: List[MerkleAuditNode] = []
        self.root_hash: str = ""

    def _compute_hmac(self, data_str: str) -> str:
        return hmac.new(self.secret_key, data_str.encode('utf-8'), hashlib.sha256).hexdigest()

    def append_block(
        self,
        block_id: int,
        quantum_data: Optional[np.ndarray],
        veto_result: Tuple[bool, str, Dict],
        biometrics: Optional[Dict] = None
    ):
        is_valid, reason, veto_meta = veto_result
        
        payload = {
            "block_id": block_id,
            "timestamp": time.time(),
            "status": "PASSED" if is_valid else "VETOED",
            "reason": reason,
            "veto_metrics": {k: (float(v) if isinstance(v, (np.floating, float)) else v) 
                            for k, v in veto_meta.items()},
            "quantum_data_hash": hashlib.sha256(quantum_data.tobytes()).hexdigest() if (is_valid and quantum_data is not None) else None,
            "biometric_telemetry": biometrics or {}
        }
        
        payload_str = json.dumps(payload, sort_keys=True, default=str)
        leaf_hash = self._compute_hmac(payload_str)
        
        self.leaves.append(MerkleAuditNode(hash_value=leaf_hash, metadata=payload))

    def build_tree(self) -> str:
        if not self.leaves:
            return ""
        
        current_level_hashes = [leaf.hash_value for leaf in self.leaves]
        
        while len(current_level_hashes) > 1:
            next_level_hashes = []
            if len(current_level_hashes) % 2 != 0:
                current_level_hashes.append(current_level_hashes[-1])
                
            for i in range(0, len(current_level_hashes), 2):
                combined_str = current_level_hashes[i] + current_level_hashes[i+1]
                combined_hash = self._compute_hmac(combined_str)
                next_level_hashes.append(combined_hash)
                
            current_level_hashes = next_level_hashes
            
        self.root_hash = current_level_hashes[0]
        return self.root_hash

    def export_audit_trail(self) -> List[Dict]:
        return [leaf.metadata for leaf in self.leaves]
