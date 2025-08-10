from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Core Settings ---
    SECRET_KEY: str
    
    # --- Database Settings ---
    DATABASE_URL: str
    
    # --- Redis Settings ---
    REDIS_URL: str

    # --- AI & Vector Store Settings ---
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4-turbo"

    # --- WhatsApp Provider Settings (Twilio) ---
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
