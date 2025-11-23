#!/usr/bin/env python3
"""
🧪 Tests para el Módulo de Revolución Noésica

Tests unitarios y de integración para validar la implementación
completa del Manifiesto de la Revolución Noésica.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
import os
import numpy as np
import json

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from revolucion_noesica import (
    RevolucionInfinito,
    ConexionRiemannNoesica,
    LimiteComputacional,
    UnificacionNoesica,
    PrediccionFalsable,
    MatrizFalsabilidad,
    EvidenciaGravitacional,
    CienciaReproducible,
    CambioParadigmatico,
    ManifiestoRevolucionNoesica,
    validar_frecuencia_fundamental,
    calcular_coherencia
)


class TestSuite:
    """Suite de tests para el módulo de Revolución Noésica."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
    
    def assert_true(self, condition, message):
        """Validar que una condición es verdadera."""
        self.tests_run += 1
        if condition:
            self.passed += 1
            print(f"  ✅ {message}")
            return True
        else:
            self.failed += 1
            print(f"  ❌ {message}")
            return False
    
    def assert_equal(self, actual, expected, message):
        """Validar que dos valores son iguales."""
        return self.assert_true(actual == expected, 
                               f"{message} (esperado: {expected}, actual: {actual})")
    
    def assert_in_range(self, value, min_val, max_val, message):
        """Validar que un valor está en un rango."""
        return self.assert_true(min_val <= value <= max_val,
                               f"{message} (valor: {value}, rango: [{min_val}, {max_val}])")
    
    def report(self):
        """Generar reporte final."""
        print(f"\n{'='*70}")
        print(f"📊 REPORTE FINAL DE TESTS")
        print(f"{'='*70}")
        print(f"Tests ejecutados: {self.tests_run}")
        print(f"Tests exitosos: {self.passed}")
        print(f"Tests fallidos: {self.failed}")
        print(f"Tasa de éxito: {self.passed/self.tests_run*100:.1f}%")
        
        if self.failed == 0:
            print(f"\n🎉 ¡TODOS LOS TESTS PASARON!")
            return 0
        else:
            print(f"\n⚠️  Algunos tests fallaron")
            return 1


def test_revolucion_infinito(suite: TestSuite):
    """Tests para la clase RevolucionInfinito."""
    print("\n🔬 Test: RevolucionInfinito")
    print("-" * 50)
    
    revolucion = RevolucionInfinito()
    
    # Verificar frecuencia fundamental
    suite.assert_equal(revolucion.frecuencia_fundamental, 141.7001,
                      "Frecuencia fundamental correcta")
    
    # Verificar alpha_psi
    suite.assert_in_range(revolucion.alpha_psi, 0.007, 0.008,
                         "Alpha Ψ en rango esperado")
    
    # Verificar que los métodos devuelven strings
    suite.assert_true(isinstance(revolucion.paradigma_tradicional(), str),
                     "paradigma_tradicional devuelve string")
    
    suite.assert_true(isinstance(revolucion.solucion_noesica(), str),
                     "solucion_noesica devuelve string")
    
    # Verificar cálculo de campo Psi
    psi = revolucion.calcular_campo_psi(intensidad=1.0, area_efectiva=2.0)
    suite.assert_equal(psi, 4.0, "Cálculo de campo Ψ correcto")


def test_conexion_riemann(suite: TestSuite):
    """Tests para ConexionRiemannNoesica."""
    print("\n🔬 Test: ConexionRiemannNoesica")
    print("-" * 50)
    
    conexion = ConexionRiemannNoesica()
    
    suite.assert_true(len(conexion.problema) > 0,
                     "Problema de Riemann definido")
    
    suite.assert_true('10⁻⁵⁰' in conexion.validacion,
                     "Criterio de validación incluye precisión esperada")


def test_unificacion_noesica(suite: TestSuite):
    """Tests para la clase UnificacionNoesica."""
    print("\n🔬 Test: UnificacionNoesica")
    print("-" * 50)
    
    unif = UnificacionNoesica()
    
    # Verificar frecuencia fundamental
    suite.assert_equal(unif.f0, 141.7001, "f₀ correcta")
    
    # Verificar razón áurea
    suite.assert_in_range(unif.R_psi, 1.618, 1.619, "Razón áurea correcta")
    
    # Verificar dominios
    dom_mat = unif.dominio_matematico()
    suite.assert_true('nucleo' in dom_mat, "Dominio matemático tiene núcleo")
    
    dom_fis = unif.dominio_fisico()
    suite.assert_true('141.7001' in dom_fis['sintesis'], 
                     "Dominio físico menciona f₀")
    
    # Verificar cálculo de armónicos
    armonicos = unif.calcular_frecuencias_armonicas(3)
    suite.assert_true(len(armonicos) > 0, "Se calculan armónicos")
    suite.assert_true(141.7001 in armonicos, "f₀ está en armónicos")


