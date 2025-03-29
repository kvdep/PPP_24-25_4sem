from fastapi import FastAPI
from fastapi import Query
import httpx
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pyvis.network import Network
from fastapi.responses import HTMLResponse
from collections import deque

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


@app.get("/vis", response_class=HTMLResponse)
async def visualize_graph(
    url: str = Query(..., description="URL сайта для загрузки"),
    max_depth: int = Query(None, description="Максимальная глубина обхода")
):
    visited = set()
    queue = deque([(url, 0)])
    graph = {}
    titles = {}
    '''
    # Собираем данные графа
    while queue:
        current_url, depth = queue.popleft()
        
        if current_url in visited:
            continue
        if max_depth is not None and depth > max_depth:
            continue
        
        response = await download_site(current_url)
        if not response:
            continue
            
        visited.add(current_url)
        html = response.text
        base_url = str(response.url)
        
        titles[current_url] = get_title(html)
        links = get_links(html, base_url)
        graph[current_url] = links
        
        # Добавляем ссылки в очередь
        for link in links:
            if link not in visited:
                queue.append((link, depth + 1))
    '''
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
    '''
    # Добавляем узлы
    for node in graph_data:
        # Учитываем измененный формат узлов в make_graph ([title, url])
        if isinstance(node, list) and len(node) == 2:
            title, url = node
            net.add_node(url, label=title, title=url)
        else:
            net.add_node(node, label=node, title=node)
    
    # Добавляем связи
    for source, targets in graph_data.items():
        source_url = source[1] if isinstance(source, list) else source
        for target in targets:
            # Проверяем, есть ли target в графе как узел
            target_in_graph = any(
                (isinstance(n, list) and n[1] == target) or n == target 
                for n in graph_data.keys()
            )
            if target_in_graph:
                net.add_edge(source_url, target)'
    '''
    #graph.update({[title,i]:nodes})
    print(graph)
    for i in graph_data:
        net.add_node(i[1], label=i[0], title=i[1])

    for [title, source_url], target_urls in graph_data.items():
        for target_url in target_urls:
            net.add_edge(source_url, target_url)


    # Генерируем HTML
    html = net.generate_html()
    return HTMLResponse(content=html)
    

    
