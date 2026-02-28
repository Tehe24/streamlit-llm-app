from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import streamlit as st

# .env ファイルを読み込む
load_dotenv()

# 環境変数を取得する
api_key = os.getenv("OPENAI_API_KEY")

# 1) 専門家ラベル（ラジオボタン候補）
EXPERT_OPTIONS = [
    "python学習用アドバイザー",
    "子供の教育用アドバイザー",
]

# 2) system prompt を先に定義（ここが“設定ファイル”みたいな役割になる）
prompt_python = (
    "あなたはPython初心者にやさしく教える専門家です。"
    "専門用語はできるだけ避け、具体例と短いコード例を使って説明してください。"
)

prompt_education = (
    "あなたは子供の学習支援に詳しい教育アドバイザーです。"
    "年齢に合わせた説明をし、やる気が出る声かけも含めて答えてください。"
)

SYSTEM_PROMPTS = {
    "python学習用アドバイザー": prompt_python,
    "子供の教育用アドバイザー": prompt_education,
}

DEFAULT_SYSTEM_PROMPT = "あなたは親切なアシスタントです。わかりやすく答えてください。"

def get_system_message(expert_type:str) -> str:
  return SYSTEM_PROMPTS.get(expert_type,DEFAULT_SYSTEM_PROMPT)

def get_llm_response(user_text: str, expert_type:str) -> str:
  if not user_text.strip():
    return "入力が空です。質問を入力してください"
  try:
    system_message = get_system_message(expert_type)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{input}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": user_text})
  except Exception as e:
    return f"エラーが発生しました{e}"
st.title("専門家アドバイザー")

selected_item = st.radio("専門家を選んでください", EXPERT_OPTIONS)

st.divider()

user_input = st.text_input(label="質問を入力してください")

if st.button("実行"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            result = get_llm_response(user_input, selected_item)
        st.divider()
        st.write(f"**回答:**")
        st.write(result)
    else:
        st.warning("質問を入力してください。")