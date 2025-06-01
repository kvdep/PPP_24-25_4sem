import httpx
import asyncio
import websockets
import json
from typing import Optional

from app.core_celery.database_back import UserMeResponse
#from app.websocket.manager import manager


class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.email: Optional[str] = None
        self.websocket_task = None


    async def sign_up(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/auth/sign-up/",
                json={"email": email, "password": password}
            )
            data = response.json()
            self.token = data["access_token"]
            self.user_id = data["id"]
            self.email = email

            return data


    async def login(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/auth/login/",
                data={"username": email, "password": password}
            )
            data = response.json()
            self.token = data["access_token"]
            self.user_id = data["id"]
            self.email = email
            

            self.websocket_task = asyncio.create_task(self._listen_websocket())

            #if not manager.listen_redis_task:
            #    manager.listen_redis_task = asyncio.create_task(manager.listen_redis())

            return data


    async def visualize_graph(self, url: str, max_depth: int = 2):
        if not self.token:
            raise Exception("Not authenticated")
        #http://127.0.0.1:8001/vis/?url=https%3A%2F%2Fwarhammer40k.fandom.com%2Fwiki%2FWarhammer_40k_Wiki&max_depth=2
        '''
        async def visualize(
            url: str,
            max_depth: int = None,
            current_user: UserMeResponse = Depends(get_current_user)
        ):'''
        #{'detail': [{'type': 'missing', 'loc': ['query', 'url'], 'msg': 'Field required', 'input': None}]}



        async with httpx.AsyncClient() as client:
            #user = UserMeResponse(id = self.user_id, email = self.email)
            response = await client.post(
                f"{self.base_url}/vis/",
                #json={"url": url, "max_depth": max_depth, "current_user" : user},
                #json={"url": url, "max_depth": max_depth, "id": self.user_id, "email": self.email},
                
                params={"url": url, "max_depth": max_depth},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()


    async def _listen_websocket(self):
        """Постоянное прослушивание WebSocket в фоне"""
        while True:
            try:
                print(f'Websocket is now listening for the server responses')
                async with websockets.connect(
                    f"ws://localhost:8001/ws/{self.user_id}?token={self.token}",
                    ping_interval=None
                ) as websocket:
                    while True:
                        message = await websocket.recv()
                        print(f'I got a message {message}')
                        print("\nWebSocket update:", json.loads(message))
            except Exception as e:
                print(f"WebSocket error: {e}, reconnecting...")
                await asyncio.sleep(2)




async def main():
    client = APIClient()
    
    while True:
        print("\n1. Sign up\n2. Login\n3. Visualize graph\n4. Exit")
        choice = input("Choose option: ")
        
        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            print(await client.sign_up(email, password))
            
        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            print(await client.login(email, password))
            
        elif choice == "3":
            url = input("URL: ")
            depth = input("Depth (default 2): ") or "2"
            print(await client.visualize_graph(url, int(depth)))
            
        elif choice == "4":
            break

if __name__ == "__main__":
    asyncio.run(main())