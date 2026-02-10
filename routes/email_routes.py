from fastapi import APIRouter, HTTPException
from utils.email_sender import send_email
from schemas.email_schemas import EmailRequest, EmailResponse

router = APIRouter()


@router.post("/send-email", response_model=EmailResponse)
def send_email_route(request: EmailRequest):
    """Send an email with sender, receiver, and content."""
    try:
        result = send_email(request.sender, request.receiver, request.content)
        return EmailResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
