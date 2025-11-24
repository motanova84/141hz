#!/usr/bin/env python3
"""
Tests para procesar_multievento_snr.py
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from procesar_multievento_snr import obtener_snr_catalogo, procesar_evento


class TestProcesarMultieventoSNR(unittest.TestCase):
    """Tests para el procesamiento de eventos gravitacionales"""

    def test_obtener_snr_catalogo(self):
        """Verifica que el catálogo contiene todos los eventos esperados"""
        catalogo = obtener_snr_catalogo()

        eventos_esperados = [
            'GW150914', 'GW151012', 'GW151226',
            'GW170104', 'GW170608', 'GW170729',
            'GW170809', 'GW170814', 'GW170817',
            'GW170818', 'GW170823',
        ]

        for evento in eventos_esperados:
            self.assertIn(evento, catalogo, f"Evento {evento} no está en el catálogo")
            self.assertIsInstance(catalogo[evento], (int, float),
                                  f"SNR de {evento} debe ser numérico")
            self.assertGreater(catalogo[evento], 0,
                               f"SNR de {evento} debe ser positivo")

    def test_valores_snr_especificos(self):
        """Verifica los valores específicos de SNR"""
        catalogo = obtener_snr_catalogo()

        # Valores esperados según el problema
        valores_esperados = {
            'GW150914': 14.49,
            'GW151012': 12.04,
            'GW151226': 23.17,
            'GW170104': 19.48,
            'GW170608': 26.81,
            'GW170729': 31.35,
            'GW170809': 26.51,
            'GW170814': 22.26,
            'GW170817': 10.78,
            'GW170818': 20.83,
            'GW170823': 27.50,
        }

        for evento, snr_esperado in valores_esperados.items():
            snr_obtenido = catalogo[evento]
            self.assertAlmostEqual(snr_obtenido, snr_esperado, places=2,
                                   msg=f"SNR de {evento} no coincide")

    def test_procesar_evento(self):
        """Verifica que procesar_evento retorna valores válidos"""
        eventos = ['GW150914', 'GW151226', 'GW170817']

        for evento in eventos:
            snr = procesar_evento(evento)
            self.assertIsNotNone(snr, f"SNR de {evento} no debe ser None")
            self.assertIsInstance(snr, (int, float),
                                  f"SNR de {evento} debe ser numérico")
            self.assertGreater(snr, 0, f"SNR de {evento} debe ser positivo")

    def test_evento_no_existente(self):
        """Verifica el comportamiento con evento inexistente"""
        snr = procesar_evento('GW999999')
        self.assertIsNone(snr, "Evento inexistente debe retornar None")

    def test_snr_gw150914(self):
        """Test específico para GW150914 (primer detección)"""
        snr = procesar_evento('GW150914')
        self.assertAlmostEqual(snr, 14.49, places=2)

    def test_snr_gw170817(self):
        """Test específico para GW170817 (fusión de estrellas de neutrones)"""
        snr = procesar_evento('GW170817')
        self.assertAlmostEqual(snr, 10.78, places=2)

    def test_todos_eventos_positivos(self):
        """Verifica que todos los SNR son positivos"""
        catalogo = obtener_snr_catalogo()

        for evento, snr in catalogo.items():
            self.assertGreater(snr, 0,
                               f"SNR de {evento} debe ser positivo: {snr}")


class TestIntegracion(unittest.TestCase):
    """Tests de integración para el script completo"""

    def test_script_ejecutable(self):
        """Verifica que el script es ejecutable"""
        script_path = os.path.join(os.path.dirname(__file__),
                                   'procesar_multievento_snr.py')
        self.assertTrue(os.path.exists(script_path),
                        "El script debe existir")
        self.assertTrue(os.access(script_path, os.X_OK),
                        "El script debe ser ejecutable")


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
