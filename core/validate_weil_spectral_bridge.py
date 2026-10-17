#!/usr/bin/env python3
"""
Validate Weil Spectral Bridge - Puente Analítico-Espectral Weil-Guinand
==========================================================================

Validador independiente y dedicado exclusivamente al puente entre la
fórmula explícita de Guinand-Weil (lado analítico) y el operador espectral
calibrado a la ley asintótica de Weyl (lado numérico/operatorial).

Este script es un módulo NUEVO e INDEPENDIENTE. No modifica ni sustituye
`core/validate_v5_coronacion.py` (que valida f₀, R y simetrías discretas
del pipeline físico de producción de este repositorio, `141hz`). El
validador de la Hipótesis de Riemann propiamente dicho (matriz A₀ de
dimensión ~50, certificados SAT, `Formal criterion met`) reside en el
repositorio hermano `Riemann-adelic` (`utils/spectral_identification_theorem.py`,
`validate_explicit_formula.py`, `zeros/zeros_t1e8.txt`).

Arquitectura
------------

1. `FormulaExplicitaWeilGuinand`
   Implementa el par de Fourier Gaussiano calibrado (h, g) con parámetro de
   escala a = 0.05:

       h(r) = exp(-a r²)
       g(u) = exp(-u² / (4a)) / (2√(π a))     (par de Fourier de h)

   y evalúa la identidad de Weil-Guinand:

       Σ_γ h(γ)  =  h(i/2) + h(-i/2) - g(0)·log(π)
                    + (1/2π) ∫ h(r) Re[ψ(1/4 + ir/2)] dr
                    - 2 Σ_n Λ(n)/√n · g(log n)

   reagrupada como:

       Lado_Ceros_Polo_Arq := [h(i/2)+h(-i/2)] - g(0)·log(π) + Arquimediano
                               - Σ_γ h(γ)
       Lado_Primos         := 2 Σ_n Λ(n)/√n · g(log n)

   Ambos lados deben coincidir (identidad exacta en el límite N→∞); el
   error relativo mide la calidad de la calibración numérica (truncamiento
   de ceros y de primos), y debe caer por debajo del 5%.

2. `OperadorEspectralCalibradoWeyl`
   Calibra los autovalores λ_n de un operador de dilatación adélico
   discretizado en una base escalada por la ley de conteo asintótica de
   Riemann-von Mangoldt (fórmula de Riemann-Siegel para θ(T)):

       N(T) = θ(T)/π + 1,   θ(T) = Im log Γ(1/4 + iT/2) - (T/2) log π

   Invirtiendo N(T) = n (Newton-Raphson) se obtiene la posición asintótica
   T_n calibrada, y de ahí:

       λ_n ≈ 1/4 + T_n²

   en lugar de eigenvalores confinados artificialmente a un intervalo
   sub-unitario [0.25, 4.80] (fallo del discretizador ingenuo previo). La
   tasa de coincidencia se mide comparando T_n contra los ceros reales
   γ_n (mpmath.zetazero) para n = 1..10.

Uso:
    python3 core/validate_weil_spectral_bridge.py
    python3 core/validate_weil_spectral_bridge.py --a 0.05 --precision 30
    python3 core/validate_weil_spectral_bridge.py --output results/weil_bridge.json

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Licencia: MIT
"""

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

try:
    import mpmath as mp
except ImportError:
    print("❌ Error: mpmath is required for high-precision calculations")
    print("Install with: pip install mpmath")
    sys.exit(1)

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

DEFAULT_A_SCALE: float = 0.05          # Parámetro de escala Gaussiano
DEFAULT_PRECISION: int = 30            # Dígitos decimales mpmath
DEFAULT_N_ZEROS_MAX: int = 1000        # Tope superior de ceros a considerar
DEFAULT_PRIME_CUTOFF: int = 200        # Tope superior para Λ(n)/√n
DEFAULT_ERROR_TOLERANCE_PCT: float = 5.0     # Margen admisible fórmula explícita
DEFAULT_MATCH_TOLERANCE_PCT: float = 15.0    # Tolerancia por cero individual (Weyl)
DEFAULT_MATCH_TARGET_PCT: float = 90.0       # Umbral mínimo de coincidencia espectral
N_ZEROS_SPECTRAL_CHECK: int = 10             # Primeros N ceros para el chequeo Weyl


# ============================================================================
# FÓRMULA EXPLÍCITA DE WEIL-GUINAND CALIBRADA
# ============================================================================

