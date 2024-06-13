import os
import flet as ft
from fletmint.utils import change_app_icon

icon_path = os.path.join("icons", "icon.png")


def main(page: ft.Page):
    page.window_width, page.window_height = 400, 400
    page.title = "Flet App with Custom Icon"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    icon_path = os.path.join("icons", "icon.png")

    page.add(
        ft.Image(src=icon_path, width=64, height=64),
        ft.Text("Hello, this is a Flet app with a custom icon!"),
    )


change_app_icon(icon_path=icon_path, app_name="Flet App with Custom Icon")

if __name__ == "__main__":
    ft.app(target=main)
