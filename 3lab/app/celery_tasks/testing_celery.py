from app.celery_tasks.tasks import vis_graph_task_test

# Запуск задачи
task = vis_graph_task_test.delay("https://www.matcalc.ru/", max_depth=2)
print(task.id)  # Сохраните ID для проверки статуса

# Проверка результата
result = task.get(timeout=30)
print(result)