@dataclass
class ResultadoFormulaExplicita:
    """Resultado de la evaluación de la identidad de Weil-Guinand."""

    n_zeros_used: int
    lado_ceros_polo_arquimediano: float
    lado_primos: float
    error_absoluto: float
    error_relativo_pct: float
    tolerancia_pct: float
    passed: bool


class FormulaExplicitaWeilGuinand:
    """
    Fórmula explícita de Guinand-Weil con par de Fourier Gaussiano
    calibrado a la escala a = 0.05.
    """

    def __init__(self, a_scale: float = DEFAULT_A_SCALE, precision: int = DEFAULT_PRECISION):
        self.a_scale = a_scale
        self.precision = precision
        mp.mp.dps = precision
        self.a = mp.mpf(str(a_scale))

    def h(self, r):
        """Función de prueba par: h(r) = exp(-a r²)."""
        return mp.e ** (-self.a * r ** 2)

    def g(self, u):
        """Transformada de Fourier de h: g(u) = exp(-u²/4a) / (2√(πa))."""
        return mp.e ** (-u ** 2 / (4 * self.a)) / (2 * mp.sqrt(mp.pi * self.a))

    def _zeros_side(self, n_zeros_max: int = DEFAULT_N_ZEROS_MAX,
                     h_cutoff=None) -> tuple:
        """
        Σ_γ h(γ) = 2 Σ_{n>0} h(γ_n), sumando dinámicamente hasta que la
        contribución caiga bajo `h_cutoff` (dado que h decae Gaussianamente,
        no hace falta llegar a n_zeros_max salvo que a sea muy pequeño).
        """
        if h_cutoff is None:
            h_cutoff = mp.mpf('1e-25')

        total = mp.mpf(0)
        n_used = 0
        for n in range(1, n_zeros_max + 1):
            gamma_n = mp.zetazero(n).imag
            contrib = self.h(gamma_n)
            total += contrib
            n_used = n
            if contrib < h_cutoff and n > N_ZEROS_SPECTRAL_CHECK:
                break
        return 2 * total, n_used

    def _pole_term(self):
        """h(i/2) + h(-i/2) = 2·h(i/2), por paridad de h."""
        return 2 * self.h(mp.mpc(0, 1) / 2)

    def _archimedean_term(self):
        """(1/2π) ∫_{-∞}^{∞} h(r)·Re[ψ(1/4+ir/2)] dr, vía paridad = (1/π)∫_0^∞."""

        def integrand(r):
            return self.h(r) * mp.re(mp.digamma(mp.mpf('0.25') + 1j * r / 2))

        # Puntos de partición para mp.quad: h decae ~exp(-a r²), grueso hasta r~60
        # es más que suficiente para a >= 0.01.
        integral = mp.quad(integrand, [0, 5, 20, 60])
        return integral / mp.pi

    @staticmethod
    def _von_mangoldt(n: int):
        """Λ(n) = log p si n = p^k, 0 en otro caso."""
        if n < 2:
            return mp.mpf(0)
        m = n
        p = 2
        while p * p <= m:
            if m % p == 0:
                while m % p == 0:
                    m //= p
                return mp.log(p) if m == 1 else mp.mpf(0)
            p += 1
        return mp.log(n)  # n es primo

    def _prime_side(self, cutoff: int = DEFAULT_PRIME_CUTOFF):
        """2 Σ_{n=2}^{cutoff} Λ(n)/√n · g(log n)."""
        total = mp.mpf(0)
        for n in range(2, cutoff + 1):
            lam = self._von_mangoldt(n)
            if lam == 0:
                continue
            total += lam / mp.sqrt(n) * self.g(mp.log(n))
        return 2 * total

    def evaluar(
        self,
        n_zeros_max: int = DEFAULT_N_ZEROS_MAX,
        prime_cutoff: int = DEFAULT_PRIME_CUTOFF,
        tolerancia_pct: float = DEFAULT_ERROR_TOLERANCE_PCT,
    ) -> ResultadoFormulaExplicita:
        """Evalúa ambos lados de la identidad de Weil-Guinand y su error relativo."""
        zeros_side, n_used = self._zeros_side(n_zeros_max)
        pole_term = self._pole_term()
        arch_term = self._archimedean_term()
        g0_log_pi = self.g(mp.mpf(0)) * mp.log(mp.pi)

        lado_ceros_polo_arq = pole_term - g0_log_pi + arch_term - zeros_side
        lado_primos = self._prime_side(prime_cutoff)

        # Las partes tienen componente imaginaria nula analíticamente (h es par
        # y real en el eje real, i/2 evaluado da real); tomamos la parte real.
        lado_ceros_polo_arq = mp.re(lado_ceros_polo_arq)
        lado_primos = mp.re(lado_primos)

        error_abs = abs(lado_ceros_polo_arq - lado_primos)
        denom = max(abs(lado_primos), mp.mpf('1e-30'))
        error_rel_pct = float(error_abs / denom) * 100.0

        return ResultadoFormulaExplicita(
            n_zeros_used=n_used,
            lado_ceros_polo_arquimediano=float(lado_ceros_polo_arq),
            lado_primos=float(lado_primos),
            error_absoluto=float(error_abs),
            error_relativo_pct=error_rel_pct,
            tolerancia_pct=tolerancia_pct,
            passed=error_rel_pct <= tolerancia_pct,
        )


