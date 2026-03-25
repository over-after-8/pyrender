from render.builder.viewmodel import ViewModel


class VMRole(ViewModel):
    search_fields = ["name"]
    show_fields = ["id", "name", "permissions"]
    list_fields = ["id", "name"]
    add_fields = ["name", "permissions"]
    edit_fields = ["name", "permissions"]
