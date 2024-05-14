import flet as ft
from .text_input import TextInput
from dataclasses import dataclass


@dataclass
class DropDownColors:
    container_background_color: str
    container_border_color: str
    selected_control_background_color: str
    selected_control_text_color: str
    unselected_control_text_color: str
    dropdown_starter_icon_color: str

    @staticmethod
    def dark():
        return DropDownColors(
            container_background_color="#323741",
            container_border_color="#3d424d",
            selected_control_background_color="#2a2e35",
            selected_control_text_color=ft.colors.with_opacity(0.9, "white"),
            unselected_control_text_color="#959cae",
            dropdown_starter_icon_color="#ffffff",
        )

    @staticmethod
    def light():
        return DropDownColors(
            container_background_color="#ffffff",
            container_border_color="#d9deec",
            selected_control_background_color="#e9efff",
            selected_control_text_color="#5182ff",
            unselected_control_text_color="#646f8e",
            dropdown_starter_icon_color="#7e879e",
        )


class Dropdown(ft.UserControl):
    def __init__(
        self,
        controls,
        drodown_icons=[
            ft.icons.ARROW_DROP_DOWN_ROUNDED,
            ft.icons.ARROW_DROP_UP_ROUNDED,
        ],
        theme=ft.ThemeMode.DARK,
        max_width=300,
        on_select=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.show_splash = False
        self.controls = controls
        self.controls_num = len(controls)
        self.max_width = max_width
        self.dropdown_icons = drodown_icons
        self.colors = (
            DropDownColors.dark()
            if theme == ft.ThemeMode.DARK
            else DropDownColors.light()
        )
        self._on_select = on_select
        self._dropdown_starter_bounds = None

    def did_mount(self):
        self.theme = self.page.theme_mode
        self.colors = (
            DropDownColors.dark()
            if self.theme == ft.ThemeMode.DARK
            else DropDownColors.light()
        )
        self.update()

    def build_controls(self):
        if isinstance(self.controls[0], str):
            return [
                ft.Text(
                    data.title(),
                    color=self.colors.unselected_control_text_color,
                    size=15,
                )
                for data in self.controls
            ]
        else:
            return self.controls

    def build_dropdown(self):
        def on_control_hover(e):
            e.control.bgcolor = (
                self.colors.selected_control_background_color
                if e.data == "true"
                else ""
            )
            e.control.content.content.color = (
                self.colors.selected_control_text_color
                if e.data == "true"
                else self.colors.unselected_control_text_color
            )
            e.control.update()

        return ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Container(
                            control,
                            width=self.max_width,
                            height=30,
                            margin=5,
                            padding=ft.padding.only(top=3, left=15),
                        ),
                        border_radius=8,
                        on_hover=on_control_hover,
                        on_click=self.on_control_click,
                    )
                    for control in self.build_controls()
                ],
                spacing=2,
            ),
            padding=10,
            bgcolor=self.colors.container_background_color,
            border=ft.border.all(2, self.colors.container_border_color),
            border_radius=10,
            width=self.max_width,
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=3,
                color=ft.colors.BLACK,
                offset=ft.Offset(0, 1),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    def on_control_click(self, e):
        self.selected_control_value = e.control.content.content.value
        self.dropdown_starter.content.content.controls[0].content.content.controls[
            0
        ].value = self.selected_control_value
        self.unfocus_dropdown()
        self.close_dropdown()

        if self._on_select:
            return self._on_select(self.selected_control_value)

    def unfocus_dropdown(self):
        self.dropdown_starter.content.content.controls[0].remove_hover_state(None)
        self.dropdown_starter.content.content.controls[1].content = ft.Icon(
            name=self.dropdown_icons[0],
            color=self.colors.dropdown_starter_icon_color,
            size=25,
        )
        self.dropdown_starter.update()

    def close_dropdown(self):
        self.page.splash = None
        self.show_splash = False
        self.page.update()

    def calculate_bounds(self, event, height=50):
        top_left = (event.global_x - event.local_x, event.global_y - event.local_y)
        return {
            "top_left": top_left,
            "top_right": (top_left[0] + self.max_width, top_left[1]),
            "bottom_left": (top_left[0], top_left[1] + float(height)),
            "bottom_right": (top_left[0] + self.max_width, top_left[1] + float(height)),
        }

    def update_dropdown_position(self, bottom_left):
        dropdown = self.dropdown
        dropdown.top = bottom_left[1] + 20
        dropdown.left = bottom_left[0]
        return dropdown

    def toggle_dropdown(self, e):
        # Check if the dropdown is already showing
        if self.show_splash:
            self.unfocus_dropdown()
            self.close_dropdown()
        else:
            # If not showing, calculate bounds and show dropdown
            # set_hover_state on textfield + toggle dropdown icon on container
            self.dropdown_starter.content.content.controls[0].set_hover_state(None)
            self.dropdown_starter.content.content.controls[1].content = ft.Icon(
                name=self.dropdown_icons[1],
                color=self.colors.dropdown_starter_icon_color,
                size=25,
            )

            self._dropdown_starter_bounds = (
                self.calculate_bounds(e)
                if not self._dropdown_starter_bounds
                else self._dropdown_starter_bounds
            )
            self.page.splash = self.update_dropdown_position(
                self._dropdown_starter_bounds["bottom_left"]
            )
            self.show_splash = True

        self.dropdown_starter.update()
        self.page.update()

    def build(self):
        self.dropdown = self.build_dropdown()
        self.dropdown_starter = ft.Container(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap_down=self.toggle_dropdown,
                content=ft.Stack(
                    [
                        TextInput(
                            dense=True,
                        ),
                        ft.Container(
                            ft.Icon(
                                name=self.dropdown_icons[0],
                                color=self.colors.dropdown_starter_icon_color,
                                size=25,
                            ),
                            right=0,
                            bottom=17,
                            padding=ft.padding.only(right=20),
                        ),
                    ]
                ),
            ),
            width=self.max_width,
        )
        return self.dropdown_starter
