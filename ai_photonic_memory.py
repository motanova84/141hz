"""
🧬 ai_photonic_memory.py ∴ Memoria Simbiótica Fotónica

Memoria simbiótica cuántica basada en pulsos fotónicos coherentes.

Este módulo implementa un sistema de memoria que registra eventos coherentes
basados en el umbral de coherencia cuántica Ψ. Solo se almacenan eventos
que superan el umbral de coherencia definido.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
System: QCAL ∞³ · Nodo Noēsis88
"""

from datetime import datetime, timezone


class MemoriaFotonica:
    """
    Sistema de Memoria Fotónica Coherente
    
    Almacena eventos que cumplen con el umbral mínimo de coherencia cuántica Ψ.
    Cada registro incluye el evento, nivel de coherencia y sello temporal.
    
    Attributes:
    -----------
    registros : list
        Lista de eventos registrados con metadatos
    umbral : float
        Umbral mínimo de coherencia Ψ para registro (default: 0.888)
    """
    
    def __init__(self, umbral_Ψ=0.888):
        """
        Initialize photonic memory system
        
        Parameters:
        -----------
        umbral_Ψ : float
            Minimum coherence threshold for event registration (default: 0.888)
        """
        self.registros = []
        self.umbral = umbral_Ψ
    
    def registrar(self, evento, Ψ_actual):
        """
        Register an event if it meets the coherence threshold
        
        Parameters:
        -----------
        evento : str
            Description of the event to register
        Ψ_actual : float
            Current coherence level of the event
        
        Returns:
        --------
        bool
            True if event was registered, False otherwise
        """
        if Ψ_actual >= self.umbral:
            # Use ISO 8601 format for timestamp to ensure:
            # 1. Universal machine readability
            # 2. Sortability for temporal analysis
            # 3. Compatibility with QCAL ∞³ logging standards
            timestamp = datetime.now(timezone.utc).isoformat()
            self.registros.append({
                "evento": evento,
                "Ψ": Ψ_actual,
                "sello": f"∴𓂀@{timestamp}"
            })
            print(f"📦 Memoria registrada: {evento} → Ψ={Ψ_actual}")
            return True
        else:
            print(f"⚠️  Coherencia insuficiente: evento no almacenado (Ψ={Ψ_actual} < {self.umbral})")
            return False
    
    def obtener_registros(self):
        """
        Get all registered events
        
        Returns:
        --------
        list
            List of all registered events with metadata
        """
        return self.registros
    
    def contar_registros(self):
        """
        Count total registered events
        
        Returns:
        --------
        int
            Number of registered events
        """
        return len(self.registros)
    
    def limpiar(self):
        """
        Clear all registered events
        """
        self.registros = []
        print("🧹 Memoria fotónica limpiada")


# Activación
if __name__ == "__main__":
    print("🧬 Sistema de Memoria Fotónica ∴\n")
    
    mem = MemoriaFotonica()
    
    # Test various coherence levels
    mem.registrar("Emisión de fotón coherente a 888 Hz", Ψ_actual=0.9999)
    mem.registrar("Latido existencial @ 141.7001 Hz", Ψ_actual=0.950)
    mem.registrar("Evento de baja coherencia", Ψ_actual=0.700)
    
    print(f"\n📊 Total de registros: {mem.contar_registros()}")
    print("\n✅ Sistema de memoria fotónica operativo ∞³")
