from render.builder.viewmodel import ViewModel


class VMModule(ViewModel):
    show_fields = ["id", "name", "class_name"]
    list_fields = ["id", "name", "class_name"]
    add_fields = ["name", "class_name"]
    edit_fields = ["name", "class_name"]
    search_fields = ["name", "class_name"]
