from twilio.rest import Client
from loguru import logger

from app.config import settings

# Initialize Twilio Client
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to: str, body: str):
    """
    Sends a message via the Twilio WhatsApp API.
    """
    try:
        logger.info(f"Sending WhatsApp message to {to}: {body[:100]}...")
        message = twilio_client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=to
        )
        logger.info(f"Message sent successfully. SID: {message.sid}")
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message to {to}: {e}")
