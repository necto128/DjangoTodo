# Create your models here.
from datetime import datetime
from softdelete.models import SoftDeleteObject
from django.contrib.auth.models import User
from django.db import models


class Todo(SoftDeleteObject, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, name="message")
    completed = models.BooleanField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    update_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"user_id: {self.user}, name: {self.name}, description: {self.message}, completed: {self.completed}, parent: {self.children}, update_at: {self.update_at}"
