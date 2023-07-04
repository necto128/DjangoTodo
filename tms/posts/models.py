from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, name="message")
    completed = models.BooleanField(default=0)
    subtask = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="subtasks")

    def __str__(self):
        return f"user_id: {self.user}, name: {self.name}, " \
               f"description: {self.message}, completed: {self.completed}, subtask: {self.todos}"

    def save(self, *args, **kwargs):
        self.name = self.user.username
        super().save(*args, **kwargs)
