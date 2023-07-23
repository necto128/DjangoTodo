from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework import status

from posts.form.todo_form import TodoForm, TodoUpdateForm
from posts.models import Todo


class Home(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request) -> render:
        data = Paginator(
            Todo.objects.prefetch_related("parent", "children").filter(parent__isnull=True, user=request.user),
            10).get_page(request.GET.get('page'))
        return render(request, 'todos.html', {'objects': data, "way": "home"})

    def post(self, request) -> render:
        name, todos = request.POST['name'], []
        if name:
            todos = Todo.objects.filter(name__startswith=name, user=request.user)
        return render(request, 'todos.html', {'objects': todos, "way": "home", "search": name})


@login_required(login_url="posts:login")
def show_todo(request, pk: int) -> [HttpResponse, render]:
    todo = Todo.objects.prefetch_related("parent", "children").filter(id=pk, user=request.user)
    if todo.count():
        return render(request, 'todos.html', {'objects': todo, "way": "solo"})
    return HttpResponse(request, status=status.HTTP_404_NOT_FOUND)


class CreateTask(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request) -> render:
        return render(request, 'todos.html', {'way': "create", "form": TodoForm()})

    def post(self, request) -> [HttpResponse, redirect]:
        todo = TodoForm(request.POST)
        if todo.is_valid():
            todo.save()
            return redirect("posts:home")
        else:
            return HttpResponse(204)


class TodoDelete(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def post(self, request, pk: int) -> HttpResponse:
        try:
            Todo.objects.get(id=pk, user=request.user).delete()
        except Exception:
            return HttpResponse({"status": 404})
        return HttpResponse({"status": 200})


class TodoUpdate(LoginRequiredMixin, View):
    login_url = "posts:login"

    def get(self, request, pk: int) -> render:
        form = TodoUpdateForm(instance=get_object_or_404(Todo, id=pk))
        return render(request, 'todos.html', {"way": "update", "form": form})

    def post(self, request, pk: int) -> [HttpResponse, redirect]:
        todo = get_object_or_404(Todo, id=pk)
        form_todo = TodoUpdateForm(request.POST, instance=todo)
        if form_todo.is_valid():
            form_todo.save()
            return redirect("posts:update", pk=pk)
        else:
            return HttpResponse({'status': 204, 'errors': form_todo.errors})


@cache_page(60 * 120)
def handling_404(request, exception):
    return render(request, '404.html', {exception})
