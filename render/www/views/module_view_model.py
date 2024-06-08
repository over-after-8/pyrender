from render.builder.viewmodel import ViewModel


class ModuleViewModel(ViewModel):
    list_fields = ["name", "class_name", "created_at", "updated_at"]
    search_fields = ["name", "class_name"]
    add_fields = ["name", "class_name"]
    show_fields = ["name", "class_name", "created_at", "updated_at"]
    edit_fields = ["name", "class_name"]
