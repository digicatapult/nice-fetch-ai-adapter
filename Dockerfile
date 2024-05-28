FROM python:3.12-slim
LABEL MAINTAINER Digital Catapult

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1
# System deps:
RUN pip install "poetry==1.6.1" --no-cache-dir
# Ensure poetry is on PATH
ENV PATH="/root/.local/bin:$PATH"
# Install dependencies:
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
COPY . /app/

CMD ["poetry", "run", "python", "run.py"]