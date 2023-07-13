from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from ..form.todo_form import TodoForm, TodoUpdateForm
from ..models import Todo


class Home(View):
    def get(self, request):
        data = Paginator(Todo.objects.filter(parent__isnull=True), 10).get_page(request.GET.get('page'))
        return render(request, 'todos.html', {'objects': data, "way": "home"})

    def post(self, request):
        name, todos = request.POST['name'], []
        if name:
            todos = Todo.objects.filter(name__startswith=name)
        return render(request, 'todos.html', {'objects': todos, "way": "home", "search": name})


def show_todo(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    return render(request, 'todos.html', {'objects': [todo], "way": "solo"})


class CreateTask(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'todos.html', {'way': "create", "form": TodoForm()})

    def post(self, request) -> HttpResponse:
        todo = TodoForm(request.POST)
        if todo.is_valid():
            todo.save()
            return redirect("posts:home")
        else:
            return HttpResponse(204)


class TodoDelete(View):
    def post(self, request, pk: int) -> HttpResponse:
        try:
            Todo.objects.get(id=pk).delete()
        except Exception:
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200})


class TodoUpdate(View):
    def get(self, request, pk):
        form = TodoUpdateForm(instance=get_object_or_404(Todo, id=pk))
        return render(request, 'todos.html', {"way": "update", "form": form})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            form_todo.save()
            return redirect("posts:update", pk=pk)
        else:
            return HttpResponse({'status': 204, 'errors': form_todo.errors})
