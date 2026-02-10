from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    sender: EmailStr
    receiver: EmailStr
    content: str

class EmailResponse(BaseModel):
    message: str
    sender: str
    receiver: str
