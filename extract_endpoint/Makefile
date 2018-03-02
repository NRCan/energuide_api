SHELL ?= /usr/bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/env || echo $$VIRTUAL_ENV)

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d env ] && python3 -m venv env || true

.PHONY: setup_python
setup_python:  virtualenv requirements.txt
	${VIRTUALENV_ROOT}/bin/pip install -q -r requirements.txt
	${VIRTUALENV_ROOT}/bin/pip install -q -e .

.PHONY: setup_project
setup_project: setup_python
	npm install -g azurite

.PHONY: test_python
test_python: virtualenv is_azurite_running
	${VIRTUALENV_ROOT}/bin/pytest tests
	${VIRTUALENV_ROOT}/bin/pylint src tests
	${VIRTUALENV_ROOT}/bin/mypy src tests --ignore-missing-imports

.PHONY: start_azurite
start_azurite:
	mkdir -p tests/azure_emulator
	azurite-blob -l tests/azure_emulator/data

is_azurite_running:
	(echo >/dev/tcp/localhost/10000) &>/dev/null && echo "Azurite is running" || ( echo "Please start Azurite before running tests (run make start_azurite in a new terminal window)" & exit 1 )

.ONESHELL:
