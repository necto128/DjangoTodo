from django.contrib.auth import logout, authenticate, login
from django.http import HttpRequest
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from rest_framework import permissions

from posts.form.todo_form import UserForm


class Login(View):
    permission_classes = [permissions.AllowAny]

    def get(self, request: HttpRequest) -> render:
        return render(request, 'todos.html', {"way": "auth", "construct": "login"})

    def post(self, request: HttpRequest) -> redirect:
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

    def get(self, request: HttpRequest) -> render:
        return render(request, 'todos.html', {"way": "auth", "construct": "registration"})

    def post(self, request: HttpRequest) -> render:
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
            return render(request, 'todos.html', {"way": "auth", "construct": "login"})
        return render(request, 'todos.html', {"way": "auth", "construct": "registration", "form": user})


@cache_page(60 * 120)
def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse('posts:login'))
