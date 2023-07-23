from django.contrib.auth.models import User

from posts.models import Todo
from datetime import datetime
import logging
import os


def save_info_user():
    today, base_dir = datetime.now().date(), 'logs'
    log_dir = f"{base_dir}/{today}"
    for path_ in [base_dir, log_dir]:
        if not os.path.exists(path_):
            os.makedirs(path_)
    for user_obj in User.objects.all():
        task_completed = Todo.objects.filter(user=user_obj, completed=True, update_at__date=datetime.now().date())
        if len(task_completed):
            filename = f'{user_obj.id}_{user_obj.username}.log'
            filepath = os.path.join(log_dir, filename)
            logger, file_handler = logging.getLogger(f'completed_tasks_logger_{user_obj.id}'), logging.FileHandler(
                filepath, mode='a')
            logger.addHandler(file_handler)
            for task in task_completed:
                user_info = f"User Name: {task.user.username}, Name: {task.name}, Task ID: {task.id}, Updated At: {task.update_at}"
                logger.info(user_info)
            logger.removeHandler(file_handler)


class TodoApi:
    pass
