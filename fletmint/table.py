import flet as ft
from dataclasses import dataclass


@dataclass
class TableColors:
    container_background_color: str
    container_border_color: str

    @staticmethod
    def light():
        return TableColors(
            container_background_color="#ffffff",
            container_border_color="#e0e4ed",
        )

    @staticmethod
    def dark():
        return TableColors(
            container_background_color="#323741",
            container_border_color="#3d424d",
        )


class Table(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = TableColors.light()
        self.max_width = 450
        self.columns = []

    def did_mount(self):
        self.colors = (
            TableColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else TableColors.light()
        )
        self.update()

    def build_table(self):
        self.navigator = ft.Row(
            [
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.ARROW_BACK_IOS_ROUNDED,
                                size=15,
                                color="#7c7b82",
                            ),
                            ft.Text("Previous", size=12, color="#7c7b82"),
                        ]
                    ),
                    style=ft.ButtonStyle(
                        side=ft.border.BorderSide(1, color="#f0f0f0"),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
                ft.Row(
                    [
                        ft.Text(txt, color="#7c7b82")
                        for txt in ("1", "2", "...", "9", "10")
                    ]
                ),
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Text("Next", size=12, color="#7c7b82"),
                            ft.Icon(
                                name=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
                                size=15,
                                color="#7c7b82",
                            ),
                        ]
                    ),
                    style=ft.ButtonStyle(
                        side=ft.border.BorderSide(1, color="#f0f0f0"),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.title = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Table",
                            weight=ft.FontWeight.BOLD,
                            size=22,
                            color=ft.colors.GREY_900,
                        ),
                        ft.Row(
                            [
                                ft.Icon(name=ft.icons.SEARCH, color=ft.colors.GREY_400),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.navigator,
            ]
        )
        return ft.Container(
            self.title,
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

    def build(self):
        return self.build_table()
