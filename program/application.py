import tkinter as tk
from program.help import Help
from program.trigonometry import Trigonometry
import resources.resources as res
from program.menu import Menu

canvas = None
pages = []


# On configure pages
def on_configure(event):
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))


# On main menu item selected
def selected_changed(new_index):
    for i in range(len(pages)):
        state = "hidden"
        if i == new_index:
            state = "normal"
        canvas.itemconfigure(pages[i], state=state)


# Main app
def main():
    global canvas
    root = tk.Tk()
    root.title("Trigonometry")
    root.geometry("1280x720")
    root.iconbitmap("../resources/icon.ico")

    # Side menu
    side_menu = Menu(root, selected_changed)
    side_menu.new_item("../resources/icon3.png", True)
    side_menu.new_item("../resources/icon2.png")
    side_menu.body.pack(side=tk.LEFT, fill=tk.Y)

    # Pages container
    canvas = tk.Canvas(root, bg=res.COLOR_LIGHT_BG)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Pages scrollbar
    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure pages container
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', on_configure)

    # Create help page
    help_page = Help(canvas)
    pages.append(canvas.create_window((20, 0), window=help_page.page, anchor='nw'))

    plot_page = Trigonometry(canvas)
    pages.append(canvas.create_window((20, 0), window=plot_page.page, anchor='nw'))

    selected_changed(0)

    # Start mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