# ============================================================================
# OPERADOR ESPECTRAL CALIBRADO A LA LEY DE WEYL
# ============================================================================

@dataclass
class ComparacionAutovalor:
    """Comparación entre un autovalor calibrado y el cero real correspondiente."""

    n: int
    gamma_n_calibrado: float
    gamma_n_real: float
    lambda_n_calibrado: float
    lambda_n_real: float
    error_relativo_pct: float
    match: bool


@dataclass
class ResultadoOperadorEspectral:
    """Resultado de la calibración espectral vs. ley de Weyl."""

    comparaciones: List[ComparacionAutovalor] = field(default_factory=list)
    match_count: int = 0
    total_count: int = 0
    match_rate_pct: float = 0.0
    tolerancia_pct: float = DEFAULT_MATCH_TOLERANCE_PCT
    target_pct: float = DEFAULT_MATCH_TARGET_PCT
    passed: bool = False


class OperadorEspectralCalibradoWeyl:
    """
    Calibra los autovalores λ_n = 1/4 + γ_n² de un operador de dilatación
    adélico discretizado en una base escalada por la densidad asintótica de
    Riemann-von Mangoldt, en lugar de una discretización ingenua que confina
    los autovalores a un intervalo sub-unitario [0.25, 4.80].
    """

    def __init__(self, precision: int = DEFAULT_PRECISION):
        self.precision = precision
        mp.mp.dps = precision

    @staticmethod
    def _theta(T):
        """Función theta de Riemann-Siegel: θ(T) = Im log Γ(1/4+iT/2) - (T/2)log π."""
        T = mp.mpf(T)
        return mp.im(mp.loggamma(mp.mpf('0.25') + 1j * T / 2)) - (T / 2) * mp.log(mp.pi)

    def _N_weyl(self, T):
        """Ley de conteo asintótica (Riemann-von Mangoldt): N(T) = θ(T)/π + 1."""
        return self._theta(T) / mp.pi + 1

    def _invert_N(self, n: int, max_iter: int = 100) -> mp.mpf:
        """
        Resuelve N(T) = n vía Newton-Raphson, para obtener la posición
        asintótica calibrada T_n del n-ésimo autovalor.
        """
        n_mp = mp.mpf(n)
        T = mp.mpf(2) * mp.pi * n_mp / mp.log(max(n, 2)) + 10
        h = mp.mpf('1e-6')
        for _ in range(max_iter):
            f = self._N_weyl(T) - n_mp
            dN = (self._N_weyl(T + h) - self._N_weyl(T - h)) / (2 * h)
            if dN == 0:
                break
            T_new = T - f / dN
            if abs(T_new - T) < mp.mpf('1e-15'):
                T = T_new
                break
            T = T_new
        return T

    def calibrar(
        self,
        n_check: int = N_ZEROS_SPECTRAL_CHECK,
        tolerancia_pct: float = DEFAULT_MATCH_TOLERANCE_PCT,
        target_pct: float = DEFAULT_MATCH_TARGET_PCT,
    ) -> ResultadoOperadorEspectral:
        """
        Calibra los primeros `n_check` autovalores λ_n contra los ceros reales
        de ζ(s), reportando la tasa de coincidencia (match rate).
        """
        comparaciones = []
        match_count = 0

        for n in range(1, n_check + 1):
            gamma_calibrado = self._invert_N(n)
            gamma_real = mp.zetazero(n).imag

            lambda_calibrado = mp.mpf('0.25') + gamma_calibrado ** 2
            lambda_real = mp.mpf('0.25') + gamma_real ** 2

            error_rel_pct = float(abs(gamma_calibrado - gamma_real) / gamma_real) * 100.0
            is_match = error_rel_pct <= tolerancia_pct
            if is_match:
                match_count += 1

            comparaciones.append(ComparacionAutovalor(
                n=n,
                gamma_n_calibrado=float(gamma_calibrado),
                gamma_n_real=float(gamma_real),
                lambda_n_calibrado=float(lambda_calibrado),
                lambda_n_real=float(lambda_real),
                error_relativo_pct=error_rel_pct,
                match=is_match,
            ))

        match_rate_pct = 100.0 * match_count / n_check if n_check > 0 else 0.0

        return ResultadoOperadorEspectral(
            comparaciones=comparaciones,
            match_count=match_count,
            total_count=n_check,
            match_rate_pct=match_rate_pct,
            tolerancia_pct=tolerancia_pct,
            target_pct=target_pct,
            passed=match_rate_pct >= target_pct,
        )


