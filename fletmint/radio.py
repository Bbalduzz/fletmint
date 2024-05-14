import flet as ft


class Radio(ft.CupertinoRadio):
    def __init__(
        self, value, label, active_color="#5a76f7", inactive_color="#26283c", **kwargs
    ):
        super().__init__(value=value, label=label)
        self.value = value
        self.label = f"  {label}"
        self.active_color = active_color
        self.inactive_color = inactive_color
        # self.kwargs = **kwargs
