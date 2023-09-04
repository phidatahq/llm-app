from typing import Generator, Optional, List, Dict, Any
from typing_extensions import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from phi.conversation import Conversation, ConversationRow
from pydantic import BaseModel

from api.routes.endpoints import endpoints
from llm.conversations.pdf_rag import get_pdf_rag_conversation
from llm.conversations.pdf_auto import get_pdf_auto_conversation
from utils.log import logger

######################################################
## Router for PDF Conversations
######################################################

ConversationType = Literal["RAG", "AUTO"]
pdf_router = APIRouter(prefix=endpoints.PDF, tags=["PDF"])


def get_conversation(
    conversation_type: ConversationType,
    conversation_id: Optional[int] = None,
    user_name: Optional[str] = None,
):
    """Get a conversation using the conversation_id"""
    if conversation_type == "RAG":
        return get_pdf_rag_conversation(
            conversation_id=conversation_id, user_name=user_name
        )
    elif conversation_type == "AUTO":
        return get_pdf_auto_conversation(
            conversation_id=conversation_id, user_name=user_name
        )


class CreateConversationRequest(BaseModel):
    user_name: str
    conversation_type: ConversationType = "RAG"


class CreateConversationResponse(BaseModel):
    conversation_id: int
    chat_history: List[Dict[str, Any]]


@pdf_router.post("/conversation/create", response_model=CreateConversationResponse)
def create_conversation(body: CreateConversationRequest):
    """Create a new conversation and return the conversation_id"""
    logger.debug(f"CreateConversationRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, user_name=body.user_name
    )
    # start() will log the conversation in the database and return the conversation_id
    # which is returned to the frontend to retrieve the conversation later
    conversation_id: Optional[int] = conversation.start()
    if conversation_id is None:
        raise HTTPException(status_code=500, detail="Failed to create conversation")
    logger.debug(f"Created Conversation: {conversation_id}")

    return CreateConversationResponse(
        user_name=conversation.user_name,
        role=conversation.user_persona,
        conversation_id=conversation_id,
        chat_history=conversation.history.get_chat_history(),
    )


def chat_response_streamer(conversation: Conversation, message: str) -> Generator:
    for chunk in conversation.chat(message):
        yield chunk


class ChatRequest(BaseModel):
    message: str
    stream: bool = True
    conversation_id: Optional[int] = None
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/chat")
def chat(body: ChatRequest):
    """Send a message to the PDF Conversation and return the response"""
    logger.debug(f"ChatRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    if body.stream:
        return StreamingResponse(
            chat_response_streamer(conversation, body.message),
            media_type="text/event-stream",
        )
    else:
        return conversation.chat(body.message, stream=False)


class ChatHistoryRequest(BaseModel):
    conversation_id: int
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/chat/history", response_model=List[Dict[str, Any]])
def get_chat_history(body: ChatHistoryRequest):
    """Return the chat history for a conversation"""
    logger.debug(f"ChatHistoryRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    # Load the conversation from the database
    conversation.read_from_storage()

    return conversation.history.get_chat_history()


class GetConversationRequest(BaseModel):
    conversation_id: int
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/conversation/get", response_model=Optional[ConversationRow])
def get_conversation_row(body: GetConversationRequest):
    """Return a conversation using the conversation_id"""
    logger.debug(f"GetConversationRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    return conversation.read_from_storage()


class GetAllConversationsRequest(BaseModel):
    user_name: str
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/conversation/get-all", response_model=List[ConversationRow])
def get_conversations(body: GetAllConversationsRequest):
    """Return all conversations for a user"""
    logger.debug(f"GetAllConversationsRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, user_name=body.user_name
    )
    return conversation.storage.get_all_conversations(user_name=body.user_name)


class GetAllConversationIdsRequest(BaseModel):
    user_name: str
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/conversation/get-all-ids", response_model=List[int])
def get_conversation_ids(body: GetAllConversationIdsRequest):
    """Return all conversation_ids for a user"""
    logger.debug(f"GetAllConversationIdsRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, user_name=body.user_name
    )
    return conversation.storage.get_all_conversation_ids(user_name=body.user_name)


class RenameConversationRequest(BaseModel):
    name: str
    conversation_id: int
    conversation_type: ConversationType = "RAG"


class RenameConversationResponse(BaseModel):
    name: str
    conversation_id: int


@pdf_router.post("/conversation/rename", response_model=RenameConversationResponse)
def rename_conversation(body: RenameConversationRequest):
    """Rename a conversation"""
    logger.debug(f"RenameConversationRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    conversation.rename(body.name)

    return RenameConversationResponse(
        name=conversation.name,
        conversation_id=conversation.id,
    )


class AutoRenameConversationRequest(BaseModel):
    conversation_id: int
    conversation_type: ConversationType = "RAG"


class AutoRenameConversationResponse(BaseModel):
    name: str
    conversation_id: int


@pdf_router.post(
    "/conversation/autorename", response_model=AutoRenameConversationResponse
)
def autorename_conversation(body: AutoRenameConversationRequest):
    """Rename a conversation using the LLM"""
    logger.debug(f"AutoRenameConversationRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    conversation.auto_rename()

    return RenameConversationResponse(
        name=conversation.name,
        conversation_id=conversation.id,
    )


class EndConversationRequest(BaseModel):
    conversation_id: int
    conversation_type: ConversationType = "RAG"


@pdf_router.post("/conversation/end", response_model=Optional[ConversationRow])
def end_conversation(body: EndConversationRequest):
    """End a conversation"""
    logger.debug(f"EndConversationRequest: {body}")

    conversation: Conversation = get_conversation(
        conversation_type=body.conversation_type, conversation_id=body.conversation_id
    )
    conversation.end()

    return conversation.read_from_storage()