from flet import (
    TextButton,
    Container,
    Text,
    Icon,
    colors,
    ButtonStyle,
    ContinuousRectangleBorder,
    MaterialState,
)
from dataclasses import dataclass


@dataclass
class ButtonColors:
    button_disabled_background_color = "#21386c"
    button_backgound_color = "#1d5ffc"
    button_content_color = "#ffffff"
    button_disabled_content_color = "#626470"


class Button(TextButton):
    def __init__(
        self,
        width=200,
        height=50,
        on_click=None,
        disabled=False,
        style=None,
        label="Button",
        icon=None,
    ):
        if icon:
            button_content = Icon(
                icon, size=13, color=ButtonColors.button_content_color
            )
        else:
            button_content = Text(
                label, size=13, color=ButtonColors.button_content_color
            )

        if not style:
            self.style = ButtonStyle(
                color={
                    "": ButtonColors.button_disabled_content_color
                    if disabled
                    else ButtonColors.button_content_color,  # MaterialState.DEFAULT
                },
                bgcolor={
                    "": ButtonColors.button_backgound_color
                    if not disabled
                    else ButtonColors.button_disabled_background_color,
                    "disabled": ButtonColors.button_disabled_background_color,
                },
                padding=18,
                shape=ContinuousRectangleBorder(radius=20),
            )
        else:
            self.style = style

        super().__init__(
            content=Container(content=button_content),
            width=width,
            height=height,
            on_click=None if disabled else on_click,
            disabled=disabled,
            style=self.style,
        )

    def set_disabled(self, disabled: bool):
        # Update the disabled state of the button programmatically
        self.disabled = disabled
        if disabled:
            self.bgcolor = ButtonColors.button_disabled_background_color
            self.color = ButtonColors.button_disabled_content_color
            self.on_click = None
        else:
            self.bgcolor = ButtonColors.button_backgound_color
            self.color = ButtonColors.button_content_color
            self.on_click = self.on_click
        self.update()


class SecondaryButton(Button):
    def __init__(
        self,
        width=200,
        height=50,
        on_click=None,
        disabled=False,
        label="Button",
        icon=None,
    ):
        # Override the background color for a destructive button (red)
        secondary_style = ButtonStyle(
            color={
                MaterialState.DEFAULT: colors.BLACK,  # MaterialState.DEFAULT
            },
            bgcolor={
                "": colors.with_opacity(0.1, ButtonColors.button_backgound_color)
                if not disabled
                else ButtonColors.button_disabled_background_color,
                "disabled": ButtonColors.button_disabled_background_color,
            },
            padding=18,
            shape=ContinuousRectangleBorder(radius=20),
        )

        # Pass the customized style to the base `Button` class
        super().__init__(
            width=width,
            height=height,
            on_click=on_click,
            disabled=disabled,
            label=label,
            icon=icon,
        )
        # Override the style attribute directly to apply the destructive color
        self.style = secondary_style

    def did_mount(self):
        self.update()

    def set_disabled(self, disabled: bool):
        super().set_disabled(disabled)
        self.bgcolor = (
            "#f0f0f0" if not disabled else ButtonColors.button_disabled_background_color
        )
        self.color = (
            "#000000" if not disabled else ButtonColors.button_disabled_content_color
        )
        self.update()


class DestructiveButton(Button):
    def __init__(
        self,
        width=200,
        height=50,
        on_click=None,
        disabled=False,
        label="Delete",
        icon=None,
    ):
        # Override the background color for a destructive button (red)
        destructive_style = ButtonStyle(
            color={
                "": ButtonColors.button_disabled_content_color
                if disabled
                else ButtonColors.button_content_color,  # MaterialState.DEFAULT
            },
            bgcolor={
                "": "#FF0000"  # Red background for the destructive action
                if not disabled
                else ButtonColors.button_disabled_background_color,
                "disabled": ButtonColors.button_disabled_background_color,
            },
            padding=18,
            shape=ContinuousRectangleBorder(radius=20),
        )

        # Pass the customized style to the base `Button` class
        super().__init__(
            width=width,
            height=height,
            on_click=on_click,
            disabled=disabled,
            label=label,
            icon=icon,
        )
        # Override the style attribute directly to apply the destructive color
        self.style = destructive_style

    def did_mount(self):
        self.update()

    def set_disabled(self, disabled: bool):
        super().set_disabled(disabled)
        # Override the background color for the destructive state when enabled
        self.bgcolor = (
            "#FF0000" if not disabled else ButtonColors.button_disabled_background_color
        )
        self.update()
