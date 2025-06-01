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

app = FastAPI()

@app.get("/download")
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
        
    

@app.get("/graph")
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


@app.get("/vis", response_class=HTMLResponse)
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
    

    
#out = await visualize_graph("https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html", 3)
#print(out)
