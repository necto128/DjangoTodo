import pytest
from django.contrib.auth.models import User
from django.test import Client
from freezegun import freeze_time

from posts.models import Todo


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_data():
    user_1 = User.objects.create_user(
        id=1,
        username="Petr",
        password="pass1",
        email="petr@mail.ru",
        is_active=True,
    )
    user_2 = User.objects.create_user(
        id=2,
        username="CristalMaiden",
        password="pass2",
        email="cristalMaiden@mail.ru",
        is_active=True,
    )
    todo_1 = Todo(
        user=user_1,
        name="Посмотреть уроки",
        message="остались ещё 3шт(30, 31)",
        deleted_at=None,
        update_at="2023-07-10T00:00:00Z",
    )
    todo_1.save()
    todo_2 = Todo(
        user=user_1,
        name="Магазин",
        message="Купить Хлеб",
        deleted_at=None,
        update_at="2023-07-10T00:00:00Z",
    )
    todo_2.save()
    todo_3 = Todo(
        user=user_2,
        name="Django",
        message="Создать модели",
        deleted_at=None,
        update_at="2023-07-10T00:00:00Z",
    )
    todo_3.save()
