import json
import uuid
from pathlib import Path

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

# ---------------- Config ----------------
DATA_FILE = Path(__file__).parent / "chats.json"   # chats are saved here
DEFAULT_MODEL = "llama3.2"
MAX_MESSAGES = 12                                   # memory window per chat
SYSTEM_PROMPT = (
    "You are Memory Bot, a friendly and concise assistant. "
    "Use the conversation history to remember what the user told you."
)
SUGGESTIONS = [
    "Explain recursion in simple words",
    "Give me 5 project ideas for a CS student",
    "Help me prepare for a coding interview",
]

st.set_page_config(page_title="Memory Bot", page_icon="🧠", layout="wide")

# ---------------- Styling ----------------
st.markdown(
    """
<style>
#MainMenu, footer, header [data-testid="stToolbar"] {visibility: hidden;}
.block-container {max-width: 820px; padding-top: 2rem; padding-bottom: 6rem;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(99,102,241,0.14), rgba(0,0,0,0));
    border-right: 1px solid rgba(128,128,128,0.2);
}
[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px;
    text-align: left;
    justify-content: flex-start;
    border: 1px solid rgba(128,128,128,0.25);
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #6366f1;
    background: rgba(99,102,241,0.12);
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    background: rgba(128,128,128,0.07);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(99,102,241,0.14);
}

/* Input box */
[data-testid="stChatInput"] {border-radius: 16px;}

/* Welcome screen */
.hero {text-align: center; margin: 3.5rem 0 1.5rem 0;}
.hero h1 {
    font-size: 2.6rem; margin-bottom: 0.2rem;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p {opacity: 0.7; font-size: 1.05rem;}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------- Storage helpers ----------------
def load_chats() -> dict:
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_chats() -> None:
    try:
        DATA_FILE.write_text(
            json.dumps(st.session_state.chats, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def new_chat() -> None:
    """Create a new chat (reuses the current one if it's still empty)."""
    cur = st.session_state.get("current")
    if cur in st.session_state.chats and not st.session_state.chats[cur]["messages"]:
        return
    cid = uuid.uuid4().hex[:8]
    st.session_state.chats[cid] = {"title": "New chat", "messages": []}
    st.session_state.current = cid
    save_chats()


def list_models() -> list[str]:
    try:
        import ollama

        names = [m.model for m in ollama.list().models]
        return names or [DEFAULT_MODEL]
    except Exception:
        return [DEFAULT_MODEL]


# ---------------- Session state ----------------
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
    st.session_state.current = None
    st.session_state.pending = None

if not st.session_state.chats:
    new_chat()
elif st.session_state.current not in st.session_state.chats:
    st.session_state.current = list(st.session_state.chats)[-1]

chats = st.session_state.chats

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## 🧠 Memory Bot")
    if st.button("➕  New chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()

    st.markdown("##### Your chats")
    for cid in reversed(list(chats)):
        c = chats[cid]
        col_open, col_del = st.columns([5, 1])
        icon = "🟣" if cid == st.session_state.current else "💬"
        if col_open.button(f"{icon}  {c['title']}", key=f"open_{cid}", use_container_width=True):
            st.session_state.current = cid
            st.rerun()
        if col_del.button("🗑️", key=f"del_{cid}", help="Delete chat"):
            del chats[cid]
            save_chats()
            if st.session_state.current == cid:
                st.session_state.current = None
            st.rerun()

    st.divider()
    models = list_models()
    model_name = st.selectbox(
        "Model", models, index=models.index(DEFAULT_MODEL) if DEFAULT_MODEL in models else 0
    )
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1)

# ---------------- Main area ----------------
chat = chats[st.session_state.current]

prompt = st.chat_input("Message Memory Bot...")
if not prompt and st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None

# Welcome screen for empty chats
if not chat["messages"] and not prompt:
    st.markdown(
        '<div class="hero"><h1>Hi, how can I help?</h1>'
        "<p>I run locally on your laptop and remember our conversation.</p></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(SUGGESTIONS))
    for col, text in zip(cols, SUGGESTIONS):
        if col.button(text, use_container_width=True):
            st.session_state.pending = text
            st.rerun()

# Past messages
for m in chat["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"] == "user" else "🧠"):
        st.markdown(m["content"])

# New message
if prompt:
    if not chat["messages"]:
        chat["title"] = prompt[:28] + ("…" if len(prompt) > 28 else "")

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    history = []
    for m in chat["messages"][-MAX_MESSAGES:]:
        history.append(HumanMessage(content=m["content"]) if m["role"] == "user"
                       else AIMessage(content=m["content"]))
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + history + [HumanMessage(content=prompt)]

    llm = ChatOllama(model=model_name, temperature=temperature)

    with st.chat_message("assistant", avatar="🧠"):
        try:
            reply = st.write_stream(chunk.content for chunk in llm.stream(messages))
        except Exception as e:
            reply = None
            st.error(
                f"Could not get a reply from '{model_name}'. "
                "Check that Ollama is running and the model is pulled.\n\n" + str(e)
            )

    if reply:
        chat["messages"].append({"role": "user", "content": prompt})
        chat["messages"].append({"role": "assistant", "content": reply})
        save_chats()
        st.rerun()  # refresh sidebar title