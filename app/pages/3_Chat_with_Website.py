from typing import List

import streamlit as st
from phi.conversation import Conversation

from app.password import check_password
from app.get_openai_key import get_openai_key
from app.sidebar_reload import show_reload
from llm.conversations.website_rag import get_website_rag_conversation
from llm.conversations.website_auto import get_website_auto_conversation

from utils.log import logger


st.title("☃️ Chat with Website")


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
    website_conversation_type = st.sidebar.selectbox(
        "Conversation Type", options=["Autonomous", "RAG"]
    )
    # Set conversation_type in session state
    if "website_conversation_type" not in st.session_state:
        st.session_state["website_conversation_type"] = website_conversation_type
    # Restart the conversation if conversation_type has changed
    elif st.session_state["website_conversation_type"] != website_conversation_type:
        st.session_state["website_conversation"] = None
        st.session_state["website_conversation_type"] = website_conversation_type
        st.experimental_rerun()

    # Get the conversation
    website_conversation: Conversation
    if (
        "website_conversation" not in st.session_state
        or st.session_state["website_conversation"] is None
    ):
        if st.session_state["website_conversation_type"] == "Autonomous":
            logger.info("---*--- Creating Autonomous Conversation ---*---")
            website_conversation = get_website_auto_conversation(
                user_name=user_name,
                debug_logs=True,
            )
        else:
            logger.info("---*--- Creating RAG Conversation ---*---")
            website_conversation = get_website_rag_conversation(
                user_name=user_name,
                debug_logs=True,
            )
        st.session_state["website_conversation"] = website_conversation
    else:
        website_conversation = st.session_state["website_conversation"]
    # Start conversation and save conversation id in session state
    st.session_state["website_conversation_id"] = website_conversation.start()

    # Check if knowlege base exists
    if website_conversation.knowledge_base and (
        "website_knowledge_base_exists" not in st.session_state
        or not st.session_state["website_knowledge_base_exists"]
    ):
        if not website_conversation.knowledge_base.exists():
            st.sidebar.write("🧠 Loading knowledge base")
            website_conversation.knowledge_base.load()
            st.session_state["website_knowledge_base_exists"] = True
            st.sidebar.success("Knowledge Base loaded")

    # Load messages if this is not a new conversation
    user_chat_history = website_conversation.history.get_chat_history()
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
            for delta in website_conversation.chat(question):
                response += delta
                resp_container.markdown(response)

            st.session_state["messages"].append(
                {"role": "assistant", "content": response}
            )

    if st.sidebar.button("New Conversation"):
        st.session_state["website_conversation"] = None
        st.session_state["website_conversation_id"] = None
        st.experimental_rerun()

    if website_conversation.knowledge_base:
        if st.sidebar.button("Update Knowledge Base"):
            website_conversation.knowledge_base.load(recreate=False)
            st.session_state["knowledge_base_exists"] = True
            st.sidebar.success("Knowledge Base Updated")

        if st.sidebar.button("Recreate Knowledge Base"):
            website_conversation.knowledge_base.load(recreate=True)
            st.session_state["knowledge_base_exists"] = True
            st.sidebar.success("Knowledge Base Recreated")

    if st.sidebar.button("Auto Rename"):
        website_conversation.auto_rename()

    if website_conversation.storage:
        all_website_conversation_ids: List[
            int
        ] = website_conversation.storage.get_all_conversation_ids(user_name=user_name)
        new_website_conversation_id = st.sidebar.selectbox(
            "Conversation ID", options=all_website_conversation_ids
        )
        if st.session_state["website_conversation_id"] != new_website_conversation_id:
            logger.debug(f"Loading conversation {new_website_conversation_id}")
            if st.session_state["website_conversation_type"] == "Autonomous":
                logger.info("---*--- Loading as Autonomous Conversation ---*---")
                st.session_state[
                    "website_conversation"
                ] = get_website_auto_conversation(
                    user_name=user_name,
                    conversation_id=new_website_conversation_id,
                    debug_logs=True,
                )
            else:
                logger.info("---*--- Loading as RAG Conversation ---*---")
                st.session_state["website_conversation"] = get_website_rag_conversation(
                    user_name=user_name,
                    conversation_id=new_website_conversation_id,
                    debug_logs=True,
                )
            st.experimental_rerun()

    website_conversation_name = website_conversation.name
    if website_conversation_name:
        st.sidebar.write(f":thread: {website_conversation_name}")

    # Show reload button
    show_reload()


if check_password():
    main()
