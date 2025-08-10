import asyncio
from celery import Celery
from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import settings
from app.services.ai_engine import get_ai_response
from app.services.whatsapp import send_whatsapp_message
from app.services.vectorstore import embed_and_store_document
from app.models.clinic import Clinic
from app.models.chat import ChatHistory, Message

# Setup Celery App
celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# Setup synchronous SQLAlchemy session for use in Celery tasks
# Celery workers are separate processes, so they need their own engine.
# We use a sync engine because Celery tasks are typically synchronous.
sync_engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", "+psycopg2"))
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

@celery_app.task(name="process_whatsapp_message", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def process_whatsapp_message(message_data: dict):
    """
    Celery task to process an incoming WhatsApp message.
    It fetches clinic info, gets an AI response, sends a reply, and logs the conversation.
    """
    customer_phone = message_data['From']
    clinic_phone = message_data['To'] # The clinic's WhatsApp number
    user_message = message_data['Body']
    
    db = SyncSessionLocal()
    try:
        # 1. Find the clinic associated with the 'To' number.
        # This is a simplification. A real app would have a mapping of Twilio numbers to clinics.
        # For now, we'll assume one clinic for demonstration.
        clinic = db.query(Clinic).first()
        if not clinic:
            logger.error(f"No clinic found for number {clinic_phone}. Cannot process message.")
            return

        clinic_id = clinic.id

        # 2. Get AI response. We need to run our async get_ai_response function
        # from this synchronous Celery task.
        ai_message = asyncio.run(run_async_get_ai_response(clinic_id, customer_phone, user_message))

        # 3. Send reply via WhatsApp
        send_whatsapp_message(to=customer_phone, body=ai_message)

        # 4. Log the conversation to the database
        chat_history = db.query(ChatHistory).filter_by(customer_phone=customer_phone, clinic_id=clinic_id).first()
        if not chat_history:
            chat_history = ChatHistory(customer_phone=customer_phone, clinic_id=clinic_id)
            db.add(chat_history)
            db.commit()
            db.refresh(chat_history)
        
        # Add user message and assistant response
        db.add(Message(content=user_message, role='user', chat_history_id=chat_history.id))
        db.add(Message(content=ai_message, role='assistant', chat_history_id=chat_history.id))
        db.commit()
        logger.info(f"Successfully processed and logged message for {customer_phone}")

    except Exception as e:
        logger.error(f"Error in Celery task for {customer_phone}: {e}")
        db.rollback()
        raise # Reraise to trigger Celery retry mechanism
    finally:
        db.close()

@celery_app.task(name="add_document_to_vectorstore")
def add_document_to_vectorstore(content: str, filename: str, clinic_id: int):
    """
    Celery task to trigger the embedding and storage of a document.
    """
    embed_and_store_document(content, filename, clinic_id)


async def run_async_get_ai_response(clinic_id: int, customer_phone: str, user_message: str) -> str:
    """
    Helper function to create an async session and call the async get_ai_response function.
    """
    from app.database import async_session_maker
    async with async_session_maker() as session:
        return await get_ai_response(session, clinic_id, customer_phone, user_message)