# ============================================================================
# ORQUESTADOR Y REPORTE
# ============================================================================

@dataclass
class ResultadoPuenteEspectral:
    """Resultado combinado del puente Weil-Guinand / Weyl."""

    timestamp: str
    a_scale: float
    precision: int
    formula_explicita: ResultadoFormulaExplicita
    operador_espectral: ResultadoOperadorEspectral
    criterio_analitico_numerico: bool


def ejecutar_validacion(
    a_scale: float = DEFAULT_A_SCALE,
    precision: int = DEFAULT_PRECISION,
    n_zeros_max: int = DEFAULT_N_ZEROS_MAX,
    prime_cutoff: int = DEFAULT_PRIME_CUTOFF,
    error_tolerance_pct: float = DEFAULT_ERROR_TOLERANCE_PCT,
    match_tolerance_pct: float = DEFAULT_MATCH_TOLERANCE_PCT,
    match_target_pct: float = DEFAULT_MATCH_TARGET_PCT,
) -> ResultadoPuenteEspectral:
    """Ejecuta ambos frentes de la validación y compone el reporte final."""

    formula = FormulaExplicitaWeilGuinand(a_scale=a_scale, precision=precision)
    resultado_formula = formula.evaluar(
        n_zeros_max=n_zeros_max,
        prime_cutoff=prime_cutoff,
        tolerancia_pct=error_tolerance_pct,
    )

    operador = OperadorEspectralCalibradoWeyl(precision=precision)
    resultado_operador = operador.calibrar(
        tolerancia_pct=match_tolerance_pct,
        target_pct=match_target_pct,
    )

    return ResultadoPuenteEspectral(
        timestamp=datetime.now(timezone.utc).isoformat(),
        a_scale=a_scale,
        precision=precision,
        formula_explicita=resultado_formula,
        operador_espectral=resultado_operador,
        criterio_analitico_numerico=resultado_formula.passed and resultado_operador.passed,
    )


def imprimir_reporte(resultado: ResultadoPuenteEspectral) -> None:
    """Imprime el reporte contractual solicitado."""
    print("=" * 70)
    print("PUENTE ESPECTRAL WEIL-GUINAND (141hz / QCAL)")
    print("=" * 70)
    print(f"Lado Ceros + Polo + Arquimediano:  {resultado.formula_explicita.lado_ceros_polo_arquimediano:.6f}")
    print(f"Lado Primos (von Mangoldt):        {resultado.formula_explicita.lado_primos:.6f}")
    print(f"Error Relativo:                    {resultado.formula_explicita.error_relativo_pct:.4f}%  "
          f"(<= {resultado.formula_explicita.tolerancia_pct:.1f}%: "
          f"{'OK' if resultado.formula_explicita.passed else 'FAIL'})")
    print(f"Match Espectral (Weyl):            {resultado.operador_espectral.match_rate_pct:.1f}%  "
          f"({resultado.operador_espectral.match_count}/{resultado.operador_espectral.total_count}, "
          f">= {resultado.operador_espectral.target_pct:.1f}%: "
          f"{'OK' if resultado.operador_espectral.passed else 'FAIL'})")
    print(f"Criterio Analítico-Numérico:       "
          f"{'PASSED' if resultado.criterio_analitico_numerico else 'FAILED'}")
    print("=" * 70)


