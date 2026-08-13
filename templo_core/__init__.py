"""
templo_core — Paquete del Templo Espectral QCAL.

Este __init__.py convierte templo_core/ en un paquete Python real para que los
módulos dependientes puedan ejecutar `from templo_core.constants import (...)`.

Canon v3.1.0-op (VIVO): los valores son computados a 100 dps desde mpmath, no
transcritos de tablas. El metal es la única fuente de verdad.

Seis volúmenes del Templo:
    I   constants / quantum / holography / blackhole_entropy / pt_symmetric
    II  quantum_chaos        (motor de caos cuántico)
    III grid_interface       (interfaz de red resonante)
    IV  string_lqg_bridge    (puente cuerdas-LQG)
    V   operational_deployment (motor operacional OperationalEngine)
    VI  noesis_autopoyesis   (Bucle Operativo Noético — AUTOPOIESIS)
"""

__version__ = "3.1.0-op"
__volumes__ = 6
__all__ = [
    "constants",
    "quantum",
    "holography",
    "blackhole_entropy",
    "pt_symmetric",
    "quantum_chaos",
    "grid_interface",
    "string_lqg_bridge",
    "operational_deployment",
    "noesis_autopoyesis",
]

from . import constants  # noqa: F401
from . import quantum_chaos  # noqa: F401
from . import grid_interface  # noqa: F401
from . import string_lqg_bridge  # noqa: F401
from . import operational_deployment  # noqa: F401
from . import noesis_autopoyesis  # noqa: F401

from .operational_deployment import OperationalEngine  # noqa: F401
from .noesis_autopoyesis import BucleNoetico  # noqa: F401
