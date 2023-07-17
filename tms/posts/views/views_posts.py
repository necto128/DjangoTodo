from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import permissions
from rest_framework import status

from posts.form.todo_form import TodoForm, TodoUpdateForm, UserForm
from posts.models import Todo


class Login(View):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'todos.html', {"way": "auth", "construct": "login"})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("posts:home")
        else:
            return redirect("posts:login")


class Registration(View):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'todos.html', {"way": "auth", "construct": "registration"})

    def post(self, request):
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
            return render(request, 'todos.html', {"way": "auth", "construct": "login"})
        return render(request, 'todos.html', {"way": "auth", "construct": "registration", "form": user})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:login'))


class Home(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request):
        data = Paginator(
            Todo.objects.prefetch_related("parent", "children").filter(parent__isnull=True, user=request.user),
            10).get_page(request.GET.get('page'))
        return render(request, 'todos.html', {'objects': data, "way": "home"})

    def post(self, request):
        name, todos = request.POST['name'], []
        if name:
            todos = Todo.objects.filter(name__startswith=name, user=request.user)
        return render(request, 'todos.html', {'objects': todos, "way": "home", "search": name})


@login_required(login_url="posts:login")
def show_todo(request, pk: int):
    todo = Todo.objects.prefetch_related("parent", "children").filter(id=pk, user=request.user)
    if todo.count():
        return render(request, 'todos.html', {'objects': todo, "way": "solo"})
    return HttpResponse(request, status=status.HTTP_404_NOT_FOUND)


class CreateTask(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

    def get(self, request) -> HttpResponse:
        return render(request, 'todos.html', {'way': "create", "form": TodoForm()})

    def post(self, request) -> HttpResponse:
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
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200})


class TodoUpdate(LoginRequiredMixin, View):
    permission_classes = [permissions.IsAuthenticated]
    login_url = "posts:login"

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


def handling_404(request, exception):
    return render(request, '404.html', {})
