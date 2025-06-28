FROM python:3.12-slim AS base

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python環境のセットアップ
RUN pip install --no-cache-dir pip setuptools wheel

# 依存関係ファイルのコピー
COPY requirements.txt .

# 依存関係のインストール
RUN pip install --upgrade pip && pip install -r requirements.txt

# アプリケーションファイルのコピー
COPY . .

EXPOSE 8501

# Streamlitアプリケーションの実行
CMD ["python", "-m", "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"] 
