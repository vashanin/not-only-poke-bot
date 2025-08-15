# Not Only Poke Bot

### Environment & keys

- Ask Vlad for the current .env values if you plan to reuse API keys.
- You may use your own keys instead. Copy .env.sample → .env and fill the values.
- Langfuse is required (it stores system prompts and traces). Get the Langfuse keys and host from Vlad.

### Prerequisites
- Docker 24+
- Make on your system (GNU Make)

### Environment variables
Create a `.env` file (see `.env.sample`):

```
OPENAI_API_KEY=
OPENAI_MODEL=
OPENAI_REASONING_EFFORT=

LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=

TAVILY_API_KEY=
```

### Build, run & test (via Makefile)

The Makefile exposes common targets. Default image name is `not_only_poke_bot`. The container serves FastAPI on port `8080` internally.

#### Build
To build a docker image named `not_only_poke_bot` using the Dockerfile in the current directory.
```bash
make build
```

#### Run (detached)
To run the container in detached mode, mapping port `8080` on the host to port `8080` in the container.
```bash
make run
```

#### Build + Run
To build the image and run the container in detached mode.
```bash
make up
```

#### Stop
To stop the running container.
```bash
make down
```

#### Logs
To view the logs of the running container.
```bash
make logs
```

#### Tests (inside the image)
To run the tests defined in the `tests` directory inside the container.
```bash
make test
```

### API base URL

Once running, the API is available at:
- `http://localhost:8080`
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

### API structure

All endpoints are namespaced under `/api/v1`.

#### Health
- **GET** `/-/health`
- Full path: `/api/v1/-/health`
- Response:
```json
{ "status": "ok" }
```
**Example**
```bash
curl http://localhost:8080/api/v1/-/health
```

#### Battle (who would win)
- **GET** `/battle`
- **Full path:** `/api/v1/battle?pokemon1=<name>&pokemon2=<name>`
- **Query params:** `pokemon1`, `pokemon2`
- **Response shape:**
```json
{
  "reasoning": "...",
  "winner": "Pikachu"
}
```

**Example**
```bash
curl "http://localhost:8080/api/v1/battle?pokemon1=Pikachu&pokemon2=Bulbasaur"
```

#### Chat (ask a question)
- **POST** `/chat`
- **Full path:** `/api/v1/chat`
- **Body:** `{ "question": "Who counters Bulbasaur?" }`
- Response shape:
```json
{
  "answer": "..."
}
```
**Example**
```bash
curl -X POST \
  http://localhost:8080/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"Who counters Bulbasaur?"}'
```
