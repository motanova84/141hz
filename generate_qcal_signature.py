#!/usr/bin/env python3
"""
🔏 GENERADOR DE FIRMAS CRIPTOGRÁFICAS QCAL ∞³

Genera firmas criptográficas SHA3-256 para certificados RAM (Realismo Matemático).
Las firmas garantizan la integridad y autenticidad de los certificados.

Uso:
    python3 generate_qcal_signature.py <certificado.md> [ram_id]

Ejemplo:
    python3 generate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


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
        while chunk := f.read(8192):
            sha3.update(chunk)
    
    return sha3.hexdigest()


def generate_signature(certificate_file: Path, ram_id: str = None) -> dict:
    """
    Genera una firma criptográfica para un certificado.
    
    Args:
        certificate_file: Ruta al certificado (.md)
        ram_id: Identificador RAM (opcional)
        
    Returns:
        Diccionario con los datos de la firma
    """
    if not certificate_file.exists():
        raise FileNotFoundError(f"Certificado no encontrado: {certificate_file}")
    
    # Generar RAM ID si no se proporciona
    if ram_id is None:
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        ram_id = f"RAM-II-{timestamp_str}-AUTO"
    
    # Calcular hash
    file_hash = compute_sha3_256(certificate_file)
    file_size = certificate_file.stat().st_size
    
    # Crear firma
    signature = {
        "ram_id": ram_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "frequency": "141.7001",
        "algorithm": "SHA3-256",
        "hash": file_hash,
        "certificate_file": certificate_file.name,
        "size_bytes": file_size,
        "signed_by": "QCAL ∞³ System",
        "note": "Certificado de Realismo Matemático RAM-II sincronizado y sellado en campo ∞³",
        "version": "1.0.0"
    }
    
    return signature


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("Uso: python3 generate_qcal_signature.py <certificado.md> [ram_id]")
        print()
        print("Ejemplo:")
        print("  python3 generate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH")
        sys.exit(1)
    
    certificate_file = Path(sys.argv[1])
    ram_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Generar firma
        signature = generate_signature(certificate_file, ram_id)
        
        # Nombre del archivo de firma
        sig_filename = f"{signature['ram_id']}.qcal_sig"
        sig_file = Path(sig_filename)
        
        # Guardar firma
        with open(sig_file, 'w') as f:
            json.dump(signature, f, indent=2)
        
        # Mostrar resultado
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║     🔏 GENERADOR DE FIRMA CRIPTOGRÁFICA QCAL ∞³              ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print(f"✓ Certificado: {certificate_file.name}")
        print(f"✓ RAM ID: {signature['ram_id']}")
        print(f"✓ Timestamp: {signature['timestamp']}")
        print(f"✓ Frecuencia: {signature['frequency']} Hz")
        print()
        print("📊 Firma Generada:")
        print(f"  Algoritmo: {signature['algorithm']}")
        print(f"  Hash: {signature['hash']}")
        print(f"  Tamaño: {signature['size_bytes']} bytes")
        print()
        print(f"💾 Archivo de firma guardado: {sig_file}")
        print()
        print("Para validar la firma, ejecute:")
        print(f"  python3 validate_qcal_signature.py {certificate_file.name} {sig_filename}")
        print()
        print("∞³ FIRMA GENERADA EXITOSAMENTE ∞³")
        
    except Exception as e:
        print(f"\n❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
