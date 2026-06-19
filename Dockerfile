FROM python:3.11-slim

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=120
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefer-binary -e .

COPY app/ app/
COPY templates/ templates/
COPY tests/ tests/

VOLUME ["/data"]
EXPOSE 8000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
