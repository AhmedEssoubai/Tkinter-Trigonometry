import tkinter as tk
from PIL import ImageTk
import resources.resources as res


class Menu:
    def __init__(self, root, selected):
        self._root = root
        self._images = []
        self._items = []
        self.index = -1
        self._on_selected = selected
        self.body = tk.Frame(root, bg=res.COLOR_DARK_BG)
        self._create_image("../resources/icon.png").pack(pady=(15, 20))

    def _create_image(self, location):
        self._images.append(ImageTk.PhotoImage(file=location))
        lb_image = tk.Label(self.body, image=self._images[-1], width=res.MENU_WIDTH, bg=res.COLOR_DARK_BG)
        return lb_image

    def new_item(self, image, is_selected=False):
        item = self._create_image(image)
        item.bind("<Button-1>", self._on_clicked)
        item.pack(pady=(5, 10))
        self._items.append(item)
        if is_selected:
            self.index = len(self._items) - 1
            self._select_item()

    def _on_clicked(self, e):
        index = self._items.index(e.widget)
        if index == self.index:
            return
        self.index = index
        self._select_item()
        self._on_selected(self.index)

    def _select_item(self):
        for item in self._items:
            item.config(bg=res.COLOR_DARK_BG)
        if self.index != -1:
            self._items[self.index].config(bg=res.COLOR_VERY_DARK_BG)


