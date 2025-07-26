import streamlit as st
from openai import OpenAI
import os

# ============================
#       HÀM ĐỌC FILE
# ============================
def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# ============================
#       CSS GIAO DIỆN TỐI ƯU MOBILE
# ============================
st.markdown("""
<style>

/* =======================
   RESET & GLOBALS
======================= */

html, body, .stApp {
    background-color: #0f1116 !important;
    margin: 0 !important;
    padding: 0 !important;
}

* {
    box-sizing: border-box;
}

/* =======================
   WRAPPER CHUNG
======================= */

.layout-wrapper {
    max-width: 820px;
    margin: 0 auto;
    padding: 0 12px;
}

/* =======================
       LOGO
======================= */
.logo-zone {
    display: flex;
    justify-content: center;
    margin: 10px 0 2px 0;
}
.logo-zone img {
    width: 135px;
    border-radius: 16px;
}

/* =======================
      TIÊU ĐỀ CHÍNH
======================= */

.header-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    margin: 6px auto 14px auto;
    color: #ffffff;
    line-height: 1.45;
    max-width: 700px;
}

/* =======================
      MÔ TẢ PHỤ
======================= */

.sub-info {
    background: #1c2333;
    padding: 13px 16px;
    color: #d6dcff;
    font-size: 14px;
    border-radius: 15px;
    margin: 0 auto 16px auto;
    max-width: 720px;
    text-align: left;
}

/* =======================
        CHAT AREA
======================= */

.chat-container {
    max-width: 820px;
    margin: 0 auto;
    padding-bottom: 95px; /* chừa chỗ cho thanh input cố định */
}

/* Bubble chung */
.msg-assistant, .msg-user {
    padding: 14px 18px;
    border-radius: 16px;
    margin: 14px 0;
    max-width: 92%;
    font-size: 16px;
    line-height: 1.45;
    word-wrap: break-word;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.25);
}

/* Assistant bubble */
.msg-assistant {
    background: #1c2333;
    color: #e8ecff;
    border-left: 4px solid #4e8cff;
}
.msg-assistant::before {
    content: "🧠 TVS - Tham vấn học đường\\A";
    font-weight: 700;
    font-size: 14px;
    display: block;
    margin-bottom: 4px;
    opacity: 0.9;
}

/* User bubble */
.msg-user {
    background: #2f405f;
    color: white;
    border-right: 4px solid #73d0ff;
    margin-left: auto;
}

/* =======================
     INPUT BOX FIXED
======================= */

[data-testid="stChatInputContainer"] {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 12px 10px;
    background: #0f1116;
    box-shadow: 0 -3px 12px rgba(0,0,0,0.55);
    z-index: 9999;
}

.stChatInput > div > div > textarea {
    background: #1a1e29 !important;
    border: 1px solid #333d55 !important;
    border-radius: 14px !important;
    padding: 12px !important;
    color: white !important;
    font-size: 15px !important;
}

/* =======================
      MOBILE STYLE
======================= */

@media (max-width: 600px) {
    
    .header-title {
        font-size: 18px;
        padding: 0 8px;
    }

    .logo-zone img {
        width: 115px;
    }

    .msg-assistant, .msg-user {
        padding: 12px 14px;
        font-size: 15px;
        max-width: 98%;
    }
    
    .chat-container {
        padding-bottom: 85px;
    }

    [data-testid="stChatInputContainer"] {
        padding: 8px 8px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================
#      LOGO + TITLE
# ============================
try:
    st.markdown('<div class="logo-zone">', unsafe_allow_html=True)
    st.image("logo.png")
    st.markdown('</div>', unsafe_allow_html=True)
except:
    pass

title_content = rfile("00.xinchao.txt")
st.markdown(f'<div class="header-title">{title_content}</div>', unsafe_allow_html=True)

# ============================
#  INIT OPENAI
# ============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# ============================
#    HIỂN THỊ LỊCH SỬ CHAT
# ============================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for m in st.session_state.messages:
    content = str(m.get("content", ""))
    if m["role"] == "assistant":
        st.markdown(f'<div class="msg-assistant">{content}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================
#        INPUT
# ============================
prompt = st.chat_input("Bạn muốn được THAM VẤN điều gì nè?...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="msg-user">{prompt}</div>', unsafe_allow_html=True)

    response_text = ""
    stream = client.chat.completions.create(
        model=rfile("module_chatgpt.txt").strip(),
        messages=[{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices:
            response_text += chunk.choices[0].delta.content or ""

    st.markdown(f'<div class="msg-assistant">{response_text}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
