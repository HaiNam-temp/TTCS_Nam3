
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       git \
       curl \
       wget \
       ca-certificates \
       libssl-dev \
       libffi-dev \
       python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wheels_build

COPY backend/requirements.txt ./requirements.txt

RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --prefer-binary --no-index --find-links /wheels -r requirements.txt

COPY . /app

EXPOSE 8010 3000

CMD ["python", "-m", "backend.main"]
