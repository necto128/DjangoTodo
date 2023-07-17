from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from posts.models import Todo
from posts.serialazers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    ordering_fields = ["id", "user", "name", "completed", "parent"]
    filterset_fields = ["id", "user", "name", "completed"]
    search_fields = ["user__username", "name"]
