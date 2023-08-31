from llm.conversations.arxiv_auto import get_arxiv_auto_conversation

arxiv_auto_conversation = get_arxiv_auto_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE:
    arxiv_auto_conversation.knowledge_base.load(recreate=False)

arxiv_auto_conversation.print_response("Tell me about Generative AI?")
arxiv_auto_conversation.print_response("What are the Security Risks of Generative AI?")
arxiv_auto_conversation.print_response("Summarize 4 papers about Generative AI?")
