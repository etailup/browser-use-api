FROM python:3.11-slim

# System deps + curl (for healthcheck) + git (needed for pip git URLs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-6 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libxshmfence1 fonts-liberation ca-certificates \
    libcups2t64 libxkbcommon0 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright browser + deps
RUN python -m playwright install chromium
RUN playwright install-deps chromium

# App code
COPY app ./app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Healthcheck to your FastAPI /health
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
