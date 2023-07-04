from django.conf import settings
from django.contrib.auth.models import User
import requests

from .models import Todo

response = requests.get(settings.TODOS_URL)


class ServicesTodo:
    @staticmethod
    def generate_record():
        user_data = {
            "user1": "pass1",
            "user2": "pass2",
            "user3": "pass3",
            "user4": "pass4",
            "user5": "pass5",
            "user6": "pass6",
            "user7": "pass7",
            "user8": "pass8",
            "user9": "pass9",
            "user10": "pass10"
        }
        for k, v in user_data.items():
            User(username=k, password=v).save()
        if not Todo.objects.count():
            for i in response.json():
                Todo(user=User.objects.filter(id=i["userId"])[0], message=i["title"],
                     completed=i["completed"]).save()
