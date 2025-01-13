.PHONY: install
install:
	pip install --upgrade pip
	pip install poetry
	poetry lock
	poetry install

.PHONY: lint-fix
lint-fix:
	poetry run ruff check --select I --fix .
	poetry run ruff format
	poetry run toml-sort -i pyproject.toml

	.PHONY: typecheck
typecheck:
	poetry run pyright