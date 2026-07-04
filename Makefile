.PHONY: install test build clean binary

install:
	uv sync

test:
	uv run pytest tests/ -v
	uv run ruff check komit/
	uv run mypy komit/
	uv run ruff format komit/

clean:
	rm -rf dist/ build/ __pycache__

binary:
	./scripts/build_binaries.sh