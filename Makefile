.PHONY: install lint format test run-api run-pipeline run-scenario clean help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -e ".[dev]"

lint:  ## Run linter and type checker
	ruff check .
	ruff format --check .
	mypy investorframe/ --ignore-missing-imports

format:  ## Auto-format code
	ruff check --fix .
	ruff format .

test:  ## Run tests with coverage
	pytest --cov=investorframe --cov-report=term-missing -v

run-api:  ## Start the FastAPI server
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-pipeline:  ## Run the daily analysis pipeline
	python -m cli.main --verbose --format all

run-scenario:  ## Run a scenario (usage: make run-scenario SCENARIO=fed_rate_hike_50bps)
	python -m cli.main --scenario $(SCENARIO) --verbose

clean:  ## Remove build artifacts and cache
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	rm -rf dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
