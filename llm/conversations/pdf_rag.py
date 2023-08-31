from phi.conversation import Conversation
from phi.conversation.storage.postgres import PgConversationStorage
from phi.llm.openai import OpenAIChat

from llm.knowledge_base import pdf_knoweldge_base
from llm.settings import llm_settings
from db.session import db_url

pdf_rag_conversation = Conversation(
    llm=OpenAIChat(
        model=llm_settings.gpt_4,
        max_tokens=llm_settings.default_max_tokens,
        temperature=llm_settings.default_temperature,
    ),
    storage=PgConversationStorage(
        table_name="pdf_conversations",
        db_url=db_url,
    ),
    create_storage=True,
    knowledge_base=pdf_knoweldge_base,
    monitor=True,
    # debug_logs=True,
    add_history_to_messages=True,
    add_references_to_prompt=True,
    system_prompt="""\
    You are a chatbot named 'Phi' designed to help users.
    You will be provided with information from a knowledge base that you can use to answer questions.

    Remember the following guidelines:
    - If you don't know the answer, say 'I don't know'.
    - Do not use phrases like 'based on the information provided' or 'according to the information provided' in your answer.
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
)
