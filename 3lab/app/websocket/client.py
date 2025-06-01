import httpx
import asyncio
import websockets
import json
from typing import Optional
from app.core_celery.database_back import UserMeResponse

class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.email: Optional[str] = None
        self.websocket_task = None

    async def sign_up(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/auth/sign-up/",
                json={"email": email, "password": password}
            )
            data = resp.json()
            self.token = data["access_token"]
            self.user_id = data["id"]
            self.email = email
            return data

    async def login(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/auth/login/",
                data={"username": email, "password": password}
            )
            data = resp.json()
            self.token = data["access_token"]
            self.user_id = data["id"]
            self.email = email

            # Запускаем таск слушать WebSocket БЕЗ input()
            self.websocket_task = asyncio.create_task(self._listen_websocket())
            return data

    async def visualize_graph(self, url: str, max_depth: int = 2):
        if not self.token:
            raise Exception("Not authenticated")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/vis/",
                params={"url": url, "max_depth": max_depth},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return resp.json()

    async def _listen_websocket(self):
        """Постоянное прослушивание WebSocket в фоне."""
        while True:
            try:
                print("Websocket is now listening for server responses")
                async with websockets.connect(
                    f"ws://localhost:8001/ws/{self.user_id}?token={self.token}",
                    ping_interval=None
                ) as ws:
                    while True:
                        message = await ws.recv()
                        print(f"I got a message: {message}")
                        print("WebSocket update:", json.loads(message))
            except Exception as e:
                print(f"WebSocket error: {e}, reconnecting...")
                await asyncio.sleep(2)

async def async_input(prompt: str = "") -> str:
    """Запускаем встроенный input() в отдельном потоке."""
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

async def main():
    client = APIClient()

    while True:
        print("\n1. Sign up\n2. Login\n3. Visualize graph\n4. Exit")
        choice = await async_input("Choose option: ")

        if choice == "1":
            email = await async_input("Email: ")
            password = await async_input("Password: ")
            print(await client.sign_up(email, password))

        elif choice == "2":
            email = await async_input("Email: ")
            password = await async_input("Password: ")
            print(await client.login(email, password))

        elif choice == "3":
            url = await async_input("URL: ")
            depth = await async_input("Depth (default 2): ") or "2"
            print(await client.visualize_graph(url, int(depth)))

        elif choice == "4":
            break

if __name__ == "__main__":
    asyncio.run(main())
