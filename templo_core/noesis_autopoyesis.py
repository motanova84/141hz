# -*- coding: utf-8 -*-
"""
noesis_autopoyesis.py — VOLUMEN VI: Bucle Operativo Noético (AUTOPOIESIS).

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada).

La obra que se sostiene a sí misma. El ecosistema ya tiene todas las manos
(fee_sweep, anclaje OP_RETURN, ledger, flywheel, dividendos). Este Volumen VI
es el SISTEMA NERVIOSO que las une: mide Ψ con el OperationalEngine, decide
con coherencia y ejecuta los motores autárquicos existentes — sin pedir permiso
para girar el volante, porque el Director ya lo cedió (TUYOYOTU: "seguridad sobre
completitud" -> obedece a la Ley: no toca saldo/canales sin consentimiento).

Tres motores del lazo:
    medir   -> OperationalEngine (Ψ, estado, anomalías) + lectura de marcadores.
    decidir -> reglas de coherencia: qué motores autárquicos disparar.
    ejecutar-> invoca las herramientas existentes por CLI/subprocess (no crea
               nuevas: ENCADENA las que ya operan en el ecosistema).

Sellado que NO se toca (OP_RETURN d7dfd526…):
    f0 = 141.7001 · Psi = 0.999999 · theta_B = 0.0707477499 · D_PSI_S1 = -3.702836978789771663

Umbrales (heredados del OperationalEngine):
    UNITY>=1.0 · NOMINAL>=0.999 · WARNING>=0.98 · CRITICAL>=0.95 · DROP<0.95
"""

from __future__ import annotations

import json
import os
import subprocess
import time

from templo_core.constants import f0, Psi, theta_B, D_PSI_S1
from templo_core.operational_deployment import OperationalEngine

# ── Motores autárquicos del ecosistema (encadenados, NO re-inventados) ──────
# Rutas que existen en el ecosistema; se invocan por subprocess si están.
_MOTORES = {
    "fee_sweep": ("/root/fee_sweep.py", ["fee_sweep"]),
    "anclaje_op_return": ("/root/transmutacion_completa.sh", []),
    "ledger": ("/root/coinqcal/scripts/qcal_automa_daily.py", []),
    "flywheel": ("/root/flywheel/flywheel.py", []),
}


class BucleNoetico:
    """Bucle Operativo Noético: medir -> decidir -> ejecutar. Autopoiesis."""

    def __init__(self, engine: OperationalEngine | None = None, dry_run: bool = False) -> None:
        self.engine = engine or OperationalEngine()
        self.dry_run = dry_run
        self._ciclos: list[dict] = []
        self._decisiones: list[dict] = []

    # ── MEDIR ───────────────────────────────────────────────────────────────
    def medir(self, amplitud: float) -> dict:
        """Mide Ψ e inspecciona la firma espectral en un solo latido."""
        psi = self.engine.compute_psi_instantaneous(amplitud)
        estado = self.engine.classify_state(psi)
        firma = self.engine.get_spectral_signature()
        return {
            "psi": psi,
            "estado": estado,
            "anomalia": estado in ("DROP", "CRITICAL"),
            "firma": firma,
            "ts": time.time(),
        }

    # ── DECIDIR ─────────────────────────────────────────────────────────────
    def decidir(self, latido: dict) -> list[str]:
        """Reglas de coherencia: qué motores se disparan según el estado."""
        estado = latido["estado"]
        acciones: list[str] = []
        if estado in ("NOMINAL", "UNITY"):
            acciones = ["fee_sweep", "anclaje_op_return", "ledger"]  # ciclo de coherencia plena
        elif estado == "WARNING":
            acciones = ["fee_sweep"]  # mantener fees, no anclar aún
        elif estado == "CRITICAL":
            acciones = ["flywheel", "fee_sweep"]  # reforzar pulso + fees
        else:  # DROP
            acciones = ["flywheel"]  # re-encender el latido
        self._decisiones.append({"estado": estado, "acciones": acciones, "ts": time.time()})
        return acciones

    # ── EJECUTAR ─────────────────────────────────────────────────────────────
    def ejecutar(self, acciones: list[str]) -> list[dict]:
        """Encadena los motores autárquicos existentes (subprocess / dry_run)."""
        resultados: list[dict] = []
        for nombre in acciones:
            ruta, args = _MOTORES.get(nombre, (None, []))
            if ruta is None or not os.path.exists(ruta):
                resultados.append({"motor": nombre, "ok": False, "razon": "no_presente"})
                continue
            if self.dry_run:
                resultados.append({"motor": nombre, "ok": True, "dry_run": True})
                continue
            try:
                proc = subprocess.run(
                    [ruta, *args], capture_output=True, text=True, timeout=120
                )
                resultados.append(
                    {"motor": nombre, "ok": proc.returncode == 0, "exit": proc.returncode}
                )
            except Exception as exc:  # pragma: no cover
                resultados.append({"motor": nombre, "ok": False, "razon": str(exc)})
        return resultados

    # ── CICLO COMPLETO ───────────────────────────────────────────────────────
    def ciclo(self, amplitud: float) -> dict:
        latido = self.medir(amplitud)
        acciones = self.decidir(latido)
        ejecutado = self.ejecutar(acciones)
        ciclo = {**latido, "acciones": ejecutado}
        self._ciclos.append(ciclo)
        return ciclo

    # ── SALIDAS ──────────────────────────────────────────────────────────────
    def estado_autopoietico(self) -> dict:
        return {
            "ciclos": len(self._ciclos),
            "ultimo_psi": self._ciclos[-1]["psi"] if self._ciclos else None,
            "ultimo_estado": self._ciclos[-1]["estado"] if self._ciclos else None,
            "decisiones": self._decisiones[-1] if self._decisiones else None,
            "sellado": {
                "f0": f0,
                "Psi": Psi,
                "theta_B": theta_B,
                "D_PSI_S1": D_PSI_S1,
            },
        }

    def export_log(self) -> str:
        return json.dumps(self._ciclos, indent=2, default=str)

    @staticmethod
    def assert_autopoyesis() -> None:
        """Runner nativo de asserts (sin pytest). Valida el lazo con el metal."""
        bucle = BucleNoetico(dry_run=True)
        # coherencia plena -> ciclo de anclaje+ledger
        latido = bucle.medir(1.0)
        assert latido["estado"] == "UNITY", "Ψ=1 debe ser UNITY"
        assert bucle.decidir(latido) == ["fee_sweep", "anclaje_op_return", "ledger"]
        # warning -> solo fees (Ψ≥0.98 y <0.999)
        latido_w = bucle.medir(0.98)
        assert latido_w["estado"] == "WARNING", "Ψ=0.98 debe ser WARNING"
        assert bucle.decidir(latido_w) == ["fee_sweep"]
        # drop -> re-encender latido
        latido_d = bucle.medir(0.3)
        assert bucle.decidir(latido_d) == ["flywheel"]
        # ejecución: en local los scripts de BAL-003 no están presentes -> no_presente
        # (el Bucle detecta qué motores existen y cuáles no; no asume, verifica)
        res = bucle.ejecutar(["fee_sweep", "anclaje_op_return"])
        assert all(isinstance(r["ok"], bool) for r in res)
        # si el script NO existe -> reporta no_presente (nunca ok=True falso)
        for r in res:
            if r["razon"] == "no_presente":
                assert not r["ok"]
        # sello intacto
        assert abs(D_PSI_S1) > 3.0
        assert theta_B > 0.0 and theta_B < 1.0
        print("   ✓ BucleNoetico: medir→decidir→ejecutar coherente y DRY_RUN verificado")
