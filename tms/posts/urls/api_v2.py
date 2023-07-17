from django.urls import path, include
from rest_framework import routers

from posts.views.views_api_v2 import TodoViewSet

router = routers.DefaultRouter()
router.register('post', TodoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
