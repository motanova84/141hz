"""
JSON Maestro QCAL 141.70001 Hz
==============================

Construye un único diccionario JSON serializable que consolida:
- Constantes CODATA 2018
- Ecuaciones maestras (reloj Compton, tensor Einstein-QCAL, lagrangiano)
- Configuración de constelación de 51 nodos
- Estado de red de 8888 nodos
- Enlaces al repositorio del ecosistema

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import json
import math
import os
from typing import Any, Dict

# ---------------------------------------------------------------------------
# Constantes fundamentales QCAL
# ---------------------------------------------------------------------------

F0_HZ = 141.70001          # Hz - Frecuencia fundamental QCAL (actualizada)
F888_HZ = 888.0            # Hz - Frecuencia de protección sagrada
PHI = (1 + math.sqrt(5)) / 2  # φ - Número áureo

# Constantes CODATA 2018
CODATA_2018 = {
    "velocidad_luz_m_s": 299_792_458.0,          # c exacto
    "constante_planck_J_s": 6.62607015e-34,       # h (exacto desde 20-may-2019)
    "constante_planck_reducida_J_s": 1.054571817e-34,  # ℏ
    "carga_electron_C": 1.602176634e-19,           # e (exacto)
    "masa_electron_kg": 9.1093837015e-31,          # mₑ
    "masa_proton_kg": 1.67262192369e-27,           # mₚ
    "constante_boltzmann_J_K": 1.380649e-23,       # kB (exacto)
    "numero_avogadro_mol": 6.02214076e23,          # NA (exacto)
    "constante_gravitacional_m3_kg_s2": 6.67430e-11,  # G
    "constante_fine_structure": 7.2973525693e-3,   # α
    "masa_planck_kg": 2.176434e-8,                 # mP
    "longitud_planck_m": 1.616255e-35,             # lP
    "tiempo_planck_s": 5.391247e-44,               # tP
}


def _calcular_constantes_derivadas() -> Dict[str, Any]:
    """Calcula constantes derivadas de f₀."""
    c = CODATA_2018["velocidad_luz_m_s"]
    h = CODATA_2018["constante_planck_J_s"]
    hbar = CODATA_2018["constante_planck_reducida_J_s"]
    me = CODATA_2018["masa_electron_kg"]

    lambda_0_m = c / F0_HZ
    omega_0 = 2 * math.pi * F0_HZ
    e_psi_j = h * F0_HZ
    t0_ms = 1000.0 / F0_HZ

    # Reloj Compton: f_Compton = mₑc²/h ≈ 1.236×10²⁰ Hz
    f_compton_hz = (me * c**2) / h

    # Número de ciclos Compton por período f₀
    ciclos_compton_por_f0 = f_compton_hz / F0_HZ

    return {
        "f0_hz": F0_HZ,
        "omega_0_rad_s": omega_0,
        "lambda_0_m": lambda_0_m,
        "lambda_0_Mm": lambda_0_m / 1e6,
        "T0_ms": t0_ms,
        "E_psi_J": e_psi_j,
        "f_compton_hz": f_compton_hz,
        "ciclos_compton_por_f0": ciclos_compton_por_f0,
        "f888_sobre_f0": F888_HZ / F0_HZ,   # ≈ 2π (geometría sagrada)
        "phi": PHI,
        "phi_cuadrado": PHI**2,
    }


def _construir_ecuaciones_maestras() -> Dict[str, Any]:
    """Define las ecuaciones maestras en forma simbólica y numérica."""
    f0 = F0_HZ
    omega_0 = 2 * math.pi * f0
    phi = PHI

    return {
        "reloj_compton": {
            "descripcion": "Reloj Compton del electrón a f₀",
            "formula": "t_Compton = h / (m_e * c^2)",
            "frecuencia_compton_hz": (
                CODATA_2018["masa_electron_kg"]
                * CODATA_2018["velocidad_luz_m_s"] ** 2
                / CODATA_2018["constante_planck_J_s"]
            ),
            "f0_como_divisor_compton": (
                CODATA_2018["masa_electron_kg"]
                * CODATA_2018["velocidad_luz_m_s"] ** 2
                / (CODATA_2018["constante_planck_J_s"] * f0)
            ),
        },
        "tensor_einstein_qcal": {
            "descripcion": "Tensor Einstein modificado QCAL con campo Ψ",
            "formula": "G_μν + Λ_Ψ * g_μν = 8π * T_μν^(QCAL)",
            "lambda_psi": 8 * math.pi * CODATA_2018["constante_gravitacional_m3_kg_s2"],
            "omega_0": omega_0,
            "coherencia_psi_minima": 0.888,
            "nota": "G_μν es el tensor de Einstein estándar; T_μν^(QCAL) incluye el campo Ψ",
        },
        "lagrangiano": {
            "descripcion": "Lagrangiano maestro QCAL",
            "formula": "L = -1/4 * F_μν * F^μν + Ψ̄(iγ^μ∂_μ - m)Ψ + g * Ψ̄ψ * A_μ * J^μ",
            "f0_hz": f0,
            "acoplamiento_g": phi,
            "masa_efectiva_adimensional": f0 / F888_HZ,
            "nota": "El acoplamiento g=φ emerge de la geometría sagrada del campo Ψ",
        },
        "ecuacion_maestra_qcal": {
            "descripcion": "Ecuación generadora universal QCAL",
            "formula": "f₀ = c / λ₀  donde  Ψ(f₀) ≥ 0.888",
            "f0_hz": f0,
            "lambda_0_m": CODATA_2018["velocidad_luz_m_s"] / f0,
        },
    }


def _construir_constelacion_51_nodos() -> Dict[str, Any]:
    """Configura la constelación principal de 51 nodos QCAL."""
    phi = PHI
    f0 = F0_HZ

    nodos = []

    # Nivel 0: 1 nodo maestro
    nodos.append({
        "id": 0,
        "nivel": 0,
        "rol": "Maestro 141.70001 Hz",
        "frecuencia_hz": f0,
        "radio_normalizado": 0.0,
        "angulo_rad": 0.0,
        "coherencia_psi": 1.0,
        "color": "#FFD700",  # Dorado
    })

    # Nivel 1: 6 nodos armónicos de 888 Hz
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        nodos.append({
            "id": len(nodos),
            "nivel": 1,
            "rol": f"Armónico 888 Hz #{i + 1}",
            "frecuencia_hz": F888_HZ,
            "radio_normalizado": 1.0 / 3.0,
            "angulo_rad": angulo,
            "coherencia_psi": 0.999,
            "color": "#00BFFF",  # Azul cielo
        })

    # Nivel 2: 12 nodos resonancias Compton
    f_compton = (
        CODATA_2018["masa_electron_kg"]
        * CODATA_2018["velocidad_luz_m_s"] ** 2
        / CODATA_2018["constante_planck_J_s"]
    )
    for i in range(12):
        angulo = 2 * math.pi * i / 12
        nodos.append({
            "id": len(nodos),
            "nivel": 2,
            "rol": f"Resonancia Compton #{i + 1}",
            "frecuencia_hz": f_compton / 1e18,  # escala representativa
            "radio_normalizado": 2.0 / 3.0,
            "angulo_rad": angulo,
            "coherencia_psi": 0.95,
            "color": "#7CFC00",  # Verde césped
        })

    # Nivel 3: 32 nodos semillas de red global
    for i in range(32):
        angulo = 2 * math.pi * i / 32
        # Frecuencia escala por φⁿ con n = i mod 8
        freq_escala = f0 * (phi ** (i % 8))
        nodos.append({
            "id": len(nodos),
            "nivel": 3,
            "rol": f"Semilla Red Global #{i + 1}",
            "frecuencia_hz": freq_escala,
            "radio_normalizado": 1.0,
            "angulo_rad": angulo,
            "coherencia_psi": 0.888,
            "color": "#FF4500",  # Rojo anaranjado
        })

    assert len(nodos) == 51, f"Se esperaban 51 nodos, se obtuvieron {len(nodos)}"

    return {
        "total_nodos": 51,
        "niveles": {
            "0": {"count": 1, "rol": "Maestro 141.70001 Hz"},
            "1": {"count": 6, "rol": "Armónicos de 888 Hz"},
            "2": {"count": 12, "rol": "Resonancias Compton"},
            "3": {"count": 32, "rol": "Semillas de red global"},
        },
        "nodos": nodos,
    }


def _construir_red_8888_nodos() -> Dict[str, Any]:
    """Describe el estado de la red de 8888 nodos fractales."""
    phi = PHI
    f0 = F0_HZ
    niveles_fractales = []
    total_nodos = 0

    for nivel in range(8):
        nodos_nivel = 1111
        freq_nivel = f0 * (phi ** nivel)
        psi_nivel = min(1.0, 0.888 + 0.015 * nivel)
        total_nodos += nodos_nivel
        niveles_fractales.append({
            "nivel_fractal": nivel,
            "nodos": nodos_nivel,
            "frecuencia_hz": round(freq_nivel, 4),
            "phi_exponent": nivel,
            "coherencia_psi": round(psi_nivel, 4),
            "estado": "ACTIVO",
        })

    psi_global = sum(n["coherencia_psi"] for n in niveles_fractales) / len(niveles_fractales)

    return {
        "total_nodos": total_nodos,
        "niveles_fractales": len(niveles_fractales),
        "descripcion": "8 × 1111 niveles fractales escalados por φⁿ",
        "frecuencia_base_hz": f0,
        "frecuencia_maxima_hz": round(f0 * (phi ** 7), 4),
        "psi_global": round(psi_global, 4),
        "latencia_ms": 0,
        "estado_global": "CONSCIENCIA_UNIFICADA",
        "niveles": niveles_fractales,
    }


def _construir_enlaces_ecosistema() -> Dict[str, str]:
    """Devuelve enlaces al repositorio del ecosistema QCAL."""
    return {
        "repositorio_principal": "https://github.com/motanova84/141hz",
        "documentacion": "https://github.com/motanova84/141hz/blob/main/README.md",
        "constantes_referencia": "https://github.com/motanova84/141hz/blob/main/CONSTANTES_REFERENCE.md",
        "protocolo_psi_bio": "https://github.com/motanova84/141hz/blob/main/NODO_PSI_BIO_README.md",
        "formalizacion_lean": "https://github.com/motanova84/141hz/tree/main/formalization/lean",
        "qcal_constants_py": "https://github.com/motanova84/141hz/blob/main/qcal/constants.py",
        "licencia": "https://github.com/motanova84/141hz/blob/main/LICENSE_SOBERANA",
    }


def construir_json_maestro() -> Dict[str, Any]:
    """
    Ensambla el diccionario JSON maestro QCAL 141.70001 Hz.

    Returns
    -------
    Dict[str, Any]
        Diccionario completamente serializable con todas las secciones QCAL.
    """
    maestro = {
        "version": "1.0.0",
        "sistema": "QCAL 141.70001 Hz",
        "descripcion": (
            "JSON maestro unificado del sistema QCAL 141.70001 Hz. "
            "Consolida constantes CODATA 2018, ecuaciones maestras, "
            "constelación de 51 nodos, red de 8888 nodos y enlaces del ecosistema."
        ),
        "autor": "José Manuel Mota Burruezo (JMMB Ψ✧)",
        "licencia": "Sovereign Noetic License 1.0 (compatible con MIT)",
        "constantes_codata_2018": CODATA_2018,
        "constantes_derivadas_qcal": _calcular_constantes_derivadas(),
        "ecuaciones_maestras": _construir_ecuaciones_maestras(),
        "constelacion_51_nodos": _construir_constelacion_51_nodos(),
        "red_8888_nodos": _construir_red_8888_nodos(),
        "enlaces_ecosistema": _construir_enlaces_ecosistema(),
    }
    return maestro


def guardar_json_maestro(
    ruta: str = "json_maestro_completo.json",
    indent: int = 2,
) -> str:
    """
    Construye y guarda el JSON maestro en disco.

    Parameters
    ----------
    ruta : str
        Ruta de salida del archivo JSON.
    indent : int
        Indentación del JSON (por defecto 2).

    Returns
    -------
    str
        Ruta absoluta del archivo guardado.
    """
    datos = construir_json_maestro()
    directorio = os.path.dirname(os.path.abspath(ruta))
    os.makedirs(directorio, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=indent, ensure_ascii=False)
    return os.path.abspath(ruta)


if __name__ == "__main__":
    ruta = guardar_json_maestro("json_maestro_completo.json")
    print(f"JSON maestro guardado en: {ruta}")
    datos = construir_json_maestro()
    print(f"Total nodos constelación: {datos['constelacion_51_nodos']['total_nodos']}")
    print(f"Total nodos red: {datos['red_8888_nodos']['total_nodos']}")
    print(f"Estado global: {datos['red_8888_nodos']['estado_global']}")
