from django.urls import path, include
from rest_framework import routers

from posts.views import views_api_v2

router = routers.DefaultRouter()
router.register('post', views_api_v2.TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views_api_v2.UserRegistrationAPIView.as_view())
]
