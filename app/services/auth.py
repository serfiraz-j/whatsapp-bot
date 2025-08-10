from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.config import settings
from app.database import get_user_db
from app.models.user import User

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    """Defines the JWT strategy for encoding/decoding tokens."""
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_db,
    [auth_backend],
)

# Dependency to get the current, active, authenticated user
current_active_user = fastapi_users.current_user(active=True)