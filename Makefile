SHELL ?= /usr/bin/bash

.PHONY: check_mongodb setup_python import_data setup

check_mongodb:
	@if [ -z "`pgrep mongo`" ]; then \
		echo "Mongo is not running"; \
		[ "`command -v brew`" ] && [ "`brew ls mongodb --versions`" ] && brew services start mongo || (echo "ERROR: You need to install MongoDB to run the API." && exit 1); \
	fi
setup_python:
	$(MAKE) -C python setup_python
import_data:
	$(MAKE) -C python import_data
setup: check_mongodb
	$(MAKE) -C python setup_python import_data

.PHONY: run build test watch
run:
	$(MAKE) -C api run
watch:
	$(MAKE) -C api watch
build:
	$(MAKE) -C api build
test:
	$(MAKE) -C api test
.ONESHELL:
