from render.builder.viewmodel import ViewModel


class VMPermission(ViewModel):
    search_fields = ["name"]
    show_fields = ["id", "name"]
    list_fields = ["id", "name"]
    add_fields = ["name"]
    edit_fields = ["name"]
