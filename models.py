from db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    chats = relationship("ChatSession", back_populates="user")


# 🔹 Each conversation
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")
    messages = relationship("ChatMessage", back_populates="chat")


# 🔹 Each message inside a conversation
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String)  # user / assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("ChatSession", back_populates="messages")
