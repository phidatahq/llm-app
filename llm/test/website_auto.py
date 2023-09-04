from llm.conversations.website_auto import get_website_auto_conversation

website_auto_conversation = get_website_auto_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE:
    website_auto_conversation.knowledge_base.load(recreate=False)

website_auto_conversation.print_response("Tell me about phidata?")
website_auto_conversation.print_response("How do I create a LLM App using phidata?")