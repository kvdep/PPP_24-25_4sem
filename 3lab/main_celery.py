from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core_celery.database_init import get_db

from app.api_celery.visualise import router as vis_router
from app.api_celery.graph import router as graph_router
from app.core_celery.database_endpoints import router as auth_router
from app.core_celery.database_init import init_db
from app.websocket.manager import WebSocketManager
from app.core.database_endpoints import get_current_user
from app.core.database_back import UserMeResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized")
    yield
    print("Application shutdown")

manager = WebSocketManager()
manager.listen_redis_task = asyncio.create_task(manager.listen_redis())
app = FastAPI(lifespan=lifespan)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    token: str = Query(...),
    #current_user: UserMeResponse = Depends(get_current_user)
):
        # manually resolve user
    try:
        db: AsyncSession = await anext(get_db())
        current_user = await get_current_user(token=token, db=db)
        print(f'User successfully authenticated')
    except Exception as e:
        await websocket.close(code=1008)
        print(f"Auth failed: {e}")
        return
    
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
    #        # Обработка входящих сообщений от клиента
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    
    #await asyncio.Future()  # <<< этот Future никогда не завершится
    #except WebSocketDisconnect:
    #    Клиент закрыл сокет – убираем его из менеджера
    #    manager.disconnect(user_id)

#self.websocket_task = asyncio.create_task(self._listen_websocket())
#asyncio.create_task(manager.listen_redis())  # Запуск в фоне

app.include_router(graph_router, prefix="/graph", tags=["Graph"])
app.include_router(vis_router, prefix="/vis", tags=["Visualise"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

def main():
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()