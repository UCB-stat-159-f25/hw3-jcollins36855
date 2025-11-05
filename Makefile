# Makefile for gravitational wave analysis

.PHONY: env

env:
	@if conda env list | grep -q '^ligotools\s'; then \
		echo "Environment 'ligotools' already exists. Updating..."; \
		conda env update -f environment.yml --prune; \
	else \
		echo "Creating new environment 'ligotools'..."; \
		conda env create -f environment.yml; \
	fi
	@echo "Environment setup complete. Activate with: conda activate ligotools"


.PHONY: html

html:
	myst build --html

.PHONY: clean

clean:
	@echo "Cleaning up build artifacts..."
	rm -rf figures/* audio/* _build/
	@echo "Clean complete."