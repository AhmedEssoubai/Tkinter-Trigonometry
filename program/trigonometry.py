import tkinter as tk
import resources.resources as res
from program.circle import Circle
from tkinter import messagebox


# Header menu item
class MenuItem:
    def __init__(self, menu, text, on_selected, index, is_checkbox=True, is_selected=False):
        self.label = tk.Label(menu, text=text, bg=res.COLOR_LIGHT_BG, anchor=tk.NW, font=(res.FONT_FAMILY, 14))
        self.is_selected = is_selected
        self.is_checkbox = is_checkbox
        self._on_selected_changed = on_selected
        self.index = index
        self.label.bind("<Button-1>", self._on_selected)
        self.set_color()

    # When the item selected or deselected
    def _on_selected(self, event):
        self.is_selected = not self.is_selected
        self.set_color()
        self._on_selected_changed(self.index)

    # Set the foreground color based if it's selected or not
    def set_color(self):
        if self.is_selected or not self.is_checkbox:
            self.label.config(fg=res.COLOR_MAIN)
        else:
            self.label.config(fg=res.COLOR_LINES_COLOR)


# Trigonometry circle page
class Trigonometry:
    def __init__(self, root):
        self._root = root
        self._items = []
        self.page = tk.Frame(root, bg=res.COLOR_LIGHT_BG)
        tk.Canvas(self.page, width=1100, height=1, bg=res.COLOR_LIGHT_BG).pack()
        form = self._create_menu([["On motion", True, True], ["Animation", True, True],
                                  ["Quadrants", True, True], ["Angles", True, True],
                                  ["Degrees", True, False]])
        self._create_angle_options(form)
        self._create_circle()
        self._create_footer()
        self._circle.to_o(0)

    # Create header menu
    def _create_menu(self, items):
        menu = tk.Frame(self.page, bg=res.COLOR_LIGHT_BG)
        menu.pack(fill=tk.X, expand=True)
        for i in range(len(items)):
            item = MenuItem(menu, items[i][0], self._on_menu_item_selected, i, items[i][2], items[i][1])
            item.label.pack(side=tk.LEFT, padx=(20, 20), pady=(20, 20))
            self._items.append(item)
        return menu

    def _on_menu_item_selected(self, index):
        if index == 0:
            self._circle.motion_option(self._items[index].is_selected)
        else:
            if index == 1:
                self._circle.animation_option(self._items[index].is_selected)
            else:
                if index == 2:
                    self._circle.quadrants_option(self._items[index].is_selected)
                else:
                    if index == 3:
                        self._circle.angles_option(self._items[index].is_selected)
                    else:
                        if index == 4:
                            if self._items[index].is_selected:
                                self._items[index].label["text"] = "Degrees"
                            else:
                                self._items[index].label["text"] = "Radians"
                        self._circle.unit_option(self._items[index].is_selected)

    # Create angle control options
    def _create_angle_options(self, panel):
        tk.Label(panel, text="Angle :", fg=res.COLOR_LINES_COLOR, bg=res.COLOR_LIGHT_BG, anchor=tk.NW,
                 font=(res.FONT_FAMILY, 12)).pack(side=tk.LEFT, padx=(40, 20), pady=(10, 10))
        ef = tk.Frame(panel, bg=res.COLOR_LIGHT_BG, bd=1, relief=tk.SOLID,
                      highlightbackground=res.COLOR_LINES_COLOR)
        ef.pack(side=tk.LEFT)
        self._tb_angle = tk.Entry(ef, fg=res.COLOR_LINES_COLOR, borderwidth=8, relief=tk.FLAT,
                                  highlightbackground=res.COLOR_LINES_COLOR,
                                  font=(res.FONT_FAMILY, 12))
        self._tb_angle.insert(0, 0)
        self._tb_angle.pack()
        tk.Button(panel, text="Draw", fg="white", bg=res.COLOR_MAIN, bd=1, relief=tk.SOLID,
                  font=(res.FONT_FAMILY, 12), command=lambda: self.on_draw_p(self._tb_angle.get())).\
            pack(side=tk.LEFT, padx=(20, 20))

    # Create circle canvas
    def _create_circle(self):
        self._canvas = tk.Canvas(self.page, width=res.WIDTH, height=res.HEIGHT, bg=res.COLOR_LIGHT_BG)
        self._circle = Circle(self._canvas, self._on_angle_changed, self._on_target_angle_changed)
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self._circle.mouse_clicked)
        self._canvas.bind("<Motion>", self._on_mouse_moved)

    # When the angle is changed
    def _on_angle_changed(self):
        unit = "°"
        if self._circle.in_radians:
            unit = ""
        self._values_text.config(text="θ = " + str(self._circle.angle)[:7] + unit +
                                      ",  Cos θ ≈ " + str(self._circle.cos)[:7] +
                                      ",  Sin θ ≈ " + str(self._circle.sin)[:7] +
                                      ",  Tan θ ≈ " + str(self._circle.tan))

    # When the target angle is changed by mouse event
    def _on_target_angle_changed(self, angle):
        self._tb_angle.delete(0, tk.END)
        self._tb_angle.insert(0, angle)

    # When the mouse is moved
    def _on_mouse_moved(self, e):
        self._values_coords.config(text="x = " + str(e.x) + ",  y = " + str(e.y))
        self._circle.mouse_moved(e)

    # Create footer
    def _create_footer(self):
        panel = tk.Frame(self.page, bg=res.COLOR_LIGHT_BG)
        panel.pack(fill=tk.X, expand=True)
        self._values_text = tk.Label(panel, text="θ = 0°,  Cos θ ≈ 1,  Sin θ ≈ 0,  Tan θ ≈ 0",
                                     fg=res.COLOR_LINES_COLOR, bg=res.COLOR_LIGHT_BG,
                                     anchor=tk.NW, font=(res.FONT_FAMILY, 8))
        self._values_text.pack(side=tk.LEFT, padx=(20, 20), pady=(10, 10))
        self._values_coords = tk.Label(panel, text="x = 10,  y = 500",
                                       fg=res.COLOR_LINES_COLOR, bg=res.COLOR_LIGHT_BG,
                                       anchor=tk.NE, font=(res.FONT_FAMILY, 8))
        self._values_coords.pack(side=tk.RIGHT, padx=(20, 20), pady=(10, 10))

    # On draw point P of degree θ
    def on_draw_p(self, deg):
        o = 0
        try:
            o = float(deg)
        except ValueError:
            messagebox.showerror("Invalid number", "The number given is not valid")
        else:
            self._circle.to_o(o)



