import flet as ft
from enum import Enum


class BadgeColors(Enum):
    SUCCESS = {"bgcolor": "#325f4c", "color": "#30b562"}
    WARNING = {"bgcolor": "#5b4e42", "color": "#c28845"}
    ERROR = {"bgcolor": "#7f0000", "color": "#FF0A0A"}


class Badge(ft.UserControl):
    def __init__(
        self,
        on_click,
        badge_text: str,
        colors: dict | BadgeColors,
        icon=ft.icons.CLOSE,
    ):
        super().__init__()
        self.badge_text = badge_text
        self.colors = colors.value if isinstance(colors, Enum) else colors
        self.icon = icon
        self.on_click = on_click

    def build(self):
        return ft.TextButton(
            content=ft.Row([ft.Text(self.badge_text), ft.Icon(self.icon, size=15)]),
            on_click=lambda e: self.on_click(e),
            style=ft.ButtonStyle(
                bgcolor=self.colors["bgcolor"],
                color=self.colors["color"],
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )
