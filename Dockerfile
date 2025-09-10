FROM python:3.11-slim

# ✅ System deps for Chromium (incl. git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-6 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libxshmfence1 fonts-liberation ca-certificates \
    libcups2t64 libxkbcommon0 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ install browsers
RUN playwright install --with-deps chromium

# app code
COPY app ./app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
