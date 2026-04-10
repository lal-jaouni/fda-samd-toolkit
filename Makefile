.PHONY: lint format typecheck test check security clean help setup

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint: ## Auto-fix lint issues
	ruff check --fix .

format: ## Auto-format code
	ruff format .

typecheck: ## Run type checker
	pyright

test: ## Run tests with JSON report
	pytest --json-report --json-report-file=test-report.json -q

check: lint format typecheck test ## Run all quality checks

security: ## Run security scan
	bandit -r src/ -q

setup: ## Set up git hooks and dev environment
	git config core.hooksPath .githooks

clean: ## Remove caches and build artifacts
	rm -rf __pycache__ .pytest_cache .ruff_cache .pyright test-report.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
