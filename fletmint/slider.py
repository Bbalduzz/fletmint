import flet as ft
from dataclasses import dataclass


@dataclass
class SliderColors:
    active_bar_color: str
    inactive_bar_color: str

    @staticmethod
    def dark():
        return SliderColors(active_bar_color="#1f5eff", inactive_bar_color="#323741")

    @staticmethod
    def light():
        return SliderColors(active_bar_color="#1f5eff", inactive_bar_color="#e8ebf4")


class Slider(ft.Slider):
    def __init__(self, theme_mode=ft.ThemeMode.DARK, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme_mode
        self.colors = None
        self.kwargs = kwargs
        self.thumb_color = ft.colors.WHITE
        self.overlay_color = ft.colors.with_opacity(0, "white")

        self.apply_theme()

    def apply_theme(self):
        self.colors = (
            SliderColors.dark()
            if self.theme == ft.ThemeMode.DARK
            else SliderColors.light()
        )
        self.change_theme(self.colors)
        self.active_color = self.colors.active_bar_color
        self.inactive_color = self.colors.inactive_bar_color

    def change_theme(self, colors=None):
        # Dynamically update attributes based on what is available in SliderColors
        for attr in vars(colors):
            if hasattr(self, attr):
                setattr(self, attr, getattr(colors, attr))

    def toggle_theme(self):
        self.theme = (
            ft.ThemeMode.LIGHT if self.theme == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.apply_theme()
        self.update()
