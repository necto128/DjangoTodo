from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import permissions

from posts.form.todo_form import TodoForm, TodoUpdateForm
from posts.models import Todo


class Home(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request) -> HttpResponse:
        data = Paginator(
            Todo.objects.prefetch_related("parent", "children").filter(parent__isnull=True, user=request.user),
            10).get_page(request.GET.get('page'))
        return HttpResponse({"todo": [model_to_dict(todo) for todo in data]})

    def post(self, request) -> HttpResponse:
        todo = TodoForm(request.POST)
        if todo.is_valid():
            return HttpResponse({"todo_create": model_to_dict(todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': todo.errors})


class ShowTodo(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request, pk: int) -> HttpResponse:
        return HttpResponse({"todo": model_to_dict(Todo.objects.get(id=pk))})

    def post(self, request, pk: int) -> HttpResponse:
        todo = get_object_or_404(Todo, id=pk)
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            return HttpResponse({'status': 200, "todo_update": model_to_dict(form_todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': form_todo.errors})


class TodoDelete(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def delete(self, request, pk: int) -> HttpResponse:
        try:
            Todo.objects.get(id=pk, user=request.user).delete()
        except Exception:
            return HttpResponse({"status": 404})
        return HttpResponse({"status": 200})
