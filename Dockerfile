FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    QDRANT_PATH=/app/qdrant_storage \
    SESSION_DB_PATH=/app/data/sessions.sqlite3

WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY pyproject.toml requirements.txt ./
COPY src ./src
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-deps .
RUN mkdir -p /app/qdrant_storage /app/data && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=3s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["uvicorn", "agentic_rag.main:app", "--host", "0.0.0.0", "--port", "8000"]
