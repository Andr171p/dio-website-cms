FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./fastapi-rag/requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY fastapi-rag/ .

CMD ["python", "main.py"]