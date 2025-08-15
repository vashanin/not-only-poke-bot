.PHONY: build run up down test logs
IMAGE    ?= not_only_poke_bot
PORT     ?= 8080
ENV_FILE ?= .env

build:
	@echo "Building Docker image $(IMAGE)..."
	@docker build -t $(IMAGE) .

run:
	@echo "Running Docker container $(IMAGE)_ctr on port $(PORT)..."
	@docker run -d -p $(PORT):8080 --env-file $(ENV_FILE) --name $(IMAGE)_ctr $(IMAGE)

up: build run

down:
	@echo "Stopping and removing Docker container $(IMAGE)_ctr..."
	@docker rm -f $$(docker ps -aq --filter "name=$(IMAGE)_ctr") 2>/dev/null || true

test:
	@echo "Running tests... Make sure you run `make build` before this step."
	@docker run --rm --env-file $(ENV_FILE) -w /app $(IMAGE) uv run pytest

logs:
	@echo "Fetching logs from Docker container $(IMAGE)_ctr..."
	@docker logs $(IMAGE)_ctr -f
