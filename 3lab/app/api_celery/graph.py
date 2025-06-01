from fastapi import FastAPI
from fastapi import Query
import httpx
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pyvis.network import Network
from fastapi.responses import HTMLResponse
from collections import deque
from urllib.parse import urljoin, urlparse
from fastapi import APIRouter, Query
from fastapi import Depends

from app.core.database_endpoints import get_current_user
from app.core.database_back import UserMeResponse
from app.services.graph_builder import *


router = APIRouter()

@router.get("/")
async def build_graph(
    url: str = Query(..., description="URL сайта"),
    max_depth: int = None,
    current_user: UserMeResponse = Depends(get_current_user)  # <-- Добавляем зависимость
):
    return await make_graph(url, max_depth)