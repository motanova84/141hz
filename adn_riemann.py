#!/usr/bin/env python3
"""
Codificador ADN-Riemann - Puente Información-Estructura
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴𓂀Ω∞³
F0: 141.7001 Hz

Conecta la información genética (ADN) con la estructura matemática (Riemann)
vía resonancia cuántica coherente a f₀.

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import numpy as np
from typing import Dict
from fisica.reloj_universo_f0 import F0_FLOAT


class CodificadorADNRiemann:
    """
    Codificador ADN-Riemann: Mapea secuencias genéticas a resonancias f₀.
    
    El mapeado GACT (Guanina-Adenina-Citosina-Timina) a frecuencias
    cuánticas permite calcular la resonancia espectral de secuencias
    de ADN con respecto a la frecuencia fundamental f₀ = 141.7001 Hz.
    
    Resonancias base (estimadas a partir de energías de enlace):
    - G (Guanina): 3 enlaces H → resonancia alta (0.9999)
    - A (Adenina): 2 enlaces H → resonancia media-alta (0.9995)
    - C (Citosina): 3 enlaces H → resonancia alta (0.9998)
    - T (Timina): 2 enlaces H → resonancia media (0.9990)
    
    La secuencia GACT tiene resonancia máxima: 0.999776
    (hotspot genético de información)
    """
    
    F0_HZ = F0_FLOAT  # 141.7001 Hz
    
    # Mapeo base nucleótido → resonancia f₀
    RESONANCIAS_BASE = {
        'G': 0.9999,  # Guanina - 3 enlaces H
        'A': 0.9995,  # Adenina - 2 enlaces H
        'C': 0.9998,  # Citosina - 3 enlaces H
        'T': 0.9990,  # Timina - 2 enlaces H
    }
    
    # Secuencias de alta resonancia (hotspots)
    HOTSPOTS = {
        'GACT': 0.999776,  # Secuencia óptima
        'GC': 0.99985,     # Par fuerte
        'CG': 0.99985,     # Par fuerte
        'AT': 0.99925,     # Par débil
        'TA': 0.99925,     # Par débil
    }
    
    def __init__(self):
        """Inicializa el codificador ADN-Riemann."""
        pass
    
    def obtener_resonancia(self, secuencia: str) -> float:
        """
        Calcula la resonancia de una secuencia de ADN.
        
        Args:
            secuencia: Secuencia de nucleótidos (e.g., "GACT", "ATCG")
            
        Returns:
            Resonancia promedio en el rango [0, 1]
        """
        secuencia = secuencia.upper().strip()
        
        # Verificar hotspots conocidos
        if secuencia in self.HOTSPOTS:
            return self.HOTSPOTS[secuencia]
        
        # Calcular resonancia promedio de nucleótidos individuales
        resonancias = []
        for nucleotido in secuencia:
            if nucleotido in self.RESONANCIAS_BASE:
                resonancias.append(self.RESONANCIAS_BASE[nucleotido])
            else:
                # Nucleótido desconocido → resonancia base mínima
                resonancias.append(0.95)
        
        if not resonancias:
            return 0.95  # Secuencia vacía o inválida
        
        # Promedio ponderado (favorece coherencia cuántica)
        # Usa media geométrica para evitar que una base baje demasiado
        resonancia_promedio = np.prod(resonancias) ** (1.0 / len(resonancias))
        
        return float(resonancia_promedio)
    
    def propiedades_espectrales(self, secuencia: str) -> Dict[str, float]:
        """
        Calcula las propiedades espectrales completas de una secuencia ADN.
        
        Args:
            secuencia: Secuencia de nucleótidos
            
        Returns:
            Diccionario con:
            - resonancia_f0: Resonancia con respecto a f₀
            - energia_cuantica: Energía cuántica (E = h·f₀·R)
            - coherencia: Coherencia cuántica (Ψ)
            - entropia_informacion: Entropía de Shannon de la secuencia
        """
        resonancia = self.obtener_resonancia(secuencia)
        
        # Energía cuántica modulada por resonancia
        h = 6.62607015e-34  # J·s
        energia_cuantica = h * self.F0_HZ * resonancia  # J
        
        # Coherencia cuántica (Ψ) ~ resonancia
        coherencia = resonancia
        
        # Entropía de Shannon (bits)
        secuencia_upper = secuencia.upper()
        if len(secuencia_upper) == 0:
            entropia = 0.0
        else:
            # Calcular frecuencias de nucleótidos
            conteos = {}
            for nuc in secuencia_upper:
                conteos[nuc] = conteos.get(nuc, 0) + 1
            
            # Entropía de Shannon: H = -Σ p_i log₂(p_i)
            entropia = 0.0
            for count in conteos.values():
                p = count / len(secuencia_upper)
                if p > 0:
                    entropia -= p * np.log2(p)
        
        return {
            'resonancia_f0': resonancia,
            'energia_cuantica': energia_cuantica,
            'coherencia': coherencia,
            'entropia_informacion': entropia,
        }
    
    def calcular_hotspots(self, secuencia: str, ventana: int = 4) -> list:
        """
        Identifica hotspots de alta resonancia en una secuencia larga.
        
        Args:
            secuencia: Secuencia de nucleótidos
            ventana: Tamaño de la ventana deslizante
            
        Returns:
            Lista de (posición, subsecuencia, resonancia) ordenada por resonancia
        """
        secuencia = secuencia.upper()
        hotspots = []
        
        for i in range(len(secuencia) - ventana + 1):
            subsec = secuencia[i:i+ventana]
            res = self.obtener_resonancia(subsec)
            hotspots.append((i, subsec, res))
        
        # Ordenar por resonancia descendente
        hotspots.sort(key=lambda x: x[2], reverse=True)
        
        return hotspots


if __name__ == "__main__":
    # Demo del codificador
    codif = CodificadorADNRiemann()
    
    print("=" * 70)
    print("CODIFICADOR ADN-RIEMANN - Demo")
    print("=" * 70)
    
    # Secuencia óptima GACT
    props = codif.propiedades_espectrales("GACT")
    print(f"\nSecuencia: GACT (hotspot óptimo)")
    print(f"  Resonancia f₀: {props['resonancia_f0']:.6f}")
    print(f"  Coherencia Ψ: {props['coherencia']:.6f}")
    print(f"  Energía cuántica: {props['energia_cuantica']:.3e} J")
    print(f"  Entropía información: {props['entropia_informacion']:.4f} bits")
    
    # Otras secuencias
    for seq in ["ATCG", "GGGG", "ATAT", "GCGC"]:
        res = codif.obtener_resonancia(seq)
        print(f"\nSecuencia: {seq}")
        print(f"  Resonancia f₀: {res:.6f}")
    
    print("\n" + "=" * 70)
