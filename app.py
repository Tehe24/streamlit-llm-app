import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env を読み込む
load_dotenv()

# APIキー取得
api_key = os.getenv("OPENAI_API_KEY")

# OpenAIクライアント作成
client = OpenAI(api_key=api_key)

st.title("LLMアプリ（最小版）")

# 入力フォーム
prompt = st.text_input("質問を入力してください")

# ボタンが押されたら実行
if st.button("送信") and prompt:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    st.write(response.output_text)