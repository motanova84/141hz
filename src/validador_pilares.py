"""Herramientas para generar reportes de validación de los tres pilares."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Union


PathLike = Union[str, Path]


def _serialise_section(section: object) -> object:
    """Normalise sections before serialisation.

    El helper garantiza que las secciones no nulas se serialicen correctamente.
    Las estructuras tipo ``dict`` o ``list`` se mantienen, mientras que valores
    ``None`` se convierten en diccionarios vacíos para evitar que ``json.dump``
    genere ``null`` donde se esperan estructuras.
    """

    if section is None:
        return {}
    return section


def guardar_json(nombre_archivo: str, contenido: object, output_dir: PathLike) -> Path:
    """Escribe ``contenido`` como JSON en ``output_dir`` y devuelve su ruta."""

    base_path = Path(output_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    ruta = base_path / nombre_archivo
    with ruta.open("w", encoding="utf-8") as handler:
        json.dump(_serialise_section(contenido), handler, indent=2, ensure_ascii=False)

    return ruta


def generar_reporte_pilares(data: Dict[str, object], output_dir: PathLike) -> List[Path]:
    """Genera los archivos JSON para cada pilar del método científico.

    Parameters
    ----------
    data:
        Diccionario que contiene las claves ``reproducibilidad``, ``falsabilidad``
        y ``evidencia_empirica``. Cada una puede ser cualquier estructura
        serializable a JSON.
    output_dir:
        Directorio donde se escribirán los archivos. Se crea automáticamente si
        no existe.

    Returns
    -------
    list of :class:`pathlib.Path`
        Rutas completas de los archivos generados, en el mismo orden en que se
        escribieron.
    """

    archivos = {
        "reproducibilidad.json": _serialise_section(data.get("reproducibilidad")),
        "falsabilidad.json": _serialise_section(data.get("falsabilidad")),
        "evidencia_empirica.json": _serialise_section(data.get("evidencia_empirica")),
    }

    rutas: List[Path] = []
    for nombre, contenido in archivos.items():
        rutas.append(guardar_json(nombre, contenido, output_dir))

    return rutas


__all__: Iterable[str] = ["guardar_json"]
