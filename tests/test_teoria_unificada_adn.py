#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Unified Theory: Biology × Number Theory × Quantum Physics
===================================================================
Comprehensive test suite for the three modules:
- adn_riemann.py
- mutaciones_resonantes.py
- teoria_unificada_adn.py

Autor: QCAL ∞³ System
Fecha: 2026-03-08
"""
import pytest
import numpy as np
from adn_riemann import (
    CalculadorCerosRiemann, CodificadorADNRiemann,
    calcular_coherencia_cuantica_adn,
    BASE_A_NUMERO, NUMERO_A_BASE, COMPLEMENTO,
    FRECUENCIA_BASE, PSI_OPTIMO, FACTOR_UNIFICACION
)
from mutaciones_resonantes import (
    AnalizadorMutaciones, OptimizadorSecuencias
)
from teoria_unificada_adn import (
    TeoriaUnificadaADN, PHI, ALPHA_FINA
)


class TestCalculadorCerosRiemann:
    """Tests para CalculadorCerosRiemann."""
    
    def test_inicializacion(self):
        """Test de inicialización básica."""
        calculador = CalculadorCerosRiemann(num_ceros=100)
        assert calculador.num_ceros == 100
        assert calculador.numero_de_ceros() > 0
    
    def test_primer_cero(self):
        """Test del primer cero de Riemann (conocido)."""
        calculador = CalculadorCerosRiemann(num_ceros=10)
        t1 = calculador.obtener_cero(1)
        # Primer cero: t₁ ≈ 14.134725
        assert abs(t1 - 14.134725) < 0.001
    
    def test_ceros_ordenados(self):
        """Test que los ceros están ordenados."""
        calculador = CalculadorCerosRiemann(num_ceros=50)
        for i in range(1, 10):
            t_i = calculador.obtener_cero(i)
            t_i_plus_1 = calculador.obtener_cero(i + 1)
            assert t_i_plus_1 > t_i, "Los ceros deben estar ordenados"
    
    def test_indice_invalido(self):
        """Test con índice inválido."""
        calculador = CalculadorCerosRiemann(num_ceros=10)
        with pytest.raises(ValueError):
            calculador.obtener_cero(0)  # Índice debe ser >= 1


class TestCodificadorADNRiemann:
    """Tests para CodificadorADNRiemann."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calculador = CalculadorCerosRiemann(num_ceros=1000)
        self.codificador = CodificadorADNRiemann(self.calculador)
    
    def test_secuencia_a_numero_basico(self):
        """Test de conversión básica secuencia a número."""
        # A=0, T=1, G=2, C=3
        # "ATGC" = 0*4³ + 1*4² + 2*4¹ + 3*4⁰ = 0 + 16 + 8 + 3 = 27
        numero = self.codificador.secuencia_a_numero("ATGC")
        assert numero == 27
    
    def test_secuencia_a_numero_casos(self):
        """Test de varios casos de conversión."""
        assert self.codificador.secuencia_a_numero("AAAA") == 0
        assert self.codificador.secuencia_a_numero("AAAT") == 1
        assert self.codificador.secuencia_a_numero("AAAG") == 2
        assert self.codificador.secuencia_a_numero("AAAC") == 3
        assert self.codificador.secuencia_a_numero("TTTT") == 85  # 1*4³ + 1*4² + 1*4 + 1
    
    def test_numero_a_secuencia_basico(self):
        """Test de conversión número a secuencia."""
        secuencia = self.codificador.numero_a_secuencia(27, 4)
        assert secuencia == "ATGC"
    
    def test_conservacion_informacion(self):
        """Test de conservación: secuencia → número → secuencia."""
        secuencias_test = ["ATGC", "GACT", "AAAA", "TTTT", "GCGC"]
        for seq_orig in secuencias_test:
            numero = self.codificador.secuencia_a_numero(seq_orig)
            seq_recuperada = self.codificador.numero_a_secuencia(numero, len(seq_orig))
            assert seq_orig == seq_recuperada, f"Conservación falló para {seq_orig}"
    
    def test_propiedades_espectrales_estructura(self):
        """Test de estructura del dict de propiedades espectrales."""
        props = self.codificador.propiedades_espectrales("ATGC")
        
        # Verificar que contiene todas las claves esperadas
        claves_esperadas = [
            'secuencia', 'numero', 'indice_cero_riemann',
            'cero_riemann_t', 'frecuencia_riemann_hz',
            'resonancia_f0', 'ratio_frecuencias',
            'espaciado_local', 'Q_factor'
        ]
        for clave in claves_esperadas:
            assert clave in props, f"Falta clave: {clave}"
    
    def test_propiedades_espectrales_valores(self):
        """Test de valores razonables en propiedades espectrales."""
        props = self.codificador.propiedades_espectrales("ATGC")
        
        # Verificar rangos razonables
        assert props['cero_riemann_t'] > 0
        assert props['frecuencia_riemann_hz'] > 0
        assert 0 <= props['resonancia_f0'] <= 1
        assert props['ratio_frecuencias'] > 0
        assert props['Q_factor'] > 0
    
    def test_base_invalida(self):
        """Test con base inválida."""
        with pytest.raises(ValueError):
            self.codificador.secuencia_a_numero("ATGX")


