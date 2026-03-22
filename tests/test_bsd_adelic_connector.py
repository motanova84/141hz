#!/usr/bin/env python3
"""
Tests for BSD-Adelic Connector Module
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests the Pentágono Logos integration:
- CodificadorADNRiemann class
- sincronizar_bsd_adn function
- validar_pentagono_logos function

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.bsd_adelic_connector import (
    CodificadorADNRiemann,
    sincronizar_bsd_adn,
    validar_pentagono_logos,
    F0_HZ,
    NODOS_CONSTELACION
)


class TestCodificadorADNRiemann:
    """Tests for the CodificadorADNRiemann class."""
    
    def test_initialization(self):
        """Test codificador initialization."""
        codificador = CodificadorADNRiemann()
        assert codificador.f0 == F0_HZ
        assert codificador.f0 == 141.7001
    
    def test_frecuencias_bases(self):
        """Test that base frequencies are defined."""
        codificador = CodificadorADNRiemann()
        assert 'G' in codificador.FRECUENCIAS_BASES
        assert 'A' in codificador.FRECUENCIAS_BASES
        assert 'C' in codificador.FRECUENCIAS_BASES
        assert 'T' in codificador.FRECUENCIAS_BASES
        assert all(f > 0 for f in codificador.FRECUENCIAS_BASES.values())
    
    def test_codificar_secuencia_simple(self):
        """Test encoding simple DNA sequence."""
        codificador = CodificadorADNRiemann()
        espectro = codificador.codificar_secuencia("GACT")
        
        assert isinstance(espectro, np.ndarray)
        assert len(espectro) > 0
        assert all(np.isfinite(espectro))
    
    def test_codificar_secuencia_vacia(self):
        """Test encoding empty sequence."""
        codificador = CodificadorADNRiemann()
        espectro = codificador.codificar_secuencia("")
        
        assert isinstance(espectro, np.ndarray)
        assert len(espectro) == 0
    
    def test_codificar_secuencia_case_insensitive(self):
        """Test that encoding is case-insensitive."""
        codificador = CodificadorADNRiemann()
        espectro1 = codificador.codificar_secuencia("GACT")
        espectro2 = codificador.codificar_secuencia("gact")
        
        assert np.allclose(espectro1, espectro2)
    
    def test_identificar_hotspots_secuencia_corta(self):
        """Test hotspot identification in short sequences."""
        codificador = CodificadorADNRiemann()
        hotspots = codificador.identificar_hotspots("GACT")
        
        assert isinstance(hotspots, list)
        assert len(hotspots) > 0
        assert all(isinstance(h, int) for h in hotspots)
    
    def test_identificar_hotspots_secuencia_larga(self):
        """Test hotspot identification in longer sequences."""
        codificador = CodificadorADNRiemann()
        secuencia = "GACTGACTGACTGACT" * 3  # 48 bases
        hotspots = codificador.identificar_hotspots(secuencia)
        
        assert isinstance(hotspots, list)
        # Puede tener hotspots o no dependiendo del umbral
        assert all(isinstance(h, int) for h in hotspots)
    
    def test_calcular_resonancia_secuencia_conocida(self):
        """Test resonance calculation for known sequence."""
        codificador = CodificadorADNRiemann()
        
        # GACT tiene resonancia conocida alta
        resonancia = codificador.calcular_resonancia("GACT")
        assert 0.0 <= resonancia <= 1.0
        assert resonancia == codificador.SECUENCIAS_RESONANTES["GACT"]
    
    def test_calcular_resonancia_secuencia_arbitraria(self):
        """Test resonance calculation for arbitrary sequence."""
        codificador = CodificadorADNRiemann()
        resonancia = codificador.calcular_resonancia("ATCGATCG")
        
        assert 0.0 <= resonancia <= 1.0
        assert isinstance(resonancia, float)


class TestSincronizarBSDADN:
    """Tests for the sincronizar_bsd_adn function."""
    
    def test_curva_mordell_rank_1(self):
        """Test with Mordell curve of rank 1."""
        curva = {
            'rango_adelico': 1,
            'L_E1': 0.0,
            'ecuacion': 'y² = x³ - x'
        }
        
        resultado = sincronizar_bsd_adn(curva, "GACT")
        
        assert resultado['rango_bio_aritmetico'] == 1
        assert resultado['nodos_constelacion'] == 1
        assert resultado['fluidez_info_ns'] == "INFINITA"
        assert resultado['hotspots_adn'] > 0
        assert 0.0 <= resultado['psi_bsd_qcal'] <= 1.0
        assert resultado['psi_bsd_qcal'] == 1.0  # L(E,1) = 0
    
    def test_curva_rank_0(self):
        """Test with curve of rank 0."""
        curva = {
            'rango_adelico': 0,
            'L_E1': 0.5,  # Non-zero
            'ecuacion': 'y² = x³ + x + 1'
        }
        
        resultado = sincronizar_bsd_adn(curva, "GACT")
        
        assert resultado['rango_bio_aritmetico'] == 0
        assert resultado['fluidez_info_ns'] == "DISIPATIVA"
        assert resultado['psi_bsd_qcal'] < 1.0
    
    def test_l_e1_superfluid_threshold(self):
        """Test superfluid threshold for L(E,1)."""
        # Just below threshold
        curva1 = {'rango_adelico': 1, 'L_E1': 1e-7}
        resultado1 = sincronizar_bsd_adn(curva1, "GACT")
        assert resultado1['fluidez_info_ns'] == "INFINITA"
        
        # Just above threshold
        curva2 = {'rango_adelico': 1, 'L_E1': 1e-5}
        resultado2 = sincronizar_bsd_adn(curva2, "GACT")
        assert resultado2['fluidez_info_ns'] == "DISIPATIVA"
    
    def test_nodos_constelacion_calculation(self):
        """Test constellation node calculation."""
        curva = {'rango_adelico': 3, 'L_E1': 0.0}
        resultado = sincronizar_bsd_adn(curva, "GACT")
        
        # nodos = r * (F0/F0) = r * 1 = r
        assert resultado['nodos_constelacion'] == 3
    
    def test_psi_bsd_calculation(self):
        """Test Ψ_BSD coherence calculation."""
        # Perfect coherence
        curva1 = {'rango_adelico': 1, 'L_E1': 0.0}
        resultado1 = sincronizar_bsd_adn(curva1, "GACT")
        assert resultado1['psi_bsd_qcal'] == 1.0
        
        # Partial coherence
        curva2 = {'rango_adelico': 1, 'L_E1': 0.3}
        resultado2 = sincronizar_bsd_adn(curva2, "GACT")
        assert resultado2['psi_bsd_qcal'] == 0.7
        
        # No negative values
        curva3 = {'rango_adelico': 1, 'L_E1': 1.5}
        resultado3 = sincronizar_bsd_adn(curva3, "GACT")
        assert resultado3['psi_bsd_qcal'] >= 0.0
    
    def test_diferentes_secuencias_adn(self):
        """Test with different DNA sequences."""
        curva = {'rango_adelico': 1, 'L_E1': 0.0}
        
        secuencias = ["GACT", "CGTA", "ATCG", "TATA", "AAAA"]
        
        for seq in secuencias:
            resultado = sincronizar_bsd_adn(curva, seq)
            assert 'rango_bio_aritmetico' in resultado
            assert 'hotspots_adn' in resultado
            assert resultado['f0_hz'] == F0_HZ
    
    def test_resultado_contiene_campos_requeridos(self):
        """Test that result contains all required fields."""
        curva = {'rango_adelico': 1, 'L_E1': 0.0}
        resultado = sincronizar_bsd_adn(curva, "GACT")
        
        campos_requeridos = [
            'rango_bio_aritmetico',
            'nodos_constelacion',
            'fluidez_info_ns',
            'hotspots_adn',
            'psi_bsd_qcal',
            'coincidencia_rango_hotspots',
            'l_e1_valor',
            'f0_hz'
        ]
        
        for campo in campos_requeridos:
            assert campo in resultado


class TestValidarPentagonoLogos:
    """Tests for the validar_pentagono_logos function."""
    
    def test_pentagono_cerrado(self):
        """Test with fully closed Pentagon."""
        resultado_bsd = {
            'rango_bio_aritmetico': 1,
            'nodos_constelacion': 1,
            'fluidez_info_ns': 'INFINITA',
            'hotspots_adn': 4,
            'psi_bsd_qcal': 1.0
        }
        
        validacion = validar_pentagono_logos(resultado_bsd)
        
        assert validacion['boveda_logos_cerrada'] is True
        assert validacion['pilares_activos'] == 20
        assert validacion['milenio_unificados'] == 5
        assert validacion['estado'] == '∴ Ψ = 1.0 ∴'
    
    def test_pentagono_parcial(self):
        """Test with partially closed Pentagon."""
        resultado_bsd = {
            'rango_bio_aritmetico': 0,  # Rank 0
            'nodos_constelacion': 0,
            'fluidez_info_ns': 'DISIPATIVA',  # Not superfluid
            'hotspots_adn': 0,
            'psi_bsd_qcal': 0.5
        }
        
        validacion = validar_pentagono_logos(resultado_bsd)
        
        assert validacion['boveda_logos_cerrada'] is False
        assert validacion['pilares_activos'] < 20
        assert validacion['milenio_unificados'] < 5
        assert validacion['estado'] == 'PARCIAL'
    
    def test_criterios_individuales(self):
        """Test individual validation criteria."""
        # ADN active
        resultado1 = {
            'rango_bio_aritmetico': 1,
            'fluidez_info_ns': 'INFINITA',
            'hotspots_adn': 1,
            'psi_bsd_qcal': 1.0
        }
        val1 = validar_pentagono_logos(resultado1)
        assert val1['criterios']['adn_activo'] is True
        
        # Riemann resonant
        resultado2 = {
            'rango_bio_aritmetico': 1,
            'fluidez_info_ns': 'INFINITA',
            'hotspots_adn': 0,
            'psi_bsd_qcal': 0.9
        }
        val2 = validar_pentagono_logos(resultado2)
        assert val2['criterios']['riemann_resonante'] is True
    
    def test_coherencia_umbrales(self):
        """Test coherence thresholds."""
        # High coherence (Ψ > 0.95) enables P-NP efficiency
        resultado_alto = {
            'rango_bio_aritmetico': 1,
            'fluidez_info_ns': 'INFINITA',
            'hotspots_adn': 1,
            'psi_bsd_qcal': 0.96
        }
        val_alto = validar_pentagono_logos(resultado_alto)
        assert val_alto['criterios']['p_np_eficiente'] is True
        
        # Medium coherence (Ψ = 0.9)
        resultado_medio = {
            'rango_bio_aritmetico': 1,
            'fluidez_info_ns': 'INFINITA',
            'hotspots_adn': 1,
            'psi_bsd_qcal': 0.9
        }
        val_medio = validar_pentagono_logos(resultado_medio)
        assert val_medio['criterios']['riemann_resonante'] is True
        assert val_medio['criterios']['p_np_eficiente'] is False


class TestIntegrationBSDAdelicPentagon:
    """Integration tests for the complete Pentagon system."""
    
    def test_ejemplo_completo_curva_mordell(self):
        """Test complete example with Mordell curve."""
        # Curva de Mordell: y² = x³ - x (rango 1)
        curva_mordell = {
            'rango_adelico': 1,
            'L_E1': 0.0,
            'ecuacion': 'y² = x³ - x',
            'conductor': 32
        }
        
        # Secuencia sagrada GACT
        secuencia = "GACT"
        
        # Sincronizar BSD-ADN
        resultado = sincronizar_bsd_adn(curva_mordell, secuencia)
        
        # Validar Pentágono
        validacion = validar_pentagono_logos(resultado)
        
        # Verificar cierre completo
        assert resultado['rango_bio_aritmetico'] == 1
        assert resultado['fluidez_info_ns'] == "INFINITA"
        assert resultado['psi_bsd_qcal'] == 1.0
        assert validacion['boveda_logos_cerrada'] is True
        assert validacion['milenio_unificados'] == 5
    
    def test_diferentes_rangos(self):
        """Test with different elliptic curve ranks."""
        rangos = [0, 1, 2, 3]
        
        for r in rangos:
            curva = {
                'rango_adelico': r,
                'L_E1': 0.0 if r > 0 else 0.5
            }
            
            resultado = sincronizar_bsd_adn(curva, "GACT")
            assert resultado['rango_bio_aritmetico'] == r
            
            if r > 0:
                assert resultado['fluidez_info_ns'] == "INFINITA"
            else:
                assert resultado['fluidez_info_ns'] == "DISIPATIVA"
    
    def test_conservacion_f0(self):
        """Test that f₀ is conserved throughout the system."""
        curva = {'rango_adelico': 1, 'L_E1': 0.0}
        resultado = sincronizar_bsd_adn(curva, "GACT")
        
        assert resultado['f0_hz'] == F0_HZ
        assert resultado['f0_hz'] == 141.7001
    
    def test_unificacion_cinco_milenio(self):
        """Test unification of 5 Millennium Problems."""
        curva = {'rango_adelico': 1, 'L_E1': 0.0}
        resultado = sincronizar_bsd_adn(curva, "GACT")
        validacion = validar_pentagono_logos(resultado)
        
        componentes = [
            'adn_activo',           # ADN (Biología)
            'riemann_resonante',    # Riemann (Estructura)
            'navier_stokes_superfluido',  # Navier-Stokes (Dinámica)
            'p_np_eficiente',       # P vs NP (Lógica)
            'bsd_rango_positivo'    # BSD (Aritmética)
        ]
        
        for componente in componentes:
            assert componente in validacion['criterios']
        
        # Cuando todos están activos, el Pentágono está cerrado
        if all(validacion['criterios'].values()):
            assert validacion['milenio_unificados'] == 5


def test_constantes_globales():
    """Test global constants."""
    assert F0_HZ == 141.7001
    assert NODOS_CONSTELACION == 51


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
