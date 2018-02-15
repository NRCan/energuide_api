SHELL ?= /usr/bin/bash
export NRCAN_DB_CONNECTION_STRING ?= mongodb://localhost:27017
export NRCAN_DB_NAME ?= energuide
export NRCAN_COLLECTION_NAME ?= dwellings

.PHONY: run build test install check_api_key watch
check_api_key:
	[ -z $$NRCAN_ENGINE_API_KEY ] && echo "NRCAN_ENGINE_API_KEY must be set!" && exit 1 || echo "NRCAN_ENGINE_API_KEY is set"
install: check_api_key
	yarn install
run: install
	yarn build && yarn start
watch: install
	yarn watch
build: install
	yarn dockerize
test: install
	yarn test
	yarn integration
.ONESHELL:
