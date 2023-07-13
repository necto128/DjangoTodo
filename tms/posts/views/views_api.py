from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ..form.todo_form import TodoForm, TodoUpdateForm
from ..models import Todo


class Home(View):
    def get(self, request):
        data = Paginator(Todo.objects.select_related().filter(parent=None), 10).get_page(request.GET.get('page'))
        return JsonResponse({"todo": [model_to_dict(todo) for todo in data]})

    def post(self, request):
        todo = TodoForm(request.POST)
        if todo.is_valid():
            return JsonResponse({"todo_create": model_to_dict(todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': todo.errors})


class ShowTodo(View):
    def get(self, request, pk: Todo):
        return JsonResponse({"todo": model_to_dict(Todo.objects.get(id=pk))})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            return JsonResponse({'status': 200, "todo_update": model_to_dict(form_todo.save())})
        else:
            return HttpResponse({'status': 204, 'errors': form_todo.errors})


class TodoDelete(View):
    def delete(self, request, pk: Todo):
        try:
            Todo.objects.get(id=pk).delete()
        except Exception:
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200})
