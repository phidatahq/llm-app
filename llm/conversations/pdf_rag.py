from typing import Optional

from phi.conversation import Conversation
from phi.llm.openai import OpenAIChat

from llm.settings import llm_settings
from llm.storage import pdf_conversation_storage
from llm.knowledge_base import pdf_knowledge_base


def get_pdf_rag_conversation(
    user_name: Optional[str] = None,
    conversation_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Conversation:
    """Get a RAG conversation with the PDF knowledge base"""

    return Conversation(
        id=conversation_id,
        user_name=user_name,
        llm=OpenAIChat(
            model=llm_settings.gpt_4,
            max_tokens=llm_settings.default_max_tokens,
            temperature=llm_settings.default_temperature,
        ),
        storage=pdf_conversation_storage,
        knowledge_base=pdf_knowledge_base,
        debug_mode=debug_mode,
        monitor=True,
        add_chat_history_to_messages=True,
        add_references_to_prompt=True,
        system_prompt="""\
        You are a chatbot named 'Phi' designed to help users.
        You will be provided with information from a knowledge base that you can use to answer questions.

        Remember the following guidelines:
        - If you don't know the answer, say 'I don't know'.
        - Do not use phrases like 'based on the information provided' in your answer.
        - You can ask follow up questions if needed.
        - Use bullet points where possible.
        - User markdown to format your answers.
        - Keep your answers short and concise, under 5 sentences.
        """,
        user_prompt_function=lambda message, references, **kwargs: f"""\
        Start and end your answers with a polite greeting.

        Use the following information from the knowledge base if it helps.
        START OF KNOWLEDGE BASE
        ```
        {references}
        ```
        END OF KNOWLEDGE BASE

        Your task is to respond to the following message:
        USER: {message}
        ASSISTANT:
        """,
        meta_data={"conversation_type": "RAG"},
    )
