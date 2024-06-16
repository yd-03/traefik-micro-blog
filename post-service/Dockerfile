FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "python create_tables.py && uvicorn app:app --host 0.0.0.0 --port 5000"]
