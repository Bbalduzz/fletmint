from flet import (
    ThemeMode,
    UserControl,
    Container,
    Row,
    Column,
    Text,
    Icon,
    icons,
    FontWeight,
    border,
    alignment,
    MainAxisAlignment,
)
from dataclasses import dataclass


@dataclass
class CheckBoxColors:
    unchecked_border_color: str
    unchecked_background_color: str
    checked_background_color: str
    checked_icon_color: str
    unchecked_icon_color: str
    disabled_border_color: str
    disabled_background_color: str
    disabled_outer_border_color: str = (
        ""  # Optional attribute if not needed in the dark theme
    )

    @staticmethod
    def dark():
        return CheckBoxColors(
            unchecked_border_color="#494D5F",
            unchecked_background_color="#353743",
            checked_background_color="#195ffb",
            checked_icon_color="#ffffff",
            unchecked_icon_color="#ffffff",  # Dark theme doesn't have this field, hence left empty
            disabled_border_color="#193fa0",
            disabled_background_color="#21386c",
        )

    @staticmethod
    def light():
        return CheckBoxColors(
            unchecked_border_color="#c1c9e0",
            unchecked_background_color="#ffffff",
            checked_background_color="#1f5eff",
            checked_icon_color="#ffffff",
            unchecked_icon_color="#1f5eff",
            disabled_border_color="#5282fe",
            disabled_background_color="#ffffff",
            disabled_outer_border_color="#dfe7fb",
        )


class CheckBox(UserControl):
    CHECK_ICON_SIZE = 15

    def __init__(
        self,
        color: str = "#195ffb",
        label: str = "",
        selection_fill: str = "#183588",
        size: int = 25,
        stroke_width: int = 1,
        animation=None,
        checked: bool = False,
        font_size: int = 16,
        on_click=None,
        disabled: bool = False,
        theme: ThemeMode | str = ThemeMode.DARK,
        alignment=MainAxisAlignment.START,
    ):
        super().__init__()
        self.color = color
        self.label = label
        self.size = size
        self.stroke_width = stroke_width
        self.animation = animation
        self.checked = checked
        self.font_size = font_size
        self.pressed = on_click
        self.disabled = disabled
        self.alignment = alignment
        self.colors = (
            CheckBoxColors.dark() if theme == ThemeMode.DARK else CheckBoxColors.light()
        )
        self._build_ui()

    def _build_ui(self):
        self.check_box = self._create_checkbox_container(self.checked, self.disabled)
        self.container = Container(
            on_click=self._toggle_check if not self.disabled else None,
            content=Row(
                controls=[self.check_box],
                alignment=self.alignment,
                expand=False,
            ),
        )
        if self.label != "":
            self.container.content.controls.append(
                Text(
                    self.label,
                    font_family="Poppins",
                    size=self.font_size,
                    weight=FontWeight.W_300,
                )
            )

    def _create_checkbox_container(self, checked: bool, disabled: bool):
        if disabled:
            bg_color = self.colors.disabled_background_color
            border_color = self.colors.disabled_border_color
            content = Icon(
                icons.HORIZONTAL_RULE_ROUNDED,
                size=self.CHECK_ICON_SIZE - 3,
                color=self.colors.unchecked_icon_color,
            )
        elif checked:
            bg_color = self.colors.checked_background_color
            border_color = self.colors.checked_background_color
            content = Icon(
                icons.CHECK_ROUNDED,
                size=self.CHECK_ICON_SIZE,
                color=self.colors.checked_icon_color,
            )
        else:
            bg_color = self.colors.unchecked_background_color
            border_color = self.colors.unchecked_border_color
            content = Container()

        return Container(
            animate=self.animation,
            width=self.size,
            height=self.size,
            border_radius=7,
            bgcolor=bg_color,
            border=border.all(color=border_color, width=self.stroke_width),
            content=content,
        )

    def _toggle_check(self, e):
        if not self.disabled:
            self.checked = not self.checked
            # Update the checkbox UI based on the new state
            self.check_box.content = (
                Icon(
                    icons.CHECK_ROUNDED,
                    size=self.CHECK_ICON_SIZE,
                    color=self.colors.checked_icon_color,
                )
                if self.checked
                else Container()
            )
            self.check_box.bgcolor = (
                self.colors.checked_background_color
                if self.checked
                else self.colors.unchecked_background_color
            )
            self.check_box.border = border.all(
                color=self.colors.checked_background_color
                if self.checked
                else self.colors.unchecked_border_color,
                width=self.stroke_width,
            )
            self.update()

            if self.pressed and not self.disabled:
                self.pressed(self.checked)

    def is_checked(self):
        return self.checked

    def build(self):
        return self.container
