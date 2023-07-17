from django.urls import path

from posts.views import views_api

urlpatterns = [
    path('home', views_api.Home.as_view(), name='home'),
    path('create', views_api.Home.as_view(), name="create"),
    path('posts/<int:pk>/delete', views_api.TodoDelete.as_view(), name="delete"),
    path('posts/<int:pk>', views_api.ShowTodo.as_view(), name="show_todo"),
    path('posts/<int:pk>/update', views_api.ShowTodo.as_view(), name="update"),
]
