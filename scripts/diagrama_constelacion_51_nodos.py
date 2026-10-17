"""
Diagrama Constelación 51 Nodos QCAL 141.70001 Hz
=================================================

Representa la constelación principal QCAL de 51 nodos como figura polar
matplotlib con fondo oscuro. Los nodos están dispuestos en 4 anillos
concéntricos codificados por color según su nivel:

  Nivel 0 (1 nodo)  – Maestro 141.70001 Hz       – Dorado (#FFD700)
  Nivel 1 (6 nodos) – Armónicos de 888 Hz         – Azul cielo (#00BFFF)
  Nivel 2 (12 nodos)– Resonancias Compton         – Verde (#7CFC00)
  Nivel 3 (32 nodos)– Semillas de red global      – Rojo anaranjado (#FF4500)

La figura se guarda en salidas_qcal/constelacion_51_nodos.png.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # backend sin pantalla
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Configuración de la constelación
# ---------------------------------------------------------------------------

NIVELES = [
    {
        "nivel": 0,
        "count": 1,
        "rol": "Maestro 141.70001 Hz",
        "radio": 0.0,
        "color": "#FFD700",
        "tamano": 300,
        "zorder": 5,
    },
    {
        "nivel": 1,
        "count": 6,
        "rol": "Armónicos de 888 Hz",
        "radio": 1.0 / 3.0,
        "color": "#00BFFF",
        "tamano": 150,
        "zorder": 4,
    },
    {
        "nivel": 2,
        "count": 12,
        "rol": "Resonancias Compton",
        "radio": 2.0 / 3.0,
        "color": "#7CFC00",
        "tamano": 80,
        "zorder": 3,
    },
    {
        "nivel": 3,
        "count": 32,
        "rol": "Semillas de red global",
        "radio": 1.0,
        "color": "#FF4500",
        "tamano": 40,
        "zorder": 2,
    },
]

DIRECTORIO_SALIDA_DEFAULT = "salidas_qcal"
NOMBRE_ARCHIVO_DEFAULT = "constelacion_51_nodos.png"


def _calcular_posiciones_nodo(nivel_cfg: dict) -> tuple:
    """Calcula ángulos y radios para todos los nodos de un nivel."""
    count = nivel_cfg["count"]
    radio = nivel_cfg["radio"]

    if count == 1:
        angulos = np.array([0.0])
        radios = np.array([0.0])
    else:
        angulos = np.linspace(0, 2 * math.pi, count, endpoint=False)
        radios = np.full(count, radio)

    return angulos, radios


def generar_datos_constelacion() -> list:
    """
    Genera la lista de todos los nodos con sus posiciones y atributos.

    Returns
    -------
    list of dict
        Cada diccionario tiene: nivel, rol, angulo_rad, radio, color, tamano.
    """
    nodos = []
    for nivel_cfg in NIVELES:
        angulos, radios = _calcular_posiciones_nodo(nivel_cfg)
        for idx in range(nivel_cfg["count"]):
            nodos.append({
                "nivel": nivel_cfg["nivel"],
                "rol": nivel_cfg["rol"],
                "angulo_rad": float(angulos[idx]),
                "radio": float(radios[idx]),
                "color": nivel_cfg["color"],
                "tamano": nivel_cfg["tamano"],
                "zorder": nivel_cfg["zorder"],
            })
    return nodos


def dibujar_constelacion(
    ruta_salida: Optional[str] = None,
    dpi: int = 150,
    mostrar_lineas_anillo: bool = True,
    mostrar_etiquetas: bool = True,
) -> str:
    """
    Dibuja la constelación QCAL de 51 nodos y guarda la figura.

    Parameters
    ----------
    ruta_salida : str, opcional
        Ruta completa del archivo PNG. Si es None se usa el valor por defecto:
        ``salidas_qcal/constelacion_51_nodos.png``.
    dpi : int
        Resolución de la imagen (por defecto 150).
    mostrar_lineas_anillo : bool
        Si True, dibuja anillos de guía para cada nivel.
    mostrar_etiquetas : bool
        Si True, añade texto con el rol de cada nivel en el primer nodo.

    Returns
    -------
    str
        Ruta absoluta del archivo guardado.
    """
    if ruta_salida is None:
        ruta_salida = os.path.join(DIRECTORIO_SALIDA_DEFAULT, NOMBRE_ARCHIVO_DEFAULT)

    # Crear directorio si no existe
    directorio = os.path.dirname(os.path.abspath(ruta_salida))
    os.makedirs(directorio, exist_ok=True)

    nodos = generar_datos_constelacion()

    # ---- Figura ----
    fig = plt.figure(figsize=(10, 10), facecolor="#0A0A1A")
    ax = fig.add_subplot(111, projection="polar")
    ax.set_facecolor("#0A0A1A")

    # ---- Anillos de guía ----
    if mostrar_lineas_anillo:
        for nivel_cfg in NIVELES:
            if nivel_cfg["radio"] > 0:
                ring_theta = np.linspace(0, 2 * math.pi, 500)
                ring_r = np.full(500, nivel_cfg["radio"])
                ax.plot(
                    ring_theta, ring_r,
                    color=nivel_cfg["color"],
                    alpha=0.15,
                    linewidth=0.8,
                    zorder=1,
                )

    # ---- Nodos ----
    for nodo in nodos:
        ax.scatter(
            nodo["angulo_rad"],
            nodo["radio"],
            c=nodo["color"],
            s=nodo["tamano"],
            zorder=nodo["zorder"],
            edgecolors="white",
            linewidths=0.3,
            alpha=0.92,
        )

    # ---- Etiquetas de nivel ----
    if mostrar_etiquetas:
        for nivel_cfg in NIVELES:
            if nivel_cfg["radio"] == 0.0:
                # Nodo central: etiqueta arriba
                ax.annotate(
                    "Maestro\n141.70001 Hz",
                    xy=(0, 0),
                    xytext=(0.5, 0.08),
                    textcoords="axes fraction",
                    color=nivel_cfg["color"],
                    fontsize=7,
                    ha="center",
                    fontweight="bold",
                )
            else:
                # Primer nodo del anillo: etiqueta exterior
                angulo_label = 0.0
                radio_label = nivel_cfg["radio"] + 0.07
                ax.annotate(
                    nivel_cfg["rol"],
                    xy=(angulo_label, nivel_cfg["radio"]),
                    xytext=(angulo_label, radio_label),
                    color=nivel_cfg["color"],
                    fontsize=6,
                    ha="center",
                    alpha=0.85,
                )

    # ---- Leyenda ----
    parches = [
        mpatches.Patch(
            color=cfg["color"],
            label=f"Nivel {cfg['nivel']}: {cfg['rol']} ({cfg['count']})",
        )
        for cfg in NIVELES
    ]
    ax.legend(
        handles=parches,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        fontsize=7,
        framealpha=0.25,
        labelcolor="white",
        facecolor="#0A0A1A",
        edgecolor="#444444",
    )

    # ---- Estilo ejes ----
    ax.set_rticks([1.0 / 3.0, 2.0 / 3.0, 1.0])
    ax.set_yticklabels(["Nivel 1", "Nivel 2", "Nivel 3"], color="#888888", fontsize=6)
    ax.tick_params(colors="#888888", labelsize=6)
    ax.spines["polar"].set_color("#333355")
    ax.grid(color="#222244", linestyle="--", linewidth=0.5, alpha=0.5)

    # ---- Título ----
    ax.set_title(
        "Constelación QCAL 141.70001 Hz — 51 Nodos",
        color="white",
        fontsize=13,
        fontweight="bold",
        pad=20,
    )

    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    return os.path.abspath(ruta_salida)


if __name__ == "__main__":
    ruta = dibujar_constelacion()
    print(f"Diagrama guardado en: {ruta}")
    nodos = generar_datos_constelacion()
    print(f"Total nodos generados: {len(nodos)}")
    conteo = {}
    for n in nodos:
        conteo[n["nivel"]] = conteo.get(n["nivel"], 0) + 1
    print(f"Por nivel: {conteo}")
