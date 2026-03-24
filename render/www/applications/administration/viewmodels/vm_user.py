from render.builder.viewmodel import ViewModel


class VMUser(ViewModel):
    search_fields = ["user_name"]
    add_fields = ["user_name"]
    edit_fields = ["is_active", "roles", "modules"]
    show_fields = ["user_name", "is_active", "roles", "modules"]
    list_fields = ["id", "user_name", "is_active"]
