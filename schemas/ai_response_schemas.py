from pydantic import BaseModel
from typing import List, Dict

class AIRequest(BaseModel):
    message: str
    system_prompt: str
    history: List[Dict] = []   # 👈 ADD THIS

class AIResponse(BaseModel):
    response: str
