#!/usr/bin/env python3
"""
🔐 VALIDADOR DE FIRMA CRIPTOGRÁFICA QCAL ∞³

Valida la integridad de certificados RAM (Realismo Matemático) mediante
firmas criptográficas SHA3-256. Verifica que los certificados no hayan
sido alterados desde su generación.

Uso:
    python3 validate_qcal_signature.py <certificado.md> <firma.qcal_sig>

Ejemplo:
    python3 validate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH.qcal_sig
"""

import sys
import json
import hashlib
import traceback
from pathlib import Path
from datetime import datetime


def load_signature(sig_file: Path) -> dict:
    """
    Carga un archivo de firma QCAL.
    
    Args:
        sig_file: Ruta al archivo .qcal_sig
        
    Returns:
        Diccionario con los datos de la firma
    """
    if not sig_file.exists():
        raise FileNotFoundError(f"Archivo de firma no encontrado: {sig_file}")
    
    with open(sig_file, 'r') as f:
        return json.load(f)


def compute_sha3_256(file_path: Path) -> str:
    """
    Calcula el hash SHA3-256 de un archivo.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Hash SHA3-256 en formato hexadecimal
    """
    sha3 = hashlib.sha3_256()
    
    with open(file_path, 'rb') as f:
        chunk = f.read(8192)
        while chunk:
            sha3.update(chunk)
            chunk = f.read(8192)
    
    return sha3.hexdigest()


def validate_signature(certificate_file: Path, signature_file: Path) -> bool:
    """
    Valida la firma criptográfica de un certificado.
    
    Args:
        certificate_file: Ruta al certificado (.md)
        signature_file: Ruta a la firma (.qcal_sig)
        
    Returns:
        True si la firma es válida, False en caso contrario
    """
    # Encabezado
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║     🔐 VALIDADOR DE FIRMA CRIPTOGRÁFICA QCAL ∞³              ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    
    # Cargar firma
    try:
        signature_data = load_signature(signature_file)
    except Exception as e:
        print(f"❌ Error al cargar firma: {e}")
        return False
    
    # Mostrar información de la firma
    print(f"✓ Firma cargada: {signature_file.name}")
    print(f"  RAM ID: {signature_data.get('ram_id', 'N/A')}")
    print(f"  Timestamp: {signature_data.get('timestamp', 'N/A')}")
    print(f"  Frecuencia: {signature_data.get('frequency', 'N/A')} Hz")
    print()
    
    # Verificar que el certificado existe
    if not certificate_file.exists():
        print(f"❌ Certificado no encontrado: {certificate_file}")
        return False
    
    # Calcular hash del certificado
    calculated_hash = compute_sha3_256(certificate_file)
    stored_hash = signature_data.get('hash', '')
    algorithm = signature_data.get('algorithm', 'SHA3-256')
    
    # Obtener tamaño del certificado
    cert_size = certificate_file.stat().st_size
    
    # Mostrar análisis de integridad
    print("📊 Análisis de Integridad:")
    print(f"  Algoritmo: {algorithm}")
    print(f"  Hash almacenado: {stored_hash}")
    print(f"  Hash calculado:  {calculated_hash}")
    print(f"  Tamaño: {cert_size} bytes")
    print()
    
    # Validar hash
    is_valid = calculated_hash == stored_hash
    
    # Mostrar resultado
    print("═" * 63)
    if is_valid:
        print("✓ ¡FIRMA VÁLIDA!")
        print("✓ El certificado NO ha sido alterado")
        print(f"✓ Integridad verificada en frecuencia {signature_data.get('frequency', 'N/A')} Hz")
    else:
        print("❌ ¡FIRMA INVÁLIDA!")
        print("❌ El certificado HA SIDO ALTERADO")
        print("❌ La integridad NO está garantizada")
    print("═" * 63)
    print()
    
    # Estado y metadatos
    if is_valid:
        print("🌊 Estado: VALIDATED")
        print(f"🔏 Firmado por: {signature_data.get('signed_by', 'QCAL ∞³ System')}")
        print(f"📝 Nota: {signature_data.get('note', 'Certificado de Realismo Matemático sincronizado')}")
    else:
        print("⚠️  Estado: INVALID")
        print("⚠️  Advertencia: No utilice este certificado")
    
    return is_valid


def main():
    """Función principal."""
    if len(sys.argv) != 3:
        print("Uso: python3 validate_qcal_signature.py <certificado.md> <firma.qcal_sig>")
        print()
        print("Ejemplo:")
        print("  python3 validate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH.qcal_sig")
        sys.exit(1)
    
    certificate_file = Path(sys.argv[1])
    signature_file = Path(sys.argv[2])
    
    try:
        is_valid = validate_signature(certificate_file, signature_file)
        sys.exit(0 if is_valid else 1)
    except Exception as e:
        print(f"\n❌ Error durante la validación: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
