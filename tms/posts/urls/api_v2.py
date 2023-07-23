from django.urls import path, include
from rest_framework import routers

from posts.views.views_api_v2 import TodoViewSet, UserRegistrationAPIView

router = routers.DefaultRouter()
router.register('post', TodoViewSet, basename='post')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='register')
]
