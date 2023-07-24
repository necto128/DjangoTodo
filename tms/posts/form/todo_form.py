import datetime

from django import forms
from django.contrib.auth.models import User

from posts.models import Todo


class TodoForm(forms.ModelForm):
    parent = forms.ModelChoiceField(required=False, initial=None, queryset=Todo.objects.filter(parent__isnull=True))

    class Meta:
        model = Todo
        fields = ['id', 'user', 'name', 'message', 'completed', 'parent']


class TodoCreateForm(TodoForm):
    class Meta:
        model = Todo
        fields = ['id', 'user', 'name', 'message', 'completed', 'parent']


class TodoUpdateForm(TodoForm):
    name = forms.CharField(required=False)
    message = forms.CharField(required=False)
    completed = forms.BooleanField(required=False)

    class Meta:
        model = Todo
        fields = ['name', 'message', 'completed']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['completed'] = cleaned_data.get('completed')
        cleaned_data['name'] = cleaned_data.get('name') or self.instance.name
        cleaned_data['message'] = cleaned_data.get('message') or self.instance.message

    def save(self, commit=True):
        todo_instance = super().save(commit=False)
        if 'completed' in self.changed_data and self.cleaned_data.get('completed'):
            todo_instance.update_at = datetime.datetime.now()
        if commit:
            todo_instance.save()
        return todo_instance


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=6)
    password = forms.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем существует.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        if commit:
            user.save()
        return user
