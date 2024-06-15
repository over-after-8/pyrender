from render.builder.viewmodel import ViewModel


class PermissionVM(ViewModel):
    list_fields = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    add_fields = ["name"]
    show_fields = ["name", "created_at", "updated_at"]
    edit_fields = ["name"]
