import tkinter as tk
from PIL import ImageTk
import resources.resources as res
import webbrowser


class Help:
    def __init__(self, root):
        self._root = root
        self._images = []
        self.page = tk.Frame(root, bg=res.COLOR_LIGHT_BG)
        self.create_content()

    def create_content(self):
        self.create_text("Trigonometry", color=res.COLOR_ERROR).pack(fill=tk.X)
        self.create_text("Trigonometry (from Greek trigōnon, \"triangle\" and metron, \"measure\") is a branch of "
                         "mathematics that studies relationships between side lengths and angles of triangles. "
                         "The field emerged in the Hellenistic world during the 3rd century BC from applications "
                         "of geometry to astronomical studies. The Greeks focused on the calculation of chords, "
                         "while mathematicians in India created the earliest-known tables of values for trigonometric "
                         "ratios (also called trigonometric functions) such as sine."
                         "\n\nThroughout history, trigonometry has been applied in areas such as geodesy, surveying, "
                         "celestial mechanics, and navigation."
                         "\n\nTrigonometry is known for its many identities, which are equations used for rewriting "
                         "trigonometrical expressions to solve equations, to find a more useful expression, or to "
                         "discover new relationships.",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img1.png").pack()
        self.create_text("Trigonometric ratios", color=res.COLOR_DARK_BG, font_size=15).pack(fill=tk.X)
        self.create_text("Trigonometric ratios are the ratios between edges of a right triangle. These ratios are "
                         "given by the following trigonometric functions of the known angle A, where a, b and c "
                         "refer to the lengths of the sides in the accompanying figure:",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img2.png").pack()
        self.create_text("\t+ Sine function (sin), defined as the ratio of the side opposite the angle to the "
                         "hypotenuse.",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img3.png").pack()
        self.create_text("\t+ Cosine function (cos), defined as the ratio of the adjacent leg (the side of the "
                         "triangle joining the angle to the right angle) to the hypotenuse.",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img4.png").pack()
        self.create_text("\t+ Tangent function (tan), defined as the ratio of the opposite leg to the adjacent leg.",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img5.png").pack()
        self.create_text("The hypotenuse is the side opposite to the 90 degree angle in a right triangle; it is the "
                         "longest side of the triangle and one of the two sides adjacent to angle A. The adjacent leg "
                         "is the other side that is adjacent to angle A. The opposite side is the side that is "
                         "opposite to angle A. The terms perpendicular and base are sometimes used for the opposite "
                         "and adjacent sides respectively. See below under Mnemonics."
                         "\n\nSince any two right triangles with the same acute angle A are similar, the value "
                         "of a trigonometric ratio depends only on the angle A."
                         "\n\nThe reciprocals of these functions are named the cosecant (csc), secant (sec), and "
                         "cotangent (cot), respectively:",
                         font_size=12).pack(fill=tk.X)
        self.create_image("../resources/img6.png").pack()
        self.create_image("../resources/img7.png").pack()
        self.create_image("../resources/img8.png").pack()
        self.create_text("The cosine, cotangent, and cosecant are so named because they are respectively the sine, "
                         "tangent, and secant of the complementary angle abbreviated to \"co-\"."
                         "\n\nWith these functions, one can answer virtually all questions about arbitrary triangles "
                         "by using the law of sines and the law of cosines. These laws can be used to compute the "
                         "remaining angles and sides of any triangle as soon as two sides and their included angle or "
                         "two angles and a side or three sides are known.",
                         font_size=12).pack(fill=tk.X)
        self.create_text("For more information :",
                         font_size=12).pack(fill=tk.X)
        self.create_hyperlink("Wikipedia", "https://en.wikipedia.org/wiki/Trigonometry").pack(fill=tk.X)
        self.create_hyperlink("Maths is fun", "https://www.mathsisfun.com/algebra/trigonometry.html").pack(fill=tk.X)
        self.create_hyperlink("khan academy", "https://www.khanacademy.org/math/trigonometry").pack(fill=tk.X)
        self.create_hyperlink("Skills you need", "https://www.skillsyouneed.com/num/trigonometry.html").pack(fill=tk.X)
        self.create_hyperlink("Britannica", "https://www.britannica.com/science/trigonometry").pack(fill=tk.X)
        self.create_text("Developed by Ahmed Essoubai and Moubarak Najih, ENSA Tanger MBISD01 2019",
                         font_size=12,
                         color=res.COLOR_DARK_BG).pack(fill=tk.X)

    # Create text UI
    def create_text(self, text, color=res.COLOR_LINES_COLOR, font_size=18):
        lb = tk.Label(self.page, text=text, bg=res.COLOR_LIGHT_BG, wraplength=1000, pady=10, anchor=tk.NW,
                      justify=tk.LEFT, fg=color, font=(res.FONT_FAMILY, font_size))
        return lb

    # Create hyperlink UI
    def create_hyperlink(self, text, link, font_size=12):
        hl = self.create_text(text, res.COLOR_MAIN, font_size)
        hl.bind("<Button-1>", lambda e: webbrowser.open_new(link))
        return hl

    # Create image UI
    def create_image(self, location):
        self._images.append(ImageTk.PhotoImage(file=location))
        lb_image = tk.Label(self.page, image=self._images[-1], bg=res.COLOR_LIGHT_BG)
        return lb_image



