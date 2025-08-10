# Bu dosya, WhatsApp ve sohbetle ilgili endpoint'leri yönetir.
# WhatsApp'tan gelen mesajları alma, doküman yükleme ve sohbet akışı gibi işlemler buradadır.

from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from loguru import logger  # Gelişmiş loglama için.
from sse_starlette.sse import EventSourceResponse  # Server-Sent Events (SSE) için.

from app.background.tasks import process_whatsapp_message, add_document_to_vectorstore  # Arka plan görevleri.
from app.schemas.chat import WhatsAppMessageIn, DocumentUpload  # Pydantic şemaları.
from app.services.ai_engine import get_streaming_chat_response  # Yapay zeka servisleri.
from app.models.user import User
from app.services.auth import current_active_user

router = APIRouter()

@router.post("/whatsapp/webhook", status_code=status.HTTP_202_ACCEPTED)
async def whatsapp_webhook(request: Request):
    """
    WhatsApp'tan (Twilio aracılığıyla) mesajları almak için webhook.
    İsteği doğrular, bir Pydantic modeline dönüştürür ve Celery ile arka planda işlenmek üzere sıraya alır.
    """
    try:
        # Gelen isteğin form verilerini al. Twilio bu formatta gönderir.
        form_data = await request.form()
        # Form verilerini Pydantic modelimizle doğrulamak için dönüştür.
        message_data = WhatsAppMessageIn(
            From=form_data.get("From"),  # Gönderenin numarası
            To=form_data.get("To"),      # Alıcının (kliniğin) numarası
            Body=form_data.get("Body")   # Mesajın içeriği
        )
        logger.info(f"Mesaj alındı: {message_data.From} -> {message_data.Body}")
        
        # Asıl işlemeyi (AI'ya sorma vb.) bir arka plan görevine devret.
        # .delay() metodu, görevi Celery kuyruğuna ekler.
        process_whatsapp_message.delay(message_data.model_dump())
        
        # Twilio'ya mesajın alındığını bildirmek için hemen yanıt ver.
        # Bu, webhook'un zaman aşımına uğramasını engeller.
        return {"status": "mesaj işlenmek üzere sıraya alındı"}
    except Exception as e:
        logger.error(f"Webhook işlenirken hata: {e}")
        raise HTTPException(status_code=400, detail="Geçersiz veya bozuk istek verisi")

@router.post("/documents/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    doc: DocumentUpload,
    user: User = Depends(current_active_user)
):
    """
    Klinik sahibinin bir doküman (örn. SSS) yüklemesini sağlar.
    Doküman içeriği, parçalara ayırma, gömme (embedding) ve vektör veritabanına
    kaydetme işlemleri için bir arka plan görevine gönderilir.
    """
    if not user.clinic:
        raise HTTPException(status_code=403, detail="Kullanıcının bir kliniği yok.")
    
    clinic_id = user.clinic.id
    # Görevi arka plan kuyruğuna ekle.
    add_document_to_vectorstore.delay(doc.content, doc.filename, clinic_id)
    
    return {"status": "Doküman yükleme başlatıldı. Arka planda işlenecektir."}

@router.get("/stream/{customer_phone}")
async def stream_chat(customer_phone: str, user_message: str, user: User = Depends(current_active_user)):
    """
    Server-Sent Events (SSE) endpoint'i. İstemcilerin (örn. bir web paneli)
    belirli bir müşteri için gerçek zamanlı yapay zeka yanıtları almasını sağlar.
    """
    if not user.clinic:
        raise HTTPException(status_code=403, detail="Kullanıcının bir kliniği yok.")

    # Yanıtı parça parça (stream) olarak döndüren EventSourceResponse'u kullan.
    return EventSourceResponse(get_streaming_chat_response(
        clinic_id=user.clinic.id,
        customer_phone=customer_phone,
        user_message=user_message
    ))
