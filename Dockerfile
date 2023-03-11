FROM python:3.11

ENV BACKEND_URL=http://backend:8000

COPY . /opt/worker
WORKDIR /opt/worker

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN ~/.local/bin/poetry install

CMD [ "/root/.local/bin/poetry", "run", "python", "-m", "worker.worker", "--backend_url", "${BACKEND_URL}" ]