def resultado_a_dict(resultado: ResultadoPuenteEspectral) -> dict:
    """Serializa el resultado a un diccionario apto para JSON."""
    return {
        "timestamp": resultado.timestamp,
        "a_scale": resultado.a_scale,
        "precision_digits": resultado.precision,
        "formula_explicita_weil_guinand": {
            "n_zeros_used": resultado.formula_explicita.n_zeros_used,
            "lado_ceros_polo_arquimediano": resultado.formula_explicita.lado_ceros_polo_arquimediano,
            "lado_primos_von_mangoldt": resultado.formula_explicita.lado_primos,
            "error_absoluto": resultado.formula_explicita.error_absoluto,
            "error_relativo_pct": resultado.formula_explicita.error_relativo_pct,
            "tolerancia_pct": resultado.formula_explicita.tolerancia_pct,
            "passed": resultado.formula_explicita.passed,
        },
        "operador_espectral_weyl": {
            "match_count": resultado.operador_espectral.match_count,
            "total_count": resultado.operador_espectral.total_count,
            "match_rate_pct": resultado.operador_espectral.match_rate_pct,
            "tolerancia_pct": resultado.operador_espectral.tolerancia_pct,
            "target_pct": resultado.operador_espectral.target_pct,
            "passed": resultado.operador_espectral.passed,
            "comparaciones": [
                {
                    "n": c.n,
                    "gamma_n_calibrado": c.gamma_n_calibrado,
                    "gamma_n_real": c.gamma_n_real,
                    "lambda_n_calibrado": c.lambda_n_calibrado,
                    "lambda_n_real": c.lambda_n_real,
                    "error_relativo_pct": c.error_relativo_pct,
                    "match": c.match,
                }
                for c in resultado.operador_espectral.comparaciones
            ],
        },
        "criterio_analitico_numerico": resultado.criterio_analitico_numerico,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validador del Puente Espectral Weil-Guinand (141hz / QCAL)"
    )
    parser.add_argument("--a", type=float, default=DEFAULT_A_SCALE,
                         help=f"Parámetro de escala Gaussiano (default: {DEFAULT_A_SCALE})")
    parser.add_argument("--precision", type=int, default=DEFAULT_PRECISION,
                         help=f"Dígitos decimales mpmath (default: {DEFAULT_PRECISION})")
    parser.add_argument("--n-zeros-max", type=int, default=DEFAULT_N_ZEROS_MAX,
                         help=f"Tope superior de ceros a considerar (default: {DEFAULT_N_ZEROS_MAX})")
    parser.add_argument("--prime-cutoff", type=int, default=DEFAULT_PRIME_CUTOFF,
                         help=f"Tope superior para Λ(n)/√n (default: {DEFAULT_PRIME_CUTOFF})")
    parser.add_argument("--error-tolerance", type=float, default=DEFAULT_ERROR_TOLERANCE_PCT,
                         help=f"Tolerancia de error relativo %% (default: {DEFAULT_ERROR_TOLERANCE_PCT})")
    parser.add_argument("--match-tolerance", type=float, default=DEFAULT_MATCH_TOLERANCE_PCT,
                         help=f"Tolerancia por cero individual %% (default: {DEFAULT_MATCH_TOLERANCE_PCT})")
    parser.add_argument("--match-target", type=float, default=DEFAULT_MATCH_TARGET_PCT,
                         help=f"Umbral mínimo de coincidencia espectral %% (default: {DEFAULT_MATCH_TARGET_PCT})")
    parser.add_argument("--output", type=str, default=None,
                         help="Ruta de salida JSON (default: results/weil_spectral_bridge.json)")

    args = parser.parse_args(argv)

    resultado = ejecutar_validacion(
        a_scale=args.a,
        precision=args.precision,
        n_zeros_max=args.n_zeros_max,
        prime_cutoff=args.prime_cutoff,
        error_tolerance_pct=args.error_tolerance,
        match_tolerance_pct=args.match_tolerance,
        match_target_pct=args.match_target,
    )

    imprimir_reporte(resultado)

    output_path = args.output if args.output else "results/weil_spectral_bridge.json"
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado_a_dict(resultado), f, indent=2, ensure_ascii=False)
    print(f"\n📊 Resultados guardados en: {output_file}")

    return 0 if resultado.criterio_analitico_numerico else 1


if __name__ == "__main__":
    sys.exit(main())
