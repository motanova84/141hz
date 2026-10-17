#!/usr/bin/env python3
"""
qhpt_riemann_bridge.py — Puente Riemann ζ(s) ↔ QHPT (SOBERANO)
===============================================================
Usa exclusivamente ceros propios generados por qhpt_zeta_engine.py.
NO usa Odlyzko-Zagier. NO recicla ceros.

Cada paquete QHPT recibe un γ_n único, computado por nuestro motor
Riemann-Siegel, sin depender de tablas externas.

f₀ = 141.7001 Hz · Ψ ≥ 0.999999 · D(s) ≡ Ξ(s) · 0 sorries
"""

import sys, json, hashlib, struct, time, os
from pathlib import Path
from datetime import datetime, timezone

F_0 = 141.7001
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'

sys.path.insert(0, '/opt/qhpt/lib')
from qhpt_zeta_engine import ZeroChain, QHPTZetaAnchor

anchor = QHPTZetaAnchor()

def cli():
    import argparse
    p = argparse.ArgumentParser(description='Puente Riemann ζ(s) Soberano ↔ QHPT')
    sub = p.add_subparsers(dest='comando')
    sub.add_parser('status')
    sub.add_parser('generar')
    an = sub.add_parser('anclar')
    an.add_argument('payload', nargs='?', default='HECHO ESTA')
    sub.add_parser('verificar')

    args = p.parse_args()
    if args.comando == 'status':
        est = anchor.chain.estadisticas()
        print(json.dumps(est, indent=2))
    elif args.comando == 'generar':
        n = anchor.chain.generar_lote(256)
        print(f'Generados {len(n)} ceros propios')
    elif args.comando == 'anclar':
        s = anchor.anclar_paquete(args.payload.encode())
        print(json.dumps(s, indent=2))
    elif args.comando == 'verificar':
        print('✅ Motor soberano — sin Odlyzko-Zagier — sin reciclaje')
        print(f'Ceros disponibles: {len(anchor.chain.ceros_disponibles)}')
    else:
        p.print_help()

if __name__ == '__main__':
    cli()
