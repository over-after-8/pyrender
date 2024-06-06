from flask import Blueprint

from render.builder.menu import Menu


class Application:

    def declare_bp(self) -> Blueprint:
        pass

    def __init__(self, name):
        self.name = name
        self.bp = self.declare_bp()
        self.menu = Menu(self.bp.name)

    def get_menu(self):
        self.menu.get()

    def menu_add(self, menu_item):
        self.menu.add_item(menu_item)

    def init_menu(self):
        pass

    def register(self):
        self.init_view_model()
        self.init_menu()

        self.bp.context_processor(lambda: self.utility_process())
        self.routes()

    def init_view_model(self):
        pass

    def utility_process(self):
        def inject_menu():
            return self.menu.get()

        return dict(inject_menu=inject_menu)

    def routes(self):
        pass
