import flet as ft
from dataclasses import dataclass


@dataclass
class TextInputColors:
    hovered_outer_textinput_border_color: str
    hovered_inner_textinput_border_color: str
    default_outer_textinput_border_color: str
    default_inner_textinput_border_color: str
    text_field_focused_background_color: str
    text_field_border_color: str
    text_field_background_color: str
    text_color: str
    cursor_color: str

    @staticmethod
    def dark():
        return TextInputColors(
            hovered_outer_textinput_border_color="#1B2C58",
            hovered_inner_textinput_border_color="#1e55e2",
            default_outer_textinput_border_color="#26376b",
            default_inner_textinput_border_color="#494D5F",
            text_field_focused_background_color="#323741",
            text_field_border_color="#2b2f3b",
            text_field_background_color="#292f3a",
            text_color="#ffffff",
            cursor_color="#ffffff",
        )

    @staticmethod
    def light():
        return TextInputColors(
            hovered_outer_textinput_border_color="#d5e0fb",
            hovered_inner_textinput_border_color="#5786ff",
            default_outer_textinput_border_color="#d3d8e7",
            default_inner_textinput_border_color="#d3d8e7",
            text_field_focused_background_color="#ffffff",
            text_field_border_color="#f5f7fb",
            text_field_background_color="#ffffff",
            text_color="#000000",
            cursor_color="#000000",
        )


class TextInput(ft.Container):
    """may be rewritten as a sublclass of TextField"""

    def __init__(
        self,
        on_focus_additional=None,
        on_blur_additional=None,
        prefix=None,
        suffix=None,
        theme=ft.ThemeMode.DARK,
        **kwargs
    ):
        self.on_focus_additional = on_focus_additional
        self.on_blur_additional = on_blur_additional
        self.colors = (
            TextInputColors.dark()
            if theme == ft.ThemeMode.DARK
            else TextInputColors.light()
        )
        self.prefix = prefix
        self.suffix = suffix
        self.kwargs = kwargs

        if self.prefix and not self.suffix:
            content_padding = ft.padding.only(left=45, right=15)
        elif self.suffix and not self.prefix:
            content_padding = ft.padding.only(right=45, left=15)
        elif self.prefix and self.suffix:
            content_padding = ft.padding.symmetric(horizontal=45)
        else:
            content_padding = ft.padding.all(15)

        # Initialize the inner text field using ft.TextField
        self.text_field = ft.TextField(
            focused_border_width=ft.border.all(0),
            focused_border_color=ft.InputBorder.NONE,
            focused_bgcolor=self.colors.text_field_focused_background_color,
            border_radius=ft.border_radius.all(7),
            border_color=self.colors.text_field_border_color,
            filled=True,
            color=self.colors.text_color,
            cursor_color=self.colors.cursor_color,
            cursor_width=1,
            on_focus=self.set_hover_state,
            on_blur=self.remove_hover_state,
            bgcolor=self.colors.text_field_background_color,
            content_padding=content_padding,
            **self.kwargs,
        )

        self.field = ft.Stack(
            [
                self.text_field,
                ft.Container(
                    self.prefix,
                    ink=True,
                    width=20,
                    height=20,
                    alignment=ft.alignment.center,
                    left=15,
                    bottom=15,
                ),
                ft.Container(
                    self.suffix,
                    ink=True,
                    width=20,
                    height=20,
                    alignment=ft.alignment.center,
                    right=15,
                    bottom=15,
                ),
            ]
        )

        # Inner container setup
        self.inner_container = ft.Container(
            border=ft.border.all(2, self.colors.default_inner_textinput_border_color),
            border_radius=10,
            content=self.field,
            padding=1,
        )

        # Call `ft.Container` constructor with initial outer container settings
        super().__init__(
            border=ft.border.all(
                4,
                ft.colors.with_opacity(
                    0, self.colors.default_outer_textinput_border_color
                ),
            ),
            border_radius=14,
            content=self.inner_container,
        )

    def did_mount(self):
        self.colors = (
            TextInputColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else TextInputColors.light()
        )
        self.update()

    def set_hover_state(self, e):
        self.border = ft.border.all(4, self.colors.hovered_outer_textinput_border_color)
        self.inner_container.border = ft.border.all(
            2, self.colors.hovered_inner_textinput_border_color
        )
        self.update()
        self.inner_container.update()

        if self.on_focus_additional:
            self.on_focus_additional(e)

    def remove_hover_state(self, e):
        self.border = ft.border.all(
            4,
            ft.colors.with_opacity(0, self.colors.default_outer_textinput_border_color),
        )
        self.inner_container.border = ft.border.all(
            2, self.colors.default_inner_textinput_border_color
        )
        self.update()
        self.inner_container.update()

        if self.on_blur_additional:
            self.on_blur_additional(e)
