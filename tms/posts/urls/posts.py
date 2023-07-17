from django.urls import path

from posts.views import views_posts


urlpatterns = [
    path('home/', views_posts.Home.as_view(), name='home'),
    path('<int:pk>', views_posts.show_todo, name="show_todo"),
    path('create', views_posts.CreateTask.as_view(), name="create"),
    path('<int:pk>/delete', views_posts.TodoDelete.as_view(), name="delete"),
    path('<int:pk>/update', views_posts.TodoUpdate.as_view(), name="update"),
    path('registration', views_posts.Registration.as_view(), name="registration"),
    path('login', views_posts.Login.as_view(), name="login"),
    path('logout', views_posts.logout_view, name="logout"),
]
