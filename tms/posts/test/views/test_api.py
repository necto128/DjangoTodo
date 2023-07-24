import pytest
from django.contrib.auth.models import User
from freezegun import freeze_time

from posts.models import Todo
from posts.test.test_app import test_data


@pytest.mark.django_db
def test_get_todos_home(client, test_data):
    response = client.get("/api/home")
    assert response.status_code == 200
    assert not (len(response.json()['todo']) == 0)
    assert response.json()['todo'][0]['name'] == "Посмотреть уроки"


@pytest.mark.django_db
@freeze_time("2023-07-13 00:00:00")  # Не работает freezetime в таблице поменял на datetime.now
def test_create_todo_valid_data_home(client, test_data):
    response = client.post("/api/create", data={
        'id': 4,
        'user': 2,
        'name': "Зайти в магазин",
        'message': "купить молоко, хлеб, колбасу"
    })
    assert response.status_code == 200
    assert Todo.objects.get(id=4) is not None
    assert response.json()['todo_create'] == {'completed': False,
                                              'id': 7,
                                              'message': 'купить молоко, хлеб, колбасу',
                                              'name': 'Зайти в магазин',
                                              'parent': None,
                                              'update_at': '"2023-07-13 00:00:00"',
                                              'user': 2,
                                              }


@pytest.mark.django_db
def test_create_todo_invalid_data_home(client, test_data):
    response = client.post("/api/home", data={
        'user': 4,
        'name2': "Зайти в магазин",
        'message': "купить молоко, хлеб, колбасу"
    })
    assert response.json()['status'] == 204
    assert response.json()['errors'] == {
        'user': ['Select a valid choice. That choice is not one of the available choices.'],
        'name': ['This field is required.']
    }


@pytest.mark.django_db
def test_get_full_view_todo_and_valid_pk_show_todo(client, test_data):
    response = client.get("/api/posts/11")  # Индекс 11
    assert response.status_code == 200
    assert response.json()['todo']['user'] == 1
    assert response.json()['todo']['id'] == 11  # Индекс 11


@pytest.mark.django_db
def test_get_full_view_todo_and_invalid_pk_show_todo(client, test_data):
    response = client.get("/api/posts/199999999")
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_todo_valid_data_show_todo(client, test_data):
    response = client.post("/api/posts/17", data={  # Индекс 17
        'message': "остались ещё 3шт(30, 31, 32)"
    })
    assert response.status_code == 200
    assert response.json()['todo_update'] == {
        'user': 1,
        'completed': False,
        'id': 17,  # Индекс 17
        'message': 'остались ещё 3шт(30, 31, 32)',
        'name': 'Посмотреть уроки',
        'parent': None,
        'update_at': '2023-07-10T00:00:00Z'
    }


@pytest.mark.django_db
def test_update_todo_invalid_pk_show_todo(client, test_data):
    response = client.post("/api/posts/1123", data={
        'message': "остались ещё 3шт(30, 31, 32)"
    })
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_todo_valid_data_tododelete(client, test_data):
    response = client.post("/api/posts/3/delete")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_todo_valid_data_tododelete(client, test_data):
    response = client.post("/api/posts/99199/delete")
    assert response.status_code == 405
