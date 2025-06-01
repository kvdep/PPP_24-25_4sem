import json
import redis
import redis.asyncio as aioredis
import asyncio
from app.websocket import manager

from app.celery_tasks.worker import celery
from app.services_celery.graph_builder import make_graph
from app.services_celery.visualiser import visualize_graph

#from app.websocket.manager import manager

#redis_client = redis.Redis(host='redis', port=6379, db=0)
redis_client = redis.Redis(host='redis', port=6379, db=0)


'''
def send_progress(redis_client,user_id: str,  progress: int, message: str):
    data = {
        "user_id": user_id,
        "status": "PROGRESS",
        "progress": progress,
        "message": message
    }
    #redis_client.publish("celery_progress", json.dumps(data))
    try:
        #redis_client.publish("celery_progress", json.dumps(data))
        print(f'Subscriber count 1:{redis_client.publish("celery_progress", json.dumps(data))}')
        print(f'I sent it like this{json.dumps(data)}')
    except Exception as e:
        print(f'REDIS IS NOT SEEING THIS.')
        print(e)
'''


@celery.task(name="vis_graph_task",bind=True)
async def vis_graph_task_test(url: str, max_depth: int = None):
    result = await visualize_graph(url, max_depth)
    return result.body.decode()  # Возвращаем HTML


@celery.task(bind=True)
def build_graph_task(self, url: str, max_depth: int, user_id: str = None):
    print(url)
    
    #redis_client = redis.Redis(host='redis', port=6379, db=0)
    #redis_client = manager.redis
    
    try:
        '''
        if user_id:
            manager.send_message(user_id, {"status": "started"})
        
        result = visualize_graph(url, max_depth, user_id)
        
        if user_id:
            manager.send_message(user_id, {
                "status": "completed",
                "result": result
            })
        
        return result
        '''
        '''
        redis_client.publish(
                f"user_{user_id}",
                json.dumps({
                    "status": "progress",
                    "current_level": f"{cur_depth}/{max_depth}",
                })
        '''
        '''
        redis_client.publish(f"user_{user_id}",
            json.dumps({
                "status": "started"
            })
        )
        result = visualize_graph(url, max_depth, user_id)
        if user_id:
            redis_client.publish(f"user_{user_id}", {
                "status": "completed",
                "result": result
            })
        '''
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop.run_until_complete(send_progress(user_id=user_id, progress=0, message="Starting graph visualization"))
        #send_progress(redis_client,user_id=user_id, progress=0, message="Starting graph visualization")
        #result = visualize_graph(url, max_depth, user_id)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            visualize_graph(url, max_depth, user_id)
        )
        result = result.body.decode()
        '''
        redis_client.publish(
                'celery_progress',
                json.dumps({'result':result})
            )
        '''
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop.run_until_complete(send_progress(user_id=user_id, progress=100, message="Graph visualization completed"))
        #send_progress(redis_client,user_id=user_id, progress=100, message="Graph visualization completed")
        #return result
        return 
    except Exception as e:
        if user_id:
            '''
            manager.send_message(user_id, {
                "status": "failed",
                "error": str(e)
            })
            '''
            '''redis_client.publish(f"user_{user_id}", {
                "status": "failed",
                "error": str(e)
            })'''
            #loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(loop)
            #loop.run_until_complete(send_progress(user_id=user_id, progress=-1, message="aborted!"))
            #send_progress(redis_client,user_id=user_id, progress=-1, message="aborted!")
            print(f'Fatal error celery! {e}')
        raise