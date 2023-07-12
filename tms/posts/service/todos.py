from ..models import Todo


class ServicesTodo:
    @staticmethod
    def get_todo():
        return Todo.objects.all()

    @staticmethod
    def get_todo_id_name():
        return Todo.objects.values("id", "name")

    @staticmethod
    def get_todo_by_id(id_todo):
        return Todo.objects.get(id=id_todo)

    @staticmethod
    def get_todo_and_user(todo_id):
        return Todo.objects.select_related('user').get(id=todo_id)

    @staticmethod
    def get_todo_by_name_partial(name):
        return Todo.objects.filter(name__contains=name)
