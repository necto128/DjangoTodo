from django.urls import path

from posts.views import views_posts
from posts.views import views_auth

urlpatterns = [
    path('home/', views_posts.Home.as_view(), name='home'),
    path('<int:pk>', views_posts.show_todo, name="show_todo"),
    path('create', views_posts.CreateTask.as_view(), name="create"),
    path('<int:pk>/delete', views_posts.TodoDelete.as_view(), name="delete"),
    path('<int:pk>/update', views_posts.TodoUpdate.as_view(), name="update"),
    path('registration', views_auth.Registration.as_view(), name="registration"),
    path('login', views_auth.Login.as_view(), name="login"),
    path('logout', views_auth.logout_view, name="logout"),
]
