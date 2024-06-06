from functools import reduce

from render.builder.utils import outside_url_for


class Menu:

    def __init__(self, root):
        self.root = root
        self.items = []

    def add_item(self, menu_item):
        self.items.append(menu_item)

    def get(self):
        # TODO check permissions

        def update_res(res, item):
            if item.category not in res:
                res[item.category] = []
            item.url = outside_url_for(f"{self.root}.{item.controller}")()
            res[item.category].append(item)
            return res

        return reduce(lambda r, x: update_res(r, x), self.items, {})


class MenuItem:
    def __init__(self, controller, name=None, category="no_grouped", icon=None):
        self.category = category
        self.name = name or controller
        self.controller = controller
        self.icon = icon
        self.url = None
