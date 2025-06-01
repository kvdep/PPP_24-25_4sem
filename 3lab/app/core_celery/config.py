
class Settings():
    # Настройки базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    
    # Настройки Celery
    #CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    #CELERY_BROKER_URL=redis://redis:6379/0


    # JWT
    SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    ALGORITHM: str = "HS256"


settings = Settings()


