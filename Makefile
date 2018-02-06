SHELL := /usr/bin/bash
run:
	cd api
	yarn build && yarn start
setup:
	mongo energuide --eval "db.dwellings.drop()"
	cd python
	python3 -m venv env
	source env/bin/activate
	pip install -q -r requirements.txt
	pip install -q -e .
	energuide extract --infile tests/randomized_energuide_data.csv --outfile allthedata.zip
	energuide load --filename allthedata.zip
	rm allthedata.zip
test:
	cd api
	yarn test
	yarn integration
.ONESHELL:
