from llm.conversations.website_rag import get_website_rag_conversation

website_rag_conversation = get_website_rag_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE:
    website_rag_conversation.knowledge_base.load(recreate=True)

website_rag_conversation.print_response("Tell me about phidata?")
website_rag_conversation.print_response("How do I create a LLM App using phidata?")
