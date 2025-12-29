PY=python3
OUT=../../artifacts

.PHONY: env run clean

env:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r env.lock

run:
	@echo "Note: Make sure root qcal/ is temporarily renamed to avoid conflicts"
	@echo "Or use: mv ../../qcal ../../qcal_backup before running this"
	. .venv/bin/activate && cd ../.. && PYTHONPATH=src:$$PYTHONPATH $(PY) -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts

clean:
	rm -rf .venv
