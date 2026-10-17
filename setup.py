"""setup.py - Empaquetado del Templo Espectral QCAL (Canon Vivo v3.0.2).

Opción A (pasarela dedicada): el Templo vive en `templo_core/`, paquete propio
no colisionante, intocadas las rutas históricas Core/ y core/.
Los valores son computados a 100 dps desde mpmath, no transcritos de tablas.
El metal es la única fuente de verdad.
"""

from setuptools import setup, find_packages

setup(
    name="templo-espectral-qcal",
    version="3.0.2",
    description=(
        "Templo Espectral QCAL — capa espectral de Riemann (D_Psi) coexistiendo "
        "con el canon 4D. Canon Vivo v3.0.2, valores computados a 100 dps."
    ),
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    packages=find_packages(include=["templo_core", "templo_core.*"]),
    python_requires=">=3.10",
    install_requires=[
        "mpmath>=1.3.0",
    ],
    author="Noesis \u03a8",
    author_email="noesis@qcal.io",
    url="https://github.com/motanova84/repo_141hz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
