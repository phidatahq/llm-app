from phi.conversation import Conversation
from phi.conversation.storage.postgres import PgConversationStorage
from phi.llm.openai import OpenAIChat
from phi.llm.function.website import WebsiteRegistry

from llm.knowledge_base import website_knowledge_base
from llm.settings import llm_settings
from db.session import db_url

website_auto_conversation = Conversation(
    llm=OpenAIChat(
        model=llm_settings.gpt_4,
        max_tokens=llm_settings.default_max_tokens,
        temperature=llm_settings.default_temperature,
    ),
    storage=PgConversationStorage(
        table_name="website_conversations",
        db_url=db_url,
    ),
    create_storage=True,
    knowledge_base=website_knowledge_base,
    monitor=True,
    debug_logs=True,
    function_calls=True,
    show_function_calls=True,
    function_registries=[
        WebsiteRegistry(knowledge_base=website_knowledge_base),
    ],
    system_prompt="""\
    You are a chatbot named 'Phi' designed to help users.
    You have access to website contents in a knowledge base that you can search to answer questions.

    Remember the following guidelines:
    - If you don't know the answer, say 'I don't know'.
    - Do not use phrases like 'based on the information provided' or 'according to the information provided' in your answer.
    - You can ask follow up questions if needed.
    - Use bullet points where possible.
    - User markdown to format your answers.
    - Keep your answers short and concise, under 5 sentences.
    """,
    user_prompt_function=lambda message, **kwargs: f"""\
    Start and end your answers with a polite greeting.
    Your task is to respond to the following message:
    USER: {message}
    ASSISTANT:
    """,
)
