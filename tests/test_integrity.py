"""
tests/test_integrity.py - Suite de Verificación Nacional/Silicio (Canon Vivo v3.0.2)

Runner nativo en `python3` (sin pytest, no está instalado). Verifica que el canon
materializado en templo_core/constants.py reproduce los valores vivos del metal y que
los 4 módulos del Templo importan desde el canon vivo sin romperse.

Estructura (Opción A — pasarela dedicada, intocadas las rutas históricas):
- templo_core/  -> paquete del Templo (constants + quantum + holography +
                   blackhole_entropy + pt_symmetric + __init__)
- Core/ y core/ -> dirs históricos IMMUTABLES (poblados, NO se tocan)

Uso:
    cd repo_141hz && python3 tests/test_integrity.py
"""

import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import templo_core
    from templo_core import constants
except ModuleNotFoundError as e:
    print(f"\u2718 No se pudo importar templo_core: {e}")
    print("   ¿Ejecutaste desde la raíz del repo?  cd repo_141hz")
    sys.exit(1)

FAILED = []


def check(label, cond):
    if cond:
        print(f"  \u2714 {label}")
    else:
        print(f"  \u2718 {label}")
        FAILED.append(label)


def load_temple_module(name):
    """Carga uno de los módulos del Templo (importa desde templo_core.constants)."""
    mod = __import__(f"templo_core.{name}", fromlist=[name])
    return mod


def main():
    print("=== CANON VIVO v3.0.2 — SUITE DE VERIFICACIÓN (SILICIO) ===")
    print()
    print(f"  paquete: {templo_core.__file__}")
    print(f"  canon:   {constants.__file__}")
    print()

    # 1. Los 5 asserts de integridad (verify_integrity interno)
    print("[1] verify_integrity() / assert_canon() — 5 invariantes")
    r = constants.verify_integrity()
    for k, v in r.items():
        check(f"assert_canon['{k}']", v is True)
    check("INTEGRITY_PASSED", constants.INTEGRITY_PASSED is True)
    check("assert_canon() lanza-True", constants.assert_canon() is True)
    print()

    # 2. Valores vivos esperados (los del metal, NO la tabla histórica)
    print("[2] Valores vivos reproducidos (100 dps, del metal)")
    check("S_finite = 0.113390105644621...",
          abs(constants.S_finite - constants.mpf('0.113390105644621846986')) < constants.mpf('1e-15'))
    check("S_total = 0.119283686741023...",
          abs(constants.S_total - constants.mpf('0.119283686741023445610')) < constants.mpf('1e-15'))
    check("D_PSI_RAW = -3.912833193561943...",
          abs(constants.D_PSI_RAW - constants.mpf('-3.912833193561942784')) < constants.mpf('1e-15'))
    check("D_PSI_S1 = -3.702836978789772...",
          abs(constants.D_PSI_S1 - constants.mpf('-3.702836978789771663')) < constants.mpf('1e-15'))
    check("cos_theta_B vivo = 0.997498421616925...",
          abs(constants.cos_theta_B - constants.mpf('0.997498421616924592')) < constants.mpf('1e-15'))
    print()

    # 3. Los 4 módulos del Templo cargan desde el canon vivo
    print("[3] Módulos dependientes importan desde templo_core.constants")
    modules = ["quantum", "holography", "blackhole_entropy", "pt_symmetric"]
    loaded = {}
    for name in modules:
        try:
            loaded[name] = load_temple_module(name)
            check(f"{name}.py importa desde templo_core.constants", True)
        except Exception as e:
            check(f"{name}.py importa desde templo_core.constants", False)
            print(f"        \u2192 {type(e).__name__}: {e}")
    print()

    # 4. Consistencia cruzada: los módulos ven el mismo D_PSI_S1
    print("[4] Consistencia cruzada con el canon")
    if loaded:
        for name, mod in loaded.items():
            lam = getattr(mod, "lambda_psi", None)
            if lam is not None:
                check(f"{name}.lambda_psi == canon.D_PSI_S1",
                      abs(lam - constants.D_PSI_S1) < constants.mpf('1e-30'))
    print()

    print("=" * 60)
    if not FAILED:
        print("\u2705 TODAS LAS VERIFICACIONES PASARON (canon vivo reproducible)")
        print("\u2234\U0001F300\u03A9\u221E\u00B3\u03A6 \u00B7 TUYOYOTU \u00B7 HECHO EST\u00C1")
        return 0
    print(f"\n\u2718 {len(FAILED)} verificación(es) fallaron: {FAILED}")
    return 1


if __name__ == '__main__':
    sys.exit(main())
