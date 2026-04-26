from fastapi import HTTPException, status
from typing import Dict, List
import importlib.util
from pathlib import Path

from logger_config import get_logger

from backend.repositories import ConversationRepository, MessageRepository
from backend.schemas import ChatRequest, ChatResponse, ConversationDTO, MessageDTO

logger = get_logger(__name__)


def _map_chatbot_error_to_message(error: Exception) -> str:
    text = str(error or "").lower()
    if "openai_api_key" in text or "api key" in text or "invalid_api_key" in text:
        return "Khong the ket noi AI do API key khong hop le hoac chua cau hinh."
    if "insufficient_quota" in text or "quota" in text or "rate limit" in text:
        return "He thong AI tam thoi het han muc hoac bi gioi han tan suat. Vui long thu lai sau."
    if "langchain" in text or "pydantic" in text or "module" in text or "import" in text:
        return "Chatbot chua san sang do loi dependency. Vui long kiem tra moi truong va requirements."
    return "Xin loi, da co loi xay ra khi xu ly yeu cau cua ban."


def _process_user_query(query: str) -> str:
    chatbot_path = Path(__file__).resolve().parents[2] / "chatbot.py"
    logger.info(
        "[conversation_service.py][_process_user_query] Start load chatbot module path=%s query_len=%s",
        chatbot_path,
        len(query or ""),
    )
    spec = importlib.util.spec_from_file_location("chatbot", chatbot_path)
    if spec is None or spec.loader is None:
        logger.error(
            "[conversation_service.py][_process_user_query] End status=error reason=invalid_import_spec path=%s",
            chatbot_path,
        )
        return "Chatbot is not configured. Please check dependencies."

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        logger.exception(
            "[conversation_service.py][_process_user_query] End status=error reason=chatbot_module_load_failed path=%s error=%s",
            chatbot_path,
            str(exc),
        )
        return _map_chatbot_error_to_message(exc)

    if not hasattr(module, "process_user_query"):
        logger.error(
            "[conversation_service.py][_process_user_query] End status=error reason=missing_entrypoint module=chatbot",
        )
        return "Chatbot is not configured. Please check dependencies."

    logger.info("[conversation_service.py][_process_user_query] Chatbot module loaded successfully")
    try:
        result = module.process_user_query(query)
    except Exception as exc:
        logger.exception(
            "[conversation_service.py][_process_user_query] End status=error reason=chatbot_runtime_error error=%s",
            str(exc),
        )
        return _map_chatbot_error_to_message(exc)
    logger.info(
        "[conversation_service.py][_process_user_query] End status=success response_len=%s",
        len(result or ""),
    )
    return result


class ConversationService:
    def __init__(self, conversation_repository: ConversationRepository, message_repository: MessageRepository):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def create_conversation(self, title: str, current_user: Dict) -> ConversationDTO:
        logger.info("[conversation_service.py][create_conversation] Start business=create conversation user=%s", current_user.get("username"))
        try:
            conversation = self.conversation_repository.create(user_id=current_user["id"], title=title)
            logger.info("[conversation_service.py][create_conversation] End status=success conversation_id=%s", conversation.id)
            return ConversationDTO(**conversation.__dict__)
        except Exception:
            logger.exception("[conversation_service.py][create_conversation] End status=error user_id=%s", current_user.get("id"))
            raise

    def get_conversations(self, current_user: Dict) -> List[ConversationDTO]:
        logger.info("[conversation_service.py][get_conversations] Start business=list conversations user=%s", current_user.get("username"))
        try:
            items = self.conversation_repository.list_by_user(current_user["id"])
            result = [ConversationDTO(**item.__dict__) for item in items]
            logger.info("[conversation_service.py][get_conversations] End status=success count=%s", len(result))
            return result
        except Exception:
            logger.exception("[conversation_service.py][get_conversations] End status=error user_id=%s", current_user.get("id"))
            raise

    def get_conversation(self, conversation_id: str, current_user: Dict) -> ConversationDTO:
        logger.info("[conversation_service.py][get_conversation] Start business=get conversation id=%s", conversation_id)
        try:
            item = self.conversation_repository.find_by_id_and_user(conversation_id, current_user["id"])
            if not item:
                logger.error("[conversation_service.py][get_conversation] End status=error reason=not_found conversation_id=%s", conversation_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
            logger.info("[conversation_service.py][get_conversation] End status=success conversation_id=%s", conversation_id)
            return ConversationDTO(**item.__dict__)
        except HTTPException:
            raise
        except Exception:
            logger.exception("[conversation_service.py][get_conversation] End status=error conversation_id=%s", conversation_id)
            raise

    def delete_conversation(self, conversation_id: str, current_user: Dict) -> None:
        logger.info("[conversation_service.py][delete_conversation] Start business=delete conversation id=%s", conversation_id)
        try:
            item = self.conversation_repository.find_by_id_and_user(conversation_id, current_user["id"])
            if not item:
                logger.error("[conversation_service.py][delete_conversation] End status=error reason=not_found conversation_id=%s", conversation_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

            self.message_repository.delete_by_conversation(conversation_id)
            self.conversation_repository.delete_by_id(conversation_id)
            logger.info("[conversation_service.py][delete_conversation] End status=success conversation_id=%s", conversation_id)
        except HTTPException:
            raise
        except Exception:
            logger.exception("[conversation_service.py][delete_conversation] End status=error conversation_id=%s", conversation_id)
            raise

    def get_messages(self, conversation_id: str, current_user: Dict) -> List[MessageDTO]:
        logger.info("[conversation_service.py][get_messages] Start business=list messages conversation=%s", conversation_id)
        try:
            item = self.conversation_repository.find_by_id_and_user(conversation_id, current_user["id"])
            if not item:
                logger.error("[conversation_service.py][get_messages] End status=error reason=not_found conversation_id=%s", conversation_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

            messages = self.message_repository.list_by_conversation(conversation_id)
            result = [MessageDTO(**msg.__dict__) for msg in messages]
            logger.info("[conversation_service.py][get_messages] End status=success count=%s conversation_id=%s", len(result), conversation_id)
            return result
        except HTTPException:
            raise
        except Exception:
            logger.exception("[conversation_service.py][get_messages] End status=error conversation_id=%s", conversation_id)
            raise

    def chat(self, conversation_id: str, request: ChatRequest, current_user: Dict) -> ChatResponse:
        logger.info("[conversation_service.py][chat] Start business=chat conversation=%s", conversation_id)
        try:
            item = self.conversation_repository.find_by_id_and_user(conversation_id, current_user["id"])
            if not item:
                logger.error("[conversation_service.py][chat] End status=error reason=not_found conversation_id=%s", conversation_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

            logger.info(
                "[conversation_service.py][chat] Persist user message conversation_id=%s user_id=%s content_len=%s",
                conversation_id,
                current_user.get("id"),
                len(request.message or ""),
            )
            user_message = self.message_repository.create(
                conversation_id=conversation_id,
                role="user",
                content=request.message,
            )
            logger.info(
                "[conversation_service.py][chat] User message persisted message_id=%s conversation_id=%s",
                user_message.id,
                conversation_id,
            )

            try:
                logger.info("[conversation_service.py][chat] Start AI processing conversation_id=%s", conversation_id)
                ai_response = _process_user_query(request.message)
                logger.info(
                    "[conversation_service.py][chat] AI processing finished conversation_id=%s response_len=%s",
                    conversation_id,
                    len(ai_response or ""),
                )
            except Exception:
                logger.exception("[conversation_service.py][chat] End status=error reason=chatbot_failure conversation_id=%s", conversation_id)
                ai_response = "Xin loi, da co loi xay ra khi xu ly yeu cau cua ban."

            logger.info("[conversation_service.py][chat] Persist assistant message conversation_id=%s", conversation_id)
            assistant_message = self.message_repository.create(
                conversation_id=conversation_id,
                role="assistant",
                content=ai_response,
            )
            logger.info(
                "[conversation_service.py][chat] Assistant message persisted message_id=%s conversation_id=%s",
                assistant_message.id,
                conversation_id,
            )
            self.conversation_repository.touch_updated_at(conversation_id, assistant_message.created_at)
            logger.info(
                "[conversation_service.py][chat] Conversation timestamp touched conversation_id=%s updated_at=%s",
                conversation_id,
                assistant_message.created_at,
            )

            logger.info("[conversation_service.py][chat] End status=success conversation_id=%s message_id=%s", conversation_id, assistant_message.id)
            return ChatResponse(
                response=ai_response,
                conversation_id=conversation_id,
                message_id=assistant_message.id,
            )
        except HTTPException:
            raise
        except Exception:
            logger.exception("[conversation_service.py][chat] End status=error conversation_id=%s", conversation_id)
            raise
