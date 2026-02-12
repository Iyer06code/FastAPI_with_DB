from utils.jwt_handler import get_current_user
from fastapi import APIRouter, HTTPException
from utils.ai_response import get_completion
from utils.search_tool import search_web
from schemas.ai_response_schemas import AIRequest, AIResponse
from utils.search_tool import search_web
from db import get_db
from fastapi import Depends
from models import ChatSession, ChatMessage

router = APIRouter()

@router.post("/ai/ask", response_model=AIResponse)
def ask_ai(
    request: AIRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # 🔥 Step 1: Ask AI if live data is needed
        decision = get_completion(
            user_message=f"Does this question require real-time or internet data? Answer only YES or NO.\nQuestion: {request.message}"
        )

        if "yes" in decision.lower():
            # 🔥 Step 2: Fetch live search results
            live_data = search_web(request.message)

            # 🔥 Step 3: Let AI format the live data nicely
            final_answer = get_completion(
                user_message=f"Using this live data:\n{live_data}\n\nAnswer the user's question clearly and professionally.",
                system_message="You are an AI assistant with access to live internet data."
            )

            return AIResponse(response=final_answer)

        # 🔥 If no live data required
        normal_response = get_completion(
            user_message=request.message,
            system_message="""
            You are a helpful assistant.
            Always reply using:
            - Headings
            - Bullet points
            - Short lines
            - Easy structure
            Avoid long paragraphs.
""",
            history=request.history
        )

        new_chat = Chat(
            user_id=current_user.id,
            message=request.message,
            response=normal_response
        )

        db.add(new_chat)
        db.commit()

        return AIResponse(response=normal_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
def get_chat_history(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    chats = db.query(Chat).filter(
        Chat.user_id == current_user.id
    ).order_by(Chat.id.desc()).all()

    return chats


    try:
        # 🔥 Step 1: Ask AI if live data is needed
        decision = get_completion(
            user_message=f"Does this question require real-time or internet data? Answer only YES or NO.\nQuestion: {request.message}"
        )

        if "yes" in decision.lower():
            # 🔥 Step 2: Fetch live search results
            live_data = search_web(request.message)

            # 🔥 Step 3: Let AI format the live data nicely
            final_answer = get_completion(
                user_message=f"Using this live data:\n{live_data}\n\nAnswer the user's question clearly and professionally.",
                system_message="You are an AI assistant with access to live internet data."
            )

            return AIResponse(response=final_answer)

        # 🔥 If no live data required
        normal_response = get_completion(
            user_message=request.message,
            system_message="""
            You are a helpful assistant.
            Always reply using:
            - Headings
            - Bullet points
            - Short lines
            - Easy structure
            Avoid long paragraphs.
""",
            history=request.history
        )

        new_chat = Chat(
            user_id=current_user.id,
            message=request.message,
            response=normal_response
        )

        db.add(new_chat)
        db.commit()

        return AIResponse(response=normal_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
