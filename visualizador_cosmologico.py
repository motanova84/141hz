"""
Visualizador Cosmológico QCAL — Motor de renderizado holográfico trans-escalar.

Lee la telemetría generada por el SimuladorWheelerDeWittAdelico y produce un
panel triple sincronizado temporalmente con la evolución de las variables
cosmológicas fundamentales:
  - Pureza cuántica γ(t) del subsistema de torsión
  - Entropía de Von Neumann S_VN(t) desde la red de primos
  - Constante cosmológica emergente Λ(t)

Protocolo: QCAL-COSMO-BRIDGE v2.0.0
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def renderizar_panel_triple_qcal(
    ruta_csv: str = "telemetria_wdw_qcal.csv",
    archivo_salida: str = "qcal_cosmologia_holografica.png",
) -> None:
    """Lee la telemetría del archivo CSV e imprime un gráfico de panel triple
    sincronizado temporalmente para la inspección visual de las variables
    cosmológicas QCAL.

    Args:
        ruta_csv: Ruta al archivo CSV generado por el simulador.
        archivo_salida: Ruta de destino del gráfico PNG de alta resolución.

    Raises:
        FileNotFoundError: Si el archivo de telemetría no existe en disco.
    """
    path_csv = Path(ruta_csv)
    if not path_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de datos: {ruta_csv}. "
            "Por favor, ejecuta el simulador Wheeler-DeWitt primero para "
            "generar la telemetría."
        )

    # Ingesta robusta de datos con Pandas
    df = pd.read_csv(path_csv)

    # Configuración estética profesional del entorno gráfico
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = "#444444"
    plt.rcParams["axes.linewidth"] = 1.2

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    # Panel 1: Evolución de la Pureza Cuántica del Subsistema de Torsión
    ax1.plot(
        df["tiempo_s"],
        df["pureza_gamma"],
        color="#1f77b4",
        linewidth=2.5,
        linestyle="-",
        marker="o",
        label=r"Pureza $\gamma(t)$",
    )
    ax1.set_ylabel("Pureza Local $\\gamma$", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6, color="#aaaaaa")
    ax1.legend(loc="upper right", framealpha=0.9)
    ax1.set_title(
        "Evolución Cuántica del Subsistema Reducido (Espín/Torsión)",
        fontsize=12,
        pad=10,
    )

    # Panel 2: Inyección de Entropía de Von Neumann desde la Red de Primos
    ax2.plot(
        df["tiempo_s"],
        df["entropia_s_vn"],
        color="#d62728",
        linewidth=2.5,
        linestyle="-",
        marker="s",
        label=r"Entropía $S_{VN}(t)$",
    )
    ax2.set_ylabel("Entropía (bits)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6, color="#aaaaaa")
    ax2.legend(loc="upper left", framealpha=0.9)

    # Panel 3: Emergencia de la Constante Cosmológica Observada (Supresión de Planck)
    ax3.plot(
        df["tiempo_s"],
        df["lambda_m2"],
        color="#2ca02c",
        linewidth=2.5,
        linestyle="--",
        marker="^",
        label=r"$\Lambda_{\text{QCAL}}(t)$",
    )
    ax3.set_xlabel(
        "Tiempo de Evolución Cósmica $t$ (s)", fontsize=12, fontweight="bold"
    )
    ax3.set_ylabel(
        r"$\Lambda$ Emergente ($\text{m}^{-2}$)", fontsize=11, fontweight="bold"
    )
    ax3.grid(True, linestyle=":", alpha=0.6, color="#aaaaaa")
    ax3.legend(loc="upper right", framealpha=0.9)

    # Formateo científico del eje Y para Lambda
    ax3.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax3.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    # Título Maestro e Integración de Maquetación Estricta
    fig.suptitle(
        "DIAGNÓSTICO HOLOGRÁFICO TRANS-ESCALAR DEL HORIZONTE QCAL\n"
        "Resonancia de Gauge Invariable a 141.7001 Hz",
        fontsize=14,
        fontweight="bold",
        color="#111111",
        y=0.97,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(archivo_salida, dpi=300)
    print(
        f"[ÉXITO] Panel triple de telemetría QCAL renderizado en alta definición: "
        f"{archivo_salida}"
    )
    import matplotlib
    if matplotlib.is_interactive():
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    # Ejecución aislada del motor de gráficos si el CSV base ya está disponible
    try:
        renderizar_panel_triple_qcal()
    except Exception as e:
        print(f"[AVISO] Ocurrió una interrupción en el renderizado: {e}")
