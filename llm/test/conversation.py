from phi.conversation import Conversation
from phi.utils.log import set_log_level_to_debug

set_log_level_to_debug()

conversation = Conversation(monitoring=True)

# Stream is True by default
conversation.print_response("Tell me a 2 sentence horror story.")
# Set stream to False
# conversation.print_response("Tell me a 1 sentence horror story.", stream=False)
