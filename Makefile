install:
	poetry update
	poetry install

test:
	poetry run pytest /home/devden/python-project-lvl3/ -W ignore::DeprecationWarning

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

done: check install build pinstall

build: check
	poetry build

try:
	python3 -m pip install .

pinstall:
	pip install --user dist/*.whl




.PHONY: install test lint selfcheck check build