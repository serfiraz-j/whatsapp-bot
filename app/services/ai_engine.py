import openai
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.clinic import Clinic
from app.models.chat import ChatHistory, Message
from app.utils.prompt_builder import build_prompt
from app.services.vectorstore import query_vectorstore

# Configure OpenAI client
openai.api_key = settings.OPENAI_API_KEY

async def get_ai_response(session: AsyncSession, clinic_id: int, customer_phone: str, user_message: str) -> str:
    """
    Generates a response from the AI, augmented with context from the vector store (RAG).
    """
    # 1. Retrieve Clinic Info
    stmt = select(Clinic).where(Clinic.id == clinic_id).options(selectinload(Clinic.services))
    result = await session.execute(stmt)
    clinic = result.scalars().first()
    if not clinic:
        logger.error(f"Clinic with ID {clinic_id} not found.")
        return "I'm sorry, I can't access the clinic information right now."

    # 2. Retrieve Chat History
    history_stmt = select(ChatHistory).where(
        ChatHistory.clinic_id == clinic_id,
        ChatHistory.customer_phone == customer_phone
    ).options(selectinload(ChatHistory.messages))
    history_result = await session.execute(history_stmt)
    chat_history = history_result.scalars().first()
    
    messages = []
    if chat_history:
        # Get last 10 messages to keep context window small and relevant
        sorted_messages = sorted(chat_history.messages, key=lambda m: m.timestamp)
        for msg in sorted_messages[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

    # 3. Retrieve RAG Context from Vector Store
    rag_context = await query_vectorstore(clinic_id, user_message)

    # 4. Build the System Prompt
    system_prompt = build_prompt(clinic, rag_context)
    messages.insert(0, {"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    # 5. Call OpenAI API
    try:
        logger.info(f"Calling OpenAI for clinic {clinic_id} with model {settings.CHAT_MODEL}...")
        response = await openai.ChatCompletion.acreate(
            model=settings.CHAT_MODEL,
            messages=messages,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
        logger.info(f"OpenAI response for {customer_phone}: {ai_message[:100]}...")
        return ai_message
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."

async def get_streaming_chat_response(clinic_id: int, customer_phone: str, user_message: str):
    """
    Yields chunks of an AI response for streaming via SSE.
    """
    # This is a simplified version. A real implementation would need to manage history
    # and context similarly to the non-streaming version.
    system_prompt = "You are a helpful assistant." # Replace with a real prompt builder call
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    try:
        response_stream = await openai.ChatCompletion.acreate(
            model=settings.CHAT_MODEL,
            messages=messages,
            stream=True
        )
        async for chunk in response_stream:
            content = chunk.choices[0].delta.get("content", "")
            if content:
                yield content
    except Exception as e:
        logger.error(f"OpenAI streaming call failed: {e}")
        yield "Error: Could not get response."
