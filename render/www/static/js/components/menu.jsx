
class MenuItem {
  constructor(category, name, controller, icon, url) {
    this.category = category;
    this.name = name;
    this.controller = controller;
    this.icon = icon;
    this.url = url;
  }
}

class ApplicationCategory {
  constructor(name, items = []) {
    this.name = name;
    this.items = items;
  }

  addItem(item) {
    this.items.push(item);
  }
}

function parseMenu(data) {
  const categories = [];

  for (const [categoryName, itemsArray] of Object.entries(data)) {
    const category = new ApplicationCategory(categoryName);
    itemsArray.forEach(itemObj => {
      const item = new MenuItem(
        itemObj.category,
        itemObj.name,
        itemObj.controller,
        itemObj.icon,
        itemObj.url
      );
      category.addItem(item);
    });
    categories.push(category);
  }

  return categories;
}

export default parseMenu