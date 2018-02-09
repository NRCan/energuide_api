SHELL ?= /usr/bin/bash
.PHONY: setup_python import_data
setup_python:
	python3 -m venv env
	source env/bin/activate
	pip install -q -r requirements.txt
	pip install -q -e .
import_data:
	mongo energuide --eval "db.dwellings.drop()"
	energuide extract --infile tests/randomized_energuide_data.csv --outfile allthedata.zip
	energuide load --filename allthedata.zip
	rm allthedata.zip
.ONESHELL:
