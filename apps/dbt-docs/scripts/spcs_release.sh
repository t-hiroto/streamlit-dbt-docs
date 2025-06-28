#!/bin/bash
set -e

# =============================
# dbt-docs リリーススクリプト
# =============================
# このスクリプトは、Dockerイメージのビルド・プッシュ、
# Snowflake Container Service へのデプロイを自動化します。
#
# 必要に応じて変数を編集してください。

if [ -z "$REGISTRY" ]; then
  echo "環境変数 REGISTRY が設定されていません。" >&2
  exit 1
fi
if [ -z "$REPO" ]; then
  echo "環境変数 REPO が設定されていません。" >&2
  exit 1
fi

# 設定
TAG="dev"
IMAGE="$REGISTRY/$REPO:$TAG"
SERVICE_NAME="dbt_docs_application_service"
SPEC_PATH="spec.yaml"
CONTEXT="dbt-docs"

# Dockerイメージをビルド
echo "[1/4] Dockerイメージをビルド: $IMAGE"
docker build . -t "$IMAGE" --no-cache --platform linux/amd64

# レジストリにログイン
echo "[2/4] レジストリにログイン"
uv run snow spcs image-registry login -c "$CONTEXT"

# Dockerイメージをプッシュ
echo "[3/4] Dockerイメージをプッシュ: $IMAGE"
docker push "$IMAGE"

# サービスをアップグレード
echo "[4/4] サービスをアップグレード: $SERVICE_NAME"
uv run snow spcs service upgrade "$SERVICE_NAME" --spec-path "$SPEC_PATH" -c "$CONTEXT"

echo "\nリリース完了！"
