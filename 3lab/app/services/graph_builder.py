from fastapi import Query
from collections import deque
from urllib.parse import urljoin, urlparse

from app.services.scraping import get_links

async def make_graph(
    url: str = Query(..., description="URL сайта для загрузки"),
    max_depth: int = None
):
    graph = {}
    visited = set()  # Для отслеживания уже обработанных узлов
    cur_list = [url]
    cur_depth = 0

    while True:
        # Проверяем, достигли ли максимальной глубины
        if max_depth is not None and cur_depth >= max_depth:
            break
        next_list = set()
        for current_url in cur_list:
            if current_url in visited:
                continue
            visited.add(current_url)
            try:
                # Получаем ссылки с текущей страницы
                links = await get_links(current_url)
                graph[current_url] = links
                # Добавляем найденные ссылки в next_list, если они еще не обработаны
                for link in links:
                    if link not in visited and link not in graph:
                        next_list.add(link)
            except Exception as e:
                print(f"Error processing {current_url}: {e}")
                graph[current_url] = None


        # Если нет новых ссылок для обработки, выходим
        if not next_list:
            break

        # Переходим к следующему уровню
        cur_list = list(next_list)
        cur_depth += 1
        print(f'Current depth: {cur_depth}')

    return graph