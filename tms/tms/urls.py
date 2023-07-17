"""
URL configuration for tms project.

The `urlpatterns` list routes URLs to views_api.py. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views_api.py
    1. Add an import:  from my_app import views_api.py
    2. Add a URL to urlpatterns:  path('', views_api.py.home, name='home')
Class-based views_api.py
    1. Add an import:  from other_app.views_api.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include(('posts.urls.posts', 'posts'))),
    path('api/', include(('posts.urls.api', 'api'))),
    path('api/v2/', include('posts.urls.api_v2')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

handler404 = 'posts.views.views_posts.handling_404'
