run:
	uvicorn not_only_poke_bot.asgi:app --reload

test:
	pytest -q

up:
	docker compose up --build

down:
	docker compose down