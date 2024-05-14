import flet as ft
from dataclasses import dataclass


@dataclass
class TabSwitchColors:
    label_text_color: str
    unfocused_label_text_color: str
    active_tab_background_color: str
    container_background_color: str
    container_border_color: str

    @staticmethod
    def dark():
        return TabSwitchColors(
            label_text_color="rgba(255, 255, 255, 0.9)",
            unfocused_label_text_color="#494D5F",
            active_tab_background_color="#323741",
            container_background_color="#1b1d22",
            container_border_color="#494D5F",
        )

    @staticmethod
    def light():
        return TabSwitchColors(
            label_text_color="#ffffff",
            unfocused_label_text_color="#263238",
            active_tab_background_color="#1f5eff",
            container_background_color="#ffffff",
            container_border_color="#e0e4ed",
        )


class TabSwitch(ft.Container):
    def __init__(
        self,
        tab_labels,
        accent_color=ft.colors.with_opacity(0.9, "white"),
        on_switch=None,
        initial_value=0,
        theme=ft.ThemeMode.DARK,
        **kwargs
    ):
        self.colors = (
            TabSwitchColors.dark()
            if theme == ft.ThemeMode.DARK
            else TabSwitchColors.light()
        )
        super().__init__(
            width=85 * len(tab_labels),
            height=50,
            bgcolor=self.colors.container_background_color,
            padding=ft.padding.all(5),
            border=ft.border.all(1, self.colors.container_border_color),
            border_radius=10,
            **kwargs,
        )

        self.accent_color = accent_color
        self.on_switch = on_switch
        self.value = initial_value
        self.tab_labels = tab_labels

        self.tabs = [
            self.get_container(label, index == self.value)
            for index, label in enumerate(self.tab_labels)
        ]

        # Initialize the row with the tabs inside the main container
        self.content = ft.Row(controls=self.tabs, alignment=ft.MainAxisAlignment.CENTER)

    def get_container(self, text, active):
        """Create an individual tab container based on active status."""
        return ft.Container(
            content=ft.Text(
                value=text,
                color=self.colors.label_text_color
                if active
                else self.colors.unfocused_label_text_color,
                size=15,
            ),
            width=15 * len(text) - 1,
            bgcolor=self.colors.active_tab_background_color if active else "",
            border_radius=5,
            alignment=ft.alignment.center,
            padding=ft.padding.all(5),
            on_click=self.toggle_switch,
        )

    def toggle_switch(self, e):
        """Switch to the tab that was clicked."""
        clicked_tab_index = self.content.controls.index(e.control)
        self.value = clicked_tab_index

        # Update the tabs to reflect the active state
        self.content.controls = [
            self.get_container(label, index == self.value)
            for index, label in enumerate(self.tab_labels)
        ]

        self.update()
        if self.on_switch:
            self.on_switch(self.value)

    def get_value(self):
        """Return the current active tab index."""
        return self.value

    def did_mount(self):
        self.colors = (
            TabSwitchColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else TabSwitchColors.light()
        )
        self.update()
