import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(sender: str, receiver: str, content: str) -> dict:
    """
    Send an email using SMTP.

    Args:
        sender: Sender's email address
        receiver: Receiver's email address
        content: Email body content

    Returns:
        dict with status message
    """
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Message from FastAPI Email Service"

    msg.attach(MIMEText(content, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender, receiver, msg.as_string())

    return {
        "message": "Email sent successfully",
        "sender": sender,
        "receiver": receiver,
    }
