from render.builder.viewmodel import ViewModel


class JobRunVM(ViewModel):
    list_fields = ["id", "status", "run_timestamp", "job"]
    search_fields = ["id", "run_timestamp", "status"]
    show_fields = ["id", "name", "task", "schedule"]
    disabled_view_models = ["add", "edit", "delete"]
