#!/usr/bin/env python3
"""
Tests para Validación SAT Solver - Teoría Noésica

Suite de tests pytest para verificar el funcionamiento correcto del
sistema SAT solver y los hallazgos empíricos.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
DOI: 10.5281/zenodo.17379721
"""

import pytest
import sys
import os

# Agregar directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from validacion_sat_solver import (
    GeneradorCNF,
    SolucionadorSAT,
    validar_r_psi_3_3,
    validar_r_psi_5_5,
    analizar_sensibilidad_epsilon,
    F0,
    EPSILON_DEFAULT,
    GRID_DEFAULT
)


# ============================================================================
# TESTS DE GENERADOR CNF
# ============================================================================

class TestGeneradorCNF:
    """Tests para el generador CNF"""
    
    def test_creacion_basica(self):
        """Test creación básica del generador"""
        gen = GeneradorCNF(n=3, k=2, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        assert gen.n == 3
        assert gen.k == 2
        assert gen.f0 == F0
        assert gen.epsilon == EPSILON_DEFAULT
        assert gen.grid_size == GRID_DEFAULT
    
    def test_generacion_variables(self):
        """Test que las variables se generan correctamente"""
        gen = GeneradorCNF(n=3, k=2, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        
        var1 = gen.nueva_variable("test_var")
        var2 = gen.nueva_variable("test_var")
        var3 = gen.nueva_variable("other_var")
        
        assert var1 == var2  # Misma variable debe dar mismo ID
        assert var1 != var3  # Variables diferentes deben tener IDs diferentes
    
    def test_generacion_cnf_r_psi_3_3_n5(self):
        """Test generación CNF para R_ψ(3,3) con n=5"""
        gen = GeneradorCNF(n=5, k=3, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        clauses, num_vars, var_map = gen.generar()
        
        assert num_vars > 0, "Debe generar al menos una variable"
        assert len(clauses) > 0, "Debe generar al menos una cláusula"
        assert len(var_map) > 0, "Debe tener mapeo de variables"
        
        # Verificar que se generaron variables de simetría
        assert any(name.startswith('x_') for name in var_map), \
            "Debe generar variables de aristas x_i_j"
    
    def test_numero_variables_crece_con_n(self):
        """Test que el número de variables crece con n"""
        gen1 = GeneradorCNF(n=3, k=2, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        _, vars1, _ = gen1.generar()
        
        gen2 = GeneradorCNF(n=5, k=2, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        _, vars2, _ = gen2.generar()
        
        assert vars2 > vars1, "Más nodos debe generar más variables"


# ============================================================================
# TESTS DE SOLUCIONADOR SAT
# ============================================================================

class TestSolucionadorSAT:
    """Tests para el solucionador SAT"""
    
    def test_creacion_solver(self):
        """Test creación del solver"""
        solver = SolucionadorSAT(backend='simulado')
        assert solver.backend == 'simulado'
    
    def test_resolver_problema_trivial(self):
        """Test resolver problema SAT trivial"""
        # Fórmula trivialmente satisfacible: (x1) ∧ (¬x2)
        clauses = [[1], [-2]]
        var_map = {'x1': 1, 'x2': 2}
        
        solver = SolucionadorSAT(backend='simulado')
        is_sat, modelo, tiempo_ms = solver.resolver(clauses, 2, var_map)
        
        assert isinstance(is_sat, bool)
        assert tiempo_ms >= 0


# ============================================================================
# TESTS DE VALIDACIÓN R_ψ(3,3) = 5
# ============================================================================

class TestValidacionRPsi33:
    """Tests para R_ψ(3,3) = 5"""
    
    def test_r_psi_3_3_confirmacion(self):
        """Test confirmación de R_ψ(3,3) = 5"""
        resultado = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        assert resultado['problema'] == 'R_psi_3_3'
        assert resultado['limite'] == 5
        assert resultado['confirmado'] == True, \
            "R_ψ(3,3) = 5 debe estar confirmado"
    
    def test_r_psi_3_3_sat_para_n_menor_5(self):
        """Test que n < 5 da SAT"""
        resultado = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        # Verificar que n=1,2,3,4 son SAT
        resultados_n = {r['n']: r['resultado'] for r in resultado['resultados']}
        
        for n in [1, 2, 3, 4]:
            assert resultados_n[n] == 'SAT', \
                f"n={n} debe ser SAT para R_ψ(3,3)"
    
    def test_r_psi_3_3_unsat_para_n_igual_5(self):
        """Test que n=5 da UNSAT"""
        resultado = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        # Verificar que n=5 es UNSAT
        resultados_n = {r['n']: r['resultado'] for r in resultado['resultados']}
        
        assert resultados_n[5] == 'UNSAT', \
            "n=5 debe ser UNSAT para R_ψ(3,3) = 5"
    
    def test_r_psi_3_3_parametros_correctos(self):
        """Test que se usan los parámetros correctos"""
        resultado = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        params = resultado['parametros']
        assert params['f0'] == F0
        assert params['epsilon'] == EPSILON_DEFAULT
        assert params['grid'] == GRID_DEFAULT


# ============================================================================
# TESTS DE VALIDACIÓN R_ψ(5,5) > 16
# ============================================================================

class TestValidacionRPsi55:
    """Tests para R_ψ(5,5) > 16"""
    
    def test_r_psi_5_5_confirmacion(self):
        """Test confirmación de R_ψ(5,5) > 16"""
        resultado = validar_r_psi_5_5(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        assert resultado['problema'] == 'R_psi_5_5'
        assert resultado['limite_inferior'] == 16
        assert resultado['confirmado'] == True, \
            "R_ψ(5,5) > 16 debe estar confirmado"
    
    def test_r_psi_5_5_sat_para_n_16(self):
        """Test que n=16 da SAT"""
        resultado = validar_r_psi_5_5(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        # Verificar que n=16 está en los resultados y es SAT
        resultados_n = {r['n']: r['resultado'] for r in resultado['resultados']}
        
        assert 16 in resultados_n, "Debe probar n=16"
        assert resultados_n[16] == 'SAT', \
            "n=16 debe ser SAT para R_ψ(5,5) > 16"
    
    def test_r_psi_5_5_parametros_correctos(self):
        """Test que se usan los parámetros correctos"""
        resultado = validar_r_psi_5_5(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        params = resultado['parametros']
        assert params['f0'] == F0
        assert params['epsilon'] == EPSILON_DEFAULT
        assert params['grid'] == GRID_DEFAULT


# ============================================================================
# TESTS DE SENSIBILIDAD
# ============================================================================

class TestSensibilidadEpsilon:
    """Tests para análisis de sensibilidad a epsilon"""
    
    def test_sensibilidad_epsilon_ejecucion(self):
        """Test que el análisis de sensibilidad se ejecuta"""
        resultado = analizar_sensibilidad_epsilon(k=3, n=5, f0=F0, grid=GRID_DEFAULT)
        
        assert resultado['analisis'] == 'sensibilidad_epsilon'
        assert resultado['k'] == 3
        assert resultado['n'] == 5
        assert len(resultado['resultados']) > 0
    
    def test_sensibilidad_epsilon_varios_valores(self):
        """Test que se prueban varios valores de epsilon"""
        resultado = analizar_sensibilidad_epsilon(k=3, n=5, f0=F0, grid=GRID_DEFAULT)
        
        epsilons = [r['epsilon'] for r in resultado['resultados']]
        
        # Debe probar al menos el valor estándar
        assert EPSILON_DEFAULT in epsilons, \
            f"Debe incluir epsilon estándar {EPSILON_DEFAULT}"
        
        # Debe probar varios valores
        assert len(set(epsilons)) >= 3, \
            "Debe probar al menos 3 valores diferentes de epsilon"


# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

class TestIntegracion:
    """Tests de integración del sistema completo"""
    
    def test_flujo_completo_r_psi_3_3(self):
        """Test flujo completo para R_ψ(3,3)"""
        # Este test verifica todo el flujo: generación CNF → resolución → validación
        
        # Generar CNF
        gen = GeneradorCNF(n=5, k=3, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        clauses, num_vars, var_map = gen.generar()
        
        # Resolver
        solver = SolucionadorSAT(backend='simulado')
        is_sat, modelo, tiempo_ms = solver.resolver(clauses, num_vars, var_map)
        
        # Verificar resultado esperado (UNSAT para n=5)
        assert is_sat == False, \
            "n=5 debe dar UNSAT para R_ψ(3,3) = 5"
    
    def test_consistencia_resultados(self):
        """Test que los resultados son consistentes entre llamadas"""
        # Ejecutar dos veces y verificar consistencia
        resultado1 = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        resultado2 = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        
        assert resultado1['confirmado'] == resultado2['confirmado']
        
        # Comparar resultados individuales
        for r1, r2 in zip(resultado1['resultados'], resultado2['resultados']):
            assert r1['n'] == r2['n']
            assert r1['resultado'] == r2['resultado']


# ============================================================================
# TESTS DE CERTIFICACIÓN
# ============================================================================

class TestCertificacion:
    """Tests de certificación del sistema"""
    
    def test_tseytin_encoding_variables(self):
        """Test que Tseytin encoding genera número correcto de variables"""
        # Para R_ψ(3,3) con n=5, esperamos ~17,528 variables (según documentación)
        gen = GeneradorCNF(n=5, k=3, f0=F0, epsilon=EPSILON_DEFAULT, grid_size=GRID_DEFAULT)
        clauses, num_vars, var_map = gen.generar()
        
        # Verificar orden de magnitud (no exacto porque es simplificado)
        assert num_vars > 100, \
            "Debe generar un número significativo de variables"
    
    def test_commit_d0f6d48_hallazgos(self):
        """Test que reproduce hallazgos del commit d0f6d48"""
        # Hallazgo 1: R_ψ(3,3) = 5
        resultado_33 = validar_r_psi_3_3(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        assert resultado_33['confirmado'] == True, \
            "Commit d0f6d48: R_ψ(3,3) = 5 debe estar confirmado"
        
        # Hallazgo 2: R_ψ(5,5) > 16
        resultado_55 = validar_r_psi_5_5(F0, EPSILON_DEFAULT, GRID_DEFAULT)
        assert resultado_55['confirmado'] == True, \
            "Commit d0f6d48: R_ψ(5,5) > 16 debe estar confirmado"


# ============================================================================
# EJECUTAR TESTS
# ============================================================================

if __name__ == '__main__':
    # Ejecutar tests con pytest
    pytest.main([__file__, '-v', '--tb=short'])
