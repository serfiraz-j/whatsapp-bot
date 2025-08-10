# Bu dosya, kullanıcı kimlik doğrulama (authentication) ile ilgili tüm API endpoint'lerini yönetir.
# Kayıt olma, giriş yapma, parola sıfırlama gibi işlemler burada tanımlanır.

from fastapi import APIRouter  # API endpoint'lerini gruplamak için kullanılan FastAPI sınıfı.
from app.models.user import User  # Veritabanındaki 'User' modelimiz.
from app.schemas.user import UserCreate, UserRead  # Kullanıcı verilerini doğrulamak ve formatlamak için Pydantic şemaları.
from app.services.auth import auth_backend, fastapi_users  # Kimlik doğrulama mantığını içeren servisler.

# Yeni bir router nesnesi oluşturuyoruz. Bu, ilgili endpoint'leri gruplamamızı sağlar.
router = APIRouter()

# JWT (JSON Web Token) ile giriş/çıkış işlemleri için endpoint'leri ekliyoruz.
# Örneğin, /auth/jwt/login ve /auth/jwt/logout yolları burada oluşturulur.
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",  # Bu gruptaki tüm yolların başına '/jwt' eklenir.
)

# Yeni kullanıcı kaydı için endpoint'i ekliyoruz.
# /auth/register yolunu oluşturur.
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
)

# Parola sıfırlama işlemleri için endpoint'leri ekliyoruz.
# /auth/forgot-password yolunu oluşturur.
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/forgot-password",
)

# Kullanıcı yönetimi (kullanıcı bilgilerini alma, güncelleme vb.) için endpoint'leri ekliyoruz.
# /auth/users/me, /auth/users/{id} gibi yolları oluşturur.
router.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix="/users",
)