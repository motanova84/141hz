#!/usr/bin/env python3
"""
Tests para la Torre Algebraica

Verifica que la implementación de la torre algebraica de 5 niveles
funcione correctamente y mantenga consistencia matemática.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import the algebraic tower module
from torre_algebraica import (
    TorreAlgebraica,
    NivelOntologia,
    NivelGeometria,
    NivelEnergia,
    NivelDinamica,
    NivelFenomenologia,
    f0
)


class TestNivelOntologia(unittest.TestCase):
    """Tests para el Nivel 5: Ontología"""

    def setUp(self):
        self.nivel = NivelOntologia()

    def test_nivel_correcto(self):
        """Verifica que el nivel sea 5"""
        self.assertEqual(self.nivel.nivel, 5)

    def test_nombre_correcto(self):
        """Verifica el nombre del nivel"""
        self.assertEqual(self.nivel.nombre, "Ontología")

    def test_definicion_campo_psi(self):
        """Verifica que la definición del campo Ψ sea correcta"""
        definicion = self.nivel.definicion_campo_psi()

        self.assertIn('campo', definicion)
        self.assertEqual(definicion['campo'], 'Ψ')
        self.assertIn('dominio', definicion)
        self.assertIn('codominio', definicion)
        self.assertIn('ecuacion_fundamental', definicion)
        self.assertIn('propiedades', definicion)

    def test_propiedades_algebraicas(self):
        """Verifica las propiedades algebraicas del campo"""
        props = self.nivel.propiedades_algebraicas()

        self.assertIn('grupo_simetria', props)
        self.assertIn('lagrangiano', props)
        self.assertIn('conservacion', props)
        self.assertIn('invarianza', props)

    def test_emergence_to_geometry(self):
        """Verifica la emergencia hacia geometría"""
        emergencia = self.nivel.emergence_to_geometry()

        self.assertIn('mecanismo', emergencia)
        self.assertIn('proceso', emergencia)
        self.assertIn('ecuacion', emergencia)
        self.assertIn('resultado', emergencia)
    
    def test_conexion_riemann_hypothesis(self):
        """Verifica la conexión con la Hipótesis de Riemann"""
        conexion = self.nivel.conexion_riemann_hypothesis()
        
        self.assertIn('tesis', conexion)
        self.assertIn('funcion_zeta', conexion)
        self.assertIn('sistema_adelico', conexion)
        self.assertIn('derivada_critica', conexion)
        self.assertIn('emergencia', conexion)
        self.assertIn('implicacion', conexion)
        
        # Verificar estructura de función zeta
        zeta = conexion['funcion_zeta']
        self.assertIn('definicion', zeta)
        self.assertIn('producto_euler', zeta)
        self.assertIn('ceros_no_triviales', zeta)
        
        # Verificar sistema adélico
        adelico = conexion['sistema_adelico']
        self.assertIn('estructura', adelico)
        self.assertIn('interpretacion', adelico)
        
        # Verificar derivada crítica
        derivada = conexion['derivada_critica']
        self.assertIn('valor', derivada)
        self.assertIn('significado', derivada)
        self.assertIn('conexion_f0', derivada)


class TestNivelGeometria(unittest.TestCase):
    """Tests para el Nivel 4: Geometría"""

    def setUp(self):
        self.nivel = NivelGeometria()

    def test_nivel_correcto(self):
        """Verifica que el nivel sea 4"""
        self.assertEqual(self.nivel.nivel, 4)

    def test_nombre_correcto(self):
        """Verifica el nombre del nivel"""
        self.assertEqual(self.nivel.nombre, "Geometría")

    def test_R_psi_calculado(self):
        """Verifica que R_Ψ esté calculado correctamente"""
        # R_Ψ = c / (2πf₀)
        import numpy as np
        c = 299792458
        R_psi_esperado = c / (2 * np.pi * f0)

        self.assertAlmostEqual(self.nivel.R_psi, R_psi_esperado, places=5)

    def test_estructura_calabi_yau(self):
        """Verifica la estructura Calabi-Yau"""
        estructura = self.nivel.estructura_calabi_yau()

        self.assertIn('variedad', estructura)
        self.assertIn('dimensiones_reales', estructura)
        self.assertIn('dimensiones_complejas', estructura)
        self.assertIn('numeros_hodge', estructura)
        self.assertIn('radio_compactificacion', estructura)

        # Verificar números de Hodge
        self.assertEqual(estructura['numeros_hodge']['h11'], 1)
        self.assertEqual(estructura['numeros_hodge']['h21'], 101)

    def test_metrica_calabi_yau(self):
        """Verifica la métrica Calabi-Yau"""
        metrica = self.nivel.metrica_calabi_yau()

        self.assertIn('metrica', metrica)
        self.assertIn('potencial_kahler', metrica)
        self.assertIn('volumen', metrica)
        self.assertIn('forma_kahler', metrica)


class TestNivelEnergia(unittest.TestCase):
    """Tests para el Nivel 3: Energía"""

    def setUp(self):
        self.nivel = NivelEnergia()

    def test_nivel_correcto(self):
        """Verifica que el nivel sea 3"""
        self.assertEqual(self.nivel.nivel, 3)

    def test_nombre_correcto(self):
        """Verifica el nombre del nivel"""
        self.assertEqual(self.nivel.nombre, "Energía")

    def test_energia_cuantica_calculada(self):
        """Verifica que E_Ψ = hf₀"""
        h = 6.62607015e-34
        E_psi_esperado = h * f0

        self.assertAlmostEqual(self.nivel.E_psi, E_psi_esperado, places=40)

    def test_energia_cuantica_dict(self):
        """Verifica la estructura del diccionario de energía cuántica"""
        energia = self.nivel.energia_cuantica()

        self.assertIn('E_psi_julios', energia)
        self.assertIn('E_psi_eV', energia)
        self.assertIn('frecuencia_Hz', energia)
        self.assertEqual(energia['frecuencia_Hz'], f0)

    def test_masa_equivalente(self):
        """Verifica que m_Ψ = hf₀/c²"""
        h = 6.62607015e-34
        c = 299792458
        m_psi_esperado = (h * f0) / (c**2)

        self.assertAlmostEqual(self.nivel.m_psi, m_psi_esperado, places=48)

    def test_masa_equivalente_dict(self):
        """Verifica la estructura del diccionario de masa"""
        masa = self.nivel.masa_equivalente()

        self.assertIn('m_psi_kg', masa)
        self.assertIn('m_psi_eV_c2', masa)
        self.assertIn('formula', masa)

    def test_temperatura_caracteristica(self):
        """Verifica que T_Ψ = E_Ψ/k_B"""
        h = 6.62607015e-34
        k_B = 1.380649e-23
        T_psi_esperado = (h * f0) / k_B

        self.assertAlmostEqual(self.nivel.T_psi, T_psi_esperado, places=35)

    def test_temperatura_orden_magnitud(self):
        """Verifica que T_Ψ ≈ 10⁻⁹ K"""
        # Debe estar en el orden de nanokelvin
        self.assertTrue(1e-10 < self.nivel.T_psi < 1e-8)

    def test_temperatura_dict(self):
        """Verifica la estructura del diccionario de temperatura"""
        temp = self.nivel.temperatura_caracteristica()

        self.assertIn('T_psi_K', temp)
        self.assertIn('T_psi_nK', temp)
        self.assertIn('orden_magnitud', temp)


class TestNivelDinamica(unittest.TestCase):
    """Tests para el Nivel 2: Dinámica"""

    def setUp(self):
        self.nivel = NivelDinamica()

    def test_nivel_correcto(self):
        """Verifica que el nivel sea 2"""
        self.assertEqual(self.nivel.nivel, 2)

    def test_nombre_correcto(self):
        """Verifica el nombre del nivel"""
        self.assertEqual(self.nivel.nombre, "Dinámica")

    def test_coherencia_dinamica(self):
        """Verifica la estructura de coherencia dinámica"""
        coherencia = self.nivel.coherencia_dinamica()

        self.assertIn('ecuacion', coherencia)
        self.assertIn('variables', coherencia)
        self.assertIn('dimensiones', coherencia)

        # Verificar que f0 esté presente
        self.assertEqual(coherencia['variables']['f0'], f"Frecuencia fundamental ({f0} Hz)")

    def test_ecuacion_evolucion(self):
        """Verifica la ecuación de evolución temporal"""
        evolucion = self.nivel.ecuacion_evolucion()

        self.assertIn('ecuacion', evolucion)
        self.assertIn('terminos', evolucion)
        self.assertIn('constantes', evolucion)
        self.assertIn('solucion_estacionaria', evolucion)


class TestNivelFenomenologia(unittest.TestCase):
    """Tests para el Nivel 1: Fenomenología"""

    def setUp(self):
        self.nivel = NivelFenomenologia()

    def test_nivel_correcto(self):
        """Verifica que el nivel sea 1"""
        self.assertEqual(self.nivel.nivel, 1)

    def test_nombre_correcto(self):
        """Verifica el nombre del nivel"""
        self.assertEqual(self.nivel.nombre, "Fenomenología")

    def test_limite_clasico(self):
        """Verifica el límite clásico E = mc²"""
        clasico = self.nivel.limite_clasico()

        self.assertIn('ecuacion', clasico)
        self.assertEqual(clasico['ecuacion'], 'E = mc²')
        self.assertIn('limite', clasico)
        self.assertIn('interpretacion', clasico)

    def test_limite_cuantico(self):
        """Verifica el límite cuántico E = hf"""
        cuantico = self.nivel.limite_cuantico()

        self.assertIn('ecuacion', cuantico)
        self.assertEqual(cuantico['ecuacion'], 'E = hf')
        self.assertIn('limite', cuantico)
        self.assertIn('interpretacion', cuantico)

    def test_fenomenos_observables(self):
        """Verifica los fenómenos observables"""
        fenomenos = self.nivel.fenomenos_observables()

        self.assertIn('gravitacionales', fenomenos)
        self.assertIn('topologicos', fenomenos)
        self.assertIn('cosmologicos', fenomenos)
        self.assertIn('laboratorio', fenomenos)

        # Verificar f0 en gravitacionales
        self.assertIn('pico_espectral', fenomenos['gravitacionales'])


class TestTorreAlgebraicaCompleta(unittest.TestCase):
    """Tests para la Torre Algebraica completa"""

    def setUp(self):
        self.torre = TorreAlgebraica()

    def test_5_niveles_implementados(self):
        """Verifica que existan exactamente 5 niveles"""
        self.assertEqual(len(self.torre.niveles), 5)

    def test_niveles_ordenados_correctamente(self):
        """Verifica que los niveles estén numerados del 1 al 5"""
        for n in range(1, 6):
            self.assertIn(n, self.torre.niveles)
            self.assertEqual(self.torre.niveles[n].nivel, n)

    def test_obtener_nivel_valido(self):
        """Verifica que se pueden obtener niveles válidos"""
        for n in range(1, 6):
            nivel = self.torre.obtener_nivel(n)
            self.assertIsNotNone(nivel)
            self.assertEqual(nivel.nivel, n)

    def test_obtener_nivel_invalido(self):
        """Verifica que niveles inválidos lancen error"""
        with self.assertRaises(ValueError):
            self.torre.obtener_nivel(0)
        with self.assertRaises(ValueError):
            self.torre.obtener_nivel(6)

    def test_estructura_completa(self):
        """Verifica la estructura completa de la torre"""
        estructura = self.torre.estructura_completa()

        self.assertIn('nombre', estructura)
        self.assertIn('descripcion', estructura)
        self.assertIn('principio', estructura)
        self.assertIn('niveles', estructura)

        # Verificar que estén los 5 niveles
        self.assertEqual(len(estructura['niveles']), 5)

    def test_flujo_emergencia(self):
        """Verifica el flujo de emergencia"""
        flujo = self.torre.flujo_emergencia()

        self.assertIn('flujo', flujo)
        self.assertIn('transiciones', flujo)
        self.assertIn('principio', flujo)
        self.assertIn('analogia', flujo)

        # Verificar las 4 transiciones
        transiciones = flujo['transiciones']
        self.assertEqual(len(transiciones), 4)
        self.assertIn('5_a_4', transiciones)
        self.assertIn('4_a_3', transiciones)
        self.assertIn('3_a_2', transiciones)
        self.assertIn('2_a_1', transiciones)

    def test_validar_consistencia(self):
        """Verifica la validación de consistencia"""
        validacion = self.torre.validar_consistencia()

        self.assertIn('timestamp', validacion)
        self.assertIn('niveles_implementados', validacion)
        self.assertIn('consistencia', validacion)

        # Verificar que pase la validación
        self.assertEqual(validacion['niveles_implementados'], 5)
        self.assertEqual(validacion['consistencia']['status'], 'PASS')
        self.assertTrue(validacion['consistencia']['geometria_energia'])
        self.assertEqual(validacion['consistencia']['f0_global'], f0)

    def test_exportar_json(self):
        """Verifica que se pueda exportar a JSON"""
        output_path = "results/test_torre_algebraica.json"
        output = self.torre.exportar_json(output_path)

        # Verificar que se haya creado el archivo
        self.assertTrue(Path(output_path).exists())

        # Verificar estructura del output
        self.assertIn('metadata', output)
        self.assertIn('estructura', output)
        self.assertIn('flujo_emergencia', output)
        self.assertIn('validacion', output)
        self.assertIn('niveles_detallados', output)

        # Verificar que el JSON sea válido
        with open(output_path, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)

        # Limpiar
        Path(output_path).unlink()


class TestConsistenciaMathematica(unittest.TestCase):
    """Tests de consistencia matemática entre niveles"""

    def setUp(self):
        self.torre = TorreAlgebraica()

    def test_f0_consistente_en_todos_los_niveles(self):
        """Verifica que f₀ sea consistente en toda la torre"""
        # Nivel 4: f0 desde R_Ψ
        nivel4 = self.torre.obtener_nivel(4)
        import numpy as np
        c = 299792458
        f0_desde_R = c / (2 * np.pi * nivel4.R_psi)

        self.assertAlmostEqual(f0_desde_R, f0, places=4)

        # Nivel 3: f0 desde E_Ψ
        nivel3 = self.torre.obtener_nivel(3)
        h = 6.62607015e-34
        f0_desde_E = nivel3.E_psi / h

        self.assertAlmostEqual(f0_desde_E, f0, places=4)

    def test_relacion_E_m_c2(self):
        """Verifica que E = mc² se cumpla"""
        nivel3 = self.torre.obtener_nivel(3)
        c = 299792458

        E_desde_m = nivel3.m_psi * c**2

        self.assertAlmostEqual(E_desde_m, nivel3.E_psi, places=38)

    def test_relacion_E_T_kB(self):
        """Verifica que E = k_B·T se cumpla"""
        nivel3 = self.torre.obtener_nivel(3)
        k_B = 1.380649e-23

        E_desde_T = k_B * nivel3.T_psi

        self.assertAlmostEqual(E_desde_T, nivel3.E_psi, places=38)


if __name__ == '__main__':
    unittest.main()
