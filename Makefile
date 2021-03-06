help:
	@echo "help  -- print this help"
	@echo "start -- start docker stack"
	@echo "stop  -- stop docker stack"
	@echo "ps    -- show status"
	@echo "build  -- build image"
	@echo "clean -- clean all artifacts"
	@echo "test  -- run tests using docker"
	@echo "dockershell -- run bash inside docker"

build:
	docker-compose build pyme 

start:
	docker-compose up -d pyme 

logs:
	docker-compose logs -f --tail=30 pyme 

up:
	docker-compose up pyme 

stop:
	docker-compose stop

ps:
	docker-compose ps

clean: stop
	docker-compose rm --force -v

only_test:
	docker-compose run --rm pyme pytest

covered_test:
	docker-compose run --rm pyme pytest --cov=. --cov-config setup.cfg

pep8:
	docker-compose run --rm pyme flake8

test: pep8 covered_test

dockershell:
	docker-compose run --rm pyme /bin/bash

clean-python:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

.PHONY: help start stop ps clean test dockershell shell_plus only_test pep8 clean-python
