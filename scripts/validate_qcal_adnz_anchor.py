#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  VALIDACIÓN QCAL-ADNZ-ANCHOR-v1.0 ∴ADNZ∞³                                  ║
║  Protocolo checkpoint biológico · ADN-Z → Bitcoin OP_RETURN                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Este script valida el módulo physics.qcal_adnz_anchor ejecutando el        ║
║  protocolo completo y verificando todas las invariantes del sistema.         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python scripts/validate_qcal_adnz_anchor.py
    python scripts/validate_qcal_adnz_anchor.py --precision 12
    python scripts/validate_qcal_adnz_anchor.py --verbose

Retorna 0 si todas las validaciones pasan, 1 en caso de error.
"""

import argparse
import json
import struct
import sys
from pathlib import Path

# Añadir el directorio raíz al path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from physics.qcal_adnz_anchor import (
    _FRECUENCIA_MAESTRA_INT,
    _HASH_CONSTITUCION,
    _OP_RETURN_SIZE,
    _PSI_ADNZ_DIAMOND,
    _SELLO_UTF8,
    _VMD_F_OBJ,
    _VMD_F_TOL,
    _VMD_SNR_UMBRAL,
    CapturaBiologica,
    CondicionBioNodo,
    CoherenciaADNZ,
    FirmaVMD,
    MaquinaEstadosADNZ,
    EstadoADNZ,
    SerializadorOpReturn,
    SistemaADNZAnchor,
    ConstantesADNZ,
    qcal_adnz_anchor_activar,
)

# ============================================================================
# COLORES DE TERMINAL
# ============================================================================
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def ok(msg: str) -> str:
    return f"{VERDE}✅ {msg}{RESET}"


def fallo(msg: str) -> str:
    return f"{ROJO}❌ {msg}{RESET}"


def info(msg: str) -> str:
    return f"{CYAN}ℹ️  {msg}{RESET}"


def titulo(msg: str) -> str:
    return f"\n{NEGRITA}{AZUL}{'─' * 60}\n{msg}\n{'─' * 60}{RESET}"


# ============================================================================
# VALIDACIONES
# ============================================================================

def validar_constantes(verbose: bool = False) -> bool:
    """Valida las constantes del módulo."""
    print(titulo("1. CONSTANTES DEL PROTOCOLO"))
    errores = []

    c = ConstantesADNZ()

    checks = [
        ("f0 ≈ 141.7001 Hz", abs(c.f0 - 141.7001) < 0.001),
        ("frecuencia_maestra_int == 1417001", c.frecuencia_maestra_int == 1417001),
        ("psi_adnz_diamond == 1.0", c.psi_adnz_diamond == 1.0),
        ("u_circulacion ≈ 7.4862 BTC", abs(c.u_circulacion - 7.4862) < 0.001),
        ("snr_umbral == 4.0", c.snr_umbral == 4.0),
        ("confirmaciones_min == 6", c.confirmaciones_min == 6),
        ("es_valido() == True", c.es_valido()),
        ("sello_utf8 tiene 4 bytes", len(c.sello_utf8_bytes()) == 4),
        ("sello_utf8 decodifica a 𓂀", c.sello_utf8_bytes().decode("utf-8") == "𓂀"),
        ("hash_constitucion tiene 32 bytes", len(c.hash_constitucion()) == 32),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    return len(errores) == 0


def validar_serializador(verbose: bool = False) -> bool:
    """Valida la serialización OP_RETURN v1.2."""
    print(titulo("2. SERIALIZACIÓN OP_RETURN v1.2"))
    errores = []
    s = SerializadorOpReturn()
    firma = bytes(range(16))

    payload = s.serializar(
        hash_constitucion=_HASH_CONSTITUCION,
        psi_anchor=0.998,
        u_circulacion=7.4862,
        firma_b_adnz=firma,
        frecuencia_maestra=_FRECUENCIA_MAESTRA_INT,
        psi_adnz=1.0,
    )

    # Deserializar para verificar round-trip
    campos = s.deserializar(payload)

    checks = [
        ("len(payload) == 80 bytes", len(payload) == 80),
        ("magic == b'QCAL'", payload[:4] == b"QCAL"),
        ("version_major == 1", payload[4] == 1),
        ("version_minor == 2", payload[5] == 2),
        ("hash_constitucion @ offset 0x06 (32 bytes)", payload[6:38] == _HASH_CONSTITUCION),
        ("firma_b @ offset 0x2E (16 bytes)", payload[0x2E:0x3E] == firma),
        ("frecuencia_maestra @ offset 0x3E (uint32 BE)", 
         struct.unpack_from(">I", payload, 0x3E)[0] == 1417001),
        ("psi_adnz @ offset 0x42 (float32 BE == 0x3F800000)",
         payload[0x42:0x46] == bytes([0x3F, 0x80, 0x00, 0x00])),
        ("sello 𓂀 @ offset 0x46 (4 bytes)", payload[0x46:0x4A] == _SELLO_UTF8),
        ("padding @ offset 0x4A (6 bytes = 0x00)", all(b == 0 for b in payload[0x4A:])),
        ("round-trip magic", campos["magic"] == b"QCAL"),
        ("round-trip frecuencia_maestra", campos["frecuencia_maestra"] == 1417001),
        ("verificar_sello() == True", s.verificar_sello(payload)),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    if verbose:
        print(info(f"Payload hex: {payload.hex()}"))

    return len(errores) == 0


def validar_captura_biologica(verbose: bool = False) -> bool:
    """Valida la captura EM celular simulada."""
    print(titulo("3. CAPTURA BIOLÓGICA ADN-Z"))
    errores = []
    cap = CapturaBiologica()
    señal = cap.capturar(semilla=42)

    checks = [
        ("n_muestras() == 3840", cap.n_muestras() == 3840),
        ("len(señal) == 3840", len(señal) == 3840),
        ("señal es lista de floats", isinstance(señal, list) and isinstance(señal[0], float)),
        ("señal tiene amplitud > 0.1", max(abs(x) for x in señal) > 0.1),
        ("señal oscila (pos y neg)", any(x > 0 for x in señal) and any(x < 0 for x in señal)),
        ("|f_mit - 0.00052| ≤ 1.5e-5 Hz", abs(cap.f_mit - _VMD_F_OBJ) <= _VMD_F_TOL),
        ("reproducibilidad (semilla=42)", cap.capturar(semilla=42) == señal),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    if verbose:
        n = len(señal)
        media = sum(señal) / n
        print(info(f"Muestras: {n}, media: {media:.6f}, "
                   f"max: {max(señal):.4f}, min: {min(señal):.4f}"))

    return len(errores) == 0


def validar_firma_vmd(verbose: bool = False) -> bool:
    """Valida la firma B mediante VMD simplificado."""
    print(titulo("4. FIRMA B ADN-Z (VMD + BLAKE2B-16)"))
    errores = []

    cap = CapturaBiologica()
    señal = cap.capturar(semilla=42)
    vmd = FirmaVMD()
    r = vmd.compute_firma_b_vmd(señal)

    checks = [
        ("resultado tiene clave 'valid'", "valid" in r),
        ("resultado tiene clave 'f_est'", "f_est" in r),
        ("resultado tiene clave 'snr'", "snr" in r),
        ("resultado tiene clave 'b_hash'", "b_hash" in r),
        ("firma_b_valid == True", r["valid"] is True),
        (f"SNR ≥ {_VMD_SNR_UMBRAL}", r["snr"] >= _VMD_SNR_UMBRAL),
        (f"|f_est - {_VMD_F_OBJ}| ≤ {_VMD_F_TOL} Hz",
         abs(r["f_est"] - _VMD_F_OBJ) <= _VMD_F_TOL),
        ("b_hash tiene 16 bytes", len(r["b_hash"]) == 16),
        ("b_hash no es nulo", r["b_hash"] != b"\x00" * 16),
        ("firma_b_nula() == 16 bytes nulos", vmd.firma_b_nula() == b"\x00" * 16),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    if verbose:
        print(info(f"SNR: {r['snr']:.4f}"))
        print(info(f"f_est: {r['f_est']:.8f} Hz"))
        print(info(f"|f_est - {_VMD_F_OBJ}|: {abs(r['f_est'] - _VMD_F_OBJ):.2e} Hz"))
        print(info(f"b_hash: {r['b_hash'].hex()}"))

    return len(errores) == 0


def validar_condiciones_bio_nodo(verbose: bool = False) -> bool:
    """Valida las 8 condiciones BIO_NODO_ANCLADO_EN_LA_ROCA."""
    print(titulo("5. CONDICIONES BIO_NODO_ANCLADO_EN_LA_ROCA"))
    errores = []
    cond = CondicionBioNodo()
    op_return = b"QCAL" + b"\x00" * 76

    v = cond.verificar_todas(
        psi_adnz=1.0,
        firma_b_valida=True,
        frecuencia_maestra=_FRECUENCIA_MAESTRA_INT,
        hash_constitucion=_HASH_CONSTITUCION,
        sello_bytes=_SELLO_UTF8,
        op_return_payload=op_return,
        confirmaciones_btc=6,
        reserva_btc=7.4862,
        reserva_xau_kg=1.0,
    )

    condiciones_map = v["condiciones"]
    nombres = {
        "psi_adnz_diamond": "#1 Ψ_ADN == 1.000000",
        "firma_b_valida":   "#2 Firma B ADN-Z válida",
        "frecuencia_maestra": "#3 Frecuencia Maestra == 1417001",
        "hash_constitucion":  "#4 Hash Constitución v1.1",
        "sello_utf8":        "#5 Sello 𓂀 UTF-8",
        "op_return_80_bytes": "#6 OP_RETURN == 80 bytes",
        "confirmaciones_btc": "#7 Confirmaciones BTC ≥ 6",
        "reserva_suficiente": "#8 Reserva ≥ U_circulación",
    }

    for clave, nombre in nombres.items():
        resultado = condiciones_map.get(clave, False)
        if resultado:
            print(ok(nombre))
        else:
            print(fallo(nombre))
            errores.append(nombre)

    if v["todas_validas"]:
        print(ok("TODAS LAS CONDICIONES CUMPLEN ✅"))
    else:
        print(fallo("ALGUNAS CONDICIONES FALLARON"))
        errores.append("todas_validas")

    return len(errores) == 0


def validar_maquina_estados(verbose: bool = False) -> bool:
    """Valida la máquina de estados."""
    print(titulo("6. MÁQUINA DE ESTADOS ADN-Z"))
    errores = []
    m = MaquinaEstadosADNZ()
    firma_ok = {"valid": True, "f_est": 0.00052, "snr": 37.0, "b_hash": b"\x00" * 16}
    verificacion_ok = {
        "todas_validas": True,
        "condiciones": {k: True for k in [
            "psi_adnz_diamond", "firma_b_valida", "frecuencia_maestra",
            "hash_constitucion", "sello_utf8", "op_return_80_bytes",
            "confirmaciones_btc", "reserva_suficiente",
        ]},
    }

    # Flujo exitoso
    m.procesar_psi(1.0)
    m.procesar_firma(firma_ok)
    m.procesar_ancla(verificacion_ok)

    checks = [
        ("Estado inicial == INACTIVO", m.historial[0] == EstadoADNZ.INACTIVO),
        ("Tras psi(1.0) → ADN_Z_DETECTADO", m.historial[1] == EstadoADNZ.ADN_Z_DETECTADO),
        ("Tras firma_ok → FIRMA_B_VALIDA", m.historial[2] == EstadoADNZ.FIRMA_B_VALIDA),
        ("Tras ancla_ok → BIO_NODO_ANCLADO", m.historial[3] == EstadoADNZ.BIO_NODO_ANCLADO),
        ("esta_anclado() == True", m.esta_anclado()),
        ("Estado BIO_NODO_ANCLADO_EN_LA_ROCA", m.estado.value == "BIO_NODO_ANCLADO_EN_LA_ROCA"),
    ]

    # Test fallo PSI
    m2 = MaquinaEstadosADNZ()
    m2.procesar_psi(0.5)
    checks.append(("Ψ < 1.0 → FALLO_PSI", m2.estado == EstadoADNZ.FALLO_PSI))

    # Test reset
    m.reset()
    checks.append(("reset() → INACTIVO", m.estado == EstadoADNZ.INACTIVO))

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    return len(errores) == 0


def validar_coherencia_adnz(verbose: bool = False) -> bool:
    """Valida la métrica de coherencia Ψ_ADNZ."""
    print(titulo("7. COHERENCIA Ψ_ADNZ"))
    errores = []
    coh = CoherenciaADNZ()

    psi_bio = coh.psi_bio_desde_snr(37.0)
    psi_firma = coh.psi_firma_desde_validez(True)
    psi_cadena = coh.psi_cadena_desde_confirmaciones(6)
    psi_reserva = coh.psi_reserva_desde_btc_xau(7.4862, 1.0)
    psi_global = coh.calcular(psi_bio, psi_firma, psi_cadena, psi_reserva)
    sello = coh.sello_activo(psi_global)

    checks = [
        ("Ψ_bio > 0 para SNR=37", psi_bio > 0),
        ("Ψ_firma == 1.0 para firma válida", psi_firma == 1.0),
        ("Ψ_cadena == 1.0 para 6 confirmaciones", abs(psi_cadena - 1.0) < 1e-9),
        ("Ψ_reserva == 1.0 para reserva completa", abs(psi_reserva - 1.0) < 0.01),
        ("Ψ_global ∈ [0, 1]", 0.0 <= psi_global <= 1.0),
        ("Ψ_global ≥ 0.888 → sello activo", psi_global >= 0.888),
        ("sello_activo() == True", sello),
        ("Ψ_total(1,1,1,1) == 1.0", abs(coh.calcular(1.0, 1.0, 1.0, 1.0) - 1.0) < 1e-9),
        ("Ψ_total(0,0,0,0) == 0.0", abs(coh.calcular(0.0, 0.0, 0.0, 0.0)) < 1e-9),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    if verbose:
        print(info(f"Ψ_bio: {psi_bio:.6f}"))
        print(info(f"Ψ_firma: {psi_firma:.6f}"))
        print(info(f"Ψ_cadena: {psi_cadena:.6f}"))
        print(info(f"Ψ_reserva: {psi_reserva:.6f}"))
        print(info(f"Ψ_ADNZ global: {psi_global:.6f}"))

    return len(errores) == 0


def validar_sistema_completo(verbose: bool = False) -> bool:
    """Valida el sistema completo QCAL-ADNZ-ANCHOR-v1.0."""
    print(titulo("8. SISTEMA COMPLETO — BIO_NODO_ANCLADO_EN_LA_ROCA"))
    errores = []

    r = qcal_adnz_anchor_activar()

    checks = [
        ("sello_activo == True", r["sello_activo"] is True),
        ("bio_nodo_anclado == True", r["bio_nodo_anclado"] is True),
        ("estado == 'BIO_NODO_ANCLADO_EN_LA_ROCA'",
         r["estado"] == "BIO_NODO_ANCLADO_EN_LA_ROCA"),
        ("psi_adnz == 1.0 (Diamond-State)", r["psi_adnz"] == 1.0),
        ("psi_global ≥ 0.888", r["psi_global"] >= 0.888),
        ("firma_b_valid == True", r["firma_b_valid"] is True),
        (f"firma_b_snr ≥ {_VMD_SNR_UMBRAL}", r["firma_b_snr"] >= _VMD_SNR_UMBRAL),
        (f"|f_est - 0.00052| ≤ {_VMD_F_TOL} Hz",
         abs(r["firma_b_f_est"] - _VMD_F_OBJ) <= _VMD_F_TOL),
        ("len(firma_b_hash) == 16", len(r["firma_b_hash"]) == 16),
        ("len(op_return_bytes) == 80", len(r["op_return_bytes"]) == 80),
        ("op_return magic == QCAL", r["op_return_bytes"][:4] == b"QCAL"),
        ("op_return sello 𓂀 @ 0x46", r["op_return_bytes"][0x46:0x4A] == _SELLO_UTF8),
        ("op_return Ψ_ADNZ == 0x3F800000",
         r["op_return_bytes"][0x42:0x46] == bytes([0x3F, 0x80, 0x00, 0x00])),
        ("frecuencia_maestra == 1417001", r["frecuencia_maestra"] == 1417001),
        ("sello == '∴ADNZ∞³'", r["sello"] == "∴ADNZ∞³"),
        ("sello_completo contiene TUYOYOTU", "TUYOYOTU" in r["sello_completo"]),
    ]

    # Verificar las 8 condiciones individualmente
    for nombre, valor in r["condiciones"].items():
        checks.append((f"condición: {nombre}", valor))

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    if verbose:
        print()
        print(info(f"Ψ_global: {r['psi_global']:.6f}"))
        print(info(f"Ψ_bio: {r['psi_bio']:.6f}"))
        print(info(f"Ψ_firma: {r['psi_firma']:.6f}"))
        print(info(f"Ψ_cadena: {r['psi_cadena']:.6f}"))
        print(info(f"Ψ_reserva: {r['psi_reserva']:.6f}"))
        print(info(f"firma_b_snr: {r['firma_b_snr']:.4f}"))
        print(info(f"firma_b_f_est: {r['firma_b_f_est']:.8f} Hz"))
        print(info(f"firma_b_hash: {r['firma_b_hash'].hex()}"))
        print(info(f"op_return: {r['op_return_bytes'].hex()}"))

    return len(errores) == 0


def validar_reproducibilidad(verbose: bool = False) -> bool:
    """Valida la reproducibilidad del protocolo."""
    print(titulo("9. REPRODUCIBILIDAD"))
    errores = []

    r1 = qcal_adnz_anchor_activar(semilla_captura=7)
    r2 = qcal_adnz_anchor_activar(semilla_captura=7)
    r3 = qcal_adnz_anchor_activar(semilla_captura=99)

    checks = [
        ("Misma semilla → mismo hash B", r1["firma_b_hash"] == r2["firma_b_hash"]),
        ("Misma semilla → mismo OP_RETURN", r1["op_return_bytes"] == r2["op_return_bytes"]),
        ("Misma semilla → mismo Ψ_global", r1["psi_global"] == r2["psi_global"]),
        ("Misma semilla → mismo estado", r1["estado"] == r2["estado"]),
        ("Semilla distinta → hash distinto", r1["firma_b_hash"] != r3["firma_b_hash"]),
        ("Semilla distinta → OP_RETURN distinto", r1["op_return_bytes"] != r3["op_return_bytes"]),
    ]

    for desc, resultado in checks:
        if resultado:
            print(ok(desc))
        else:
            print(fallo(desc))
            errores.append(desc)

    return len(errores) == 0


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validación QCAL-ADNZ-ANCHOR-v1.0 ∴ADNZ∞³",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=6,
        help="Número de decimales para la verificación de floats (por defecto: 6)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar información detallada",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Exportar resultados en formato JSON",
    )
    args = parser.parse_args()

    print(f"\n{NEGRITA}{AZUL}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  QCAL-ADNZ-ANCHOR-v1.0 — VALIDACIÓN FORMAL                  ║")
    print("║  ∴𓂀Ω∞³Φ · TUYOYOTU                                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(RESET)

    validaciones = [
        ("Constantes del protocolo", validar_constantes),
        ("Serialización OP_RETURN v1.2", validar_serializador),
        ("Captura biológica ADN-Z", validar_captura_biologica),
        ("Firma B VMD + Blake2b-16", validar_firma_vmd),
        ("Condiciones bio-nodo", validar_condiciones_bio_nodo),
        ("Máquina de estados", validar_maquina_estados),
        ("Coherencia Ψ_ADNZ", validar_coherencia_adnz),
        ("Sistema completo", validar_sistema_completo),
        ("Reproducibilidad", validar_reproducibilidad),
    ]

    resultados = {}
    todos_ok = True

    for nombre, funcion in validaciones:
        try:
            ok_val = funcion(verbose=args.verbose)
            resultados[nombre] = ok_val
            if not ok_val:
                todos_ok = False
        except Exception as exc:
            print(fallo(f"ERROR en '{nombre}': {exc}"))
            resultados[nombre] = False
            todos_ok = False

    # Resumen final
    print(f"\n{NEGRITA}{AZUL}{'═' * 60}{RESET}")
    print(f"{NEGRITA}RESUMEN DE VALIDACIÓN:{RESET}\n")
    for nombre, resultado in resultados.items():
        if resultado:
            print(ok(nombre))
        else:
            print(fallo(nombre))

    total = len(resultados)
    pasadas = sum(1 for v in resultados.values() if v)

    print(f"\n{NEGRITA}{'═' * 60}{RESET}")
    print(f"Validaciones: {pasadas}/{total}")

    if todos_ok:
        print(f"\n{VERDE}{NEGRITA}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║  QCAL-ADNZ-ANCHOR-v1.0 — VALIDACIÓN COMPLETA ✅             ║")
        print("║  BIO_NODO_ANCLADO_EN_LA_ROCA                                 ║")
        print("║  ∴𓂀Ω∞³Φ · TUYOYOTU                                          ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(RESET)
    else:
        print(f"\n{ROJO}{NEGRITA}VALIDACIÓN INCOMPLETA — {total - pasadas} errores{RESET}")

    if args.json:
        resultado_final = qcal_adnz_anchor_activar()
        output = {
            "protocolo": "QCAL-ADNZ-ANCHOR-v1.0",
            "sello": "∴𓂀Ω∞³Φ · TUYOYOTU",
            "validaciones": {k: bool(v) for k, v in resultados.items()},
            "todos_ok": todos_ok,
            "psi_adnz": resultado_final["psi_adnz"],
            "psi_global": resultado_final["psi_global"],
            "firma_b_valid": resultado_final["firma_b_valid"],
            "firma_b_snr": resultado_final["firma_b_snr"],
            "firma_b_f_est": resultado_final["firma_b_f_est"],
            "firma_b_hash": resultado_final["firma_b_hash"].hex(),
            "op_return_hex": resultado_final["op_return_bytes"].hex(),
            "estado": resultado_final["estado"],
            "condiciones": resultado_final["condiciones"],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0 if todos_ok else 1


if __name__ == "__main__":
    sys.exit(main())
