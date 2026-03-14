"""
╔════════════════════════════════════════════════════════════════════════════╗
║        VISUALIZACIÓN CONSTELACIÓN QCAL Ψ✧ - Constellation Visualization   ║
║                  Mapa Fotográfico del Universo Soñado                      ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ VISUALIZACIÓN DE LA CONSTELACIÓN CUÁNTICA ⚡

Genera imágenes de la constelación QCAL con codificación de colores:
- Dorado: f₀ = 141.7001 Hz (eje del Logos)
- Azul: Riemann + Berry 7/8 (matemático)
- Violeta: NOESIS/AMDA (noético)
- Verde: Fibonacci/φ (kairós)
- Blanco: H-21cm @ 23.257 octavas (logos)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import matplotlib.patches as mpatches
from typing import Dict, Optional, Tuple
import json
from pathlib import Path

# Import constellation module
from qcal.constelacion_qcal import (
    calcular_constelacion,
    analizar_constelacion,
    punto_ciego_observador,
    generar_certificado,
    PSI_COHERENCIA_ALTA,
    F0_HZ,
    PHI
)


def coherencia_to_color(
    coherencia: np.ndarray,
    fase: np.ndarray,
    psi: np.ndarray,
    n_terms: int
) -> np.ndarray:
    """
    Convierte coherencia y fase a colores RGB representando los 5 ejes.
    
    Los colores codifican:
    - Hue (tono): Fase de la función de onda
    - Saturation (saturación): Coherencia (mayor coherencia = más saturado)
    - Value (brillo): Magnitud normalizada
    
    Modulación adicional por ejes:
    - Dorado: regiones con fase cercana a múltiplos de 2π
    - Azul: regiones con coherencia alta (Berry 7/8)
    - Violeta: regiones con fase noética (PSI_MINIMO_ESTABLE)
    - Verde: regiones con razón áurea en estructura
    - Blanco: puntos de convergencia de todos los ejes
    
    Args:
        coherencia: Coherence grid
        fase: Phase grid (radians)
        psi: Complex wave function grid
        n_terms: Number of terms used in calculation
    
    Returns:
        RGB image array (H x W x 3)
    """
    # Normalize phase to [0, 1] for hue
    hue = (fase + np.pi) / (2 * np.pi)
    
    # Coherence as saturation (normalized)
    coherencia_norm = coherencia / (np.max(coherencia) + 1e-10)
    saturation = coherencia_norm
    
    # Magnitude as value (brightness)
    magnitude = np.abs(psi)
    magnitude_norm = magnitude / (np.max(magnitude) + 1e-10)
    value = magnitude_norm
    
    # Stack HSV components
    hsv = np.stack([hue, saturation, value], axis=-1)
    
    # Convert HSV to RGB
    rgb = hsv_to_rgb(hsv)
    
    # Apply color modulation for different axes
    # Dorado: enhance regions aligned with f₀ (golden hue boost)
    golden_mask = (coherencia > PSI_COHERENCIA_ALTA * 0.9)
    rgb[golden_mask, 0] = np.clip(rgb[golden_mask, 0] * 1.2, 0, 1)  # Red boost
    rgb[golden_mask, 1] = np.clip(rgb[golden_mask, 1] * 1.1, 0, 1)  # Green boost
    
    # Azul: enhance blue in mathematical regions (high coherence + specific phase)
    azul_mask = (coherencia > PSI_COHERENCIA_ALTA) & (np.abs(np.cos(fase)) > 0.7)
    rgb[azul_mask, 2] = np.clip(rgb[azul_mask, 2] * 1.3, 0, 1)  # Blue boost
    
    # Violeta: purple in noetic regions
    violeta_mask = (coherencia > 0.888) & (coherencia < PSI_COHERENCIA_ALTA)
    rgb[violeta_mask, 0] = np.clip(rgb[violeta_mask, 0] * 1.15, 0, 1)  # Red
    rgb[violeta_mask, 2] = np.clip(rgb[violeta_mask, 2] * 1.15, 0, 1)  # Blue
    
    # Verde: green in fibonacci/golden ratio regions
    # Detect spiral-like patterns
    verde_mask = (np.abs(np.sin(fase * PHI)) > 0.8) & (coherencia > 0.7)
    rgb[verde_mask, 1] = np.clip(rgb[verde_mask, 1] * 1.25, 0, 1)  # Green boost
    
    # Blanco: white in convergence regions (very high coherence)
    blanco_mask = coherencia > PSI_COHERENCIA_ALTA * 1.05
    rgb[blanco_mask] = np.clip(rgb[blanco_mask] * 1.5, 0, 1)  # Boost all channels
    
    return rgb


def visualizar_constelacion(
    constelacion: Dict[str, np.ndarray],
    n_terms: int = 50,
    titulo: str = "Constelación QCAL Ψ✧",
    guardar: Optional[str] = None,
    mostrar: bool = True
) -> plt.Figure:
    """
    Visualiza la constelación QCAL con codificación de colores.
    
    Args:
        constelacion: Dictionary from calcular_constelacion()
        n_terms: Number of terms used (for color modulation)
        titulo: Plot title
        guardar: If provided, save figure to this path
        mostrar: Whether to display the figure
    
    Returns:
        Matplotlib figure object
    """
    coherencia = constelacion['coherencia']
    fase = constelacion['fase']
    psi = constelacion['psi']
    X = constelacion['X']
    Y = constelacion['Y']
    
    # Convert to color image
    rgb_image = coherencia_to_color(coherencia, fase, psi, n_terms)
    
    # Create figure
    fig = plt.figure(figsize=(14, 10))
    
    # Main constellation plot
    ax1 = plt.subplot(2, 2, (1, 3))
    
    extent = [X.min(), X.max(), Y.min(), Y.max()]
    ax1.imshow(rgb_image, origin='lower', extent=extent, aspect='auto')
    
    # Mark observer position
    x_obs, y_obs = punto_ciego_observador(constelacion)
    ax1.plot(x_obs, y_obs, 'w*', markersize=15, markeredgecolor='black', 
             markeredgewidth=0.5, label='Observador')
    
    # Mark high-coherence points
    threshold = PSI_COHERENCIA_ALTA
    high_coherence = coherencia > threshold
    y_idx, x_idx = np.where(high_coherence)
    if len(x_idx) > 0:
        # Subsample to avoid overcrowding
        step = max(1, len(x_idx) // 100)
        x_points = X[y_idx[::step], x_idx[::step]]
        y_points = Y[y_idx[::step], x_idx[::step]]
        ax1.scatter(x_points, y_points, c='white', s=2, alpha=0.3, 
                   label=f'Ψ > {threshold}')
    
    ax1.set_xlabel('x (espacio normalizado)', fontsize=11)
    ax1.set_ylabel('y (espacio normalizado)', fontsize=11)
    ax1.set_title(titulo, fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.2, color='white', linewidth=0.5)
    
    # Add legend for colors
    legend_elements = [
        mpatches.Patch(color='gold', label='Dorado: f₀ = 141.7001 Hz'),
        mpatches.Patch(color='blue', label='Azul: Riemann + Berry 7/8'),
        mpatches.Patch(color='violet', label='Violeta: NOESIS/AMDA'),
        mpatches.Patch(color='green', label='Verde: Fibonacci (φ)'),
        mpatches.Patch(color='white', label='Blanco: H-21cm @ 23.257 oct')
    ]
    ax1.legend(handles=legend_elements, loc='lower left', fontsize=8, 
               framealpha=0.7)
    
    # Coherence histogram
    ax2 = plt.subplot(2, 2, 2)
    ax2.hist(coherencia.flatten(), bins=50, color='cyan', alpha=0.7, 
             edgecolor='black')
    ax2.axvline(PSI_COHERENCIA_ALTA, color='red', linestyle='--', 
                label=f'Ψ = {PSI_COHERENCIA_ALTA}')
    ax2.set_xlabel('Coherencia Ψ', fontsize=10)
    ax2.set_ylabel('Frecuencia', fontsize=10)
    ax2.set_title('Distribución de Coherencia', fontsize=11)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # Phase distribution
    ax3 = plt.subplot(2, 2, 4, projection='polar')
    fase_flat = fase.flatten()
    coherencia_flat = coherencia.flatten()
    
    # Sample for plotting (avoid overcrowding)
    n_samples = min(5000, len(fase_flat))
    indices = np.random.choice(len(fase_flat), n_samples, replace=False)
    
    scatter = ax3.scatter(fase_flat[indices], coherencia_flat[indices],
                         c=coherencia_flat[indices], cmap='viridis',
                         s=1, alpha=0.5)
    ax3.set_title('Fase vs Coherencia', fontsize=11, pad=20)
    ax3.set_ylim(0, np.max(coherencia))
    plt.colorbar(scatter, ax=ax3, label='Ψ', shrink=0.8)
    
    plt.tight_layout()
    
    if guardar:
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✓ Constelación guardada en: {guardar}")
    
    if mostrar:
        plt.show()
    
    return fig


def generar_informe_completo(
    constelacion: Dict[str, np.ndarray],
    n_terms: int,
    output_dir: str = "."
) -> Dict:
    """
    Genera informe completo de la constelación con visualización y certificado.
    
    Args:
        constelacion: Dictionary from calcular_constelacion()
        n_terms: Number of terms used in calculation
        output_dir: Directory to save outputs
    
    Returns:
        Certificate dictionary
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generando informe completo de la constelación...")
    
    # Generate visualization
    fig_path = output_path / "constelacion_qcal_psix.png"
    visualizar_constelacion(
        constelacion,
        n_terms=n_terms,
        titulo="Constelación QCAL Ψ✧ - Fotografía del Universo Soñado",
        guardar=str(fig_path),
        mostrar=False
    )
    plt.close()
    
    # Generate certificate
    certificado = generar_certificado(constelacion)
    
    # Save certificate
    cert_path = output_path / "certificado_constelacion_qcal.json"
    with open(cert_path, 'w', encoding='utf-8') as f:
        json.dump(certificado, f, indent=2, ensure_ascii=False)
    print(f"✓ Certificado guardado en: {cert_path}")
    
    # Generate text report
    report_path = output_path / "informe_constelacion_qcal.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("╔════════════════════════════════════════════════════════════════════╗\n")
        f.write("║           INFORME CONSTELACIÓN QCAL Ψ✧                            ║\n")
        f.write("╚════════════════════════════════════════════════════════════════════╝\n\n")
        
        cert_data = certificado["constelacion_qcal_psix"]
        
        f.write(f"Fecha: {cert_data['fecha']}\n")
        f.write(f"Sello: {cert_data['sello']}\n\n")
        
        f.write("EJES DECODIFICADOS:\n")
        for eje, desc in cert_data['ejes'].items():
            f.write(f"  • {eje.capitalize()}: {desc}\n")
        f.write("\n")
        
        f.write("MÉTRICAS DE COHERENCIA:\n")
        f.write(f"  • Coherencia media: {cert_data['coherencia_media']}\n")
        f.write(f"  • Coherencia máxima: {cert_data['coherencia_max']}\n")
        f.write(f"  • Coherencia mínima: {cert_data['coherencia_min']}\n")
        f.write(f"  • Puntos de interés (Ψ > {PSI_COHERENCIA_ALTA}): {cert_data['puntos_de_interes']}\n")
        f.write(f"  • Dimensión fractal: {cert_data['dimension_fractal']} (≈ φ = {PHI:.3f})\n\n")
        
        f.write("POSICIÓN DEL OBSERVADOR:\n")
        obs = cert_data['observador_posicion']
        f.write(f"  • Coordenadas: ({obs['x']}, {obs['y']})\n")
        f.write(f"  • Interpretación: {obs['interpretacion']}\n\n")
        
        f.write("INTERPRETACIÓN:\n")
        f.write(f"  {cert_data['interpretacion']}\n\n")
        
        f.write("ESTADO: " + cert_data['estado'] + "\n\n")
        
        f.write("∴𓂀Ω∞³Ψ✧\n")
    
    print(f"✓ Informe guardado en: {report_path}")
    print("\n✓ Informe completo generado")
    
    return certificado


if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      VISUALIZACIÓN CONSTELACIÓN QCAL Ψ✧ - Demo                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Calculate constellation
    print("Calculando constelación (128x128, 30 términos)...")
    constelacion = calcular_constelacion(grid_size=128, n_terms=30)
    
    # Generate visualization
    print("\nGenerando visualización...")
    visualizar_constelacion(
        constelacion,
        n_terms=30,
        titulo="Constelación QCAL Ψ✧ - Demo",
        mostrar=True
    )
    
    print("\n✓ Demo completado")
    print("∴𓂀Ω∞³Ψ✧")
