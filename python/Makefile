SHELL ?= /usr/bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/env || echo $$VIRTUAL_ENV)

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d env ] && python3 -m venv env || true

.PHONY: setup_python
setup_python:  virtualenv requirements.txt
		${VIRTUALENV_ROOT}/bin/pip install -q -r requirements.txt
		${VIRTUALENV_ROOT}/bin/pip install -q -e .

.PHONY: import_data
import_data: virtualenv
	echo "Removing all NRCAN data"
	mongo energuide --eval "db.dwellings.drop()"
	${VIRTUALENV_ROOT}/bin/energuide extract --infile tests/randomized_energuide_data.csv --outfile allthedata.zip
	echo "Importing new NRCAN data"
	${VIRTUALENV_ROOT}/bin/energuide load --filename allthedata.zip
	rm allthedata.zip

.PHONY: test_python
test_python: virtualenv
	${VIRTUALENV_ROOT}/bin/pytest tests
	${VIRTUALENV_ROOT}/bin/pylint src tests
	${VIRTUALENV_ROOT}/bin/mypy src tests --ignore-missing-imports

lint: src/**/*.py tests/**/*.py
	@${VIRTUALENV_ROOT}/bin/pylint $? | tee lint
.ONESHELL:
