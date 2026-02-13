from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.ai_response_schemas import AIRequest, AIResponse
from utils.ai_response import get_completion
from utils.search_tool import search_web
from db import get_db
from models import ChatSession, ChatMessage
import datetime

router = APIRouter()

@router.post("/ai/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db)):
    try:
        # 1. Handle Chat Session
        chat_id = request.chat_id
        if not chat_id:
            # Create new chat session
            new_chat = ChatSession(user_id=request.user_id, title=request.message[:30] + "...")
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            chat_id = new_chat.id
        
        # 2. Save User Message
        user_msg = ChatMessage(chat_id=chat_id, role="user", content=request.message)
        db.add(user_msg)
        db.commit()

        # 3. Fetch Chat History (for context)
        # Get last 10 messages to provide context
        history_records = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at.asc()).limit(10).all()
        history = [{"role": msg.role, "content": msg.content} for msg in history_records]

        # 4. Fetch live web results
        live_data = search_web(request.message)

        system_message = f"""
You are a helpful assistant with access to live web data.

Here is the latest information from the web for the user's query:
---
{live_data}
---

Rules:
- Use the live web data above to provide accurate, up-to-date answers with real numbers and prices.
- NEVER use placeholder values like X,XXX or approximate numbers. Always use the exact figures from the web data.
- Cite sources when providing data.
"""

        # 5. Get AI Response
        response_text = get_completion(
            user_message=request.message,
            system_message=system_message,
            history=history
        )

        # 6. Save AI Message
        ai_msg = ChatMessage(chat_id=chat_id, role="assistant", content=response_text)
        db.add(ai_msg)
        db.commit()

        return AIResponse(response=response_text, chat_id=chat_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import List
from pydantic import BaseModel

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

@router.get("/chat/history/{user_id}", response_model=List[ChatSessionResponse])
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    # Get all chat sessions for the user
    chats = db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc()).all()
    return chats

@router.get("/chat/messages/{chat_id}", response_model=List[ChatMessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    # Get all messages for a specific chat session
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at.asc()).all()
    return messages



