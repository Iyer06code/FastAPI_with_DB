from pydantic import BaseModel

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str   