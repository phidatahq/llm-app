from llm.conversations.arxiv_rag import get_arxiv_rag_conversation

arxiv_rag_conversation = get_arxiv_rag_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE:
    arxiv_rag_conversation.knowledge_base.load(recreate=False)

arxiv_rag_conversation.print_response("Tell me about Generative AI?")
arxiv_rag_conversation.print_response("What are the Security Risks of Generative AI?")
arxiv_rag_conversation.print_response("Summarize 4 papers about Generative AI?")
