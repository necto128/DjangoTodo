from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import status

from posts.form.todo_form import TodoForm, TodoUpdateForm
from posts.models import Todo


class Home(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        data = Paginator(
            Todo.objects.prefetch_related("parent", "children").filter(parent__isnull=True), 10).get_page(
            request.GET.get('page'))
        return JsonResponse({"todo": [model_to_dict(todo) for todo in data]})

    def post(self, request) -> JsonResponse:
        todo = TodoForm(request.POST)
        if todo.is_valid():
            return JsonResponse({"todo_create": model_to_dict(todo.save())})
        else:
            return JsonResponse({'status': status.HTTP_204_NO_CONTENT, 'errors': todo.errors})


class ShowTodo(View):

    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            todo = Todo.objects.get(id=pk)
        except Exception:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={})
        return JsonResponse({"todo": model_to_dict(todo)})

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            todo = Todo.objects.get(id=pk)
        except Exception:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={})
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            return JsonResponse(status=status.HTTP_200_OK, data={"todo_update": model_to_dict(form_todo.save())})
        else:
            return JsonResponse(status=status.HTTP_204_NO_CONTENT, data={'errors': form_todo.errors})


class TodoDelete(View):

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            Todo.objects.get(id=pk).delete()
        except Exception:
            return JsonResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={})
        return JsonResponse(status=status.HTTP_200_OK, data={})
