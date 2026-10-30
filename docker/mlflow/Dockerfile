FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Pin MLflow to a known release; review compatibility before upgrades.
RUN pip install "mlflow==3.17.2" "psycopg2-binary==2.9.11" "boto3>=1.40,<2"

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin mlflow
USER mlflow
WORKDIR /home/mlflow
EXPOSE 5000
