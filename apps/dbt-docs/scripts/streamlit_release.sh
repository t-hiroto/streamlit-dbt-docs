#!/bin/bash
set -e

# デフォルトのコネクション名
CONNECTION=${1:-__connection__}

echo "=== Streamlit アプリのリリースを開始します ==="
echo "使用するコネクション: $CONNECTION"

uv run snow streamlit deploy --replace --connection "$CONNECTION"

echo "=== Streamlit アプリのリリースが完了しました ==="
