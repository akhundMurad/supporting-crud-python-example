check-linting:
	poetry run isort --check --profile black src/ tests/
	poetry run flake8 --exit-zero src/ tests/ --exit-zero
	poetry run black --check --diff src/ tests/ --line-length 119

fix-linting:
	poetry run isort --profile black src/ tests/
	poetry run black src/ tests/ --line-length 119

test:
	poetry run pytest -v
