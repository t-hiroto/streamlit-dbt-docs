import os
from logging import getLogger
from typing import List, Optional

import streamlit as st
import streamlit.components.v1 as components

from common.snowflake_connection import SnowflakeConnection

logger = getLogger(__name__)

HIDE_DEPLOY_BUTTON_CSS = """
<style>
.stDeployButton {
    visibility: hidden;
}
</style>
"""
STAGE_NAME = "@dbt_docs_stage"
HTML_EXTENSION = ".html"
DOWNLOAD_DIR = "statics"


def read_html_file(file_path: str) -> Optional[str]:
    """HTMLファイルを読み込む

    Args:
        file_path (str): HTMLファイルのパス

    Returns:
        Optional[str]: HTMLコンテンツ
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logger.error(f"ファイル読み込みエラー: {e}")
        return None


def display_html(html_file_path: str, height: int = 1024) -> None:
    """HTMLファイルを表示する関数

    Args:
        html_file_path (str): 表示するHTMLファイルのパス
        height (int, optional): 表示高さ. デフォルト 1024
    """
    html_content = read_html_file(html_file_path)
    if not html_content:
        st.error(f"ファイルの読み込みに失敗しました: {html_file_path}")
        return

    # デプロイボタンを非表示にするCSS
    st.markdown(HIDE_DEPLOY_BUTTON_CSS, unsafe_allow_html=True)

    try:
        # HTMLコンテンツを表示
        components.html(html_content, height=height, scrolling=True)
    except Exception as e:
        logger.error(f"HTML表示エラー: {e}")
        st.error(f"HTMLの表示中にエラーが発生しました: {str(e)}")


def get_html_files_from_stage(session) -> List[str]:
    """ステージからHTMLファイルの一覧を取得する

    Returns:
        List[str]: HTMLファイルのパスリスト
    """
    try:
        result = session.sql(f"LIST {STAGE_NAME}/").collect()
        file_names = [os.path.basename(row["name"]) for row in result if row["name"].endswith(HTML_EXTENSION)]
    except Exception as e:
        logger.error(f"ステージからファイル一覧の取得に失敗: {e}")
        st.error(f"ステージからファイル一覧の取得に失敗しました: {str(e)}")
        return []
    try:
        for file_name in file_names:
            local_path = f"{DOWNLOAD_DIR}/{file_name}"
            if not os.path.exists(local_path):
                session.file.get(f"{STAGE_NAME}/{DOWNLOAD_DIR}/{file_name}", DOWNLOAD_DIR)
    except Exception as e:
        logger.error(f"ファイルのダウンロードに失敗: {e}")
        st.error(f"ファイルのダウンロードに失敗しました: {str(e)}")
        return []
    return file_names


def main():
    st.set_page_config(
        page_title="dbt Documentation",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    session = SnowflakeConnection().get_session()
    html_files = get_html_files_from_stage(session)

    if not html_files:
        st.warning("ステージにHTMLファイルが見つかりません。")
        return

    selected_file = st.sidebar.selectbox("表示するドキュメントを選択してください", html_files)
    if selected_file:
        file_path = f"{DOWNLOAD_DIR}/{os.path.basename(selected_file)}"
        display_html(file_path)


if __name__ == "__main__":
    main()
