from fastapi import FastAPI
from fastapi import Query
import httpx
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = FastAPI()

@app.get("/download")
async def download_site(url: str = Query(..., description="URL сайта для загрузки")):
    print(url)
    try:
        async with httpx.AsyncClient() as client:
            answer = await client.get(url)
            return answer.text
    except:
        print('HTTP could not be loaded.');return None



def get_links(html):
    if not(html):
        print('File is empty.');return None
    
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    for i in soup.find_all('a', href=True):
        cur = i['href']
        if cur.startswith('#') or cur.strip() == '':
            continue
        links.append(cur)
    return links

def get_title(html, graph):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        return title.text.strip()
    else:
        i = 0
        while True:
            try:
                graph[f'Page{i}']
            except:
                return f'Page{i}'
            i+=1
    

@app.get("/graph")
async def make_graph(url: str = Query(..., description="URL сайта для загрузки"), max_depth = None):
    html = await download_site(url)
    graph = {}
    cur_list = get_links(html)
    try:
        graph.update({get_title(html,graph):cur_list})
    except:
        print(f'Couldnt open the html. Closing.');return
    cur_depth = 0

    next_list = set()
    while True:
        print(cur_list)
        for i in cur_list:
            #Добавим вершину в граф
            try:
                html = await download_site(i)
                title = get_title(html,graph)
                #Одинаковые не нужны
                if [title,i] in graph.keys():
                    continue
                nodes = get_links(html)
                graph.update({[title,i]:nodes})
                #Следующие ноды 
                for j in nodes:
                    next_list.add(j)
            except:
                continue

        #Проверим текущую глубину (если задана)
        if max_depth and cur_depth == max_depth:
            break

        if not(next_list):
            break
        cur_list = list(next_list)
        next_list = set()

    return graph




    

    
