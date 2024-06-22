from render.builder.viewmodel import ViewModel


class JobRunVM(ViewModel):
    list_fields = ["id", "status", "run", "job"]
    search_fields = ["id", "job", "run", "status"]
    show_fields = ["id", "name", "task", "schedule"]
    disabled_view_models = ["add", "edit", "delete"]
