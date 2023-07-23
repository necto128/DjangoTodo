from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Todo
from posts.serialazers import TodoSerializer, UserSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todos to be viewed or edited.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    ordering_fields = ["id", "user", "name", "completed", "parent"]
    filterset_fields = ["id", "user", "name", "completed"]
    search_fields = ["user__username", "name"]


class UserRegistrationAPIView(APIView):
    """
    Retrieve, create a user instance.
    """

    def get_permissions(self) -> permissions:
        if self.request.method == 'PUT':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({'error': 'User is exist'},
                                status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )

            return Response({'message': 'ACCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
