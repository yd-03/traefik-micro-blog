FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# エントリポイントを設定
ENTRYPOINT ["sh", "-c", "python create_tables.py && python app.py"]

# 必要なポートを公開
EXPOSE 5000
