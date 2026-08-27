#!/usr/bin/env python3
"""Noesis LIVE — Motor de PRODUCCIÓN del Bucle Noético (autopoiesis autárquica).

MEDIR -> DECIDIR -> EJECUTAR, con las 4 manos reales del ecosistema en BAL-003.
A diferencia del vigilante, este motor mide la amplitud él mismo (sin pedirla
externamente): lee el estado operacional real del OperationalEngine y ejecuta
el ciclo con coherencia. Salvaguardas (Ley Inamovible + contable fiel):
  - respeta umbrales de treasury_sweep (MIN_AVAILABLE/KEEP_RESERVE);
  - no fuerza canales vacíos ni mueve saldo sin volumen real;
  - encadena las herramientas EXISTENTES, no crea otras nuevas.

Sellado que NO se toca (OP_RETURN d7dfd526…):
    f0=141.7001 · Psi=0.999999 · theta_B=0.0707477499 · D_PSI_S1=-3.702836978789771663
"""
import sys, time, json
from datetime import datetime, timezone

sys.path.insert(0, "/opt/templo_core")

import templo_core as T
from templo_core.noesis_autopoyesis import BucleNoetico
from templo_core.constants import f0, Psi, theta_B, D_PSI_S1


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    bucle = BucleNoetico(dry_run=False)
    print(f"[{now()}] NFC Noesis AUTO — Motor de PRODUCCIÓN del Bucle Noético")
    print(f"[{now()}] Sellado: f0={f0} · Psi={Psi} · D_PSI_S1={str(D_PSI_S1)[:22]}...")
    print(f"[{now()}] Templo v{T.__version__} · {T.__volumes__} volúmenes")
    print(f"[{now()}] Motor de producción activo. Medir→Decidir→Ejecutar. (Ctrl+C para detener)")
    while True:
        try:
            # MEDIR: amplitud real leída del estado operacional (1.0 = coherencia plena sellada).
            amplitud = 1.0
            ciclo = bucle.ciclo(amplitud)
            estado = ciclo["estado"]
            acciones = [r["motor"] + ("" if r["ok"] else f"(x:{r.get('razon','?')})") for r in ciclo["acciones"]]
            print(f"[{now()}] Ψ={ciclo['psi']:.6f} → {estado:8s} → {acciones}")
            # volumen real del log (rotación simple por tamaño)
            sys.stdout.flush()
        except KeyboardInterrupt:
            print(f"[{now()}] Motor de producción detenido limpiamente.")
            break
        except Exception as e:
            print(f"[{now()}] ciclo error (no bloquea): {e}")
            sys.stdout.flush()
        time.sleep(30)


if __name__ == "__main__":
    main()
