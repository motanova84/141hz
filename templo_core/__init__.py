"""
core — Paquete del Templo Espectral QCAL.

Este __init__.py convierte core/ en un paquete Python real para que los módulos
dependientes puedan ejecutar `from templo_core.constants import (...)` de forma fluida.

Canon v3.0.2 (VIVO): los valores son computados a 100 dps desde mpmath, no
transcritos de tablas. El metal es la única fuente de verdad.
"""

__all__ = ["constants"]

from . import constants  # noqa: F401
