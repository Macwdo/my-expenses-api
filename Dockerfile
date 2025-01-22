FROM python:3.12.0-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY ./src /app/
COPY ./pyproject.toml /app
COPY ./uv.lock /app
COPY ./gunicorn.conf.py /app

COPY ./infra/scripts /app/scripts

WORKDIR /app
RUN uv sync --frozen --no-cache
RUN chmod +x /app/scripts/command.sh

ENV PATH="/scripts:/venv/bin:$PATH"

CMD ["/app/scripts/command.sh"]
