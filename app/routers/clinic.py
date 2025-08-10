# Bu dosya, klinikler ve onlara ait servislerle ilgili API endpoint'lerini yönetir.
# Klinikleri oluşturma, getirme, güncelleme ve servislere ekleme işlemleri buradadır.

from fastapi import APIRouter, Depends, HTTPException, status  # Gerekli FastAPI bileşenleri.
from sqlalchemy.ext.asyncio import AsyncSession  # Asenkron veritabanı oturumları için.
from sqlalchemy.future import select  # Modern SQLAlchemy sorguları için.
from sqlalchemy.orm import selectinload  # İlişkili verileri (örn. servisler) verimli bir şekilde yüklemek için.
from typing import List  # Tip ipuçları için (örn. bir liste döneceğini belirtmek).

from app.database import get_async_session  # Veritabanı oturumu almak için dependency.
from app.models.clinic import Clinic, Service  # Veritabanı modelleri.
from app.models.user import User  # User modeli.
from app.schemas.clinic import ClinicCreate, Clinic as ClinicSchema, ServiceCreate, Service as ServiceSchema  # Pydantic şemaları.
from app.services.auth import current_active_user  # Aktif ve kimliği doğrulanmış kullanıcıyı getiren dependency.

# Yeni bir router nesnesi oluşturuyoruz.
router = APIRouter()

@router.post("/", response_model=ClinicSchema, status_code=status.HTTP_201_CREATED)
async def create_clinic(
    clinic_data: ClinicCreate,  # İstek gövdesinden gelen ve ClinicCreate şemasıyla doğrulanan klinik verileri.
    session: AsyncSession = Depends(get_async_session),  # Veritabanı oturumu.
    user: User = Depends(current_active_user),  # O anki aktif kullanıcı.
):
    """
    Kimliği doğrulanmış kullanıcı için yeni bir klinik oluşturur.
    Bir kullanıcının sadece bir kliniği olabilir.
    """
    # Eğer kullanıcının zaten bir kliniği varsa, hata döndür.
    if user.clinic:
        raise HTTPException(status_code=400, detail="Kullanıcının zaten bir kliniği var.")
    
    # Yeni bir Clinic nesnesi oluştur ve verileri ata. owner_id'yi mevcut kullanıcıdan al.
    db_clinic = Clinic(**clinic_data.model_dump(), owner_id=user.id)
    session.add(db_clinic)  # Yeni kliniği veritabanı oturumuna ekle.
    await session.commit()  # Değişiklikleri veritabanına kaydet.
    await session.refresh(db_clinic)  # Veritabanından güncel verileri (örn. ID) çek.
    return db_clinic  # Oluşturulan kliniği döndür.

@router.get("/", response_model=ClinicSchema)
async def get_my_clinic(
    user: User = Depends(current_active_user),  # Aktif kullanıcıyı al.
):
    """
    Kimliği doğrulanmış kullanıcının sahip olduğu kliniğin detaylarını getirir.
    """
    # Eğer kullanıcının bir kliniği yoksa, 404 Not Found hatası döndür.
    if not user.clinic:
        raise HTTPException(status_code=404, detail="Bu kullanıcı için klinik bulunamadı.")
    
    # fastapi_users'dan gelen user nesnesi, doğru yapılandırıldıysa,
    # 'clinic' ilişkisini zaten yüklenmiş olarak içermelidir.
    return user.clinic

@router.put("/", response_model=ClinicSchema)
async def update_clinic(
    clinic_data: ClinicCreate,  # Güncelleme için de Create şemasını kullanıyoruz.
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    Kullanıcının kliniğinin detaylarını günceller.
    """
    clinic = user.clinic  # Kullanıcının kliniğini al.
    if not clinic:
        raise HTTPException(status_code=404, detail="Klinik bulunamadı.")

    # Gelen verilerdeki her bir anahtar-değer çifti için...
    for key, value in clinic_data.model_dump(exclude_unset=True).items():
        # ...klinik nesnesinin ilgili özelliğini güncelle.
        setattr(clinic, key, value)
    
    session.add(clinic)  # Güncellenmiş nesneyi oturuma ekle.
    await session.commit()  # Değişiklikleri kaydet.
    await session.refresh(clinic)  # Güncel veriyi çek.
    return clinic

@router.post("/services", response_model=ServiceSchema, status_code=status.HTTP_201_CREATED)
async def add_service_to_clinic(
    service_data: ServiceCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    Kullanıcının kliniğine yeni bir servis ekler.
    """
    if not user.clinic:
        raise HTTPException(status_code=404, detail="Servis eklemek için kullanıcının bir kliniği olmalı.")
    
    # Yeni bir Service nesnesi oluştur ve clinic_id'yi kullanıcının kliniğinden al.
    db_service = Service(**service_data.model_dump(), clinic_id=user.clinic.id)
    session.add(db_service)
    await session.commit()
    await session.refresh(db_service)
    return db_service

@router.get("/services", response_model=List[ServiceSchema])
async def list_services(user: User = Depends(current_active_user)):
    """
    Kullanıcının kliniği için tüm servisleri listeler.
    """
    if not user.clinic:
        raise HTTPException(status_code=404, detail="Klinik bulunamadı.")
    return user.clinic.services

# ---------------------------------------------------------------------------
