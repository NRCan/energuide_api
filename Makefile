SHELL ?= /usr/bin/bash
run:
	$(MAKE) -C api run
setup_python:
	$(MAKE) -C python setup_python
import_data:
	$(MAKE) -C python import_data
setup:
	$(MAKE) -C python setup_python import_data
build:
	$(MAKE) -C api build
test:
	$(MAKE) -C api test
.ONESHELL:
