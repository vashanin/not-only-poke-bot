FROM python:3.12.11-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir uv==0.8.8

COPY pyproject.toml uv.lock /app/

RUN uv sync --locked --no-dev

COPY . /app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src/not_only_poke_bot:$PYTHONPATH"

ENTRYPOINT []

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
