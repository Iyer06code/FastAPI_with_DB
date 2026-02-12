from fastapi import APIRouter, HTTPException
from schemas.ai_response_schemas import AIRequest, AIResponse
from utils.ai_response import get_completion

router = APIRouter()

@router.post("/ai/ask", response_model=AIResponse)
def ask_ai(request: AIRequest):
    try:
        response = get_completion(
            user_message=request.message,
            system_message="""
You are a helpful assistant.

Rules:
- Use headings
- Use bullet points
- Keep answers structured
- Avoid long paragraphs
"""
        )

        return AIResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
