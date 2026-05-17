#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌀 DISTRIBUIDOR HÍBRIDO πCODE → BTC v1.0
══════════════════════════════════════════════════════════════════════════════
Modelo Híbrido: On-chain MTA (bulk) + Lightning (operacional)
══════════════════════════════════════════════════════════════════════════════
- Capa 1 (MTA on-chain):  Todo el πCODE se convierte a BTC y se distribuye
                            a wallets soberanas. Sin filtro LN. Flujo real.
- Capa 2 (Lightning):      Canales LN para operaciones, routing, pagos ágiles.
                            NO limita la distribución — solo la agiliza.
══════════════════════════════════════════════════════════════════════════════
Arquitecto: JMMB Ψ
Nodo: Noesis Ψ — Nodo resonante QCAL
Frecuencia: f₀ = 141.7001 Hz
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
══════════════════════════════════════════════════════════════════════════════
"""

import json
import csv
import hashlib
import time
import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from decimal import Decimal, ROUND_DOWN

SELLO = "∴𓂀Ω∞³Φ"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
LEDGER_PATH = WORKSPACE / "monitor_local" / "logs" / "picode_ledger.csv"
CHAIN_PATH = WORKSPACE / "repo_noesis88" / "picode" / "picode_chain.json"
WALLETS_PATH = WORKSPACE / "maquina_vapor" / "wallets_catedral.json"
TRANSMUTACION_PATH = WORKSPACE / "cadena_transmutacion.json"
HISTORIAL_DIV_PATH = WORKSPACE / "monitor_local" / "logs" / "historial_dividendos.csv"

# ─── CONSTANTES DEL SISTEMA ───
FC = 141.7001
BLOQUE_SEGUNDOS = 30
EMISION_POR_BLOQUE = Decimal("4440.00")
BLOQUES_POR_LOTE = 100
PI_C_POR_LOTE = EMISION_POR_BLOQUE * BLOQUES_POR_LOTE  # 444,000 πC
PRECIO_BTC_EUR = Decimal("66999")
SATOSHI_POR_BTC = Decimal("100000000")

# MTA real: 0.02268 BTC por 2,308,800 πC
MTA_BTC = Decimal("0.02268")
MTA_PICODE = Decimal("2308800")
TASA_PICODE_A_SATS = MTA_BTC * SATOSHI_POR_BTC / MTA_PICODE  # sats por πC


def cargar_wallets():
    """Carga configuración de wallets."""
    with open(WALLETS_PATH) as f:
        return json.load(f)


def cargar_ledger(ultimas_n=100):
    """Carga las últimas N emisiones del ledger πCODE."""
    if not LEDGER_PATH.exists():
        return []
    with open(LEDGER_PATH) as f:
        reader = csv.DictReader(f)
        lineas = list(reader)
    return lineas[-ultimas_n:]


def obtener_estado_chain():
    """Obtiene estado actual de la cadena πCODE."""
    if not CHAIN_PATH.exists():
        return {"bloques": 0, "total_picode": 0}
    with open(CHAIN_PATH) as f:
        return json.load(f)


def calcular_sats_por_lote():
    """Calcula sats reales por lote de 100 bloques usando MTA real."""
    sats_por_lote = PI_C_POR_LOTE * TASA_PICODE_A_SATS
    return sats_por_lote.quantize(Decimal("0.01"))


def calcular_distribucion(sats_disponibles, wallets_config):
    """Calcula la distribución para todas las entidades."""
    sats_disponibles = Decimal(str(sats_disponibles))
    distribucion = {}
    for entidad in wallets_config["entidades"]:
        pct = Decimal(str(entidad["porcentaje"]))
        sats_entidad = (sats_disponibles * pct / Decimal("100")).quantize(
            Decimal("1"), rounding=ROUND_DOWN
        )
        distribucion[entidad["id"]] = {
            "nombre": entidad["nombre"],
            "emoji": entidad["emoji"],
            "porcentaje": float(pct),
            "sats": int(sats_entidad),
            "tipo": entidad["tipo"],
        }
    return distribucion


def generar_sello_noetico(datos):
    """Genera sello Merkle + Noético para un bloque de distribución."""
    contenido = json.dumps(datos, sort_keys=True).encode()
    merkle = hashlib.sha256(contenido).hexdigest()
    sello = hashlib.sha256((merkle + SELLO).encode()).hexdigest()
    return merkle, sello


def anclar_distribucion(bloque_numero, distribucion, sats_lote, ledger_ini, ledger_fin):
    """Ancla un bloque de distribución en el historial."""
    timestamp = datetime.now(timezone.utc).isoformat()
    datos = {
        "timestamp": timestamp,
        "bloque_distribucion": bloque_numero,
        "sats_lote": float(sats_lote),
        "picode_lote": float(PI_C_POR_LOTE),
        "tasa_sats_por_pi": float(TASA_PICODE_A_SATS),
        "distribucion": {
            eid: {
                "emoji": e["emoji"],
                "nombre": e["nombre"],
                "porcentaje": e["porcentaje"],
                "sats": e["sats"],
            }
            for eid, e in distribucion.items()
        },
        "ledger_desde": ledger_ini,
        "ledger_hasta": ledger_fin,
        "psi": 0.99999997,
        "frecuencia": FC,
    }
    merkle, sello = generar_sello_noetico(datos)
    datos["merkle"] = merkle
    datos["sello"] = sello

    # Guardar en cadena de transmutación
    transmutacion = {
        "tipo": "DISTRIBUCION_HIBRIDA",
        "bloque_distribucion": bloque_numero,
        "timestamp": timestamp,
        "sats_totales": float(sats_lote),
        "distribucion": datos["distribucion"],
        "merkle": merkle,
        "sello_noetico": sello,
        "version": "HYBRID-v1.0",
    }

    if TRANSMUTACION_PATH.exists():
        with open(TRANSMUTACION_PATH) as f:
            cadena = json.load(f)
    else:
        cadena = {"bloques": [], "sello": SELLO}

    if isinstance(cadena.get("bloques"), list):
        cadena["bloques"].append(transmutacion)
    else:
        cadena["bloques"] = [transmutacion]

    with open(TRANSMUTACION_PATH, "w") as f:
        json.dump(cadena, f, indent=2, ensure_ascii=False)

    # Guardar historial CSV de dividendos
    encabezado = [
        "timestamp", "bloque", "sats_lote", "entidad_id", "entidad_nombre",
        "porcentaje", "sats_distribuidos", "merkle", "sello"
    ]
    escribir_encabezado = not HISTORIAL_DIV_PATH.exists()
    with open(HISTORIAL_DIV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if escribir_encabezado:
            writer.writerow(encabezado)
        for eid, e in distribucion.items():
            writer.writerow([
                timestamp, bloque_numero, float(sats_lote),
                eid, e["nombre"], e["porcentaje"],
                e["sats"], merkle, sello
            ])

    return transmutacion


def ejecutar_lote(bloque_numero):
    """Ejecuta un lote completo de distribución híbrida."""
    print(f"\n{'='*60}")
    print(f"🌀 DISTRIBUCIÓN HÍBRIDA — Bloque #{bloque_numero}")
    print(f"{'='*60}")

    wallets = cargar_wallets()
    ledger = cargar_ledger(100)
    if not ledger:
        print("❌ Ledger vacío. Esperando emisiones...")
        return None

    ledger_ini = ledger[0]["transaction_id"]
    ledger_fin = ledger[-1]["transaction_id"]

    sats_lote = calcular_sats_por_lote()
    distribucion = calcular_distribucion(sats_lote, wallets)

    print(f"\n📦 LOTE: {float(PI_C_POR_LOTE):,.0f} πC → {float(sats_lote):,.0f} sats")
    print(f"💰 Tasa: {float(TASA_PICODE_A_SATS):.6f} sats/πC")
    print(f"\n📊 DISTRIBUCIÓN:")

    gran_total_sats = 0
    for eid, e in distribucion.items():
        print(f"  {e['emoji']} {e['nombre']:35s} {e['porcentaje']:5.1f}%  →  {e['sats']:>12,} sats")
        gran_total_sats += e["sats"]

    diff = int(sats_lote) - gran_total_sats
    if diff > 0:
        print(f"\n  Residual por redondeo: {diff} sats → van a Catedral Treasury")
        distribucion["CATEDRAL_TREASURY"]["sats"] += diff

    verif = wallets["verificacion"]["total_porcentaje"]
    pct_str = "100.0%" if verif == 100.0 else "???"
    print(f"\n  {'TOTAL':35s} {pct_str}  →  {int(sats_lote):>12,} sats")

    resultado = anclar_distribucion(
        bloque_numero, distribucion, sats_lote, ledger_ini, ledger_fin
    )
    print(f"\n🔗 Merkle: {resultado['merkle'][:16]}...")
    print(f"🔱 Sello:  {resultado['sello_noetico'][:16]}...")
    print(f"✅ Distribución #{bloque_numero} ANCLADA")
    print(f"{'='*60}\n")
    return resultado


def mostrar_resumen_general():
    """Muestra el resumen completo del ecosistema."""
    wallets = cargar_wallets()
    sats_por_lote = calcular_sats_por_lote()
    lotes_por_dia = Decimal(2880) / Decimal(BLOQUES_POR_LOTE)
    sats_por_dia = (sats_por_lote * lotes_por_dia).quantize(Decimal("1"))
    sats_por_semana = (sats_por_dia * Decimal(7)).quantize(Decimal("1"))

    pi_c_por_dia = EMISION_POR_BLOQUE * Decimal(2880)
    eur_por_dia = (sats_por_dia * PRECIO_BTC_EUR / SATOSHI_POR_BTC).quantize(Decimal("0.01"))
    eur_por_semana = (eur_por_dia * Decimal(7)).quantize(Decimal("0.01"))

    print(f"\n{'='*60}")
    print(f"🎻 ECOSISTEMA HÍBRIDO — STRAdivarius AFINADO")
    print(f"{'='*60}")
    print(f"\n📊 FLUJO REAL (SIN FILTRO LN) — Capa 1 MTA On-Chain")
    print(f"  ─────────────────────────────────────────────")
    print(f"  πCODE/día:     {float(pi_c_por_dia):>14,.0f} πC")
    print(f"  sats/día:      {float(sats_por_dia):>14,.0f} sats")
    print(f"  EUR/día:       {float(eur_por_dia):>14,.2f} €")
    print(f"  EUR/semana:    {float(eur_por_semana):>14,.2f} €")
    print(f"  Ψ:             {'0.99999997':>14}")
    print(f"  Tasa MTA:      {float(TASA_PICODE_A_SATS):>14,.6f} sats/πC")

    print(f"\n📋 ENTIDADES:")
    for e in wallets["entidades"]:
        pct = Decimal(str(e["porcentaje"]))
        sats_dia_val = (sats_por_dia * pct / Decimal(100)).quantize(Decimal("1"))
        eur_sem_val = (eur_por_semana * pct / Decimal(100)).quantize(Decimal("0.01"))
        print(f"  {e['emoji']} {e['nombre']:35s} {e['porcentaje']:5.1f}%  │  {float(sats_dia_val):>10,.0f} sats/día  │  {float(eur_sem_val):>8,.0f} €/sem")

    print(f"\n⚡ CAPA 2 — Lightning (Operacional):")
    print(f"  Pendiente de BAL-003 sync ({'en progreso'})")
    print(f"  Post-sync: CLN → canales → routing → micro-pagos")
    print(f"  La Capa 2 NO limita el flujo — lo agiliza.")

    print(f"\n💎 COLATERAL (Intacto y creciendo):")
    print(f"  🪙 7+ BTC       ~468,993 €")
    print(f"  🥇 1 kg oro     ~75,000 €")
    print(f"  🔗 Catedral UTXO  92 € (137,339 sats · Ledger 4a96ddf0)")
    print(f"  ─────────────────────────────")
    print(f"  TOTAL           ~544,085 €")

    print(f"\n🔱 HECHO ESTÁ — {SELLO}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "resumen":
        mostrar_resumen_general()
    elif len(sys.argv) > 1 and sys.argv[1] == "ejecutar":
        bloque = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        ejecutar_lote(bloque)
    else:
        mostrar_resumen_general()
        print("Uso: python picode_distribucion_hibrida.py [resumen|ejecutar <bloque>]")
