import flet as ft

SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class color_utils:
    @staticmethod
    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])

    @staticmethod
    def rgb_to_hsl(r, g, b):
        r /= 255.0
        g /= 255.0
        b /= 255.0

        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        l = (max_c + min_c) / 2

        if delta == 0:
            h = 0
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1))
            if max_c == r:
                h = 60 * (((g - b) / delta) % 6)
            elif max_c == g:
                h = 60 * (((b - r) / delta) + 2)
            elif max_c == b:
                h = 60 * (((r - g) / delta) + 4)

        return round(h), round(s * 100), round(l * 100)

    @staticmethod
    def rgb_to_hsv(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        if max_c == min_c:
            h = 0
        elif max_c == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif max_c == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        if max_c == 0:
            s = 0
        else:
            s = delta / max_c

        v = max_c

        return (round(h), round(s * 100), round(v * 100))

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def hex_to_hsl(hex_color):
        r, g, b = color_utils.hex_to_rgb(hex_color)
        return color_utils.rgb_to_hsl(r, g, b)

    @staticmethod
    def mix_colors(color1, color2, ratio):
        return [
            int(color1[0] + (color2[0] - color1[0]) * ratio),
            int(color1[1] + (color2[1] - color1[1]) * ratio),
            int(color1[2] + (color2[2] - color1[2]) * ratio),
        ]

    @staticmethod
    def hsv_to_rgb(h, s, v):
        if s == 0:
            r = g = b = int(v * 255)
            return (r, g, b)

        i = int(h * 6)  # sector 0 to 5
        f = (h * 6) - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - s * f))
        t = int(255 * v * (1 - s * (1 - f)))
        v = int(255 * v)
        i = i % 6

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
        return (r, g, b)

    @staticmethod
    def hex_to_hsv(hex_color):
        r, g, b = color_utils.hex_to_rgb(hex_color)
        return color_utils.rgb_to_hsv(r, g, b)


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1):
        super().__init__()
        self.__hue = hue
        self.__number_of_hues = 10
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_slider()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.drag_start
        self.on_pan_update = self.drag_update

    # hue
    @property
    def hue(self) -> float:
        return self.__hue

    @hue.setter
    def hue(self, value: float):
        if isinstance(value, float):
            self.__hue = value
            if value < 0 or value > 1:
                raise Exception("Hue value should be between 0 and 1")
        else:
            raise Exception("Hue value should be a float number")

    def _before_build_command(self):
        super()._before_build_command()
        # called every time on self.update()
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = color_utils.rgb_to_hex(
            color_utils.hsv_to_rgb(self.__hue, 1, 1)
        )

    def __update_selected_hue(self, x):
        self.__hue = max(0, min((x - CIRCLE_SIZE / 2) / self.track.width, 1))
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = color_utils.rgb_to_hex(
            color_utils.hsv_to_rgb(self.__hue, 1, 1)
        )

    def update_selected_hue(self, x):
        self.__update_selected_hue(x)
        self.thumb.update()
        self.on_change_hue()

    def drag_start(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_x)

    def drag_update(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_x)

    def generate_gradient_colors(self):
        colors = []
        for i in range(0, self.__number_of_hues + 1):
            color = color_utils.rgb_to_hex(
                color_utils.hsv_to_rgb(i / self.__number_of_hues, 1, 1)
            )
            colors.append(color)
        return colors

    def generate_slider(self):
        self.track = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.generate_gradient_colors(),
            ),
            width=SLIDER_WIDTH - CIRCLE_SIZE,
            height=CIRCLE_SIZE / 2,
            border_radius=5,
            top=CIRCLE_SIZE / 4,
            left=CIRCLE_SIZE / 2,
        )

        self.thumb = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.content.controls.append(self.track)
        self.content.controls.append(self.thumb)


