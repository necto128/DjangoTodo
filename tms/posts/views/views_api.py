from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import permissions

from ..form.todo_form import TodoForm, TodoUpdateForm
from ..models import Todo


class Home(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request):
        data = Paginator(
            Todo.objects.prefetch_related("parent", "children").filter(parent__isnull=True, user=request.user,
                                                                       is_delete=False),
            10).get_page(request.GET.get('page'))
        return JsonResponse({"todo": [model_to_dict(todo) for todo in data]})

    def post(self, request):
        todo = TodoForm(request.POST)
        if todo.is_valid():
            return JsonResponse({"todo_create": model_to_dict(todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': todo.errors})


class ShowTodo(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request, pk: Todo):
        return JsonResponse({"todo": model_to_dict(Todo.objects.get(id=pk, is_delete=True))})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, id=pk, is_delete=True)
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            return JsonResponse({'status': 200, "todo_update": model_to_dict(form_todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': form_todo.errors})


class TodoDelete(View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def delete(self, request, pk: Todo):
        try:
            todo = Todo.objects.get(id=pk, user=request.user)
            todo.is_delete = True
            todo.save()
        except Exception:
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200})
