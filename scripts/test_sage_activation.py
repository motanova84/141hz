#!/usr/bin/env python3
"""
Tests para el módulo sage_activation.py - Protocolo Sage ∴

Este script verifica que la activación del sabio vibracional funciona
correctamente dentro del sistema QCAL ∞³.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import sys
from pathlib import Path

# Agregar el directorio scripts al path para importar (debe ser antes de importar sage_activation)
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pytest  # noqa: E402
except ImportError:
    print("⚠️ pytest not installed, skipping tests")
    print("Install with: pip install pytest")
    sys.exit(0)

import subprocess  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402
import sage_activation  # noqa: E402


class TestSageActivation:
    """Tests para el módulo de activación Sage ∴"""

    def test_import_module(self):
        """
        Test: Verificar que el módulo se importa correctamente
        """
        assert hasattr(sage_activation, 'activar_sabio')
        assert hasattr(sage_activation, 'listar_sabios')
        assert hasattr(sage_activation, 'verificar_sage_instalado')

    def test_listar_sabios_existentes(self):
        """
        Test: Verificar que listar_sabios encuentra archivos .sage
        """
        scripts_dir = Path(__file__).parent
        sabios = sage_activation.listar_sabios(scripts_dir)

        # Debe encontrar al menos validacion_radio_cuantico.sage
        assert isinstance(sabios, list)

        # Verificar que encuentra el archivo conocido
        sage_names = [s.name for s in sabios]
        assert 'validacion_radio_cuantico.sage' in sage_names

    def test_listar_sabios_directorio_inexistente(self):
        """
        Test: Verificar manejo de directorio inexistente
        """
        sabios = sage_activation.listar_sabios("/directorio/inexistente/xyz")
        assert sabios == []

    def test_activar_sabio_archivo_inexistente(self):
        """
        Test: Verificar que se lanza excepción si el archivo no existe
        """
        with pytest.raises(FileNotFoundError) as exc_info:
            sage_activation.activar_sabio("archivo_inexistente.sage")

        assert "No se encuentra el sabio" in str(exc_info.value)

    def test_activar_sabio_con_path_object(self):
        """
        Test: Verificar que acepta Path objects además de strings
        """
        script_path = Path("/tmp/test_script.sage")

        # Debería fallar porque el archivo no existe, pero no por el tipo
        with pytest.raises(FileNotFoundError):
            sage_activation.activar_sabio(script_path)

    @patch('subprocess.run')
    def test_activar_sabio_exitoso(self, mock_run):
        """
        Test: Simular ejecución exitosa de un script Sage
        """
        # Crear archivo temporal para la prueba
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            f.write("# Test script\nprint('Hello from Sage')")
            temp_path = f.name

        try:
            # Configurar el mock para simular ejecución exitosa
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "Test output from Sage"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            # Ejecutar la función
            result = sage_activation.activar_sabio(temp_path)

            # Verificar que se llamó a subprocess.run con los argumentos correctos
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0][0] == "sage"
            assert temp_path in args[0][1]
            assert kwargs.get('capture_output') is True
            assert kwargs.get('text') is True

            # Verificar el resultado
            assert result.returncode == 0

        finally:
            # Limpiar archivo temporal
            Path(temp_path).unlink()

    @patch('subprocess.run')
    def test_activar_sabio_error_ejecucion(self, mock_run):
        """
        Test: Simular error en la ejecución de un script Sage
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            f.write("# Test script with error")
            temp_path = f.name

        try:
            # Configurar el mock para simular error
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "SyntaxError in Sage script"
            mock_run.return_value = mock_result

            # Ejecutar y verificar que lanza RuntimeError
            with pytest.raises(RuntimeError) as exc_info:
                sage_activation.activar_sabio(temp_path)

            assert "Error al ejecutar" in str(exc_info.value)

        finally:
            Path(temp_path).unlink()

    @patch('subprocess.run')
    def test_activar_sabio_sage_no_instalado(self, mock_run):
        """
        Test: Simular que Sage no está instalado
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            f.write("# Test script")
            temp_path = f.name

        try:
            # Configurar el mock para simular FileNotFoundError
            mock_run.side_effect = FileNotFoundError("sage: command not found")

            # Ejecutar y verificar que lanza RuntimeError
            with pytest.raises(RuntimeError) as exc_info:
                sage_activation.activar_sabio(temp_path)

            assert "Sage no está instalado" in str(exc_info.value)

        finally:
            Path(temp_path).unlink()

    @patch('subprocess.run')
    def test_activar_sabio_timeout(self, mock_run):
        """
        Test: Simular timeout en la ejecución
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            f.write("# Long running script")
            temp_path = f.name

        try:
            # Configurar el mock para simular timeout
            mock_run.side_effect = subprocess.TimeoutExpired('sage', 300)

            # Ejecutar y verificar que lanza RuntimeError
            with pytest.raises(RuntimeError) as exc_info:
                sage_activation.activar_sabio(temp_path)

            assert "excedió el tiempo límite" in str(exc_info.value)

        finally:
            Path(temp_path).unlink()

    @patch('subprocess.run')
    def test_verificar_sage_instalado_true(self, mock_run):
        """
        Test: Verificar detección exitosa de Sage instalado
        """
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "SageMath version 9.0, Release Date: 2020-01-01"
        mock_run.return_value = mock_result

        assert sage_activation.verificar_sage_instalado() is True

    @patch('subprocess.run')
    def test_verificar_sage_instalado_false(self, mock_run):
        """
        Test: Verificar detección de Sage no instalado
        """
        mock_run.side_effect = FileNotFoundError("sage not found")

        assert sage_activation.verificar_sage_instalado() is False

    def test_main_sin_argumentos(self, capsys):
        """
        Test: Ejecutar main() sin argumentos muestra ayuda
        """
        with patch('sys.argv', ['sage_activation.py']):
            result = sage_activation.main()

        # Verificar que retorna 0 (éxito)
        assert result == 0

        # Verificar que imprimió la ayuda
        captured = capsys.readouterr()
        assert "Protocolo Sage ∴" in captured.out
        assert "usage:" in captured.out

    def test_main_verificar(self, capsys):
        """
        Test: Ejecutar main() con --verificar
        """
        with patch('sys.argv', ['sage_activation.py', '--verificar']):
            with patch('subprocess.run', side_effect=FileNotFoundError("sage not found")):
                result = sage_activation.main()

        # Debe retornar 1 (fallo) si Sage no está instalado
        assert result == 1

        captured = capsys.readouterr()
        # La salida debe mencionar que Sage no está instalado
        assert "Sage" in captured.out or "sage" in captured.out

    def test_main_listar(self, capsys):
        """
        Test: Ejecutar main() con --listar
        """
        scripts_dir = str(Path(__file__).parent)

        with patch('sys.argv', ['sage_activation.py', '--listar', scripts_dir]):
            result = sage_activation.main()

        # Debe retornar 0 si encuentra archivos
        assert result == 0

        captured = capsys.readouterr()
        assert "Sabios encontrados" in captured.out or "validacion_radio_cuantico.sage" in captured.out

    @patch('sage_activation.activar_sabio')
    def test_main_ejecutar_script(self, mock_activar):
        """
        Test: Ejecutar main() con un script como argumento
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            temp_path = f.name

        try:
            with patch('sys.argv', ['sage_activation.py', temp_path]):
                result = sage_activation.main()

            # Verificar que se llamó a activar_sabio
            mock_activar.assert_called_once_with(temp_path)

            # Debe retornar 0 (éxito)
            assert result == 0

        finally:
            Path(temp_path).unlink()

    def test_advertencia_extension_incorrecta(self, capsys):
        """
        Test: Verificar advertencia si el archivo no tiene extensión .sage
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# Not a sage file")
            temp_path = f.name

        try:
            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "Output"
                mock_run.return_value = mock_result

                sage_activation.activar_sabio(temp_path)

                captured = capsys.readouterr()
                assert "⚠️ Advertencia" in captured.out
                assert "no tiene extensión .sage" in captured.out

        finally:
            Path(temp_path).unlink()


