from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_async_session
from app.models.user import User
from app.models.chat import ChatHistory
from app.services.auth import current_active_user
from app.schemas.chat import ChatHistoryWithMessages # You would need to create this schema

router = APIRouter()

# Dependency for checking if the user is a superuser
async def get_current_active_superuser(user: User = Depends(current_active_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user

@router.get("/chat_history/{clinic_id}", response_model=List[ChatHistoryWithMessages])
async def get_chat_history_for_clinic(
    clinic_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_superuser), # Protect this endpoint
):
    """
    Admin endpoint to view all chat histories for a specific clinic.
    Only accessible by superusers.
    """
    stmt = select(ChatHistory).where(ChatHistory.clinic_id == clinic_id).options(
        selectinload(ChatHistory.messages)
    )
    result = await session.execute(stmt)
    histories = result.scalars().all()
    
    if not histories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chat history found for clinic ID {clinic_id}",
        )
        
    return histories