from django import forms

from ..models import Todo


class TodoForm(forms.ModelForm):
    parent = forms.ModelChoiceField(required=False, initial=None, queryset=Todo.objects.filter(parent__isnull=True))

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