class TestCoherenciaCuantica:
    """Tests para calcular_coherencia_cuantica_adn."""
    
    def test_coherencia_estructura(self):
        """Test de estructura del dict de coherencia."""
        coherencia = calcular_coherencia_cuantica_adn("ATGC")
        
        claves_esperadas = [
            'secuencia', 'temperatura_K', 'energia_termica_J',
            'energia_cuantica_J', 'ratio_ruido_termico',
            'tau_decoherencia_s', 'psi_efectivo', 'Q_efectivo', 'coherente'
        ]
        for clave in claves_esperadas:
            assert clave in coherencia, f"Falta clave: {clave}"
    
    def test_coherencia_temperatura_corporal(self):
        """Test con temperatura corporal (310 K)."""
        coherencia = calcular_coherencia_cuantica_adn("ATGC", temperatura=310.0)
        
        assert coherencia['temperatura_K'] == 310.0
        assert coherencia['energia_termica_J'] > 0
        assert coherencia['energia_cuantica_J'] > 0
        assert 0 <= coherencia['psi_efectivo'] <= 1
        assert coherencia['Q_efectivo'] > 0
    
    def test_coherencia_temperatura_cero(self):
        """Test con temperatura muy baja."""
        # A temperatura más baja, mayor coherencia
        coherencia_baja = calcular_coherencia_cuantica_adn("ATGC", temperatura=10.0)
        coherencia_alta = calcular_coherencia_cuantica_adn("ATGC", temperatura=310.0)
        
        # A menor temperatura, menor ratio de ruido
        assert coherencia_baja['ratio_ruido_termico'] < coherencia_alta['ratio_ruido_termico']


class TestAnalizadorMutaciones:
    """Tests para AnalizadorMutaciones."""
    
    def setup_method(self):
        """Setup para cada test."""
        calculador = CalculadorCerosRiemann(num_ceros=1000)
        self.codificador = CodificadorADNRiemann(calculador)
        self.analizador = AnalizadorMutaciones(self.codificador)
    
    def test_analizar_mutacion_puntual(self):
        """Test de análisis de mutación puntual."""
        resultado = self.analizador.analizar_mutacion_puntual("ATGC", 0, "G")
        
        assert resultado['secuencia_original'] == "ATGC"
        assert resultado['secuencia_mutada'] == "GTGC"
        assert resultado['posicion'] == 0
        assert resultado['base_original'] == "A"
        assert resultado['base_nueva'] == "G"
        
        # Verificar que tiene deltas
        assert 'delta_resonancia' in resultado
        assert 'delta_coherencia' in resultado
    
    def test_mutacion_posicion_invalida(self):
        """Test con posición inválida."""
        with pytest.raises(ValueError):
            self.analizador.analizar_mutacion_puntual("ATGC", 10, "G")
    
    def test_encontrar_mejores_mutaciones(self):
        """Test de búsqueda de mejores mutaciones."""
        mejores = self.analizador.encontrar_mejores_mutaciones("ATGC", num_mejores=3)
        
        assert len(mejores) <= 3
        
        # Verificar que están ordenadas por mejora
        if len(mejores) > 1:
            for i in range(len(mejores) - 1):
                score_i = mejores[i]['delta_resonancia'] + mejores[i]['delta_coherencia']
                score_i_plus_1 = mejores[i+1]['delta_resonancia'] + mejores[i+1]['delta_coherencia']
                assert score_i >= score_i_plus_1
    
    def test_analizar_complementariedad(self):
        """Test de análisis de complementariedad."""
        resultado = self.analizador.analizar_complementariedad("ATGC")
        
        assert resultado['secuencia'] == "ATGC"
        assert resultado['complemento'] == "TACG"
        assert 'diferencia_resonancia' in resultado
        assert 'simetrica' in resultado


