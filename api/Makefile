SHELL ?= /usr/bin/bash
.PHONY: run build test
run:
	yarn build && yarn start
build:
	yarn dockerize
test:
	yarn test
	yarn integration
.ONESHELL:
