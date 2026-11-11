"""
Simple local chatbot: Ollama (local LLM) + LangChain memory.

Setup:
    1. Install Ollama: https://ollama.com
    2. ollama pull llama3.2
    3. pip install langchain langchain-core langchain-ollama
    4. python chatbot.py
"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

MODEL_NAME = "llama3.2"   # any model you've pulled with `ollama pull`
MAX_MESSAGES = 10         # memory window: last 10 messages (5 turns)


# ---------- Memory ----------
class WindowedHistory(InMemoryChatMessageHistory):
    """Chat history that only keeps the most recent N messages,
    so the prompt never outgrows the local model's context window."""

    max_messages: int = MAX_MESSAGES

    def add_messages(self, messages):
        super().add_messages(messages)
        self.messages = self.messages[-self.max_messages:]


_sessions: dict[str, WindowedHistory] = {}


def get_history(session_id: str) -> WindowedHistory:
    if session_id not in _sessions:
        _sessions[session_id] = WindowedHistory()
    return _sessions[session_id]


# ---------- Chain ----------
llm = ChatOllama(model=MODEL_NAME, temperature=0.7)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a friendly, concise assistant. Use the conversation history for context."),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm | StrOutputParser()

chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)


# ---------- CLI ----------
def main(session_id: str = "default") -> None:
    config = {"configurable": {"session_id": session_id}}
    print(f"Local chatbot ({MODEL_NAME}). Commands: /clear to reset memory, /quit to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input == "/quit":
            print("Bye!")
            break
        if user_input == "/clear":
            get_history(session_id).clear()
            print("Memory cleared.\n")
            continue

        print("Bot: ", end="", flush=True)
        for chunk in chatbot.stream({"input": user_input}, config=config):
            print(chunk, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    main()