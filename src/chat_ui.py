import streamlit as st
import requests


def langchain_chat(query: str):
    url = "https://gpt.bokji24.com/chat"
    payload = {"query": query}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["output_text"]
    else:
        return "에러..."


def chat_ui():
    global chat_history
    st.title("DEU GPT")

    # 채팅 내역을 저장할 리스트
    chat_history = []

    # 채팅창
    chat_container = st.container()
    chat_input = chat_container.text_input("Guest", placeholder="무엇이든 물어보세요.")
    is_loading = True

    if is_loading and st.button("전송"):
        # 로딩바 표시
        with st.spinner("로딩중..."):
            bot_response = langchain_chat(chat_input)

        # 로딩바 제거
        st.spinner()

        chat_history.append(("Langchain", bot_response))
        chat_input = ""

    with chat_container:
        for i, item in enumerate(chat_history):
            sender, message = item
            st.text_input("DEU GPT 챗봇", message, key=i)
        is_loading = False


# 채팅 UI 실행
chat_ui()


st.markdown(
    """
    <style>
        div[data-baseweb="input"]:hover {
            border-color: #3F5FFF !important;
            box-shadow: 0 0 0 1px #3F5FFF !important;
        }
        </style>
    """,
    unsafe_allow_html=True,
)
