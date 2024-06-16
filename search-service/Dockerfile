FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "python -c 'import time; time.sleep(30)' && python index_data.py && python app.py"]
