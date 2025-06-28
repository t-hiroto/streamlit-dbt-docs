# streamlit-dbt-docs

## セットアップ

### ローカル開発時のアプリ起動

`apps/<application_name>/.streamlit/secrets.toml` に以下のように記載してください。

```toml
[snowflake]
user = "YOUR_USER"
private_key_file_path = "YOUR_PRIVATE_KEY_PATH"
account = "YOUR_ACCOUNT"
role = "YOUR_ROLE"
warehouse = "YOUR_WAREHOUSE"
database = "YOUR_DATABASE"
schema = "YOUR_SCHEMA"
```

```sh
uv run streamlit run streamlit_app.py
```

## リリース

## 事前準備

Snowflake CLIの設定をしておく必要があります。以下を参考にsnowコマンドを実行できるように準備してください。

https://docs.snowflake.com/en/developer-guide/snowflake-cli/index

### Streamlit in Snowflakeとしてデプロイする場合

```sh
sh scripts/streamlit_release.sh
```

### SPCSとしてデプロイする場合

1. 環境変数の設定

2. 以下のコマンドを実行

```sh
sh scripts/spcs_release.sh
```
