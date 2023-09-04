from typing import List

import streamlit as st
from phi.conversation import Conversation

from app.get_openai_key import get_openai_key
from app.sidebar_reload import show_reload
from llm.conversations.pdf_rag import get_pdf_rag_conversation
from llm.conversations.pdf_auto import get_pdf_auto_conversation

from utils.log import logger


st.title("☃️ Chat with PDF")


def main() -> None:
    # Check if OpenAI API key is set
    openai_key = get_openai_key()
    if openai_key is None or openai_key == "" or openai_key == "sk-***":
        st.write("🔑  OpenAI API key not set")
        return

    # Get username
    if "user_name" not in st.session_state:
        username_input_container = st.sidebar.empty()
        username = username_input_container.text_input(":astronaut: Enter username")
        if username != "":
            st.session_state["user_name"] = username
            username_input_container.empty()

    user_name = st.session_state.get("user_name", None)
    if user_name:
        st.sidebar.info(f":astronaut: User: {user_name}")
    else:
        st.write(":astronaut: Please enter a username")
        return

    # Get conversation type
    pdf_conversation_type = st.sidebar.selectbox(
        "Conversation Type", options=["RAG", "Autonomous"]
    )
    # Set conversation_type in session state
    if "pdf_conversation_type" not in st.session_state:
        st.session_state["pdf_conversation_type"] = pdf_conversation_type
    # Restart the conversation if conversation_type has changed
    elif st.session_state["pdf_conversation_type"] != pdf_conversation_type:
        st.session_state["pdf_conversation"] = None
        st.session_state["pdf_conversation_type"] = pdf_conversation_type
        st.experimental_rerun()

    # Get the conversation
    pdf_conversation: Conversation
    if (
        "pdf_conversation" not in st.session_state
        or st.session_state["pdf_conversation"] is None
    ):
        if st.session_state["pdf_conversation_type"] == "Autonomous":
            logger.info("---*--- Creating Autonomous Conversation ---*---")
            pdf_conversation = get_pdf_auto_conversation(
                user_name=user_name,
                debug_logs=True,
            )
        else:
            logger.info("---*--- Creating RAG Conversation ---*---")
            pdf_conversation = get_pdf_rag_conversation(
                user_name=user_name,
                debug_logs=True,
            )
        st.session_state["pdf_conversation"] = pdf_conversation
    else:
        pdf_conversation = st.session_state["pdf_conversation"]
    # Start conversation and save conversation id in session state
    st.session_state["pdf_conversation_id"] = pdf_conversation.start()

    # Check if knowlege base exists
    if (
        "pdf_knowledge_base_exists" not in st.session_state
        or not st.session_state["pdf_knowledge_base_exists"]
    ):
        if not pdf_conversation.knowledge_base.exists():
            st.sidebar.write("🧠 Loading knowledge base")
            pdf_conversation.knowledge_base.load()
            st.session_state["pdf_knowledge_base_exists"] = True
            st.sidebar.success("Knowledge Base loaded")

    # Load messages if this is not a new conversation
    user_chat_history = pdf_conversation.history.get_chat_history()
    if len(user_chat_history) > 0:
        logger.debug("Loading chat history")
        st.session_state["messages"] = user_chat_history
    else:
        logger.debug("No chat history found")
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Ask me anything..."}
        ]

    # Prompt for user input and save
    if prompt := st.chat_input():
        st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display the existing chat messages
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is from a user, generate a new response
    last_message = st.session_state["messages"][-1]
    if last_message.get("role", "") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in pdf_conversation.chat(question):
                response += delta
                resp_container.markdown(response)

            st.session_state["messages"].append(
                {"role": "assistant", "content": response}
            )

    if st.sidebar.button("New Conversation"):
        st.session_state["pdf_conversation"] = None
        st.session_state["pdf_conversation_id"] = None
        st.experimental_rerun()

    if st.sidebar.button("Update Knowledge Base"):
        pdf_conversation.knowledge_base.load(recreate=False)
        st.session_state["pdf_knowledge_base_exists"] = True
        st.sidebar.success("Knowledge Base Updated")

    if st.sidebar.button("Recreate Knowledge Base"):
        pdf_conversation.knowledge_base.load(recreate=True)
        st.session_state["pdf_knowledge_base_exists"] = True
        st.sidebar.success("Knowledge Base Recreated")

    if st.sidebar.button("Auto Rename"):
        pdf_conversation.auto_rename()

    all_pdf_conversation_ids: List[
        int
    ] = pdf_conversation.storage.get_all_conversation_ids(user_name=user_name)
    new_pdf_conversation_id = st.sidebar.selectbox(
        "Conversation ID", options=all_pdf_conversation_ids
    )
    if st.session_state["pdf_conversation_id"] != new_pdf_conversation_id:
        logger.debug(f"Loading conversation {new_pdf_conversation_id}")
        if st.session_state["pdf_conversation_type"] == "Autonomous":
            logger.info("---*--- Loading as Autonomous Conversation ---*---")
            st.session_state["pdf_conversation"] = get_pdf_auto_conversation(
                user_name=user_name,
                conversation_id=new_pdf_conversation_id,
                debug_logs=True,
            )
        else:
            logger.info("---*--- Loading as RAG Conversation ---*---")
            st.session_state["pdf_conversation"] = get_pdf_rag_conversation(
                user_name=user_name,
                conversation_id=new_pdf_conversation_id,
                debug_logs=True,
            )
        st.experimental_rerun()

    pdf_conversation_name = pdf_conversation.name
    if pdf_conversation_name:
        st.sidebar.write(f":thread: {pdf_conversation_name}")

    # Show reload button
    show_reload()


main()