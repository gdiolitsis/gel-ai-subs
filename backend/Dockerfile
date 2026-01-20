# GEL AI Subs — Whisper Backend Docker Image

FROM python:3.10-slim

# System deps
RUN apt update && apt install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# App dir
WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY app.py .

# Runtime data
RUN mkdir -p data/subs

EXPOSE 9000

CMD ["python", "app.py"]
