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

from app.services_celery.scraping import *

async def make_graph(url: str = Query(..., description="URL сайта для загрузки"), max_depth = None):
    #html = await download_site(url)
    graph = {}
    cur_list = await get_links(url)
    #print(cur_list)
    try:
        graph.update({url:cur_list})
    except:
        print(f'Couldnt open the html. Closing.');return
    cur_depth = 0
    #print(graph)
    next_list = set()
    while True:
        print(cur_list)
        for i in cur_list:
            print(i)
            #Добавим вершину в граф
            try:
                #html = await download_site(i)
                #title = get_title(html,graph)
                #Одинаковые не нужны
                nodes = await get_links(i)
                graph.update({i:nodes})
                #Следующие ноды 
                for j in nodes:
                    if not(j in graph.keys()):
                        next_list.add(j)
            except:
                try:
                    graph[i]
                except:
                    graph.update({i:None})
                continue

        #Проверим текущую глубину (если задана)
        if max_depth and cur_depth == max_depth:
            break

        if not(next_list):
            break
        cur_list = list(next_list)
        next_list = set()
        cur_depth+=1
        print(f'\n\n\nCurrent depth: {cur_depth}\n\n\n')
        
    #print(graph)
    return graph