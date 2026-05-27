.PHONY: setup run run-api run-dashboard run-all clean test

# Setup
setup:
	cd agent && uv sync
	cd dashboard && npm install

# Run agent (CLI)
run:
	cd agent && uv run python -m agent.main "$(MESSAGE)"

# Run API server
run-api:
	cd agent && uv run uvicorn agent.server:app --reload --port 8000

# Run dashboard
run-dashboard:
	cd dashboard && npm run dev

# Run everything
run-all:
	@echo "Starting Reflexion..."
	@echo "1. API server on http://localhost:8000"
	@echo "2. Dashboard on http://localhost:3000"
	@make -j2 run-api run-dashboard

# Test
test:
	cd agent && uv run pytest tests/ -v

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true

# Demo mode
demo:
	DEMO_MODE=true make run-all
