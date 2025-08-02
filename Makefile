.PHONY: help install install-dev format lint test test-cov clean build docs
.DEFAULT_GOAL := help

PYTHON := python3
PIP := pip
UV := uv

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	$(UV) pip install -e .

install-dev: ## Install project with development dependencies
	$(UV) pip install -e ".[dev]"

setup-dev: install-dev ## Setup development environment
	pre-commit install

format: ## Format code with black and isort
	black src tests
	isort src tests

lint: ## Run linting checks
	ruff check src tests
	mypy src
	black --check src tests
	isort --check-only src tests

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=remote_check_meter --cov-report=html --cov-report=term-missing

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build the package
	$(PYTHON) -m build

check: format lint test ## Run all checks (format, lint, test)

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

# CLI shortcuts
cli: ## Run the main CLI
	remote-check-meter

cli-help: ## Show CLI help
	remote-check-meter --help