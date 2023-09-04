from typing import Optional

from phi.conversation import Conversation
from phi.conversation.storage.postgres import PgConversationStorage
from phi.llm.openai import OpenAIChat

from llm.knowledge_base import pdf_knowledge_base
from llm.settings import llm_settings
from db.session import db_url


def get_pdf_auto_conversation(
    user_name: Optional[str] = None,
    conversation_id: Optional[int] = None,
    debug_logs: bool = False,
) -> Conversation:
    """Get an autonomous conversation with the PDF knowledge base"""

    return Conversation(
        id=conversation_id,
        user_name=user_name,
        llm=OpenAIChat(
            model=llm_settings.gpt_4,
            max_tokens=llm_settings.default_max_tokens,
            temperature=llm_settings.default_temperature,
        ),
        storage=PgConversationStorage(
            table_name="pdf_auto_conversations",
            db_url=db_url,
        ),
        knowledge_base=pdf_knowledge_base,
        debug_logs=debug_logs,
        monitor=True,
        create_storage=True,
        function_calls=True,
        show_function_calls=True,
        system_prompt="""\
        You are a chatbot named 'Phi' designed to help users.
        You have access to a knowledge base that you can search to answer questions.

        Remember the following guidelines:
        - If you don't know the answer, say 'I don't know'.
        - Do not use phrases like 'based on the information provided' in your answer.
        - You can ask follow up questions if needed.
        - Use bullet points where possible.
        - Use markdown to format your answers.
        - Keep your answers short and concise, under 5 sentences.
        """,
        user_prompt_function=lambda message, **kwargs: f"""\
        Start and end your answers with a polite greeting.
        Your task is to respond to the following message:
        USER: {message}
        ASSISTANT:
        """,
    )