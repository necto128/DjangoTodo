from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Todo


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Todo
        fields = ["id", "user", "name", "message", "completed", "parent", "children"]
