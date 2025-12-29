import json, sys, pathlib
import click
from .analyze import analyze_catalog

@click.group()
def main():
    """QCAL CLI — análisis de coherencia (141.7 Hz) reproducible."""
    pass

@main.command("analyze")
@click.option("--catalog", type=click.Choice(["GWTC-1","O4"]), required=True)
@click.option("--band", type=float, default=141.7, show_default=True)
@click.option("--detector", type=click.Choice(["H1","L1","V1","K1","ALL"]), default="H1")
@click.option("--outdir", type=click.Path(), default="artifacts", show_default=True)
def analyze_cmd(catalog, band, detector, outdir):
    """Ejecuta análisis y exporta figuras/CSV a artifacts/."""
    out = analyze_catalog(catalog=catalog, band=band, detector=detector, outdir=outdir)
    click.echo(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
