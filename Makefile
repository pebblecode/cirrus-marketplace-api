SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)
rootdir =$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
deploydir = $(rootdir)/build
to_deploy = app \
	    application.py \
	    config.py \
	    .ebextensions \
	    json_schemas \
	    data \
	    requirements.txt \
	    scripts \
	    setup.cfg \
	    tests
app_dir = $(rootdir)/app

run_all: requirements run_migrations run_app

run_app: virtualenv
	${VIRTUALENV_ROOT}/bin/python application.py runserver

run_migrations: virtualenv
	${VIRTUALENV_ROOT}/bin/python application.py db upgrade

virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && virtualenv venv || true

bootstrap: virtualenv
	./scripts/bootstrap.sh

requirements: virtualenv requirements.txt
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt

requirements_for_test: virtualenv requirements_for_test.txt
	${VIRTUALENV_ROOT}/bin/pip install -r requirements_for_test.txt

test: test_pep8 test_migrations test_unit

test_pep8: virtualenv
	${VIRTUALENV_ROOT}/bin/pep8 .

test_migrations: virtualenv
	${VIRTUALENV_ROOT}/bin/python ./scripts/list_migrations.py 1>/dev/null

test_unit: virtualenv
	${VIRTUALENV_ROOT}/bin/py.test ${PYTEST_ARGS}

bundle_app:
	mkdir -p $(deploydir)
	for dir in $(to_deploy); do \
		cp -r $$dir $(deploydir); \
	done

.PHONY: virtualenv requirements requirements_for_test test_pep8 test_migrations test_unit test test_all run_migrations run_app run_all
