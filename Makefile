install:
	poetry update
	poetry install

test:
	poetry run pytest --disable-warnings

test-coverage:
	poetry run pytest --cov=page-loader --cov-report xml

lint:
	poetry run flake8 page-loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

local:
	python3 -m pip install .

package-install:
	pip install --user dist/*.whl



.PHONY: install test lint selfcheck check build
