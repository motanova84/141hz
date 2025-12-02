#!/usr/bin/env python3
"""
Tests para el Protocolo de Falsación
Valida la lógica de evaluación de condiciones de refutación
"""
import sys
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from protocolo_falsacion import ProtocoloFalsacion


def test_teoria_no_falsada():
    """Test: Teoría NO falsada con resultados favorables"""
    print("🧪 TEST 1: Teoría NO falsada (resultados favorables)")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # Resultados favorables a la teoría
    resultados = {
        'bi2se3': {
            'snr': 8.5,  # SNR alto (> 3)
            'p_value': 0.001,  # p bajo (< 0.01)
            'n_muestras_independientes': 10
        },
        'cmb': {
            'delta_chi2': 12.0,  # Δχ² alto (> 5)
            'bayes_factor': 15.0  # BF alto (> 1)
        },
        'gw': {
            'snr': 15.2,  # SNR alto (> 5)
            'p_value': 0.0001,  # p bajo (< 0.001)
            'n_eventos': 20
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert not verificacion['teoria_falsada'], "La teoría NO debería estar falsada"
    assert len(verificacion['razones']) == 0, "No debería haber razones de falsación"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente NO falsada\n")


def test_teoria_falsada_bi2se3():
    """Test: Teoría falsada por Bi2Se3"""
    print("🧪 TEST 2: Teoría falsada por Bi2Se3")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # Bi2Se3 cumple condiciones de falsación
    resultados = {
        'bi2se3': {
            'snr': 2.0,  # SNR < 3
            'p_value': 0.05,  # p > 0.01
            'n_muestras_independientes': 10
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert verificacion['teoria_falsada'], "La teoría DEBERÍA estar falsada"
    assert 'bi2se3' in str(verificacion['razones']), "Razón debería incluir bi2se3"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente falsada por Bi2Se3\n")


def test_teoria_falsada_cmb():
    """Test: Teoría falsada por CMB"""
    print("🧪 TEST 3: Teoría falsada por CMB")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # CMB cumple condiciones de falsación
    resultados = {
        'cmb': {
            'delta_chi2': 3.0,  # Δχ² < 5
            'bayes_factor': 0.5  # BF < 1
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert verificacion['teoria_falsada'], "La teoría DEBERÍA estar falsada"
    assert 'cmb' in str(verificacion['razones']), "Razón debería incluir cmb"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente falsada por CMB\n")


def test_teoria_falsada_gw():
    """Test: Teoría falsada por ondas gravitacionales"""
    print("🧪 TEST 4: Teoría falsada por ondas gravitacionales")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # GW cumple condiciones de falsación
    resultados = {
        'gw': {
            'snr': 4.0,  # SNR < 5
            'p_value': 0.002,  # p > 0.001
            'n_eventos': 15
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert verificacion['teoria_falsada'], "La teoría DEBERÍA estar falsada"
    assert 'gw' in str(verificacion['razones']), "Razón debería incluir gw"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente falsada por GW\n")


def test_teoria_falsada_multiple():
    """Test: Teoría falsada por múltiples sistemas"""
    print("🧪 TEST 5: Teoría falsada por múltiples sistemas")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # Múltiples sistemas cumplen condiciones de falsación
    resultados = {
        'bi2se3': {
            'snr': 2.5,  # SNR < 3
            'p_value': 0.02,  # p > 0.01
            'n_muestras_independientes': 12
        },
        'cmb': {
            'delta_chi2': 4.0,  # Δχ² < 5
            'bayes_factor': 0.8  # BF < 1
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert verificacion['teoria_falsada'], "La teoría DEBERÍA estar falsada"
    assert len(verificacion['razones']) == 2, "Debería haber 2 razones de falsación"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente falsada por múltiples sistemas\n")


def test_datos_parciales():
    """Test: Teoría con datos parciales"""
    print("🧪 TEST 6: Teoría con datos parciales")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # Solo algunos sistemas tienen datos
    resultados = {
        'gw': {
            'snr': 15.2,  # SNR alto (> 5)
            'p_value': 0.0001,  # p bajo (< 0.001)
            'n_eventos': 20
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    assert not verificacion['teoria_falsada'], "La teoría NO debería estar falsada"
    assert len(verificacion['razones']) == 0, "No debería haber razones de falsación"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Teoría correctamente evaluada con datos parciales\n")


def test_criterios_boundary():
    """Test: Valores en el límite de los criterios"""
    print("🧪 TEST 7: Valores en límites de criterios")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    # Valores exactos en los límites
    resultados = {
        'bi2se3': {
            'snr': 3.0,  # Exactamente en el límite
            'p_value': 0.01,  # Exactamente en el límite
            'n_muestras_independientes': 10
        },
        'cmb': {
            'delta_chi2': 5.0,  # Exactamente en el límite
            'bayes_factor': 1.0  # Exactamente en el límite
        },
        'gw': {
            'snr': 5.0,  # Exactamente en el límite
            'p_value': 0.001,  # Exactamente en el límite
            'n_eventos': 15
        }
    }
    
    verificacion = protocolo.verificar_falsacion(resultados)
    
    # En los límites exactos, las condiciones NO deben cumplirse
    # (usamos < y > estrictos, no <= ni >=)
    assert not verificacion['teoria_falsada'], "La teoría NO debería estar falsada en los límites"
    
    print(f"   ✅ Teoría falsada: {verificacion['teoria_falsada']}")
    print(f"   ✅ Razones: {verificacion['razones']}")
    print("   ✅ TEST PASADO: Límites correctamente evaluados\n")


def test_generar_reporte():
    """Test: Generación de reporte"""
    print("🧪 TEST 8: Generación de reporte")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    resultados = {
        'gw': {
            'snr': 15.2,
            'p_value': 0.0001,
            'n_eventos': 20
        }
    }
    
    reporte = protocolo.generar_reporte_falsacion(resultados)
    
    assert isinstance(reporte, str), "El reporte debe ser un string"
    assert "PROTOCOLO DE FALSACIÓN" in reporte, "Debe incluir el título"
    assert "GW" in reporte.upper(), "Debe incluir información sobre GW"
    assert "2025-12-31" in reporte, "Debe incluir la fecha límite"
    
    print("   ✅ Reporte generado correctamente")
    print("   ✅ TEST PASADO: Generación de reporte funcional\n")


def test_obtener_criterios():
    """Test: Obtención de criterios"""
    print("🧪 TEST 9: Obtención de criterios de refutación")
    print("-" * 60)
    
    protocolo = ProtocoloFalsacion()
    
    criterios = protocolo.obtener_criterios()
    
    assert 'bi2se3' in criterios, "Debe incluir criterios de bi2se3"
    assert 'cmb' in criterios, "Debe incluir criterios de cmb"
    assert 'gw' in criterios, "Debe incluir criterios de gw"
    
    for sistema, criterio in criterios.items():
        assert 'descripcion' in criterio, f"Sistema {sistema} debe tener descripción"
        assert 'condicion' in criterio, f"Sistema {sistema} debe tener condición"
        assert 'significancia' in criterio, f"Sistema {sistema} debe tener significancia"
        assert 'consecuencia' in criterio, f"Sistema {sistema} debe tener consecuencia"
    
    print(f"   ✅ Criterios obtenidos: {list(criterios.keys())}")
    print("   ✅ TEST PASADO: Criterios correctamente estructurados\n")


def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🔬 TESTS DEL PROTOCOLO DE FALSACIÓN")
    print("=" * 70)
    print()
    
    tests = [
        ("Teoría NO falsada", test_teoria_no_falsada),
        ("Teoría falsada por Bi2Se3", test_teoria_falsada_bi2se3),
        ("Teoría falsada por CMB", test_teoria_falsada_cmb),
        ("Teoría falsada por GW", test_teoria_falsada_gw),
        ("Teoría falsada por múltiples sistemas", test_teoria_falsada_multiple),
        ("Datos parciales", test_datos_parciales),
        ("Valores límite", test_criterios_boundary),
        ("Generación de reporte", test_generar_reporte),
        ("Obtención de criterios", test_obtener_criterios)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            test_func()
            resultados.append((nombre, True, None))
        except AssertionError as e:
            print(f"   ❌ FALLO: {e}\n")
            resultados.append((nombre, False, str(e)))
        except Exception as e:
            print(f"   ❌ ERROR: {e}\n")
            resultados.append((nombre, False, str(e)))
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    
    total = len(resultados)
    pasados = sum(1 for _, passed, _ in resultados if passed)
    
    for nombre, passed, error in resultados:
        estado = "✅" if passed else "❌"
        print(f"{estado} {nombre}")
        if error:
            print(f"   Error: {error}")
    
    print()
    print(f"Tests ejecutados: {total}")
    print(f"Tests pasados: {pasados}")
    print(f"Tasa de éxito: {pasados/total*100:.1f}%")
    
    if pasados == total:
        print("\n🎉 ¡TODOS LOS TESTS PASADOS!")
        return 0
    else:
        print(f"\n❌ {total - pasados} test(s) fallido(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
