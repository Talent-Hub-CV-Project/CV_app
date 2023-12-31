# https://github.com/samuelcolvin/pydantic/blob/master/Makefile
.DEFAULT_GOAL := all
dirs = src/
poetry = poetry run
isort = isort
black = black
mypy = mypy
flake8  = flake8
pyupgrade = pyupgrade --py311-plus


.PHONY: install-linting
install-linting:
	poetry add flake8 black isort mypy pyupgrade -G dev

.PHONY: install
install: install-linting
	pre-commit install
	@echo 'installed development requirements'

.PHONY: lint
lint: lint
	$(isort) --df --check-only
	$(black) --diff --check
	$(flake8)

.PHONY: format
format:
	$(poetry) $(pyupgrade)
	$(poetry) $(isort) $(dirs)
	$(poetry) $(black) $(dirs)
	$(poetry) $(mypy) $(dirs)
	$(poetry) $(flake8) $(dirs)

.PHONY: export-dependencies
export-dependencies:
    # pip can't install cuda libraries with missing hashes, because indirect install from poetry
	poetry export -f requirements.txt --output requirements/requirements.txt --without-hashes
	poetry export -f requirements.txt --output requirements/requirements-dev.txt --with=dev --without-hashes

.PHONY: database
database:
	docker compose up database -d

.PHONY: test
test:
	poetry run pytest --cov=app --cov-report=html

.PHONY: migrate
migrate:
	@read -p "Enter migration message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"

.PHONY: downgrade
downgrade:
	alembic downgrade -1

.PHONY: upgrade
upgrade:
	alembic upgrade +1

.PHONY: upgrade-offline
upgrade-offline:
	alembic upgrade head --sql

.PHONY: all
all: format export-dependencies
