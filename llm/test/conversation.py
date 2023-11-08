from phi.conversation import Conversation

conversation = Conversation(monitoring=True)

# Stream is True by default
conversation.print_response("Tell me a 2 sentence horror story.")
# Set stream to False
# conversation.print_response("Tell me a 1 sentence horror story.", stream=False)
