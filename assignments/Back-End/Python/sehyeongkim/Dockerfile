FROM python:3.9.18-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY ./pyproject.toml /src/pyproject.toml
COPY ./poetry.lock /src/poetry.lock

RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && apt-get remove -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/root/.local"
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN poetry install --no-root

COPY . /src

EXPOSE 8080

RUN chmod +x /src/wait-for-it.sh
RUN chmod +x /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]