def test_matriz_falsabilidad(suite: TestSuite):
    """Tests para la clase MatrizFalsabilidad."""
    print("\n🔬 Test: MatrizFalsabilidad")
    print("-" * 50)
    
    matriz = MatrizFalsabilidad()
    
    # Verificar que existen predicciones
    suite.assert_true(len(matriz.predicciones) > 0,
                     "Matriz tiene predicciones")
    
    # Verificar predicción gravitacional
    pred_grav = matriz.obtener_prediccion('gravitacional')
    suite.assert_true(pred_grav is not None,
                     "Predicción gravitacional existe")
    
    suite.assert_equal(pred_grav.estado, '✅ Confirmado',
                      "Predicción gravitacional confirmada")
    
    suite.assert_true('GW150914' in pred_grav.resultados['evento'],
                     "Resultados incluyen GW150914")
    
    # Verificar métodos de listado
    confirmadas = matriz.listar_confirmadas()
    suite.assert_true('gravitacional' in confirmadas,
                     "Gravitacional está en confirmadas")
    
    pendientes = matriz.listar_pendientes()
    suite.assert_true(len(pendientes) > 0,
                     "Existen predicciones pendientes")
    
    # Verificar reporte
    reporte = matriz.generar_reporte()
    suite.assert_true(len(reporte) > 100,
                     "Reporte generado tiene contenido")


def test_ciencia_reproducible(suite: TestSuite):
    """Tests para la clase CienciaReproducible."""
    print("\n🔬 Test: CienciaReproducible")
    print("-" * 50)
    
    ciencia = CienciaReproducible()
    
    # Verificar principios
    principios = ciencia.principios()
    suite.assert_true('GWOSC' in principios,
                     "Principios mencionan GWOSC")
    
    # Verificar implementación
    impl = ciencia.implementacion()
    suite.assert_true('repositorio' in impl,
                     "Implementación define repositorio")
    
    suite.assert_true('GWPy' in impl['tecnologias'],
                     "Tecnologías incluyen GWPy")
    
    # Verificar validación
    es_reproducible = ciencia.validar_reproducibilidad(
        datos_publicos=True,
        codigo_abierto=True,
        metodos_documentados=True
    )
    suite.assert_true(es_reproducible,
                     "Sistema es reproducible cuando cumple criterios")


def test_cambio_paradigmatico(suite: TestSuite):
    """Tests para la clase CambioParadigmatico."""
    print("\n🔬 Test: CambioParadigmatico")
    print("-" * 50)
    
    cambio = CambioParadigmatico()
    
    # Verificar paradigmas
    antiguo = cambio.paradigma_antiguo()
    suite.assert_true('FRAGMENTADA' in antiguo,
                     "Paradigma antiguo menciona fragmentación")
    
    nuevo = cambio.paradigma_noesico()
    suite.assert_true('UNIFICADA' in nuevo,
                     "Paradigma nuevo menciona unificación")
    
    # Verificar implicaciones
    impl = cambio.implicaciones()
    suite.assert_true('epistemologia' in impl,
                     "Implicaciones incluyen epistemología")
    
    # Verificar comparación
    comp = cambio.comparar_paradigmas()
    suite.assert_true('matematicas' in comp,
                     "Comparación incluye matemáticas")
    
    suite.assert_true('141.7001' in comp['fisica'][1],
                     "Nueva física menciona f₀")