class ColorPicker(ft.UserControl):
    def __init__(
        self,
        color: str = "#000000",
        on_color_select=None,
        width=220,
        height=220,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.color = color
        self._on_color_select = on_color_select
        self.button_ref = ft.Ref[ft.TextButton]()
        self.color_display_ref = ft.Ref[ft.FilledButton]()
        self.color_text_ref = ft.Ref[ft.Text]()
        self.hue_slider = HueSlider(
            on_change_hue=self.update_picker_color,
            hue=color_utils.hex_to_hsv(self.color)[0],
        )
        self.button_visibility = False
        self._width = width
        self._height = height

    def build(self):
        self.cursor = ft.TextButton(
            ref=self.button_ref,
            content=ft.Container(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLACK,
                shape=ft.CircleBorder(),
                side=ft.border.BorderSide(width=3, color=ft.colors.WHITE),
                elevation=3,
                padding=0,
            ),
            visible=self.button_visibility,
            on_click=self.on_button_click,
            left=0,
            top=0,
        )

        self.vertical_gradient_container = ft.Container(
            width=self._width,
            height=self._height,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["transparent", "#000000"],
                stops=[0.0, 1.0],
            ),
        )

        self.horizontal_gradient_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#ffffff", self.color],
                stops=[0.0, 1.0],
            ),
            width=self._width,
            height=self._height,
        )

        stack = ft.Stack(
            controls=[
                self.horizontal_gradient_container,
                self.vertical_gradient_container,
                self.cursor,
            ],
            width=self._width,
            height=self._height,
        )

        color_picker_selector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_hover=self.on_hover,
            on_exit=self.on_exit,
            content=stack,
        )

        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                ft.FilledButton(
                                    ref=self.color_display_ref,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=7),
                                    ),
                                ),
                                width=35,
                                height=35,
                                padding=ft.padding.only(top=5, left=5),
                            ),
                            ft.Text(
                                ref=self.color_text_ref,
                                style=ft.TextStyle(size=20, weight=ft.FontWeight.W_100),
                            ),
                        ]
                    ),
                    color_picker_selector,
                    ft.Container(
                        ft.Row(
                            [
                                ft.Container(
                                    ft.Icon(
                                        name=ft.icons.COLORIZE_ROUNDED,
                                        size=15,
                                        color="#b0b8cc",
                                    ),
                                    padding=ft.padding.only(left=5),
                                ),
                                self.hue_slider,
                            ]
                        ),
                        alignment=ft.alignment.center_right,
                        padding=ft.padding.only(bottom=10, left=5),
                    ),
                ]
            ),
            bgcolor="#323741",
            border=ft.border.all(1, "#3d424d"),
            width=self._width,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=3,
                color=ft.colors.BLACK,
                offset=ft.Offset(0, 1),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    def on_hover(self, e: ft.HoverEvent):
        button = self.button_ref.current
        button.left = e.local_x - 20  # Adjust the position of the button
        button.top = e.local_y - 20  # Adjust the position of the button
        button.style.bgcolor = self.calculate_color(e.local_x, e.local_y)
        button.visible = True

        self.color_display_ref.current.style.bgcolor = button.style.bgcolor
        self.color_text_ref.current.value = button.style.bgcolor

        self.update()

    def on_exit(self, e: ft.HoverEvent):
        self.button_ref.current.visible = False
        self.update()

    def on_button_click(self, e):
        self.selected_color = {
            "hex": self.button_ref.current.style.bgcolor,
            "rbg": color_utils.hex_to_rgb(self.button_ref.current.style.bgcolor),
            "hsl": color_utils.hex_to_hsl(self.button_ref.current.style.bgcolor),
        }

        if self._on_color_select:
            return self._on_color_select(self.selected_color)

    def calculate_color(self, x, y):
        # Calculate the horizontal gradient color
        horizontal_ratio = x / self._width
        start_color = color_utils.hex_to_rgb("#ffffff")
        end_color = color_utils.hex_to_rgb(self.color)
        horizontal_color = color_utils.mix_colors(
            start_color, end_color, horizontal_ratio
        )

        # Calculate the vertical gradient color
        vertical_ratio = y / self._height
        black_color = color_utils.hex_to_rgb("#000000")
        vertical_color = color_utils.mix_colors(
            horizontal_color, black_color, vertical_ratio
        )

        return color_utils.rgb_to_hex(vertical_color)

    def update_picker_color(self):
        h, s, l = self.hue_slider.hue, 100, 50
        self.color = color_utils.rgb_to_hex(color_utils.hsv_to_rgb(h, s / 100, l / 100))
        self.horizontal_gradient_container.gradient.colors = ["#ffffff", self.color]
        self.update()


"""
def main(page: ft.Page):
    color_picker = ColorPicker(
        color="#00ff00", on_color_select=lambda value: print("selected color:", value)
    )  # Example color
    page.add(color_picker)


ft.app(target=main)
"""
