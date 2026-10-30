FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY control-plane/ ./control-plane/
RUN pip install ./control-plane
RUN useradd --uid 10002 --create-home --shell /usr/sbin/nologin service \
    && mkdir -p /data \
    && chown service:service /data
USER service
EXPOSE 8000
CMD ["uvicorn", "mlflow_service.api:app", "--host", "0.0.0.0", "--port", "8000"]
