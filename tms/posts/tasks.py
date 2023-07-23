from posts.service.todos_api import save_info_user
from tms.celery import app


@app.task
def todo_for_day(*args, **kwargs):
    save_info_user()
