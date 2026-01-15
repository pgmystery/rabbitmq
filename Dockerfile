FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install .

COPY src/ src/

CMD ["python", "src/producer.py"]
