from llm.conversations.pdf_auto import pdf_auto_conversation

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE:
    pdf_auto_conversation.knowledge_base.load(recreate=False)

pdf_auto_conversation.print_response("Tell me about food safety?")
pdf_auto_conversation.print_response("Share a good evening recipe?")
pdf_auto_conversation.print_response("How do I make chicken casserole?")
pdf_auto_conversation.print_response("How do I make Spaghetti Bolognaise?")
pdf_auto_conversation.print_response("Summarize our conversation")
