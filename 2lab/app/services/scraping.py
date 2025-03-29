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


async def download_site(url: str = Query(..., description="URL сайта для загрузки")):
    #print(url)
    try:
        async with httpx.AsyncClient() as client:
            answer = await client.get(url)
            return answer.text
    except:
        print('HTTP could not be loaded.');return None



async def get_links(url):
    html = await download_site(url)
    if not(html):
        print('File is empty.');return None
    
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    for i in soup.find_all('a', href=True):
        cur = i['href']
        if cur.startswith('#') or cur.strip() == '':
            continue
        if urlparse(cur).netloc:  # Проверяем, есть ли в ссылке домен (значит, это абсолютный URL)
            links.append(cur)
        else:
            links.append(urljoin(url, cur))  # Преобразуем относительную ссылку в абсолютную

        #links.append(cur)
    return links

async def get_title(url):
    html = await download_site(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        if title:
            return title.text.strip()
        else:
            i = 0
            while True:
                return url
                #try:
                #    graph[f'Page{i}']
                #except:
                #    return f'Page{i}'
                #i+=1
    else:
        print(f'No HTML.');return