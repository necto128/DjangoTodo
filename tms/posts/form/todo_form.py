from django import forms

from ..models import Todo


class TodoForm(forms.ModelForm):
    completed = forms.BooleanField(required=False, initial=0)
    todos = forms.IntegerField(required=False, initial=None)

    class Meta:
        model = Todo
        fields = '__all__'


class TodoUpdateForm(TodoForm):
    message = forms.CharField(required=False)
    completed = forms.BooleanField(required=False)

    class Meta:
        model = Todo
        fields = ['message', 'completed']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['message'] = cleaned_data.get('message') or self.instance.message
        cleaned_data['completed'] = cleaned_data.get('completed') or self.instance.completed