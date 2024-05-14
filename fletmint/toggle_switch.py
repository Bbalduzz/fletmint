import flet as ft
from dataclasses import dataclass


@dataclass
class ToggleSwitchColors:
    container_background_color: str
    container_border_color: str
    active_icon_color: str
    non_active_icon_color: str
    active_switch_background_color: str

    @staticmethod
    def dark():
        return ToggleSwitchColors(
            container_background_color="#1b1d22",
            container_border_color="#494D5F",
            active_icon_color="#c3c3c8",
            non_active_icon_color="#494D5F",
            active_switch_background_color="#333742",
        )

    @staticmethod
    def light():
        return ToggleSwitchColors(
            container_background_color="#ffffff",
            container_border_color="#e0e4ed",
            active_icon_color="#ffffff",
            non_active_icon_color="#7b849c",
            active_switch_background_color="#1f5eff",
        )


class ToggleSwitch(ft.Container):
    def __init__(
        self, on_switch=None, initial_value=0, theme=ft.ThemeMode.DARK, **kwargs
    ):
        # Set initial toggle state and callback
        self.colors = (
            ToggleSwitchColors.dark()
            if theme == ft.ThemeMode.DARK
            else ToggleSwitchColors.light()
        )
        self.on_switch = on_switch
        self.value = initial_value

        # Icons for moon and sun
        self.moon_icon = ft.icons.DARK_MODE
        self.sun_icon = ft.icons.LIGHT_MODE

        # Initialize the parent container with appearance settings
        super().__init__(
            width=133,
            height=45,
            bgcolor=self.colors.container_background_color,
            padding=ft.padding.all(5),
            border=ft.border.all(1, self.colors.container_border_color),
            border_radius=10,
            **kwargs,
        )

        # Set up the initial UI elements
        self.dark_container = self.get_container(self.moon_icon, self.value == 0)
        self.light_container = self.get_container(self.sun_icon, self.value == 1)

        # Create the main row to hold the toggles
        self.content = ft.Row(
            controls=[self.dark_container, self.light_container],
        )

    def did_mount(self):
        self.colors = (
            ToggleSwitchColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ToggleSwitchColors.light()
        )
        self.update()

    def get_container(self, icon, active):
        """Helper function to create individual toggle containers."""
        return ft.Container(
            content=ft.Icon(
                icon,
                size=20,
                color=self.colors.active_icon_color
                if active
                else self.colors.non_active_icon_color,
            ),
            width=55,
            bgcolor=self.colors.active_switch_background_color if active else "",
            border_radius=5,
            alignment=ft.alignment.center,
            padding=ft.padding.all(5),
            on_click=self.toggle_switch,
        )

    def toggle_switch(self, e):
        """Toggle between the two states."""
        self.value = 0 if self.value == 1 else 1
        self.content.controls[0] = self.get_container(self.moon_icon, self.value == 0)
        self.content.controls[1] = self.get_container(self.sun_icon, self.value == 1)
        self.update()
        if self.on_switch:
            self.on_switch(self.value)

    def get_value(self):
        """Return the current toggle state."""
        return self.value
