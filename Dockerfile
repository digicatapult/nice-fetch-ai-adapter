FROM python:3.12-slim
LABEL MAINTAINER Digital Catapult
# LABEL org.opencontainers.image.source=https://github.com/CDECatapult/soniclabs-resultsmanager

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1
# System deps:
RUN pip install "poetry==1.6.1" --no-cache-dir
# Install dependencies:
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
COPY /app setup.cfg /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "4"]