SHELL ?= /usr/bin/bash

.PHONY: start_mongodb stop_mongodb setup_python import_data setup
start_mongodb:
	brew services start mongodb
stop_mongodb:
	brew services stop mongodb
setup_python:
	$(MAKE) -C python setup_python
import_data:
	$(MAKE) -C python import_data
setup:
	$(MAKE) start_mongodb
	$(MAKE) -C python setup_python import_data

.PHONY: run build test
run:
		$(MAKE) -C api run
build:
	$(MAKE) -C api build
test:
	$(MAKE) -C api test
.ONESHELL:
