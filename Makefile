.PHONY: install test build clean binary

install:
	uv sync

test:
	uv run pytest tests/ -v

clean:
	rm -rf dist/ build/ __pycache__

binary:
	./scripts/build_binaries.sh