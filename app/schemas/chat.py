from pydantic import BaseModel
from typing import Optional

class WhatsAppMessageIn(BaseModel):
    """
    Schema for incoming Twilio webhook.
    See: https://www.twilio.com/docs/messaging/twiml/webhook-request
    """
    From: str  # e.g., "whatsapp:+14155238886"
    To: str    # e.g., "whatsapp:+15005550006"
    Body: str  # The message text

class DocumentUpload(BaseModel):
    content: str
    filename: str