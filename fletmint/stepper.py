import flet as ft
from dataclasses import dataclass


@dataclass
class StepperColors:
    textfield_border_color: str
    textfield_background_color: str
    outer_container_border_color: str
    stepper_button_color: str
    stepper_buttons_background_color: str
    stepper_count_text_color: str
    suffix_text_color: str

    @staticmethod
    def dark():
        return StepperColors(
            textfield_border_color="#2b2f3b",
            textfield_background_color="#323741",
            outer_container_border_color="#494D5F",
            stepper_button_color="#ffffff",
            stepper_buttons_background_color="#484e5c",
            stepper_count_text_color="#ffffff",
            suffix_text_color="#757575",  # Adjusted from ft.colors.GREY_600 to a hex value
        )

    @staticmethod
    def light():
        return StepperColors(
            textfield_border_color="#ffffff",
            textfield_background_color="#ffffff",
            outer_container_border_color="#bcc5dd",
            stepper_button_color="#b6bfda",
            stepper_buttons_background_color="#e8ebf4",
            stepper_count_text_color="#000000",
            suffix_text_color="#d3d7e2",
        )


class Stepper(ft.Container):
    def __init__(
        self, suffix="px", initial_value=123, theme=ft.ThemeMode.DARK, **kwargs
    ):
        super().__init__(**kwargs)
        self.kwargs = kwargs
        self.stepper_count = initial_value
        self.suffix_value = suffix
        self.colors = (
            StepperColors.dark()
            if theme == ft.ThemeMode.DARK
            else StepperColors.light()
        )

        # Initialize stepper components
        self.textfield = ft.TextField(
            focused_border_width=ft.border.all(0),
            focused_border_color=ft.InputBorder.NONE,
            border_radius=ft.border_radius.all(7),
            border_color=self.colors.textfield_border_color,
            filled=True,
            read_only=True,
            color=ft.colors.WHITE,
            cursor_color=ft.colors.WHITE,
            cursor_width=1,
            bgcolor=self.colors.textfield_background_color,
            **self.kwargs,
        )
        self.container = ft.Container(
            border=ft.border.all(2, self.colors.outer_container_border_color),
            border_radius=10,
            content=self.textfield,
            padding=1,
        )
        self.stepper_buttons = ft.Column(
            [
                ft.Container(
                    ft.Icon(
                        name=ft.icons.ARROW_DROP_UP_ROUNDED,
                        color=self.colors.stepper_button_color,
                        size=15,
                    ),
                    on_click=self.increase_counter,
                ),
                ft.Container(
                    ft.Icon(
                        name=ft.icons.ARROW_DROP_DOWN_ROUNDED,
                        color=self.colors.stepper_button_color,
                        size=15,
                    ),
                    on_click=self.decrease_counter,
                ),
            ],
            spacing=0,
        )
        self.stepper_count_text = ft.Text(
            self.stepper_count,
            size=20,
            weight=ft.FontWeight.NORMAL,
            color=self.colors.stepper_count_text_color,
        )
        self.suffix = ft.Text(
            self.suffix_value,
            size=18,
            weight=ft.FontWeight.NORMAL,
            color=self.colors.suffix_text_color,
        )

        # Set up the stepper UI
        self.content = ft.Stack(
            [
                self.container,
                ft.Container(
                    self.stepper_buttons,
                    border_radius=6,
                    bgcolor=self.colors.stepper_buttons_background_color,
                    padding=5,
                    left=10,
                    bottom=11,
                ),
                ft.Row(
                    [
                        ft.Container(self.stepper_count_text),
                        ft.Container(self.suffix),
                    ],
                    spacing=5,
                    right=15,
                    bottom=18,
                ),
            ]
        )
        self.width = 150

    def increase_counter(self, e):
        self.stepper_count += 1
        self.stepper_count_text.value = self.stepper_count
        self.stepper_count_text.update()

    def decrease_counter(self, e):
        self.stepper_count -= 1
        self.stepper_count_text.value = self.stepper_count
        self.stepper_count_text.update()

    def did_mount(self):
        self.colors = (
            StepperColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else StepperColors.light()
        )
        self.update()
