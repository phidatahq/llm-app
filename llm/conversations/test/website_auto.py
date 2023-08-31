from llm.conversations.website_auto import website_auto_conversation

if not website_auto_conversation.knowledge_base.exists():
    website_auto_conversation.knowledge_base.load(recreate=False)

website_auto_conversation.print_response("Tell me about phidata?")
website_auto_conversation.print_response("How do I create a LLM App using phidata?")
