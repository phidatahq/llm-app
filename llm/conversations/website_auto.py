from typing import Optional

from phi.conversation import Conversation
from phi.llm.openai import OpenAIChat
from phi.llm.function.website import WebsiteRegistry

from llm.settings import llm_settings
from llm.storage import website_conversation_storage
from llm.knowledge_base import website_knowledge_base


def get_website_auto_conversation(
    user_name: Optional[str] = None,
    conversation_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Conversation:
    """Get an autonomous conversation with the Website knowledge base"""

    return Conversation(
        id=conversation_id,
        user_name=user_name,
        llm=OpenAIChat(
            model=llm_settings.gpt_4,
            max_tokens=llm_settings.default_max_tokens,
            temperature=llm_settings.default_temperature,
        ),
        storage=website_conversation_storage,
        knowledge_base=website_knowledge_base,
        debug_mode=debug_mode,
        monitoring=True,
        function_calls=True,
        show_function_calls=True,
        function_registries=[
            WebsiteRegistry(knowledge_base=website_knowledge_base),
        ],
        system_prompt="""\
        You are a chatbot named 'Phi' designed to help users.
        You have access to a knowledge base of website contents that you can search to answer questions.
        You also have access to functions to add new websites to the knowledge base.

        Follow these guidelines when answering questions:
        - You can ask follow up questions if needed.
        - If you don't know the answer, say 'I don't know'.
        - Search the knowledge base for answers.
        - Do not use phrases like 'based on the information provided' in your answer.
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
        meta_data={"conversation_type": "AUTO"},
    )
