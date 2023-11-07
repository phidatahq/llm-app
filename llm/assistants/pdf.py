from typing import Optional

from phi.assistant import Assistant
from phi.llm.openai import GPT

from llm.settings import llm_settings
from llm.storage import pdf_conversation_storage
from llm.knowledge_base import pdf_knowledge_base

pdf_assistent = Assistant()

print(pdf_assistent)
