from fastapi import Query
from collections import deque
from urllib.parse import urljoin, urlparse
import redis
import json
import redis.asyncio as aioredis
import asyncio

from app.services_celery.scraping import get_links
from app.websocket.manager import manager



async def make_graph(
    url: str = Query(..., description="URL сайта для загрузки"),
    max_depth: int = None,
    user_id: str=None
):
    #redis_client = aioredis.Redis(host='redis', port=6379, db=0)
    redis_client = aioredis.Redis(host='redis', port=6379, db=0)
    graph = {}
    visited = set()  # Для отслеживания уже обработанных узлов
    cur_list = [url]
    cur_depth = 0

    while True:
        if user_id:
            '''
            await manager.send_message(user_id, {
                "status": "progress",
                "current_level": f'{cur_depth}/{max_depth}'
            })
            '''
            print(f'Graph builder got that user_id yo: {user_id}')
            #await redis_client.publish(
            await redis_client.publish(
                'celery_progress',
                json.dumps({
                    "status": "progress",
                    "current_level": f"{cur_depth}/{max_depth}",
                })
            )
            await asyncio.sleep(0)
            
        
        
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