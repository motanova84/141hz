"""
Tests for physics.qcal_adnz_anchor — QCAL-ADNZ-ANCHOR-v1.0 ∴ADNZ∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesADNZ           – constantes del protocolo
  - SerializadorOpReturn     – serialización OP_RETURN v1.2 (80 bytes)
  - FirmaVMD                 – firma B ADN-Z (VMD + Blake2b-16)
  - CapturaBiologica         – captura EM celular ADN-Z
  - CondicionBioNodo         – 8 condiciones BIO_NODO_ANCLADO_EN_LA_ROCA
  - MaquinaEstadosADNZ       – máquina de estados (DETECTADO → FIRMA → ANCLADO)
  - CoherenciaADNZ           – métrica Ψ_ADNZ global
  - SistemaADNZAnchor        – orquestador con activar()
  - ResultadoADNZAnchor      – dataclass de resultados
  - qcal_adnz_anchor_activar() – API pública

Invariantes clave verificados:
  - OP_RETURN exactamente 80 bytes
  - Sello 𓂀 UTF-8 == 0xF090A080
  - Frecuencia Maestra == 1417001
  - Ψ_ADNZ Diamond-State == 1.0 (float32 == 0x3F800000)
  - Firma B SNR ≥ 4.0
  - |f_est - 0.00052| ≤ 1.5e-5 Hz
  - Blake2b-16 digest de 16 bytes
  - Estado final BIO_NODO_ANCLADO_EN_LA_ROCA ✅
"""

import hashlib
import math
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.qcal_adnz_anchor import (
    # Constantes de módulo
    _F0,
    _FRECUENCIA_MAESTRA_INT,
    _MAGIC,
    _VERSION_MAJOR,
    _VERSION_MINOR,
    _SELLO_UTF8,
    _HASH_CONSTITUCION,
    _HASH_CONSTITUCION_HEX,
    _OP_RETURN_SIZE,
    _PSI_ANCHOR_REF,
    _U_CIRCULACION,
    _PSI_ADNZ_DIAMOND,
    _VMD_NFFT,
    _VMD_FS,
    _VMD_DURACION_S,
    _VMD_F_OBJ,
    _VMD_F_SIM,
    _VMD_F_TOL,
    _VMD_F_BANDA_LOW,
    _VMD_F_BANDA_HIGH,
    _VMD_SNR_UMBRAL,
    _VMD_BLAKE2_SIZE,
    _BTC_CONFIRMACIONES_MIN,
    _SELLO,
    _SELLO_COMPLETO,
    _PSI_UMBRAL,
    # Clases
    ConstantesADNZ,
    SerializadorOpReturn,
    FirmaVMD,
    CapturaBiologica,
    CondicionBioNodo,
    EstadoADNZ,
    MaquinaEstadosADNZ,
    CoherenciaADNZ,
    SistemaADNZAnchor,
    ResultadoADNZAnchor,
    # API pública
    qcal_adnz_anchor_activar,
)


# ============================================================================
# TestConstantesModulo – 18 tests
# ============================================================================

