# Build e run para deploy (Railway, Render, Fly, etc.)
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Plataformas que definem PORT na execução; fallback 5000
EXPOSE 5000
CMD ["sh", "-c", "python app.py"]