def test_manifiesto_revolucion(suite: TestSuite):
    """Tests para la clase ManifiestoRevolucionNoesica."""
    print("\n🔬 Test: ManifiestoRevolucionNoesica")
    print("-" * 50)
    
    manifiesto = ManifiestoRevolucionNoesica()
    
    # Verificar atributos básicos
    suite.assert_equal(manifiesto.frecuencia_fundamental, 141.7001,
                      "Frecuencia fundamental correcta")
    
    # Verificar proclamaciones
    proclamaciones = manifiesto.proclamaciones()
    suite.assert_equal(len(proclamaciones), 6,
                      "Existen 6 proclamaciones")
    
    suite.assert_true('INFINITO' in proclamaciones[0],
                     "Primera proclamación sobre infinito")
    
    # Verificar texto completo
    texto = manifiesto.texto_completo()
    suite.assert_true('LA ERA Ψ HA COMENZADO' in texto,
                     "Texto incluye proclamación final")
    
    # Verificar verificación de revolución
    verif = manifiesto.verificacion_revolucion()
    suite.assert_true('problemas_resueltos' in verif,
                     "Verificación incluye problemas resueltos")
    
    suite.assert_true(len(verif['problemas_resueltos']) >= 5,
                     "Al menos 5 problemas resueltos")
    
    # Verificar exportación JSON
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name
    
    try:
        data = manifiesto.exportar_json(filepath)
        suite.assert_true(os.path.exists(filepath),
                         "Archivo JSON creado")
        
        suite.assert_true('version' in data,
                         "JSON contiene versión")
        
        suite.assert_true('frecuencia_fundamental' in data,
                         "JSON contiene frecuencia fundamental")
        
        # Leer y verificar
        with open(filepath, 'r') as f:
            loaded = json.load(f)
            suite.assert_equal(loaded['frecuencia_fundamental'], 141.7001,
                              "Frecuencia en JSON correcta")
    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_funciones_auxiliares(suite: TestSuite):
    """Tests para funciones auxiliares."""
    print("\n🔬 Test: Funciones Auxiliares")
    print("-" * 50)
    
    # Test validar_frecuencia_fundamental
    coincide, desv = validar_frecuencia_fundamental(141.7001)
    suite.assert_true(coincide, "Frecuencia exacta coincide")
    suite.assert_equal(desv, 0.0, "Desviación es cero para f₀")
    
    coincide, desv = validar_frecuencia_fundamental(141.69)
    suite.assert_true(not coincide, "141.69 Hz no coincide (fuera de tolerancia)")
    
    coincide, desv = validar_frecuencia_fundamental(141.7002)
    suite.assert_true(coincide, "141.7002 Hz coincide (dentro de tolerancia)")
    
    # Test calcular_coherencia
    sample_rate = 4096
    duration = 1
    t = np.arange(0, duration, 1/sample_rate)
    
    # Señal pura en f₀
    signal_puro = np.sin(2 * np.pi * 141.7001 * t)
    coherencia = calcular_coherencia(signal_puro, 141.7001, sample_rate)
    suite.assert_true(coherencia > 0, "Coherencia positiva para señal pura")
    
    # Señal con ruido
    signal_ruido = signal_puro + np.random.normal(0, 0.5, len(t))
    coherencia_ruido = calcular_coherencia(signal_ruido, 141.7001, sample_rate)
    suite.assert_true(coherencia_ruido > 0, "Coherencia positiva con ruido")


def test_integracion_completa(suite: TestSuite):
    """Test de integración completo del sistema."""
    print("\n🔬 Test: Integración Completa")
    print("-" * 50)
    
    # Crear instancia completa
    manifiesto = ManifiestoRevolucionNoesica()
    
    # Verificar todos los componentes están inicializados
    suite.assert_true(manifiesto.revolucion_infinito is not None,
                     "RevolucionInfinito inicializada")
    
    suite.assert_true(manifiesto.unificacion is not None,
                     "UnificacionNoesica inicializada")
    
    suite.assert_true(manifiesto.matriz_falsabilidad is not None,
                     "MatrizFalsabilidad inicializada")
    
    suite.assert_true(manifiesto.ciencia_reproducible is not None,
                     "CienciaReproducible inicializada")
    
    suite.assert_true(manifiesto.cambio_paradigmatico is not None,
                     "CambioParadigmatico inicializada")
    
    # Verificar workflow completo
    reporte = manifiesto.generar_reporte_completo()
    suite.assert_true(len(reporte) > 500,
                     "Reporte completo generado")
    
    suite.assert_true('MANIFIESTO' in reporte,
                     "Reporte contiene manifiesto")
    
    suite.assert_true('VERIFICACIÓN' in reporte,
                     "Reporte contiene verificación")
    
    suite.assert_true('MATRIZ DE FALSABILIDAD' in reporte,
                     "Reporte contiene matriz")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("🧪 SUITE DE TESTS - REVOLUCIÓN NOÉSICA")
    print("=" * 70)
    
    suite = TestSuite()
    
    # Ejecutar tests
    test_revolucion_infinito(suite)
    test_conexion_riemann(suite)
    test_unificacion_noesica(suite)
    test_matriz_falsabilidad(suite)
    test_ciencia_reproducible(suite)
    test_cambio_paradigmatico(suite)
    test_manifiesto_revolucion(suite)
    test_funciones_auxiliares(suite)
    test_integracion_completa(suite)
    
    # Reporte final
    return suite.report()


if __name__ == "__main__":
    sys.exit(main())
