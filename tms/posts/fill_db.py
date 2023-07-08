import random

import requests
from django.conf import settings
from django.contrib.auth.models import User

from .models import Todo
from .utils import build_generator, generate_text

response = requests.get(settings.TODOS_URL)


class ServicesTodo:
    @staticmethod
    def generate_record():
        users = [
            User.objects.create_user(
                username="Petr",
                password="pass1",
                email="petr@mail.ru",
                is_active=True
            ),
            User.objects.create_user(
                username="CristalMaiden",
                password="pass2",
                email="cristalMaiden@mail.ru",
                is_active=True
            ),
            User.objects.create_user(
                username="Bain",
                password="pass3",
                email="bain@mail.ru",
                is_active=True
            ),
            User.objects.create_user(
                username="Arc_Warden",
                password="pass10",
                email="arc_warden@mail.ru",
                is_active=True
            ),
            User.objects.create_user(
                username="Bein",
                password="pass7",
                email="bein@mail.ru",
                is_active=True
            ),
            User.objects.create_user(
                username="Lina",
                password="pass8",
                email="lina@mail.ru",
                is_active=True
            )
        ]
        generator = build_generator()
        for user_obj in users:
            for i in range(10):
                todos = Todo.objects.create(
                    user=user_obj,
                    name=generate_text(generator, random.randint(1, 5)),
                    message=generate_text(generator, random.randint(1, 20)),
                    completed=random.choice([0, 1]),
                )
                counter = 1
                while counter:
                    counter = random.choice([0, 1])
                    if counter:
                        Todo.objects.create(
                            user=user_obj,
                            name=generate_text(generator, random.randint(1, 5)),
                            message=generate_text(generator, random.randint(1, 20)),
                            completed=random.choice([0, 1]),
                            parent=todos
                        )
