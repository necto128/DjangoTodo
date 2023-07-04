from django.urls import path

from ..views import views_posts

urlpatterns = [
    path('home/', views_posts.home, name='home'),
    path('', views_posts.list_todo, name="list_todo"),
    path('<int:pk>', views_posts.show_todo, name="show_todo"),
    path('create', views_posts.CreateTask.as_view(), name="create"),
]
