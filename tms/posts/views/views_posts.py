from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from ..form.todo_form import TodoForm
from ..models import Todo


def home(request):
    data = Paginator(Todo.objects.prefetch_related().all(), 10).get_page(request.GET.get('page'))
    return render(request, 'todos.html', {'objects': data, "way": "home"})


def list_todo(request):
    return JsonResponse({'todos': list(Todo.objects.all().values())})


def show_todo(request, pk: Todo):
    return render(request, 'todos.html', {'objects': [Todo.objects.get(id=pk)], "way": "solo"})


class CreateTask(View):
    def get(self, request):
        return render(request, 'todos.html', {'way': "create"})

    def post(self, request):
        todo = TodoForm(request.POST)
        if todo.is_valid():
            todo.save()
            return redirect("posts:home")
        else:
            return HttpResponse(204)
