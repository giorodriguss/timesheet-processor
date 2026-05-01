FROM python:3.12-slim

WORKDIR /app

COPY data.json .
COPY process.py .

CMD ["python", "process.py"]
