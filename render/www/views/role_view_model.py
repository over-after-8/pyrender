from render.builder.viewmodel import ViewModel


class RoleVM(ViewModel):
    list_fields = ["name", "permissions", "created_at", "updated_at"]
    search_fields = ["name"]
    add_fields = ["name"]
    show_fields = ["name", "permissions", "created_at", "updated_at"]
    edit_fields = ["name", "permissions"]
