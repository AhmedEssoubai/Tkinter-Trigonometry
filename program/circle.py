import tkinter as tk
import math as math
import resources.resources as res


# Circle
class Circle:
    def __init__(self, canvas, on_p_changed, on_target_changed, x=res.CIRCLE_X, y=res.CIRCLE_Y, radius=res.RADIUS):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._radius = radius
        self._on_angle_changed = on_p_changed
        self._on_target_angle_changed = on_target_changed
        self._center_x = x + radius
        self._center_y = y + radius
        self._animation = True
        self._mouse_motion = True
        self._draw_circle()
        self._draw_quadrants(radius / 3)
        self._draw_angles(radius / 10)
        self._target_o = 0
        self.in_radians = False
        self.angle = 0
        self.cos = 1
        self.sin = 0
        self.tan = 0
        self._speed = 0
        self._dir = 0
        self._create_p_shapes()

    # Draw circle
    def _draw_circle(self):
        # Draw main circle
        self._canvas.create_oval(self._x, self._y, self._x + self._radius * 2, self._y + self._radius * 2,
                                 outline=res.COLOR_LINES_COLOR)
        # Draw axis
        self._draw_axis()
        # Draw center oval
        self._draw_oval(self._center_x, self._center_y)

    # Draw axis
    def _draw_axis(self):
        # Draw vertical axi
        self._canvas.create_line(self._center_x,
                                 self._y - res.LINE_OUTER,
                                 self._center_x,
                                 self._center_y + self._radius + res.LINE_OUTER,
                                 fill=res.COLOR_LINES_COLOR,
                                 arrow=tk.FIRST,
                                 arrowshape="16 20 6")
        # Draw y and Y(1, 0)
        self._canvas.create_text(self._center_x - 15, self._y - res.LINE_OUTER, text="y", fill=res.COLOR_LINES_COLOR,
                                 font=(res.FONT_FAMILY, 12))
        self._canvas.create_text(self._center_x + 30, self._y - 15, text="Y (0, 1)", fill=res.COLOR_LINES_COLOR,
                                 font=(res.FONT_FAMILY, 10))
        # Draw horizontal axi
        self._canvas.create_line(self._x - res.LINE_OUTER,
                                 self._center_y,
                                 self._center_x + self._radius + res.LINE_OUTER,
                                 self._center_y,
                                 fill=res.COLOR_LINES_COLOR,
                                 arrow=tk.LAST,
                                 arrowshape="16 20 6")
        # Draw x and X(1, 0)
        self._canvas.create_text(self._center_x + self._radius + res.LINE_OUTER, self._center_y + 15, text="x",
                                 fill=res.COLOR_LINES_COLOR, font=(res.FONT_FAMILY, 12))
        self._canvas.create_text(self._center_x + self._radius + 30, self._center_y - 15, text="X (1, 0)",
                                 fill=res.COLOR_LINES_COLOR, font=(res.FONT_FAMILY, 10))
        # Draw sparks on V/H lines
        self._draw_circle_sparks()
        self._draw_circle_sparks(orient=tk.HORIZONTAL)

    # Draw an oval in canvas
    def _draw_oval(self, x, y, radius=res.LITTLE_OVAL_RADIUS, color=res.COLOR_LINES_COLOR,
                   outline=res.COLOR_LINES_COLOR):
        return self._canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=outline,
                                        width=2)

    # Draw sparks on a axi in canvas
    def _draw_circle_sparks(self, n=9, size=7, orient=tk.VERTICAL):
        spacing = self._radius / (n + 1)
        x = self._x
        y = self._y
        if orient == tk.HORIZONTAL:
            holder = x
            x = y
            y = holder
        sy = y + spacing
        for j in range(2):
            for i in range(n):
                sz = size
                if i == int(n / 2):
                    sz = sz * 2
                sx = (x + self._radius) - (sz / 2)
                px = sx + sz
                if orient == tk.VERTICAL:
                    self._canvas.create_line(sx, sy, px, sy, fill=res.COLOR_LINES_COLOR)
                else:
                    self._canvas.create_line(sy, sx, sy, px, fill=res.COLOR_LINES_COLOR)
                sy += spacing
            sy += spacing

    # Draw quadrants
    def _draw_quadrants(self, space, color=res.COLOR_LINES_COLOR):
        self._quadrants = []
        self._quadrants.append(self._canvas.create_text(self._center_x + space, self._center_y - space, text="I",
                                                        fill=color,
                                                        font=(res.FONT_FAMILY, 12)))
        self._quadrants.append(self._canvas.create_text(self._center_x - space, self._center_y - space, text="II",
                                                        fill=color,
                                                        font=(res.FONT_FAMILY, 12)))
        self._quadrants.append(self._canvas.create_text(self._center_x + space, self._center_y + space, text="III",
                                                        fill=color,
                                                        font=(res.FONT_FAMILY, 12)))
        self._quadrants.append(self._canvas.create_text(self._center_x - space, self._center_y + space, text="IV",
                                                        fill=color,
                                                        font=(res.FONT_FAMILY, 12)))

    # Show or hide quadrants
    def quadrants_option(self, active):
        self._show_hide_items(active, self._quadrants)

    # Draw angles
    def _draw_angles(self, space, color=res.COLOR_LINES_COLOR):
        self._angles = []
        jump = 30
        times = 1
        angle = 0
        for i in range(16):
            rad = angle * math.pi / 180
            cos = math.cos(rad)
            sin = math.sin(rad)
            self._angles.append(
                self._draw_oval(self._center_x + cos * self._radius, self._center_y - sin * self._radius, color=color,
                                radius=res.LITTLE_OVAL_RADIUS / 1.7))
            self._angles.append(self._canvas.create_text(self._center_x + cos * (self._radius - space),
                                                         self._center_y - sin * (self._radius - space),
                                                         text=str(angle) + "°",
                                                         font=(res.FONT_FAMILY, 10),
                                                         fill=color))
            angle += jump
            times += 1
            if times > 1:
                times = 0
                if jump == 30:
                    jump = 15
                else:
                    jump = 30

    # Show or hide angles
    def angles_option(self, active):
        self._show_hide_items(active, self._angles)

    # Show or hide items given
    def _show_hide_items(self, show, items):
        state = "normal"
        if not show:
            state = "hidden"
        for item in items:
            self._canvas.itemconfigure(item, state=state)

    # Draw the shapes of point P
    def _create_p_shapes(self, cos_color=res.COLOR_MAIN, sin_color=res.COLOR_GOOD, tan_color=res.COLOR_ERROR):
        # Create shapes list
        self._p_shapes = []
        # Find the coords of P
        px = self._center_x + self._radius
        py = self._center_y
        # Draw the line
        self._p_shapes.append(self._canvas.create_line(self._center_x, self._center_y, px, py,
                                                       fill=res.COLOR_LINES_COLOR))
        # Draw cos line
        self._p_shapes.append(self._canvas.create_line(self._center_x, self._center_y, px, self._center_y,
                                                       fill=cos_color, width=2))
        # Draw cos dash line
        self._p_shapes.append(self._canvas.create_line(px, py, px, self._center_y, dash=2,
                                                       fill=res.COLOR_LINES_COLOR))
        # Draw sin line
        self._p_shapes.append(self._canvas.create_line(self._center_x, self._center_y, self._center_x, py,
                                                       fill=sin_color, width=2))
        # Draw sin dash line
        self._p_shapes.append(self._canvas.create_line(px, py, self._center_x, py, dash=2, fill=res.COLOR_LINES_COLOR))
        # Draw tan line
        self._p_shapes.append(self._canvas.create_line(px, py, px, py, fill=tan_color))
        # Draw P olav
        self._p_shapes.append(self._draw_oval(px, py, color=res.COLOR_LIGHT_BG))
        # Draw angle line
        self._p_shapes.append(self._canvas.create_arc(self._center_x - 40,
                                                      self._center_y - 40,
                                                      self._center_x + 40,
                                                      self._center_y + 40,
                                                      start=0, extent=0,
                                                      outline=res.COLOR_WARNING))
        # Draw P coordinates
        self._p_shapes.append(self._canvas.create_text(px + 60, py - 20,
                                                       text="P(1, 0, 0)",
                                                       fill=res.COLOR_DARK_BG,
                                                       font=(res.FONT_FAMILY, 12)))
        # Draw angle value
        self._p_shapes.append(self._canvas.create_text(self._center_x + self._radius / 3,
                                                       self._center_y - self._radius / 4,
                                                       text="O",
                                                       fill=res.COLOR_WARNING,
                                                       font=(res.FONT_FAMILY, 11)))
        # Draw cos value
        self._p_shapes.append(self._canvas.create_text(px, py,
                                                       text="Cos",
                                                       fill=cos_color,
                                                       font=(res.FONT_FAMILY, 11)))
        # Draw sin value
        self._p_shapes.append(self._canvas.create_text(px, py,
                                                       text="Sin",
                                                       fill=sin_color,
                                                       font=(res.FONT_FAMILY, 11)))
        # Draw tan value
        self._p_shapes.append(self._canvas.create_text(px, py,
                                                       text="Tan",
                                                       fill=tan_color,
                                                       font=(res.FONT_FAMILY, 11)))

    # Draw P point (Change coordinates)
    def _draw_p(self):
        rad = self.angle
        # Convert degree to radian if needed
        if not self.in_radians:
            rad = self.angle * math.pi / 180
        # Calculate the value of Cosθ and Sinθ and Tanθ
        self.cos = math.cos(rad)
        if rad == math.pi / 2 or rad == math.pi * 3 / 2:
            self.cos = 0
        self.sin = math.sin(rad)
        if rad == math.pi:
            self.sin = 0
        self.tan = math.tan(rad)
        # Find the coords of P
        px = self._center_x + self.cos * self._radius
        py = self._center_y - self.sin * self._radius
        # Change the coords of P line
        self._canvas.coords(self._p_shapes[0], self._center_x, self._center_y, px, py)
        # Change cos line coords
        self._canvas.coords(self._p_shapes[1], self._center_x, self._center_y, px, self._center_y)
        # Change cos dash line coords
        self._canvas.coords(self._p_shapes[2], px, py, px, self._center_y)
        # Change sin line coords
        self._canvas.coords(self._p_shapes[3], self._center_x, self._center_y, self._center_x, py)
        # Change sin dash line coords
        self._canvas.coords(self._p_shapes[4], px, py, self._center_x, py)
        # Change tan line coords
        if rad == math.pi / 2 or rad == math.pi * 3 / 2:
            if rad == math.pi / 2:
                tx = self._center_x + self._radius * 5
            else:
                tx = self._center_x - self._radius * 5
            ty = py
        else:
            t = self.tan * self._radius * Circle.sing(self.tan)
            tx = self._center_x + (self._radius + t) * Circle.sing(self.cos)
            ty = self._center_y
        self._canvas.coords(self._p_shapes[5], px, py, tx, ty)
        # Change P point
        self._canvas.coords(self._p_shapes[6], px - res.LITTLE_OVAL_RADIUS, py - res.LITTLE_OVAL_RADIUS,
                            px + res.LITTLE_OVAL_RADIUS, py + res.LITTLE_OVAL_RADIUS)
        # Change angle
        a = self.angle
        if self.in_radians:
            a = self.angle * 180 / math.pi
        self._canvas.itemconfigure(self._p_shapes[7], start=0, extent=a)
        # Change P coordinates and text
        self.tan = str(self.tan)[:5]
        if rad == math.pi:
            self.tan = str(0)
        else:
            if rad == math.pi / 2 or rad == math.pi * 3 / 2:
                self.tan = "undefined"
        self._canvas.coords(self._p_shapes[8], px + 80 * Circle.sing(self.cos), py - 20 * Circle.sing(self.sin))
        self._canvas.itemconfig(self._p_shapes[8],
                                text="P(" + str(self.cos)[:5] + ", " + str(self.sin)[:5] + ", " + self.tan + ")")
        # Change the coordinates and text of Angle
        self._set_angle_to_ui()
        r = rad - 30 * math.pi / 180
        x = self._center_x + math.cos(r) * self._radius / 3
        y = self._center_y - math.sin(r) * self._radius / 3
        self._canvas.coords(self._p_shapes[9],  x, y)
        # Change the coordinates and text of Cos
        self._canvas.itemconfig(self._p_shapes[10], text="cos θ\n≈ " + str(self.cos)[:5])
        x = self._center_x + (px - self._center_x) / 2
        y = self._center_y + 30
        if self.sin < 0:
            y = self._center_y - 30
        self._canvas.coords(self._p_shapes[10],  x, y)
        # Change the coordinates and text of Sin
        self._canvas.itemconfig(self._p_shapes[11], text="sin θ\n≈ " + str(self.sin)[:5])
        y = self._center_y + (py - self._center_y) / 2
        x = self._center_x - 50
        if self.cos < 0:
            x = self._center_x + 50
        self._canvas.coords(self._p_shapes[11],  x, y)
        # Change the coordinates and text of Tan
        self._canvas.itemconfig(self._p_shapes[12], text="tan θ\n≈ " + str(self.tan))
        y = self._center_y + (py - self._center_y) / 2
        x = px + 100
        if self.cos < 0:
            x = px - 100
        self._canvas.coords(self._p_shapes[12],  x, y)
        # Fire event
        self._on_angle_changed()

    # Get the sing of a number given
    @staticmethod
    def sing(x):
        if x < 0:
            return -1
        return 1

    # Set the angle text to angle UI
    def _set_angle_to_ui(self):
        angle_text = "θ = " + str(math.floor(self.angle)) + "°"
        if self.in_radians:
            angle_text = "θ = " + str(self.angle)[:5]
        self._canvas.itemconfig(self._p_shapes[9], text=angle_text)

    # On mouse click
    def mouse_clicked(self, event):
        mouse_x, mouse_y = event.x, event.y

        hypotenuse = math.sqrt(math.pow(mouse_x - self._center_x, 2) + math.pow(mouse_y - self._center_y, 2))
        adjacent = math.sqrt(math.pow(mouse_x - self._center_x, 2) + math.pow(mouse_y - mouse_y, 2))

        if hypotenuse == 0:
            cos = 1
        else:
            cos = adjacent / hypotenuse

        angle = math.acos(cos)
        half = math.pi

        if not self.in_radians:
            angle = math.floor(angle * 180 / math.pi)
            half = 180

        if mouse_y > self._center_y:
            if mouse_x > self._center_x:
                angle = half - angle
            angle = angle + half
        else:
            if mouse_x < self._center_x:
                angle = half - angle

        # Fire on target angle changed event
        self._on_target_angle_changed(angle)

        # Go to target angle
        self.to_o(angle)

    # When the mouse move
    def mouse_moved(self, event):
        if not self._mouse_motion:
            return

        self.mouse_clicked(event)

    # An update function execute every 10 ms
    def _update(self):
        sp = self._speed
        if self.in_radians:
            sp = sp / 60
        mv = (self._dir == 1 and self._target_o > self.angle + sp) or \
             (self._dir == -1 and self._target_o < self.angle - sp)
        if mv:
            self.angle += sp * self._dir
        else:
            self._dir = 0
            self.angle = self._target_o
        if self._speed * 1.05 < res.MAX_SPEED:
            self._speed = self._speed * 1.05
        else:
            self._speed = res.MAX_SPEED
        self._draw_p()
        if self._dir != 0 and self._animation:
            self._canvas.after(10, self._update)

    # Go to target θ in a animation
    def to_o(self, o):
        if self.in_radians:
            self._target_o = o % (math.pi * 2)
        else:
            self._target_o = o % 360
        # Draw directly if animation deactivated
        if not self._animation:
            self.angle = self._target_o
            self._dir = 0
            self._draw_p()
            return
        # Check if animation already active from the direction
        is_active = False
        if self._dir != 0:
            is_active = True
        if self.angle > self._target_o:
            self._dir = -1
        else:
            self._dir = 1
        # Change only the target and direction if it's already active
        if is_active:
            return
        self._speed = res.MIN_SPEED
        self._update()

    # Activate or deactivate motion option
    def motion_option(self, active):
        self._mouse_motion = active

    # Activate or deactivate animation
    def animation_option(self, active):
        self._animation = active

    # Change the angle unit from or to radians
    def unit_option(self, active):
        current_in_radians = self.in_radians
        self.in_radians = not active
        if current_in_radians and not self.in_radians:
            self.angle = self.angle * 180 / math.pi
            self._target_o = self._target_o * 180 / math.pi
        else:
            if not current_in_radians and self.in_radians:
                self.angle = self.angle * math.pi / 180
                self._target_o = self._target_o * math.pi / 180
        self._set_angle_to_ui()
        self._on_angle_changed()
        self._on_target_angle_changed(self._target_o)
