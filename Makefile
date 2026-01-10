.PHONY: help test test-verbose build clean install dev lint format check-format

help:
	@echo "Available targets:"
	@echo "  test           - Run tests using uv"
	@echo "  test-verbose   - Run tests with verbose output"
	@echo "  build          - Build the package using uv"
	@echo "  clean          - Remove build artifacts and cache files"
	@echo "  install        - Install package in development mode"
	@echo "  dev            - Install development dependencies"
	@echo "  lint           - Run linting (if configured)"
	@echo "  format         - Format code (if configured)"
	@echo "  check-format   - Check code formatting"

test:
	uv run python ipgroup_test.py

test-verbose:
	uv run python ipgroup_test.py -v

build: clean
	uv build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

lint:
	@echo "No linting configured yet. Install ruff or flake8 to enable linting."

format:
	@echo "No formatting configured yet. Install ruff or black to enable formatting."

check-format:
	@echo "No format checking configured yet."
