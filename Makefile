TYPSTYLE_OPTS := --wrap-text

.PHONY: all svg pdf lint check format help

all: svg pdf ## Generate SVG plots and compile PDF

svg: img/ticket_price_plot.svg img/violin_plot.svg ## Generate SVG plots

img/ticket_price_plot.svg img/violin_plot.svg: ticket_price.py
	uv run ticket_price.py

pdf: doc/ticket_price.pdf ## Compile Typst document to PDF

doc/ticket_price.pdf: ticket_price.typ img/ticket_price_plot.svg img/violin_plot.svg
	typst compile ticket_price.typ doc/ticket_price.pdf

lint: ## Check formatting (Python, TOML, Typst)
	uv run ruff check .
	uv run ruff format --check .
	typstyle $(TYPSTYLE_OPTS) --check *.typ

check: ## Run type checkers (ty, taplo)
	uv run ty check .
	taplo check

format: ## Auto-format all sources
	uv run ruff format .
	taplo format
	typstyle $(TYPSTYLE_OPTS) -i *.typ

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'
