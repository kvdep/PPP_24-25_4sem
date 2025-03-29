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

from app.services.visualiser import *

router = APIRouter()

@router.get("/")
async def visualize(url: str = Query(..., description="URL сайта"), max_depth: int = None):
    return await visualize_graph(url, max_depth)