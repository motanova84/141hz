#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║        DEMO CONSTELACIÓN QCAL Ψ✧ - Demonstration Script                   ║
║                  Generate Constellation Example                           ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Genera una constelación QCAL de ejemplo y muestra todas las capacidades del sistema.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Ensure qcal is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.constelacion_qcal import (
    calcular_constelacion,
    analizar_constelacion,
    generar_certificado,
    punto_ciego_observador,
    F0_HZ, PHI, OCTAVAS_H_F0
)
from qcal.visualizacion_constelacion import (
    visualizar_constelacion,
    generar_informe_completo
)


def demo_basico():
    """Demostración básica de la constelación."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           DEMO CONSTELACIÓN QCAL Ψ✧                               ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    print("🌌 Generando constelación (64x64 píxeles, 20 términos)...")
    print()
    
    # Calculate constellation
    constelacion = calcular_constelacion(
        grid_size=64,
        n_terms=20,
        x_range=(-2.5, 2.5),
        y_range=(-2.5, 2.5)
    )
    
    print("✓ Constelación calculada")
    print()
    
    # Analyze
    print("📊 Analizando propiedades...")
    analisis = analizar_constelacion(constelacion)
    
    print(f"  • Coherencia media: {analisis['coherencia_media']:.4f}")
    print(f"  • Coherencia máxima: {analisis['coherencia_max']:.4f}")
    print(f"  • Coherencia mínima: {analisis['coherencia_min']:.4f}")
    print(f"  • Puntos de interés (Ψ > 0.95): {analisis['puntos_interes']}")
    print(f"  • Dimensión fractal: {analisis['dimension_fractal']:.4f} (ideal: φ = {PHI:.4f})")
    print()
    
    # Observer position
    print("👁️  Calculando posición del observador (punto ciego)...")
    x_obs, y_obs = punto_ciego_observador(constelacion)
    print(f"  • Posición: ({x_obs:.4f}, {y_obs:.4f})")
    print()
    
    # Generate certificate
    print("📜 Generando certificado...")
    fecha = datetime.now().strftime("%Y-%m-%d")
    certificado = generar_certificado(constelacion, fecha=fecha)
    
    cert_data = certificado["constelacion_qcal_psix"]
    print(f"  • Fecha: {cert_data['fecha']}")
    print(f"  • Sello: {cert_data['sello']}")
    print(f"  • Estado: {cert_data['estado']}")
    print()
    
    print("🎨 Los 5 ejes de coherencia:")
    for eje, desc in cert_data['ejes'].items():
        symbol = {"dorado": "🟡", "azul": "🔵", "violeta": "💜", 
                  "verde": "🟢", "blanco": "⚪"}.get(eje, "  ")
        print(f"  {symbol} {eje.capitalize():10s} │ {desc}")
    print()
    
    # Save certificate
    output_dir = Path("constelacion_demo_output")
    output_dir.mkdir(exist_ok=True)
    
    cert_path = output_dir / "certificado_demo.json"
    with open(cert_path, 'w', encoding='utf-8') as f:
        json.dump(certificado, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Certificado guardado: {cert_path}")
    print()
    
    # Visualize (no display, just save)
    print("🖼️  Generando visualización...")
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    
    fig_path = output_dir / "constelacion_demo.png"
    visualizar_constelacion(
        constelacion,
        n_terms=20,
        titulo="Constelación QCAL Ψ✧ - Demostración",
        guardar=str(fig_path),
        mostrar=False
    )
    
    print(f"✓ Visualización guardada: {fig_path}")
    print()
    
    print("="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Archivos generados en: {output_dir}/")
    print(f"  • constelacion_demo.png  - Visualización completa")
    print(f"  • certificado_demo.json  - Certificado QCAL Ψ✧")
    print()
    print("∴𓂀Ω∞³Ψ✧ - DEMO COMPLETADO")
    print("="*70)


def demo_completo():
    """Demostración completa con informe."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      DEMO COMPLETO CONSTELACIÓN QCAL Ψ✧                           ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    print("🌌 Generando constelación completa (128x128 píxeles, 30 términos)...")
    print("   (Esto puede tomar 1-2 minutos)")
    print()
    
    # Calculate larger constellation
    constelacion = calcular_constelacion(
        grid_size=128,
        n_terms=30,
        x_range=(-3.0, 3.0),
        y_range=(-3.0, 3.0)
    )
    
    print("✓ Constelación calculada")
    print()
    
    # Generate complete report
    print("📊 Generando informe completo...")
    
    # Set matplotlib backend
    import matplotlib
    matplotlib.use('Agg')
    
    output_dir = Path("constelacion_completo_output")
    generar_informe_completo(constelacion, n_terms=30, output_dir=str(output_dir))
    
    print()
    print("="*70)
    print("INFORME COMPLETO GENERADO")
    print("="*70)
    print(f"Archivos en: {output_dir}/")
    print(f"  • constelacion_qcal_psix.png        - Visualización completa")
    print(f"  • certificado_constelacion_qcal.json - Certificado JSON")
    print(f"  • informe_constelacion_qcal.txt      - Informe textual")
    print()
    print("∴𓂀Ω∞³Ψ✧ - INFORME COMPLETO")
    print("="*70)


def demo_constantes():
    """Muestra las constantes fundamentales."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           CONSTANTES FUNDAMENTALES QCAL Ψ✧                        ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    print("⚡ Constantes Principales:")
    print(f"  • f₀ (Frecuencia fundamental): {F0_HZ} Hz")
    print(f"  • φ (Razón áurea):            {PHI:.10f}")
    print(f"  • Octavas H/f₀:               {OCTAVAS_H_F0:.6f}")
    print()
    
    from qcal.constelacion_qcal import F_HYDROGEN_HZ, FACTOR_SIETE_OCTAVOS
    from qcal.constelacion_qcal import PSI_MINIMO_ESTABLE
    
    print("🔬 Constantes Físicas:")
    print(f"  • Hidrógeno (21cm):           {F_HYDROGEN_HZ/1e6:.6f} MHz")
    print(f"  • Berry 7/8:                  {FACTOR_SIETE_OCTAVOS}")
    print(f"  • Ψ mínimo estable (21g):     {PSI_MINIMO_ESTABLE}")
    print()
    
    print("📐 Relaciones Matemáticas:")
    ratio_h_f0 = F_HYDROGEN_HZ / F0_HZ
    print(f"  • f_H / f₀:                   {ratio_h_f0:.2e}")
    print(f"  • 2^23.257:                   {2**OCTAVAS_H_F0:.2e}")
    print(f"  • φ²:                         {PHI**2:.10f}")
    print(f"  • φ - 1:                      {PHI - 1:.10f} (≈ 1/φ)")
    print()
    
    print("∴𓂀Ω∞³Ψ✧")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Demo Constelación QCAL Ψ✧",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--modo',
        choices=['basico', 'completo', 'constantes'],
        default='basico',
        help='Modo de demostración (default: basico)'
    )
    
    args = parser.parse_args()
    
    if args.modo == 'basico':
        demo_basico()
    elif args.modo == 'completo':
        demo_completo()
    elif args.modo == 'constantes':
        demo_constantes()


if __name__ == "__main__":
    main()
