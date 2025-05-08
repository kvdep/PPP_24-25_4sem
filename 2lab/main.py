from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.visualise import router as vis_router
from app.api.graph import router as graph_router
from app.core.database_endpoints import router as auth_router
from app.core.database_init import init_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код выполняется при запуске приложения
    await init_db()
    print("Database initialized")
    yield
    # Код выполняется при остановке приложения (опционально)
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)
#app.include_router(scrape_router, prefix="/scrape", tags=["Scraping"])
app.include_router(graph_router, prefix="/graph", tags=["Graph"])
app.include_router(vis_router, prefix="/vis", tags=["Visualise"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

def main():
    uvicorn.run(app, host="0.0.0.0", port=8001)
    pass

if __name__ == "__main__":
    main()

