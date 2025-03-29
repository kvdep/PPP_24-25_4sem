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

from app.services.scraping import *
from app.services.graph_builder import *

async def visualize_graph(
    url: str = Query(..., description="URL сайта для загрузки"),
    max_depth: int = Query(None, description="Максимальная глубина обхода")
):
    visited = set()
    queue = deque([(url, 0)])
    graph = {}
    titles = {}
    
    graph_data = await make_graph(url, max_depth)
    
    if not graph_data:
        return HTMLResponse(content="<h1>Error: Could not generate graph data</h1>")
    # Создаем визуализацию
    net = Network(
        height="600px",
        width="100%",
        notebook=True,
        cdn_resources="remote",
        select_menu=True
    )
    #graph.update({[title,i]:nodes})
    print(graph)
    for i in graph_data:
        net.add_node(i, label=await get_title(i), title=i)

    for i in graph_data:
        if graph_data[i]:
            for j in graph_data[i]:
                print(i,j)
                try:
                    net.add_edge(i, j)
                except AssertionError:
                    net.add_node(j,label=await get_title(j), title=j)
                    net.add_edge(i, j)


    # Генерируем HTML
    html = net.generate_html()
    return HTMLResponse(content=html)
    