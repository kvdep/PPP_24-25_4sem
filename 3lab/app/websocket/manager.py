from fastapi import WebSocket
from typing import Dict
import redis
import json
import asyncio
import redis.asyncio as aioredis

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.redis = aioredis.Redis(host='redis', port=6379, db=0)
        #self.listen_redis_task = asyncio.create_task(self.listen_redis())
        self.listen_redis_task = None



    async def connect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            await self.active_connections[user_id].close()
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f'user_list: {self.active_connections.items()}')
        if not self.listen_redis_task:
            self.listen_redis_task = asyncio.create_task(self.listen_redis())
        await self.redis.publish("celery_progress", json.dumps({
        "user_id": user_id,
        "type": "test",
        "message": "Redis test message"
    }))

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def listen_redis(self):
        print(f'Manager listening to redis rn')
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("celery_progress")  # Общий канал для всех задач
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
            print(f'damn a message! {message}')
            print(f'user_list: {self.active_connections.items()}')
            if message:
                #data = json.loads(message["data"])
                for user_id in self.active_connections:
                    print(f'user got it. {user_id}')
                    payload = json.loads(message["data"])
                    await self.send_message(user_id, payload)
            await asyncio.sleep(0.01)

'''
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.redis = redis.Redis(host='redis', port=6379, db=0)
        #self.listen_redis_task = asyncio.create_task(self.listen_redis())
        self.listen_redis_task = None



    def connect(self, user_id: str, websocket: WebSocket):
        websocket.accept()
        if user_id in self.active_connections:
            self.active_connections[user_id].close()
        self.active_connections[user_id] = websocket
        if not self.listen_redis_task:
            self.listen_redis_task = asyncio.create_task(self.listen_redis())
        self.redis.publish("celery_progress", json.dumps({
        "user_id": user_id,
        "type": "test",
        "message": "Redis test message"
    }))

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def listen_redis(self):
        print(f'Manager listening to redis rn')
        pubsub = self.redis.pubsub()
        pubsub.subscribe("celery_progress")  # Общий канал для всех задач
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            print(f'damn a message! {message}')
            if message:
                data = json.loads(message["data"])
                for user_id in self.active_connections:
                    print(f'user got it. {user_id}')
                    await self.send_message(user_id, data)
            await asyncio.sleep(0.01)
   
'''


manager = WebSocketManager()  