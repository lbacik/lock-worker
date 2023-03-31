FROM python:3.11

ENV BACKEND_URL http://backend:8000

COPY . /opt/worker
WORKDIR /opt/worker

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/bin/poetry config virtualenvs.create false && \
    ~/.local/bin/poetry install --no-root --no-dev --no-interaction --no-ansi

CMD [ "python", "-u", "-m", "worker.main" ]

