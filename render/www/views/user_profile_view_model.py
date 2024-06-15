from render.builder.viewmodel import ViewModel


class UserProfileVM(ViewModel):
    list_fields = ["name", "gender", "birth_date"]
    search_fields = ["name"]
    add_fields = ["name", "gender", "birth_date", "avatar"]
    show_fields = ["name", "gender", "birth_date", "avatar"]
    edit_fields = ["name", "gender", "birth_date", "avatar"]