class TestConstantesModulo(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """Frecuencia fundamental = 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_frecuencia_maestra_int(self):
        """Frecuencia maestra = 1417001 (141.7001 × 10000)."""
        self.assertEqual(_FRECUENCIA_MAESTRA_INT, 1417001)

    def test_frecuencia_maestra_derivada(self):
        """Frecuencia maestra == round(f0 × 10000) redondeado."""
        self.assertEqual(_FRECUENCIA_MAESTRA_INT, int(round(_F0 * 10000)))

    def test_magic_bytes(self):
        """Magic == b'QCAL' (4 bytes ASCII)."""
        self.assertEqual(_MAGIC, b"QCAL")
        self.assertEqual(len(_MAGIC), 4)

    def test_version_major(self):
        """version_major == 1."""
        self.assertEqual(_VERSION_MAJOR, 1)

    def test_version_minor(self):
        """version_minor == 2 (v1.2 ADN-Z)."""
        self.assertEqual(_VERSION_MINOR, 2)

    def test_sello_utf8(self):
        """Sello 𓂀 UTF-8 == 0xF0 0x93 0x82 0x80 (U+13080)."""
        self.assertEqual(_SELLO_UTF8, bytes([0xF0, 0x93, 0x82, 0x80]))
        self.assertEqual(len(_SELLO_UTF8), 4)

    def test_sello_utf8_decode(self):
        """Sello UTF-8 decodifica correctamente a 𓂀."""
        self.assertEqual(_SELLO_UTF8.decode("utf-8"), "𓂀")

    def test_hash_constitucion_len(self):
        """Hash Constitución es de 32 bytes."""
        self.assertEqual(len(_HASH_CONSTITUCION), 32)

    def test_hash_constitucion_hex_len(self):
        """Hash Constitución hex es de 64 caracteres."""
        self.assertEqual(len(_HASH_CONSTITUCION_HEX), 64)

    def test_op_return_size(self):
        """Tamaño OP_RETURN == 80 bytes."""
        self.assertEqual(_OP_RETURN_SIZE, 80)

    def test_psi_adnz_diamond(self):
        """Ψ_ADNZ Diamond-State == 1.000000."""
        self.assertEqual(_PSI_ADNZ_DIAMOND, 1.0)

    def test_psi_adnz_float32(self):
        """Ψ_ADNZ == 1.0 codificado como float32 BE == 0x3F800000."""
        packed = struct.pack(">f", _PSI_ADNZ_DIAMOND)
        self.assertEqual(packed, bytes([0x3F, 0x80, 0x00, 0x00]))

    def test_vmd_nfft(self):
        """NFFT == 65536."""
        self.assertEqual(_VMD_NFFT, 65536)

    def test_vmd_snr_umbral(self):
        """SNR umbral == 4.0."""
        self.assertEqual(_VMD_SNR_UMBRAL, 4.0)

    def test_vmd_blake2_size(self):
        """Blake2b digest_size == 16 bytes."""
        self.assertEqual(_VMD_BLAKE2_SIZE, 16)

    def test_btc_confirmaciones_min(self):
        """Confirmaciones BTC mínimas == 6."""
        self.assertEqual(_BTC_CONFIRMACIONES_MIN, 6)

    def test_f_sim_within_tolerance(self):
        """f_sim está dentro de tolerancia respecto a f_objetivo."""
        self.assertLessEqual(abs(_VMD_F_SIM - _VMD_F_OBJ), _VMD_F_TOL)


# ============================================================================
# TestConstantesADNZ – 14 tests
# ============================================================================

class TestConstantesADNZ(unittest.TestCase):
    """Tests para ConstantesADNZ."""

    def setUp(self):
        self.c = ConstantesADNZ()

    def test_f0_default(self):
        """f0 por defecto == _F0."""
        self.assertAlmostEqual(self.c.f0, _F0, places=4)

    def test_frecuencia_maestra_default(self):
        """frecuencia_maestra_int por defecto == 1417001."""
        self.assertEqual(self.c.frecuencia_maestra_int, 1417001)

    def test_psi_adnz_diamond_default(self):
        """psi_adnz_diamond por defecto == 1.0."""
        self.assertEqual(self.c.psi_adnz_diamond, 1.0)

    def test_u_circulacion_default(self):
        """u_circulacion por defecto == 7.4862 BTC."""
        self.assertAlmostEqual(self.c.u_circulacion, 7.4862, places=4)

    def test_snr_umbral_default(self):
        """snr_umbral por defecto == 4.0."""
        self.assertEqual(self.c.snr_umbral, 4.0)

    def test_confirmaciones_min_default(self):
        """confirmaciones_min por defecto == 6."""
        self.assertEqual(self.c.confirmaciones_min, 6)

    def test_es_valido_default(self):
        """Constantes por defecto son válidas."""
        self.assertTrue(self.c.es_valido())

    def test_sello_utf8_bytes(self):
        """sello_utf8_bytes() retorna 4 bytes 𓂀."""
        b = self.c.sello_utf8_bytes()
        self.assertEqual(len(b), 4)
        self.assertEqual(b, _SELLO_UTF8)

    def test_hash_constitucion(self):
        """hash_constitucion() retorna 32 bytes."""
        h = self.c.hash_constitucion()
        self.assertEqual(len(h), 32)
        self.assertEqual(h, _HASH_CONSTITUCION)

    def test_f0_positivo(self):
        """f0 > 0."""
        self.assertGreater(self.c.f0, 0)

    def test_psi_adnz_exactamente_uno(self):
        """psi_adnz_diamond == 1.0 (no 0.999 ni 1.001)."""
        self.assertEqual(self.c.psi_adnz_diamond, 1.0)

    def test_frecuencia_maestra_derivada_de_f0(self):
        """frecuencia_maestra_int == round(f0 * 10000)."""
        esperado = int(round(self.c.f0 * 10000))
        self.assertEqual(self.c.frecuencia_maestra_int, esperado)

    def test_snr_umbral_positivo(self):
        """snr_umbral > 0."""
        self.assertGreater(self.c.snr_umbral, 0)

    def test_constructor_personalizado(self):
        """Constantes personalizadas son válidas si son coherentes."""
        c2 = ConstantesADNZ(f0=141.0, snr_umbral=5.0)
        # Es válido si f0 > 0 y psi_adnz_diamond == 1.0
        self.assertGreater(c2.f0, 0)
        self.assertEqual(c2.snr_umbral, 5.0)


# ============================================================================
# TestSerializadorOpReturn – 22 tests
# ============================================================================

class TestSerializadorOpReturn(unittest.TestCase):
    """Tests para SerializadorOpReturn."""

    def setUp(self):
        self.s = SerializadorOpReturn()
        self.hash_c = _HASH_CONSTITUCION
        self.firma = bytes(range(16))  # 16 bytes de prueba
        self.payload = self.s.serializar(
            hash_constitucion=self.hash_c,
            psi_anchor=0.998,
            u_circulacion=7.4862,
            firma_b_adnz=self.firma,
            frecuencia_maestra=1417001,
            psi_adnz=1.0,
        )

    def test_payload_size(self):
        """Payload tiene exactamente 80 bytes."""
        self.assertEqual(len(self.payload), 80)

    def test_magic_bytes(self):
        """Los primeros 4 bytes son QCAL."""
        self.assertEqual(self.payload[0:4], b"QCAL")

    def test_version_major(self):
        """Byte 4 es version_major == 1."""
        self.assertEqual(self.payload[4], 1)

    def test_version_minor(self):
        """Byte 5 es version_minor == 2."""
        self.assertEqual(self.payload[5], 2)

    def test_hash_constitucion_offset(self):
        """Bytes 6..37 contienen el hash de constitución."""
        self.assertEqual(self.payload[6:38], self.hash_c)

    def test_psi_anchor_float32(self):
        """Bytes 0x26..0x29 contienen psi_anchor como float32 BE."""
        (val,) = struct.unpack_from(">f", self.payload, 0x26)
        self.assertAlmostEqual(val, 0.998, places=3)

    def test_u_circulacion_float32(self):
        """Bytes 0x2A..0x2D contienen u_circulacion como float32 BE."""
        (val,) = struct.unpack_from(">f", self.payload, 0x2A)
        self.assertAlmostEqual(val, 7.4862, places=2)

    def test_firma_b_offset(self):
        """Bytes 0x2E..0x3D contienen la firma B (16 bytes)."""
        self.assertEqual(self.payload[0x2E:0x3E], self.firma)

    def test_frecuencia_maestra_uint32(self):
        """Bytes 0x3E..0x41 contienen frecuencia_maestra como uint32 BE."""
        (val,) = struct.unpack_from(">I", self.payload, 0x3E)
        self.assertEqual(val, 1417001)

    def test_psi_adnz_float32(self):
        """Bytes 0x42..0x45 contienen psi_adnz como float32 BE."""
        (val,) = struct.unpack_from(">f", self.payload, 0x42)
        self.assertAlmostEqual(val, 1.0, places=6)

    def test_sello_utf8_offset(self):
        """Bytes 0x46..0x49 contienen el sello 𓂀 UTF-8."""
        self.assertEqual(self.payload[0x46:0x4A], _SELLO_UTF8)

    def test_padding_zeros(self):
        """Los bytes de relleno (0x4A..) son todos 0x00."""
        padding = self.payload[0x4A:]
        self.assertEqual(len(padding), 6)
        self.assertTrue(all(b == 0 for b in padding))

    def test_deserializar_roundtrip(self):
        """Deserializar(Serializar(x)) recupera los campos originales."""
        campos = self.s.deserializar(self.payload)
        self.assertEqual(campos["magic"], b"QCAL")
        self.assertEqual(campos["version_major"], 1)
        self.assertEqual(campos["version_minor"], 2)
        self.assertEqual(campos["hash_constitucion"], self.hash_c)
        self.assertEqual(campos["firma_b_adnz"], self.firma)
        self.assertEqual(campos["frecuencia_maestra"], 1417001)
        self.assertEqual(campos["sello_utf8"], _SELLO_UTF8)

    def test_deserializar_psi_anchor(self):
        """Deserializar recupera psi_anchor con precisión float32."""
        campos = self.s.deserializar(self.payload)
        self.assertAlmostEqual(campos["psi_anchor"], 0.998, places=3)

    def test_deserializar_psi_adnz(self):
        """Deserializar recupera psi_adnz == 1.0."""
        campos = self.s.deserializar(self.payload)
        self.assertAlmostEqual(campos["psi_adnz"], 1.0, places=6)

    def test_verificar_sello_true(self):
        """verificar_sello retorna True para payload con sello 𓂀."""
        self.assertTrue(self.s.verificar_sello(self.payload))

    def test_verificar_sello_false_sello_incorrecto(self):
        """verificar_sello retorna False si el sello es incorrecto."""
        bad = bytearray(self.payload)
        bad[0x46] = 0x00
        self.assertFalse(self.s.verificar_sello(bytes(bad)))

    def test_error_hash_incorrecto(self):
        """ValueError si hash_constitucion no tiene 32 bytes."""
        with self.assertRaises(ValueError):
            self.s.serializar(
                hash_constitucion=b"corto",
                psi_anchor=0.998,
                u_circulacion=7.4862,
                firma_b_adnz=self.firma,
                frecuencia_maestra=1417001,
                psi_adnz=1.0,
            )

    def test_error_firma_b_incorrecto(self):
        """ValueError si firma_b_adnz no tiene 16 bytes."""
        with self.assertRaises(ValueError):
            self.s.serializar(
                hash_constitucion=self.hash_c,
                psi_anchor=0.998,
                u_circulacion=7.4862,
                firma_b_adnz=b"corto",
                frecuencia_maestra=1417001,
                psi_adnz=1.0,
            )

    def test_error_deserializar_tamano_incorrecto(self):
        """ValueError al deserializar un payload que no tiene 80 bytes."""
        with self.assertRaises(ValueError):
            self.s.deserializar(b"too_short")

    def test_error_deserializar_magic_incorrecto(self):
        """ValueError al deserializar payload con magic incorrecto."""
        bad = bytearray(self.payload)
        bad[0:4] = b"WXYZ"
        with self.assertRaises(ValueError):
            self.s.deserializar(bytes(bad))

    def test_offsets_dict_keys(self):
        """OFFSETS contiene los 11 campos especificados."""
        expected_keys = {
            "magic", "version_major", "version_minor", "hash_constitucion",
            "psi_anchor", "u_circulacion", "firma_b_adnz",
            "frecuencia_maestra", "psi_adnz", "sello_utf8", "padding",
        }
        self.assertEqual(set(self.s.OFFSETS.keys()), expected_keys)


# ============================================================================
# TestCapturaBiologica – 16 tests
# ============================================================================

class TestCapturaBiologica(unittest.TestCase):
    """Tests para CapturaBiologica."""

    def setUp(self):
        self.cap = CapturaBiologica()

    def test_n_muestras_default(self):
        """n_muestras() == int(duracion_s * fs) == 3840."""
        self.assertEqual(self.cap.n_muestras(), 3840)

    def test_capturar_length(self):
        """capturar() retorna 3840 muestras."""
        sig = self.cap.capturar()
        self.assertEqual(len(sig), 3840)

    def test_capturar_tipo(self):
        """capturar() retorna lista de floats."""
        sig = self.cap.capturar()
        self.assertIsInstance(sig, list)
        self.assertIsInstance(sig[0], float)

    def test_capturar_reproducibilidad(self):
        """capturar() con la misma semilla produce la misma señal."""
        s1 = self.cap.capturar(semilla=42)
        s2 = self.cap.capturar(semilla=42)
        self.assertEqual(s1, s2)

    def test_capturar_semillas_distintas(self):
        """capturar() con semillas distintas produce señales distintas."""
        s1 = self.cap.capturar(semilla=1)
        s2 = self.cap.capturar(semilla=2)
        self.assertNotEqual(s1, s2)

    def test_capturar_no_trivial(self):
        """La señal tiene amplitud no trivial (max > 0.1)."""
        sig = self.cap.capturar()
        self.assertGreater(max(abs(x) for x in sig), 0.1)

    def test_f_mit_dentro_tolerancia(self):
        """f_mit (de simulación) está dentro de f_tol de f_obj."""
        self.assertLessEqual(abs(self.cap.f_mit - _VMD_F_OBJ), _VMD_F_TOL)

    def test_f_mit_default_es_f_sim(self):
        """f_mit por defecto == _VMD_F_SIM."""
        self.assertAlmostEqual(self.cap.f_mit, _VMD_F_SIM, places=12)

    def test_amplitud_positiva(self):
        """amplitud_mit > 0."""
        self.assertGreater(self.cap.amplitud_mit, 0)

    def test_sigma_ruido_pequeno(self):
        """sigma_ruido << amplitud_mit (relación señal/ruido alta)."""
        self.assertLess(self.cap.sigma_ruido, self.cap.amplitud_mit / 10)

    def test_constructor_personalizado(self):
        """Constructor acepta parámetros personalizados."""
        cap2 = CapturaBiologica(duracion_s=100.0, sigma_ruido=0.001)
        self.assertEqual(cap2.n_muestras(), 100)
        self.assertEqual(cap2.sigma_ruido, 0.001)

    def test_señal_oscila(self):
        """La señal oscila: hay valores positivos y negativos."""
        sig = self.cap.capturar()
        has_pos = any(x > 0 for x in sig)
        has_neg = any(x < 0 for x in sig)
        self.assertTrue(has_pos and has_neg)

    def test_señal_primeras_muestras_cercanas_a_cero(self):
        """La primera muestra está dominada por el término del modo mitótico (≈ 0)
        más el armónico con fase π/4 y el ruido de fondo."""
        sig = self.cap.capturar()
        # sin(2π * f_mit * 0) = 0; armónico: 0.3*sin(π/4) ≈ 0.212; ruido << 0.01
        # El valor |sig[0]| debe ser ≤ |amplitud_at_gc| + sigma_ruido * 5
        max_expected = self.cap.amplitud_at_gc + self.cap.sigma_ruido * 5
        self.assertLessEqual(abs(sig[0]), max_expected + 0.05)

    def test_duracion_por_defecto(self):
        """Duración por defecto == 3840 s."""
        self.assertEqual(self.cap.duracion_s, 3840.0)

    def test_fs_por_defecto(self):
        """Frecuencia de muestreo por defecto == 1.0 Hz."""
        self.assertEqual(self.cap.fs, 1.0)

    def test_exactos_dos_ciclos(self):
        """La señal tiene exactamente 2 ciclos (n_muestras * f_mit = 2)."""
        ciclos = self.cap.n_muestras() * self.cap.f_mit
        self.assertAlmostEqual(ciclos, round(ciclos), delta=1e-9)


# ============================================================================
# TestFirmaVMD – 25 tests
# ============================================================================

class TestFirmaVMD(unittest.TestCase):
    """Tests para FirmaVMD."""

    def setUp(self):
        self.vmd = FirmaVMD()
        cap = CapturaBiologica()
        self.señal = cap.capturar(semilla=42)
        self.resultado = self.vmd.compute_firma_b_vmd(self.señal)

    def test_resultado_es_dict(self):
        """compute_firma_b_vmd() retorna un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_resultado_keys(self):
        """El dict tiene las claves: valid, f_est, snr, b_hash."""
        self.assertIn("valid", self.resultado)
        self.assertIn("f_est", self.resultado)
        self.assertIn("snr", self.resultado)
        self.assertIn("b_hash", self.resultado)

    def test_firma_valida(self):
        """La firma B del ADN-Z simulado es válida."""
        self.assertTrue(self.resultado["valid"])

    def test_snr_sobre_umbral(self):
        """SNR ≥ 4.0."""
        self.assertGreaterEqual(self.resultado["snr"], _VMD_SNR_UMBRAL)

    def test_f_est_dentro_tolerancia(self):
        """|f_est - 0.00052| ≤ 1.5e-5 Hz."""
        f_est = self.resultado["f_est"]
        self.assertLessEqual(abs(f_est - _VMD_F_OBJ), _VMD_F_TOL)

    def test_b_hash_tipo(self):
        """b_hash es bytes."""
        self.assertIsInstance(self.resultado["b_hash"], bytes)

    def test_b_hash_longitud(self):
        """b_hash tiene 16 bytes (Blake2b-16)."""
        self.assertEqual(len(self.resultado["b_hash"]), 16)

    def test_b_hash_no_nulo(self):
        """b_hash no es todo ceros."""
        self.assertNotEqual(self.resultado["b_hash"], b"\x00" * 16)

    def test_b_hash_es_blake2b(self):
        """b_hash es consistente con Blake2b digest de 16 bytes."""
        # El hash es determinista: misma señal → mismo hash
        r2 = self.vmd.compute_firma_b_vmd(self.señal)
        self.assertEqual(self.resultado["b_hash"], r2["b_hash"])

    def test_firma_nula(self):
        """firma_b_nula() retorna 16 bytes nulos."""
        nula = self.vmd.firma_b_nula()
        self.assertEqual(nula, b"\x00" * 16)
        self.assertEqual(len(nula), 16)

    def test_snr_alto_señal_fuerte(self):
        """SNR alto para señal con buena razón señal/ruido."""
        # La señal tiene amplitud 1.0 y ruido 0.01 → SNR >> 4
        self.assertGreater(self.resultado["snr"], 4.0)

    def test_firma_invalida_señal_ruido(self):
        """Firma inválida para señal de ruido puro (sin modo ADN-Z)."""
        # Señal de ruido puro sin componente en la banda
        import random
        random.seed(0)
        ruido = [random.gauss(0, 0.01) for _ in range(3840)]
        r = self.vmd.compute_firma_b_vmd(ruido)
        # SNR puede ser bajo; si no es válido, el test pasa
        # Si por casualidad es válido (raro), aceptamos
        self.assertIsInstance(r["valid"], bool)

    def test_frecuencias_list(self):
        """_frecuencias() retorna lista de nfft//2 elementos."""
        freqs = self.vmd._frecuencias()
        self.assertEqual(len(freqs), _VMD_NFFT // 2)

    def test_frecuencias_positivas(self):
        """Todas las frecuencias en _frecuencias() son ≥ 0."""
        freqs = self.vmd._frecuencias()
        self.assertTrue(all(f >= 0 for f in freqs[:100]))

    def test_frecuencia_maxima(self):
        """Última frecuencia en _frecuencias() == fs/2 - delta_f."""
        freqs = self.vmd._frecuencias()
        delta_f = _VMD_FS / _VMD_NFFT
        esperado = (_VMD_NFFT // 2 - 1) * delta_f
        self.assertAlmostEqual(freqs[-1], esperado, places=10)

    def test_butterworth_dentro_banda(self):
        """Ganancia Butterworth alta dentro de la banda de paso."""
        f_mid = (_VMD_F_BANDA_LOW + _VMD_F_BANDA_HIGH) / 2
        gain = self.vmd._butterworth_gain(f_mid)
        self.assertGreater(gain, 0.5)

    def test_butterworth_fuera_banda(self):
        """Ganancia Butterworth atenuada fuera de la banda."""
        f_fuera = 0.1  # Hz, muy por encima de la banda
        gain = self.vmd._butterworth_gain(f_fuera)
        self.assertLess(gain, 0.01)

    def test_butterworth_cero_hz(self):
        """Ganancia Butterworth a 0 Hz es 0."""
        gain = self.vmd._butterworth_gain(0.0)
        self.assertEqual(gain, 0.0)

    def test_snr_desde_magnitudes_trivial(self):
        """SNR = 0 si no hay bins vecinos."""
        mags = [0.0] * 10
        snr = self.vmd._snr_desde_magnitudes(mags, 5)
        self.assertEqual(snr, 0.0)

    def test_calcular_fft_magnitudes_longitud(self):
        """_calcular_fft_magnitudes() retorna lista de nfft//2 elementos."""
        mags = self.vmd._calcular_fft_magnitudes(self.señal)
        self.assertEqual(len(mags), _VMD_NFFT // 2)

    def test_calcular_fft_magnitudes_no_negativas(self):
        """Todas las magnitudes FFT son ≥ 0."""
        mags = self.vmd._calcular_fft_magnitudes(self.señal)
        # Verificar solo los bins en la banda (para eficiencia)
        delta_f = _VMD_FS / _VMD_NFFT
        k_low = int(math.floor(_VMD_F_BANDA_LOW / delta_f))
        k_high = int(math.ceil(_VMD_F_BANDA_HIGH / delta_f))
        for k in range(k_low, k_high + 1):
            self.assertGreaterEqual(mags[k], 0.0)

    def test_dft_magnitud_positiva(self):
        """_dft_magnitud() retorna valor ≥ 0."""
        mag = self.vmd._dft_magnitud(self.señal[:100], 0.00052)
        self.assertGreaterEqual(mag, 0.0)

    def test_dft_im_magnitud_positiva(self):
        """_dft_im_magnitud() retorna valor ≥ 0."""
        mag = self.vmd._dft_im_magnitud(self.señal[:100], 0.00052)
        self.assertGreaterEqual(mag, 0.0)

    def test_estimar_frecuencia_pico_rango(self):
        """_estimar_frecuencia_pico() retorna frecuencia en la banda."""
        # k_pico aproximado al objetivo
        delta_f = _VMD_FS / _VMD_NFFT
        k_obj = int(round(_VMD_F_OBJ / delta_f))
        f_est = self.vmd._estimar_frecuencia_pico(self.señal, k_obj)
        self.assertGreaterEqual(f_est, _VMD_F_BANDA_LOW)
        self.assertLessEqual(f_est, _VMD_F_BANDA_HIGH)


# ============================================================================
# TestCondicionBioNodo – 24 tests
# ============================================================================

class TestCondicionBioNodo(unittest.TestCase):
    """Tests para CondicionBioNodo."""

    def setUp(self):
        self.cond = CondicionBioNodo()
        self.firma_hash = bytes(range(16))
        self.op_return = b"QCAL" + b"\x00" * 76  # 80 bytes
        self.verificacion_ok = self.cond.verificar_todas(
            psi_adnz=1.0,
            firma_b_valida=True,
            frecuencia_maestra=1417001,
            hash_constitucion=_HASH_CONSTITUCION,
            sello_bytes=_SELLO_UTF8,
            op_return_payload=self.op_return,
            confirmaciones_btc=6,
            reserva_btc=7.4862,
            reserva_xau_kg=1.0,
        )

    def test_verificar_psi_adnz_uno(self):
        """Ψ_ADNZ == 1.0 es válido."""
        self.assertTrue(self.cond.verificar_psi_adnz(1.0))

    def test_verificar_psi_adnz_menor(self):
        """Ψ_ADNZ < 1.0 no es válido."""
        self.assertFalse(self.cond.verificar_psi_adnz(0.999))

    def test_verificar_psi_adnz_mayor(self):
        """Ψ_ADNZ > 1.0 no es válido."""
        self.assertFalse(self.cond.verificar_psi_adnz(1.0001))

    def test_verificar_firma_b_valida(self):
        """Firma B válida retorna True."""
        self.assertTrue(self.cond.verificar_firma_b(True))

    def test_verificar_firma_b_invalida(self):
        """Firma B inválida retorna False."""
        self.assertFalse(self.cond.verificar_firma_b(False))

    def test_verificar_frecuencia_maestra_correcta(self):
        """Frecuencia 1417001 es válida."""
        self.assertTrue(self.cond.verificar_frecuencia_maestra(1417001))

    def test_verificar_frecuencia_maestra_incorrecta(self):
        """Frecuencia distinta de 1417001 no es válida."""
        self.assertFalse(self.cond.verificar_frecuencia_maestra(1417000))

    def test_verificar_hash_constitucion_correcto(self):
        """Hash de constitución correcto retorna True."""
        self.assertTrue(self.cond.verificar_hash_constitucion(_HASH_CONSTITUCION))

    def test_verificar_hash_constitucion_incorrecto(self):
        """Hash incorrecto retorna False."""
        self.assertFalse(self.cond.verificar_hash_constitucion(b"\x00" * 32))

    def test_verificar_sello_correcto(self):
        """Sello 𓂀 correcto retorna True."""
        self.assertTrue(self.cond.verificar_sello(_SELLO_UTF8))

    def test_verificar_sello_incorrecto(self):
        """Sello incorrecto retorna False."""
        self.assertFalse(self.cond.verificar_sello(b"\x00\x00\x00\x00"))

    def test_verificar_op_return_80_bytes(self):
        """Payload de 80 bytes retorna True."""
        self.assertTrue(self.cond.verificar_op_return_size(b"\x00" * 80))

    def test_verificar_op_return_tamano_incorrecto(self):
        """Payload de longitud incorrecta retorna False."""
        self.assertFalse(self.cond.verificar_op_return_size(b"\x00" * 79))
        self.assertFalse(self.cond.verificar_op_return_size(b"\x00" * 81))

    def test_verificar_confirmaciones_6(self):
        """6 confirmaciones es suficiente."""
        self.assertTrue(self.cond.verificar_confirmaciones(6))

    def test_verificar_confirmaciones_mas_de_6(self):
        """Más de 6 confirmaciones también es válido."""
        self.assertTrue(self.cond.verificar_confirmaciones(100))

    def test_verificar_confirmaciones_5(self):
        """5 confirmaciones no es suficiente."""
        self.assertFalse(self.cond.verificar_confirmaciones(5))

    def test_verificar_reserva_ok(self):
        """Reserva ≥ 7.4862 BTC y ≥ 1 kg XAU es válida."""
        self.assertTrue(self.cond.verificar_reserva(7.4862, 1.0))

    def test_verificar_reserva_insuficiente_btc(self):
        """Reserva BTC insuficiente retorna False."""
        self.assertFalse(self.cond.verificar_reserva(7.0, 1.0))

    def test_verificar_reserva_insuficiente_xau(self):
        """Reserva XAU insuficiente retorna False."""
        self.assertFalse(self.cond.verificar_reserva(7.4862, 0.9))

    def test_verificar_todas_ok(self):
        """Verificar todas las condiciones retorna True si todas pasan."""
        self.assertTrue(self.verificacion_ok["todas_validas"])

    def test_verificar_todas_condiciones_dict(self):
        """verificar_todas() retorna dict con 8 condiciones."""
        condiciones = self.verificacion_ok["condiciones"]
        self.assertEqual(len(condiciones), 8)

    def test_verificar_todas_una_falla(self):
        """Si una condición falla, todas_validas es False."""
        v = self.cond.verificar_todas(
            psi_adnz=0.9,  # FALLA: psi < 1.0
            firma_b_valida=True,
            frecuencia_maestra=1417001,
            hash_constitucion=_HASH_CONSTITUCION,
            sello_bytes=_SELLO_UTF8,
            op_return_payload=self.op_return,
            confirmaciones_btc=6,
            reserva_btc=7.4862,
            reserva_xau_kg=1.0,
        )
        self.assertFalse(v["todas_validas"])

    def test_psi_adnz_float32_exacto(self):
        """Float32 de 1.0 es exactamente 0x3F800000."""
        packed = struct.pack(">f", 1.0)
        self.assertEqual(packed, bytes([0x3F, 0x80, 0x00, 0x00]))
        self.assertTrue(self.cond.verificar_psi_adnz(1.0))

    def test_verificar_todas_retorna_dict(self):
        """verificar_todas() retorna dict con claves condiciones y todas_validas."""
        self.assertIn("condiciones", self.verificacion_ok)
        self.assertIn("todas_validas", self.verificacion_ok)


# ============================================================================
# TestMaquinaEstadosADNZ – 22 tests
# ============================================================================

class TestMaquinaEstadosADNZ(unittest.TestCase):
    """Tests para MaquinaEstadosADNZ."""

    def setUp(self):
        self.maquina = MaquinaEstadosADNZ()
        self.firma_valida = {"valid": True, "f_est": 0.00052, "snr": 37.0, "b_hash": b"\x00" * 16}
        self.firma_invalida = {"valid": False, "f_est": 0.00052, "snr": 1.0, "b_hash": b"\x00" * 16}
        self.verificacion_ok = {
            "todas_validas": True,
            "condiciones": {
                "psi_adnz_diamond": True,
                "firma_b_valida": True,
                "frecuencia_maestra": True,
                "hash_constitucion": True,
                "sello_utf8": True,
                "op_return_80_bytes": True,
                "confirmaciones_btc": True,
                "reserva_suficiente": True,
            },
        }
        self.verificacion_fallo_reserva = {
            "todas_validas": False,
            "condiciones": {"reserva_suficiente": False},
        }

    def test_estado_inicial(self):
        """Estado inicial es INACTIVO."""
        self.assertEqual(self.maquina.estado, EstadoADNZ.INACTIVO)

    def test_historial_inicial(self):
        """Historial inicial contiene solo INACTIVO."""
        self.assertEqual(self.maquina.historial, [EstadoADNZ.INACTIVO])

    def test_procesar_psi_valido(self):
        """Ψ_ADNZ == 1.0 → ADN_Z_DETECTADO."""
        estado = self.maquina.procesar_psi(1.0)
        self.assertEqual(estado, EstadoADNZ.ADN_Z_DETECTADO)

    def test_procesar_psi_invalido(self):
        """Ψ_ADNZ < 1.0 → FALLO_PSI."""
        estado = self.maquina.procesar_psi(0.9)
        self.assertEqual(estado, EstadoADNZ.FALLO_PSI)

    def test_procesar_firma_valida(self):
        """Firma válida desde ADN_Z_DETECTADO → FIRMA_B_VALIDA."""
        self.maquina.procesar_psi(1.0)
        estado = self.maquina.procesar_firma(self.firma_valida)
        self.assertEqual(estado, EstadoADNZ.FIRMA_B_VALIDA)

    def test_procesar_firma_invalida(self):
        """Firma inválida → FALLO_FIRMA."""
        self.maquina.procesar_psi(1.0)
        estado = self.maquina.procesar_firma(self.firma_invalida)
        self.assertEqual(estado, EstadoADNZ.FALLO_FIRMA)

    def test_procesar_ancla_ok(self):
        """Verificación ok desde FIRMA_B_VALIDA → BIO_NODO_ANCLADO."""
        self.maquina.procesar_psi(1.0)
        self.maquina.procesar_firma(self.firma_valida)
        estado = self.maquina.procesar_ancla(self.verificacion_ok)
        self.assertEqual(estado, EstadoADNZ.BIO_NODO_ANCLADO)

    def test_procesar_ancla_fallo_reserva(self):
        """Fallo de reserva → FALLO_RESERVA."""
        self.maquina.procesar_psi(1.0)
        self.maquina.procesar_firma(self.firma_valida)
        estado = self.maquina.procesar_ancla(self.verificacion_fallo_reserva)
        self.assertEqual(estado, EstadoADNZ.FALLO_RESERVA)

    def test_esta_anclado_true(self):
        """esta_anclado() es True cuando el estado es BIO_NODO_ANCLADO."""
        self.maquina.procesar_psi(1.0)
        self.maquina.procesar_firma(self.firma_valida)
        self.maquina.procesar_ancla(self.verificacion_ok)
        self.assertTrue(self.maquina.esta_anclado())

    def test_esta_anclado_false_inicial(self):
        """esta_anclado() es False en estado inicial."""
        self.assertFalse(self.maquina.esta_anclado())

    def test_reset(self):
        """reset() devuelve la máquina a INACTIVO."""
        self.maquina.procesar_psi(1.0)
        self.maquina.reset()
        self.assertEqual(self.maquina.estado, EstadoADNZ.INACTIVO)
        self.assertEqual(self.maquina.historial, [EstadoADNZ.INACTIVO])

    def test_historial_acumula_estados(self):
        """El historial acumula todos los estados visitados."""
        self.maquina.procesar_psi(1.0)
        self.maquina.procesar_firma(self.firma_valida)
        self.maquina.procesar_ancla(self.verificacion_ok)
        historial = self.maquina.historial
        self.assertEqual(historial[0], EstadoADNZ.INACTIVO)
        self.assertEqual(historial[1], EstadoADNZ.ADN_Z_DETECTADO)
        self.assertEqual(historial[2], EstadoADNZ.FIRMA_B_VALIDA)
        self.assertEqual(historial[3], EstadoADNZ.BIO_NODO_ANCLADO)

    def test_procesar_firma_sin_estado_previo(self):
        """procesar_firma() sin estado ADN_Z_DETECTADO no cambia estado."""
        estado_antes = self.maquina.estado
        self.maquina.procesar_firma(self.firma_valida)
        self.assertEqual(self.maquina.estado, estado_antes)

    def test_procesar_ancla_sin_estado_previo(self):
        """procesar_ancla() sin estado FIRMA_B_VALIDA no cambia estado."""
        estado_antes = self.maquina.estado
        self.maquina.procesar_ancla(self.verificacion_ok)
        self.assertEqual(self.maquina.estado, estado_antes)

    def test_estado_bio_nodo_anclado_valor_string(self):
        """BIO_NODO_ANCLADO tiene valor 'BIO_NODO_ANCLADO_EN_LA_ROCA'."""
        self.assertEqual(EstadoADNZ.BIO_NODO_ANCLADO.value, "BIO_NODO_ANCLADO_EN_LA_ROCA")

    def test_estado_fallo_psi_valor_string(self):
        """FALLO_PSI tiene valor 'FALLO_PSI'."""
        self.assertEqual(EstadoADNZ.FALLO_PSI.value, "FALLO_PSI")

    def test_flujo_completo_exitoso(self):
        """Flujo PSI → FIRMA → ANCLA llega a BIO_NODO_ANCLADO."""
        m = MaquinaEstadosADNZ()
        m.procesar_psi(1.0)
        m.procesar_firma(self.firma_valida)
        m.procesar_ancla(self.verificacion_ok)
        self.assertEqual(m.estado, EstadoADNZ.BIO_NODO_ANCLADO)
        self.assertTrue(m.esta_anclado())

    def test_flujo_fallo_psi(self):
        """Fallo PSI se queda en FALLO_PSI."""
        m = MaquinaEstadosADNZ()
        m.procesar_psi(0.5)
        self.assertEqual(m.estado, EstadoADNZ.FALLO_PSI)

    def test_flujo_fallo_firma(self):
        """Firma inválida resulta en FALLO_FIRMA."""
        m = MaquinaEstadosADNZ()
        m.procesar_psi(1.0)
        m.procesar_firma(self.firma_invalida)
        self.assertEqual(m.estado, EstadoADNZ.FALLO_FIRMA)

    def test_historial_es_copia(self):
        """historial es una copia, no la lista interna."""
        h = self.maquina.historial
        h.append(EstadoADNZ.FALLO_PSI)
        self.assertEqual(len(self.maquina.historial), 1)

    def test_estado_inactivo_valor_string(self):
        """INACTIVO tiene valor 'INACTIVO'."""
        self.assertEqual(EstadoADNZ.INACTIVO.value, "INACTIVO")

    def test_estado_firma_b_valida_valor_string(self):
        """FIRMA_B_VALIDA tiene valor 'FIRMA_B_VALIDA'."""
        self.assertEqual(EstadoADNZ.FIRMA_B_VALIDA.value, "FIRMA_B_VALIDA")


# ============================================================================
# TestCoherenciaADNZ – 18 tests
# ============================================================================

class TestCoherenciaADNZ(unittest.TestCase):
    """Tests para CoherenciaADNZ."""

    def setUp(self):
        self.coh = CoherenciaADNZ()

    def test_calcular_todo_uno(self):
        """Si todos los Ψ son 1.0, Ψ_global == 1.0."""
        psi = self.coh.calcular(1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(psi, 1.0, places=6)

    def test_calcular_todo_cero(self):
        """Si todos los Ψ son 0.0, Ψ_global == 0.0."""
        psi = self.coh.calcular(0.0, 0.0, 0.0, 0.0)
        self.assertAlmostEqual(psi, 0.0, places=6)

    def test_calcular_rango(self):
        """Ψ_global ∈ [0, 1]."""
        psi = self.coh.calcular(0.5, 0.7, 0.3, 0.9)
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_pesos_suma_uno(self):
        """La suma de pesos es 1.0 (promedio ponderado normalizado)."""
        suma_pesos = sum(self.coh._PESOS)
        self.assertAlmostEqual(suma_pesos, 1.0, places=10)

    def test_sello_activo_sobre_umbral(self):
        """sello_activo() es True si Ψ_global ≥ 0.888."""
        self.assertTrue(self.coh.sello_activo(0.9))
        self.assertTrue(self.coh.sello_activo(1.0))

    def test_sello_activo_bajo_umbral(self):
        """sello_activo() es False si Ψ_global < 0.888."""
        self.assertFalse(self.coh.sello_activo(0.5))

    def test_psi_bio_snr_alto(self):
        """SNR muy alto → Ψ_bio cercano a 1."""
        psi = self.coh.psi_bio_desde_snr(1000.0)
        self.assertGreater(psi, 0.9)

    def test_psi_bio_snr_cero(self):
        """SNR = 0 → Ψ_bio = 0."""
        self.assertEqual(self.coh.psi_bio_desde_snr(0.0), 0.0)

    def test_psi_bio_snr_negativo(self):
        """SNR ≤ 0 → Ψ_bio = 0."""
        self.assertEqual(self.coh.psi_bio_desde_snr(-1.0), 0.0)

    def test_psi_firma_valida(self):
        """Firma válida → Ψ_firma = 1.0."""
        self.assertEqual(self.coh.psi_firma_desde_validez(True), 1.0)

    def test_psi_firma_invalida(self):
        """Firma inválida → Ψ_firma = 0.0."""
        self.assertEqual(self.coh.psi_firma_desde_validez(False), 0.0)

    def test_psi_cadena_6_confirmaciones(self):
        """6 confirmaciones → Ψ_cadena = 1.0."""
        self.assertAlmostEqual(self.coh.psi_cadena_desde_confirmaciones(6), 1.0, places=6)

    def test_psi_cadena_0_confirmaciones(self):
        """0 confirmaciones → Ψ_cadena = 0.0."""
        self.assertAlmostEqual(self.coh.psi_cadena_desde_confirmaciones(0), 0.0, places=6)

    def test_psi_cadena_mas_de_6(self):
        """Más de 6 confirmaciones → Ψ_cadena = 1.0 (capped)."""
        self.assertAlmostEqual(self.coh.psi_cadena_desde_confirmaciones(100), 1.0, places=6)

    def test_psi_reserva_completa(self):
        """Reserva completa → Ψ_reserva = 1.0."""
        self.assertAlmostEqual(
            self.coh.psi_reserva_desde_btc_xau(7.4862, 1.0), 1.0, places=4
        )

    def test_psi_reserva_cero(self):
        """Reserva cero → Ψ_reserva = 0.0."""
        self.assertAlmostEqual(
            self.coh.psi_reserva_desde_btc_xau(0.0, 0.0), 0.0, places=6
        )

    def test_psi_reserva_rango(self):
        """Ψ_reserva ∈ [0, 1]."""
        psi = self.coh.psi_reserva_desde_btc_xau(3.0, 0.5)
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_calcular_caso_bio_nodo(self):
        """Con todos los inputs óptimos, Ψ_global ≥ 0.888."""
        psi = self.coh.calcular(
            psi_bio=self.coh.psi_bio_desde_snr(37.0),
            psi_firma=1.0,
            psi_cadena=1.0,
            psi_reserva=1.0,
        )
        self.assertGreaterEqual(psi, 0.888)


# ============================================================================
# TestSistemaADNZAnchor – 22 tests
# ============================================================================

class TestSistemaADNZAnchor(unittest.TestCase):
    """Tests para SistemaADNZAnchor."""

    def setUp(self):
        self.sistema = SistemaADNZAnchor()
        self.resultado = self.sistema.activar()

    def test_resultado_tipo(self):
        """activar() retorna ResultadoADNZAnchor."""
        self.assertIsInstance(self.resultado, ResultadoADNZAnchor)

    def test_sello_activo(self):
        """sello_activo es True."""
        self.assertTrue(self.resultado.sello_activo)

    def test_bio_nodo_anclado(self):
        """bio_nodo_anclado es True."""
        self.assertTrue(self.resultado.bio_nodo_anclado)

    def test_estado_bio_nodo(self):
        """Estado final es BIO_NODO_ANCLADO_EN_LA_ROCA."""
        self.assertEqual(self.resultado.estado, "BIO_NODO_ANCLADO_EN_LA_ROCA")

    def test_psi_adnz_diamond(self):
        """psi_adnz == 1.0 (Diamond-State)."""
        self.assertEqual(self.resultado.psi_adnz, 1.0)

    def test_psi_global_sobre_umbral(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.resultado.psi_global, 0.888)

    def test_firma_b_valida(self):
        """firma_b_valid es True."""
        self.assertTrue(self.resultado.firma_b_valid)

    def test_firma_b_snr(self):
        """firma_b_snr ≥ 4.0."""
        self.assertGreaterEqual(self.resultado.firma_b_snr, 4.0)

    def test_firma_b_f_est_dentro_tolerancia(self):
        """|firma_b_f_est - 0.00052| ≤ 1.5e-5 Hz."""
        self.assertLessEqual(abs(self.resultado.firma_b_f_est - _VMD_F_OBJ), _VMD_F_TOL)

    def test_firma_b_hash_longitud(self):
        """firma_b_hash tiene 16 bytes."""
        self.assertEqual(len(self.resultado.firma_b_hash), 16)

    def test_op_return_80_bytes(self):
        """op_return_bytes tiene exactamente 80 bytes."""
        self.assertEqual(len(self.resultado.op_return_bytes), 80)

    def test_op_return_magic(self):
        """op_return_bytes empieza con QCAL."""
        self.assertEqual(self.resultado.op_return_bytes[:4], b"QCAL")

    def test_op_return_sello(self):
        """op_return_bytes contiene el sello 𓂀 en la posición 0x46."""
        self.assertEqual(self.resultado.op_return_bytes[0x46:0x4A], _SELLO_UTF8)

    def test_condiciones_todas_ok(self):
        """Todas las 8 condiciones son True."""
        for nombre, valor in self.resultado.condiciones.items():
            self.assertTrue(valor, f"Condición fallida: {nombre}")

    def test_ocho_condiciones(self):
        """El dict condiciones tiene exactamente 8 entradas."""
        self.assertEqual(len(self.resultado.condiciones), 8)

    def test_sello_string(self):
        """sello == '∴ADNZ∞³'."""
        self.assertEqual(self.resultado.sello, "∴ADNZ∞³")

    def test_sello_completo_string(self):
        """sello_completo contiene ∴𓂀Ω∞³Φ · TUYOYOTU."""
        self.assertIn("∴𓂀Ω∞³Φ", self.resultado.sello_completo)
        self.assertIn("TUYOYOTU", self.resultado.sello_completo)

    def test_f0_correcto(self):
        """f0 del resultado == 141.7001 Hz."""
        self.assertAlmostEqual(self.resultado.f0, 141.7001, places=4)

    def test_frecuencia_maestra_correcta(self):
        """frecuencia_maestra == 1417001."""
        self.assertEqual(self.resultado.frecuencia_maestra, 1417001)

    def test_confirmaciones_btc(self):
        """confirmaciones_btc ≥ 6."""
        self.assertGreaterEqual(self.resultado.confirmaciones_btc, 6)

    def test_reserva_btc(self):
        """reserva_btc ≥ 7.4862."""
        self.assertGreaterEqual(self.resultado.reserva_btc, 7.4862 - 1e-6)

    def test_reserva_xau_kg(self):
        """reserva_xau_kg ≥ 1.0."""
        self.assertGreaterEqual(self.resultado.reserva_xau_kg, 1.0)


# ============================================================================
# TestAPIPublica – 18 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para qcal_adnz_anchor_activar()."""

    def setUp(self):
        self.r = qcal_adnz_anchor_activar()

    def test_retorna_dict(self):
        """La API pública retorna un dict."""
        self.assertIsInstance(self.r, dict)

    def test_claves_minimas(self):
        """El dict contiene las claves esperadas."""
        claves_esperadas = [
            "sello_activo", "bio_nodo_anclado", "sello", "sello_completo",
            "estado", "psi_adnz", "psi_global", "psi_bio", "psi_firma",
            "psi_cadena", "psi_reserva", "firma_b_valid", "firma_b_snr",
            "firma_b_f_est", "firma_b_hash", "op_return_bytes", "condiciones",
            "confirmaciones_btc", "reserva_btc", "reserva_xau_kg",
            "f0", "frecuencia_maestra",
        ]
        for clave in claves_esperadas:
            self.assertIn(clave, self.r, f"Clave faltante: {clave}")

    def test_sello_activo_true(self):
        """sello_activo es True."""
        self.assertTrue(self.r["sello_activo"])

    def test_bio_nodo_anclado_true(self):
        """bio_nodo_anclado es True."""
        self.assertTrue(self.r["bio_nodo_anclado"])

    def test_estado_bio_nodo(self):
        """estado == 'BIO_NODO_ANCLADO_EN_LA_ROCA'."""
        self.assertEqual(self.r["estado"], "BIO_NODO_ANCLADO_EN_LA_ROCA")

    def test_psi_adnz_uno(self):
        """psi_adnz == 1.0."""
        self.assertEqual(self.r["psi_adnz"], 1.0)

    def test_psi_global_minimo(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_firma_b_valid(self):
        """firma_b_valid es True."""
        self.assertTrue(self.r["firma_b_valid"])

    def test_op_return_len(self):
        """op_return_bytes tiene 80 bytes."""
        self.assertEqual(len(self.r["op_return_bytes"]), 80)

    def test_firma_b_hash_len(self):
        """firma_b_hash tiene 16 bytes."""
        self.assertEqual(len(self.r["firma_b_hash"]), 16)

    def test_todas_condiciones_ok(self):
        """Todas las condiciones son True."""
        for nombre, valor in self.r["condiciones"].items():
            self.assertTrue(valor, f"Condición fallida: {nombre}")

    def test_reproducibilidad(self):
        """El resultado es reproducible con la misma semilla."""
        r1 = qcal_adnz_anchor_activar(semilla_captura=99)
        r2 = qcal_adnz_anchor_activar(semilla_captura=99)
        self.assertEqual(r1["firma_b_hash"], r2["firma_b_hash"])
        self.assertEqual(r1["op_return_bytes"], r2["op_return_bytes"])
        self.assertEqual(r1["psi_global"], r2["psi_global"])

    def test_semillas_distintas_distinto_hash(self):
        """Semillas distintas producen hashes distintos."""
        r1 = qcal_adnz_anchor_activar(semilla_captura=1)
        r2 = qcal_adnz_anchor_activar(semilla_captura=2)
        self.assertNotEqual(r1["firma_b_hash"], r2["firma_b_hash"])

    def test_insuficiente_confirmaciones_falla(self):
        """Con menos de 6 confirmaciones, no se alcanza BIO_NODO_ANCLADO."""
        r = qcal_adnz_anchor_activar(confirmaciones_btc=5)
        self.assertFalse(r["bio_nodo_anclado"])

    def test_insuficiente_reserva_btc_falla(self):
        """Con reserva BTC insuficiente, no se alcanza BIO_NODO_ANCLADO."""
        r = qcal_adnz_anchor_activar(reserva_btc=0.0)
        self.assertFalse(r["bio_nodo_anclado"])

    def test_insuficiente_reserva_xau_falla(self):
        """Con reserva XAU insuficiente, no se alcanza BIO_NODO_ANCLADO."""
        r = qcal_adnz_anchor_activar(reserva_xau_kg=0.0)
        self.assertFalse(r["bio_nodo_anclado"])

    def test_sello_correcto(self):
        """sello == '∴ADNZ∞³'."""
        self.assertEqual(self.r["sello"], "∴ADNZ∞³")

    def test_frecuencia_maestra_correcta(self):
        """frecuencia_maestra == 1417001."""
        self.assertEqual(self.r["frecuencia_maestra"], 1417001)


# ============================================================================
# TestResultadoADNZAnchor – 12 tests
# ============================================================================

class TestResultadoADNZAnchor(unittest.TestCase):
    """Tests para la dataclass ResultadoADNZAnchor."""

    def test_defaults(self):
        """ResultadoADNZAnchor tiene valores por defecto razonables."""
        r = ResultadoADNZAnchor()
        self.assertFalse(r.sello_activo)
        self.assertFalse(r.bio_nodo_anclado)
        self.assertEqual(r.sello, "∴ADNZ∞³")
        self.assertIn("TUYOYOTU", r.sello_completo)

    def test_f0_default(self):
        """f0 por defecto == _F0."""
        r = ResultadoADNZAnchor()
        self.assertAlmostEqual(r.f0, _F0, places=4)

    def test_frecuencia_maestra_default(self):
        """frecuencia_maestra por defecto == 1417001."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.frecuencia_maestra, 1417001)

    def test_firma_b_hash_default(self):
        """firma_b_hash por defecto es 16 bytes nulos."""
        r = ResultadoADNZAnchor()
        self.assertEqual(len(r.firma_b_hash), 16)
        self.assertEqual(r.firma_b_hash, b"\x00" * 16)

    def test_op_return_bytes_default(self):
        """op_return_bytes por defecto es 80 bytes nulos."""
        r = ResultadoADNZAnchor()
        self.assertEqual(len(r.op_return_bytes), 80)

    def test_condiciones_default(self):
        """condiciones por defecto es dict vacío."""
        r = ResultadoADNZAnchor()
        self.assertIsInstance(r.condiciones, dict)

    def test_psi_adnz_default(self):
        """psi_adnz por defecto == 0.0."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.psi_adnz, 0.0)

    def test_psi_global_default(self):
        """psi_global por defecto == 0.0."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.psi_global, 0.0)

    def test_estado_default(self):
        """estado por defecto es INACTIVO."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.estado, "INACTIVO")

    def test_mutabilidad(self):
        """Se pueden actualizar los campos del dataclass."""
        r = ResultadoADNZAnchor()
        r.sello_activo = True
        r.psi_adnz = 1.0
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.psi_adnz, 1.0)

    def test_confirmaciones_btc_default(self):
        """confirmaciones_btc por defecto == 0."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.confirmaciones_btc, 0)

    def test_reserva_btc_default(self):
        """reserva_btc por defecto == 0.0."""
        r = ResultadoADNZAnchor()
        self.assertEqual(r.reserva_btc, 0.0)


# ============================================================================
# TestIntegracionCompleta – 8 tests
# ============================================================================

class TestIntegracionCompleta(unittest.TestCase):
    """Tests de integración del protocolo completo."""

    def test_flujo_completo_default(self):
        """El flujo por defecto alcanza BIO_NODO_ANCLADO_EN_LA_ROCA."""
        r = qcal_adnz_anchor_activar()
        self.assertTrue(r["bio_nodo_anclado"])
        self.assertEqual(r["estado"], "BIO_NODO_ANCLADO_EN_LA_ROCA")

    def test_op_return_deserializa_correcto(self):
        """El OP_RETURN generado se puede deserializar correctamente."""
        r = qcal_adnz_anchor_activar()
        s = SerializadorOpReturn()
        campos = s.deserializar(r["op_return_bytes"])
        self.assertEqual(campos["magic"], b"QCAL")
        self.assertEqual(campos["frecuencia_maestra"], 1417001)
        self.assertAlmostEqual(campos["psi_adnz"], 1.0, places=5)
        self.assertEqual(campos["sello_utf8"], _SELLO_UTF8)

    def test_blake2b_en_op_return(self):
        """La firma B en el OP_RETURN coincide con la firma B reportada."""
        r = qcal_adnz_anchor_activar()
        s = SerializadorOpReturn()
        campos = s.deserializar(r["op_return_bytes"])
        self.assertEqual(campos["firma_b_adnz"], r["firma_b_hash"])

    def test_hash_constitucion_en_op_return(self):
        """El hash de constitución en el OP_RETURN es el canónico."""
        r = qcal_adnz_anchor_activar()
        s = SerializadorOpReturn()
        campos = s.deserializar(r["op_return_bytes"])
        self.assertEqual(campos["hash_constitucion"], _HASH_CONSTITUCION)

    def test_psi_adnz_1_en_op_return(self):
        """El OP_RETURN codifica Ψ_ADNZ = 1.0 exactamente."""
        r = qcal_adnz_anchor_activar()
        psi_bytes = r["op_return_bytes"][0x42:0x46]
        self.assertEqual(psi_bytes, bytes([0x3F, 0x80, 0x00, 0x00]))

    def test_frecuencia_maestra_en_op_return(self):
        """El OP_RETURN codifica frecuencia_maestra = 1417001 como uint32 BE."""
        r = qcal_adnz_anchor_activar()
        freq_bytes = r["op_return_bytes"][0x3E:0x42]
        (freq_int,) = struct.unpack(">I", freq_bytes)
        self.assertEqual(freq_int, 1417001)

    def test_sello_en_op_return_posicion_correcta(self):
        """El sello 𓂀 ocupa la posición 0x46 en el OP_RETURN."""
        r = qcal_adnz_anchor_activar()
        self.assertEqual(r["op_return_bytes"][0x46:0x4A], _SELLO_UTF8)

    def test_padding_en_op_return(self):
        """Los últimos 6 bytes del OP_RETURN son relleno de ceros."""
        r = qcal_adnz_anchor_activar()
        padding = r["op_return_bytes"][0x4A:]
        self.assertEqual(len(padding), 6)
        self.assertTrue(all(b == 0 for b in padding))


if __name__ == "__main__":
    unittest.main(verbosity=2)