class TestOptimizadorSecuencias:
    """Tests para OptimizadorSecuencias."""
    
    def setup_method(self):
        """Setup para cada test."""
        calculador = CalculadorCerosRiemann(num_ceros=1000)
        self.codificador = CodificadorADNRiemann(calculador)
        self.analizador = AnalizadorMutaciones(self.codificador)
        self.optimizador = OptimizadorSecuencias(self.codificador, self.analizador)
    
    def test_optimizar_local(self):
        """Test de optimización local."""
        resultado = self.optimizador.optimizar_local("AAAA", max_iteraciones=10)
        
        assert 'secuencia_original' in resultado
        assert 'secuencia_optimizada' in resultado
        assert 'score_final' in resultado
        assert resultado['score_final'] >= resultado['score_original']
    
    def test_buscar_secuencia_optima(self):
        """Test de búsqueda de secuencia óptima."""
        resultado = self.optimizador.buscar_secuencia_optima(longitud=4, num_candidatos=50)
        
        assert len(resultado['secuencia_optima']) == 4
        assert resultado['score'] > 0
        assert resultado['candidatos_evaluados'] == 50


class TestTeoriaUnificadaADN:
    """Tests para TeoriaUnificadaADN."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.teoria = TeoriaUnificadaADN()
    
    def test_inicializacion(self):
        """Test de inicialización."""
        assert self.teoria.calculador_riemann is not None
        assert self.teoria.codificador is not None
        assert self.teoria.analizador_mutaciones is not None
    
    def test_calcular_entropia_informacion(self):
        """Test de cálculo de entropía."""
        entropia = self.teoria.calcular_entropia_informacion("ATGC")
        
        claves_esperadas = [
            'secuencia', 'entropia_shannon_bits', 'entropia_relativa',
            'complejidad_kolmogorov_proxy', 'entropia_riemann',
            'contenido_informacion'
        ]
        for clave in claves_esperadas:
            assert clave in entropia
        
        # Entropía de Shannon para secuencia equiprobable
        assert abs(entropia['entropia_shannon_bits'] - 2.0) < 0.01
    
    def test_entropia_homopolimero(self):
        """Test de entropía para homopolímero (máxima redundancia)."""
        entropia = self.teoria.calcular_entropia_informacion("AAAA")
        
        # Entropía debe ser 0 (una sola base)
        assert entropia['entropia_shannon_bits'] < 0.01
        assert entropia['entropia_relativa'] < 0.01
    
    def test_calcular_funcion_onda_unificada(self):
        """Test de función de onda unificada."""
        func_onda = self.teoria.calcular_funcion_onda_unificada("ATGC")
        
        claves_esperadas = [
            'secuencia', 'amplitud', 'fase_rad', 'psi_cuantico',
            'amplitud_zeta', 'resonancia_f0', 'probabilidad',
            'coherencia_unificada'
        ]
        for clave in claves_esperadas:
            assert clave in func_onda
        
        # Verificar rangos
        assert 0 <= func_onda['amplitud'] <= 1
        assert 0 <= func_onda['fase_rad'] < 2 * np.pi
        assert 0 <= func_onda['probabilidad'] <= 1
    
    def test_calcular_acoplamiento_triada(self):
        """Test de acoplamiento triádico."""
        acoplamiento = self.teoria.calcular_acoplamiento_triada("ATGC")
        
        claves_esperadas = [
            'secuencia', 'acoplamiento_bio_math', 'acoplamiento_math_quantum',
            'acoplamiento_quantum_bio', 'acoplamiento_triada',
            'acoplamiento_normalizado_qcal', 'unificacion_fuerte',
            'factor_unificacion'
        ]
        for clave in claves_esperadas:
            assert clave in acoplamiento
        
        # Factor de unificación debe ser 1/7
        assert abs(acoplamiento['factor_unificacion'] - 1.0/7.0) < 1e-6
    
    def test_predecir_propiedades_biologicas(self):
        """Test de predicción de propiedades biológicas."""
        predicciones = self.teoria.predecir_propiedades_biologicas("ATGC")
        
        claves_esperadas = [
            'secuencia', 'estabilidad_termodinamica_pct',
            'potencial_expresion_0_10', 'conservacion_evolutiva_pct',
            'funcionalidad_predicha_pct', 'clasificacion', 'recomendacion'
        ]
        for clave in claves_esperadas:
            assert clave in predicciones
        
        # Verificar rangos
        assert 0 <= predicciones['estabilidad_termodinamica_pct'] <= 100
        assert 0 <= predicciones['potencial_expresion_0_10'] <= 10
        assert 0 <= predicciones['conservacion_evolutiva_pct'] <= 100
        assert 0 <= predicciones['funcionalidad_predicha_pct'] <= 100
    
    def test_clasificacion_secuencias(self):
        """Test de clasificación de secuencias."""
        # Debe clasificar cualquier secuencia sin error
        secuencias = ["ATGC", "AAAA", "GACT", "TTTT"]
        for seq in secuencias:
            predicciones = self.teoria.predecir_propiedades_biologicas(seq)
            assert isinstance(predicciones['clasificacion'], str)
            assert len(predicciones['clasificacion']) > 0


class TestConstantesUnificacion:
    """Tests para constantes de unificación."""
    
    def test_frecuencia_base(self):
        """Test de frecuencia base."""
        assert FRECUENCIA_BASE == 141.7001
    
    def test_psi_optimo(self):
        """Test de Ψ óptimo."""
        assert 0 < PSI_OPTIMO <= 1
        assert abs(PSI_OPTIMO - 0.999) < 0.001
    
    def test_factor_unificacion(self):
        """Test de factor de unificación."""
        assert abs(FACTOR_UNIFICACION - 1.0/7.0) < 1e-10
    
    def test_phi_aurea(self):
        """Test de proporción áurea."""
        phi_esperado = (1 + np.sqrt(5)) / 2
        assert abs(PHI - phi_esperado) < 1e-10
    
    def test_alpha_fina(self):
        """Test de constante de estructura fina."""
        # α ≈ 1/137.036
        assert abs(ALPHA_FINA - 1.0/137.035999084) < 1e-12


class TestComplementariedad:
    """Tests específicos de simetría de complementariedad."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.teoria = TeoriaUnificadaADN()
    
    def test_complemento_watson_crick(self):
        """Test de complementos Watson-Crick."""
        assert COMPLEMENTO['A'] == 'T'
        assert COMPLEMENTO['T'] == 'A'
        assert COMPLEMENTO['G'] == 'C'
        assert COMPLEMENTO['C'] == 'G'
    
    def test_simetria_complementaria(self):
        """Test de simetría entre secuencia y complemento."""
        secuencia = "ATGC"
        complemento = ''.join([COMPLEMENTO[base] for base in secuencia])
        
        props_seq = self.teoria.codificador.propiedades_espectrales(secuencia)
        props_comp = self.teoria.codificador.propiedades_espectrales(complemento)
        
        # Ambos deben tener resonancia positiva
        assert props_seq['resonancia_f0'] > 0
        assert props_comp['resonancia_f0'] > 0


def test_integracion_completa():
    """Test de integración completa del sistema."""
    # Crear instancia de teoría unificada
    teoria = TeoriaUnificadaADN()
    
    # Secuencia de prueba
    secuencia = "ATGC"
    
    # Ejecutar análisis completo
    entropia = teoria.calcular_entropia_informacion(secuencia)
    func_onda = teoria.calcular_funcion_onda_unificada(secuencia)
    acoplamiento = teoria.calcular_acoplamiento_triada(secuencia)
    predicciones = teoria.predecir_propiedades_biologicas(secuencia)
    
    # Verificar que todo retorna datos válidos
    assert entropia is not None
    assert func_onda is not None
    assert acoplamiento is not None
    assert predicciones is not None
    
    # Verificar coherencia entre módulos
    assert entropia['secuencia'] == secuencia
    assert func_onda['secuencia'] == secuencia
    assert acoplamiento['secuencia'] == secuencia
    assert predicciones['secuencia'] == secuencia


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
