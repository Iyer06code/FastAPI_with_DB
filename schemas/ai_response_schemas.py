from pydantic import BaseModel
from typing import List, Dict, Optional

class AIRequest(BaseModel):
    user_id: int  # Required to associate chat with a user
    chat_id: Optional[int] = None # Optional, if None -> New Chat
    message: str

class AIResponse(BaseModel):
    response: str
    chat_id: int