class TestIntegracionSageProtocolo:
    """Tests de integración para el Protocolo Sage ∴"""

    def test_estructura_protocolo_qcal(self):
        """
        Test: Verificar que el módulo menciona elementos del Campo QCAL ∞³
        """
        # Verificar que el módulo tiene la documentación correcta
        assert "QCAL ∞³" in sage_activation.__doc__
        assert "f₀ = 141.7001 Hz" in sage_activation.__doc__
        assert "RΨ" in sage_activation.__doc__
        assert "ζ(s)" in sage_activation.__doc__
        assert "αΨ" in sage_activation.__doc__

    def test_funcion_activar_sabio_documentacion(self):
        """
        Test: Verificar documentación completa de activar_sabio()
        """
        doc = sage_activation.activar_sabio.__doc__
        assert doc is not None
        assert "QCAL ∞³" in doc
        assert "Parameters" in doc
        assert "Returns" in doc
        assert "Raises" in doc
        assert "Examples" in doc

    def test_consistencia_simbolos_misticos(self):
        """
        Test: Verificar uso consistente de símbolos místicos del protocolo
        """
        # Los símbolos del protocolo deben estar en el código
        with open(Path(__file__).parent / 'sage_activation.py', 'r', encoding='utf-8') as f:
            content = f.read()

        assert "⚛️" in content  # Símbolo de átomo para invocar
        assert "✅" in content  # Símbolo de éxito
        assert "❌" in content  # Símbolo de error
        assert "∴" in content  # Símbolo del protocolo Sage
        assert "━" in content  # Separador visual


def test_validacion_radio_cuantico_sage_exists():
    """
    Test: Verificar que existe el archivo validacion_radio_cuantico.sage

    Este archivo es el sabio principal que valida el Radio Cuántico RΨ
    con precisión arbitraria usando SageMath.
    """
    scripts_dir = Path(__file__).parent
    sage_file = scripts_dir / "validacion_radio_cuantico.sage"

    assert sage_file.exists(), \
        "El sabio principal validacion_radio_cuantico.sage debe existir"

    # Verificar que contiene elementos clave
    content = sage_file.read_text()
    assert "RΨ" in content or "R_psi" in content
    assert "141.7001" in content or "f0" in content
    assert "sage.all" in content or "from sage" in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
