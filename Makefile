.PHONY: build pre-commit up run down test logs
IMAGE    ?= not_only_poke_bot
PORT     ?= 8000
ENV_FILE ?= .env

build:
	@echo "Building Docker image $(IMAGE)..."
	@docker build -t $(IMAGE) .

up:
	@echo "Starting Docker container $(IMAGE)_ctr..."
	@docker build -t $(IMAGE) .
	@docker run -d -p $(PORT):8000 --env-file $(ENV_FILE) --name $(IMAGE)_ctr $(IMAGE)

run:
	build
	up

down:
	@echo "Stopping and removing Docker container $(IMAGE)_ctr..."
	@docker rm -f $$(docker ps -aq --filter "name=$(IMAGE)_ctr") 2>/dev/null || true

test:
	@echo "Running tests..."
	@docker run --rm -v $(CURDIR):/app --env-file $(ENV_FILE) -w /app $(IMAGE) pytest -q

logs:
	@echo "Fetching logs from Docker container $(IMAGE)_ctr..."
	@docker logs $(IMAGE)_ctr

pre-commit:
	@echo "Running pre-commit hooks..."
	@docker run --rm \
		--env-file $(ENV_FILE) \
		-v $(CURDIR):/app -w /app \
		$(IMAGE) uv run pre-commit run --all-files
