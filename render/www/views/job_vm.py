from render.builder.viewmodel import ViewModel


class JobVM(ViewModel):
    list_fields = ["id", "name", "task", "schedule", "start", "end"]
    search_fields = ["id", "name", "task"]
    add_fields = ["name", "task", "schedule", "start", "end"]
    show_fields = ["id", "name", "task", "schedule", "start", "end"]
    edit_fields = ["name", "task", "schedule", "start", "end"]
