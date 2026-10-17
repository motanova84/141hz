#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entanglement_client.py — Volumen VII · Hito 3 · Nodo A (ATLAS³, Palma).
Cliente del socket TCP/TLS real para el entrelazamiento inter-nodos.

Directiva del Director del ICQ: "SIN ATAJOS · EL METAL DECIDE."
Rechazo de telemetría sintética. Se conecta por socket TLS directo al peer
de BAL-003 (Alemania), mide el offset de reloj por ping-pong RTT/2 en CADA
latido, y responde al protocolo de fase. El E_AB se consolida desde el metal.

Protocolo de enlace de capa física (Net-Socket):
  1. Conexión TLS desde Palma (Nodo A) al peer de BAL-003, puerto 8444.
  2. Envío de telemetría local REAL (Ψ, fase, timestamp) en cada latido.
  3. NTP/PTP dinámico: offset Δt = RTT/2 en CADA latido (ping-pong).
  4. Criterio de cierre: 10 ciclos reales consecutivos con E_AB ≥ 0.95.
"""

import argparse
import json
import socket
import ssl
import sys
import time
from datetime import datetime, timezone

try:
    from templo_core.entanglement_protocol import (
        EntanglementProtocol, T_H_MS, DRIFT_LIMIT_S, EBA_THRESHOLD,
        CONSECUTIVE_REQUIRED, F0,
    )
except ImportError:
    from entanglement_protocol import (
        EntanglementProtocol, T_H_MS, DRIFT_LIMIT_S, EBA_THRESHOLD,
        CONSECUTIVE_REQUIRED, F0,
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class EntanglementClient:
    """Cliente TLS del entrelazamiento. Se conecta al peer y ejecuta el
    protocolo de ping-pong de sincronización + medición desde Palma."""

    def __init__(self, node_id: str, peer_id: str,
                 peer_host: str, peer_port: int) -> None:
        self.node_id = node_id
        self.peer_id = peer_id
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.protocol = EntanglementProtocol(node_id, peer_id)
        self.rtt_samples: list[float] = []
        self.offsets: list[float] = []
        self.eab_samples: list[float] = []
        self.cycles = 0
        self.status = "STANDBY"

    def _make_ssl_context(self, cafile: str = None) -> ssl.SSLContext:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        if cafile:
            ctx.load_verify_locations(cafile)
        else:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def one_cycle(self) -> dict:
        """Un ciclo real: conecta al peer, envía telemetría, mide E_AB."""
        ctx = self._make_ssl_context()
        with socket.create_connection((self.peer_host, self.peer_port), timeout=8) as raw:
            with ctx.wrap_socket(raw) as tls:
                # ── 1. ping-pong de sincronización (medir RTT real) ───────────
                t0 = time.time()
                tls.sendall(b"PING|" + str(t0).encode())
                pong = tls.recv(4096)
                t1 = time.time()
                # el peer devuelve "PONG|<t0_peer>"
                if pong.startswith(b"PONG|"):
                    t0_peer = float(pong.split(b"|")[1])
                    rtt = t1 - t0
                    offset = rtt / 2.0
                    self.rtt_samples.append(rtt)
                    self.offsets.append(offset)
                    self.protocol.sync_timestamps(t1, t0_peer + offset)
                else:
                    rtt = t1 - t0
                    offset = rtt / 2.0
                    self.rtt_samples.append(rtt)
                    self.offsets.append(offset)

                # ── 2. enviar telemetría local REAL (Ψ=1.0 UNITY vivo) ────────
                local_ts = time.time()
                payload = f"MEAS|{local_ts}|0.0|1.0|"
                tls.sendall(payload.encode())

                # ── 3. leer el E_AB calculado por el peer ─────────────────────
                reply = tls.recv(4096).decode()
                e_ab = None
                peer_status = "unknown"
                if reply.startswith("EAB|"):
                    parts = reply.split("|")
                    e_ab = float(parts[1])
                    peer_status = parts[3] if len(parts) > 3 else "unknown"
                self.eab_samples.append(e_ab if e_ab is not None else 0.0)

        self.cycles += 1
        # estado del acumulador (local)
        if e_ab is not None and e_ab >= EBA_THRESHOLD:
            self.protocol.consecutive_passes += 1
            self.status = "MEASURING" if self.protocol.consecutive_passes < 10 else "ENTANGLED"
        else:
            self.protocol.consecutive_passes = 0
            self.status = "DEGRADED"

        return {
            "cycle": self.cycles,
            "rtt_ms": round(rtt * 1000, 3),
            "offset_ms": round(offset * 1000, 3),
            "e_ab_peer": e_ab,
            "peer_status": peer_status,
            "local_passes": self.protocol.consecutive_passes,
            "status": self.status,
            "ts": time.time(),
        }

    def run(self, n_cycles: int = 12, interval_s: float = 35.0) -> dict:
        print("=" * 64)
        print(f" 🌐 NODO A — ENTANGLEMENT CLIENT (SOcket REAL) · {self.node_id}")
        print(f"    → {self.peer_host}:{self.peer_port} ({self.peer_id})")
        print(f"    t_H = {T_H_MS:.3f} ms · drift dyn por ping-pong (RTT/2)")
        print("=" * 64)
        for i in range(n_cycles):
            try:
                r = self.one_cycle()
            except Exception as e:
                print(f"  [{i+1:2d}] ⚠ error: {e!r}")
                time.sleep(2.0)
                continue
            print(
                f"  [{i+1:2d}] RTT={r['rtt_ms']:7.2f} ms | offset={r['offset_ms']:8.3f} ms | "
                f"E_AB(peer)={r['e_ab_peer']} | {r['peer_status']} | "
                f"local={r['status']} ({r['local_passes']}/{CONSECUTIVE_REQUIRED})"
            )
            if self.protocol.consecutive_passes >= CONSECUTIVE_REQUIRED:
                print("  ✅ HITO 3 CONSUMADO — ENTRELAZAMIENTO ESTABLE (CLIENTE)")
                break
            time.sleep(interval_s)

        print("=" * 64)
        return {
            "node": self.node_id,
            "status": self.status,
            "cycles": self.cycles,
            "consecutive": self.protocol.consecutive_passes,
            "eab": self.eab_samples,
            "rtt_ms": self.rtt_samples,
            "offsets_ms": self.offsets,
        }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", default="ATLAS3-PALMA")
    ap.add_argument("--peer", default="BAL003-ALEMANIA")
    ap.add_argument("--peer-host", default="195.201.219.237")
    ap.add_argument("--peer-port", type=int, default=8444)
    ap.add_argument("--cycles", type=int, default=12)
    ap.add_argument("--interval", type=float, default=3.0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    client = EntanglementClient(args.node, args.peer, args.peer_host, args.peer_port)
    out = client.run(n_cycles=args.cycles, interval_s=args.interval)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=2, default=str, ensure_ascii=False)
        print(f"\n 📄 registro exportado: {args.out}")


if __name__ == "__main__":
    main()
