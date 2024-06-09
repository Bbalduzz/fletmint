import flet as ft
from time import sleep
from enum import Enum


class ToastPosition(Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class ToastType(Enum):
    DEFAULT = "default"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    PROMISE = "promise"


class ToastColors(Enum):
    INFO = {
        "light": {
            "bgcolor": "#f1f8fe",
            "border_color": "#d5e0fa",
            "text_color": "#3572d5",
        },
        "dark": {
            "bgcolor": "#1e2a35",
            "border_color": "#3b4a5a",
            "text_color": "#72a1d5",
        },
    }
    SUCCESS = {
        "light": {
            "bgcolor": "#effdf3",
            "border_color": "#dbfce6",
            "text_color": "#3c883b",
        },
        "dark": {
            "bgcolor": "#1b2c1f",
            "border_color": "#3b5a44",
            "text_color": "#6dbb65",
        },
    }
    ERROR = {
        "light": {
            "bgcolor": "#fcf0f0",
            "border_color": "#fae2e1",
            "text_color": "#d22d1d",
        },
        "dark": {
            "bgcolor": "#2a1c1c",
            "border_color": "#5a3b3b",
            "text_color": "#e57373",
        },
    }
    WARNING = {
        "light": {
            "bgcolor": "#fefcf1",
            "border_color": "#fbf7db",
            "text_color": "#d3863e",
        },
        "dark": {
            "bgcolor": "#2a261a",
            "border_color": "#5a523b",
            "text_color": "#d19a5c",
        },
    }
    DEFAULT = {
        "light": {
            "bgcolor": ft.colors.WHITE,  # Replace with `ft.colors.WHITE` if using a specific color module
            "border_color": "#f1f1f1",
            "text_color": ft.colors.BLACK,  # Replace with `ft.colors.BLACK` if using a specific color module
        },
        "dark": {
            "bgcolor": "#1e1e1e",
            "border_color": "#3b3b3b",
            "text_color": "#ffffff",
        },
    }
    PROMISE = {
        "light": {
            "bgcolor": ft.colors.WHITE,  # Replace with `ft.colors.WHITE` if using a specific color module
            "border_color": "#f1f1f1",
            "text_color": ft.colors.BLACK,  # Replace with `ft.colors.BLACK` if using a specific color module
        },
        "dark": {
            "bgcolor": "#1e1e1e",
            "border_color": "#3b3b3b",
            "text_color": "#ffffff",
        },
    }


class Toast(ft.Container):
    def __init__(
        self,
        content=None,
        text=None,
        description=None,
        toast_type: ToastType | str = ToastType.DEFAULT,
        **kwargs
    ):
        if isinstance(toast_type, str):
            toast_type = ToastType(toast_type)
        colors = self.get_colors(toast_type)
        content = (
            content
            if content
            else self.default_content(toast_type, text, description, colors)
        )
        width = kwargs.get("width", 300)
        height = kwargs.get("height", 50)
        opacity = kwargs.get("opacity", 1)
        scale = kwargs.get("scale", 1)
        animate_position = kwargs.get("animate_position", 80)
        animate_opacity = kwargs.get("animate_opacity", ft.Animation(400, "ease"))
        animate_scale = kwargs.get("animate_scale", ft.Animation(400, "ease"))

        super().__init__(
            content=content,
            bgcolor=colors["bgcolor"],
            border=ft.border.all(1, colors["border_color"]),
            padding=10,
            border_radius=5,
            width=width,
            height=height,
            alignment=ft.alignment.center,
            left=None,
            right=None,
            top=None,
            bottom=None,
            opacity=opacity,
            scale=scale,  # Initial scale
            animate_position=animate_position,
            animate_opacity=animate_opacity,
            animate_scale=animate_scale,
            on_click=lambda e: print("toast clicked"),
            on_hover=lambda e: print("toast hovered"),
        )

    @staticmethod
    def get_colors(toast_type):
        return ToastColors[toast_type.name].value["dark"]

    def default_content(self, toast_type, message, description, colors):
        content = [ft.Text(message, color=colors["text_color"])]
        if description:
            content.append(ft.Text(description, color=colors["text_color"], size=9))

        if toast_type == ToastType.INFO:
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.INFO_ROUNDED,
                        size=18,
                        color=colors["text_color"],
                    ),
                    ft.Column(
                        content, alignment=ft.MainAxisAlignment.CENTER, spacing=0
                    ),
                ]
            )
        elif toast_type == ToastType.SUCCESS:
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.CHECK_CIRCLE_ROUNDED,
                        size=18,
                        color=colors["text_color"],
                    ),
                    ft.Column(
                        content, alignment=ft.MainAxisAlignment.CENTER, spacing=0
                    ),
                ]
            )
        elif toast_type == ToastType.WARNING:
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.WARNING_ROUNDED,
                        size=18,
                        color=colors["text_color"],
                    ),
                    ft.Column(
                        content, alignment=ft.MainAxisAlignment.CENTER, spacing=0
                    ),
                ]
            )
        elif toast_type == ToastType.ERROR:
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.ERROR_ROUNDED,
                        size=18,
                        color=colors["text_color"],
                    ),
                    ft.Column(
                        content, alignment=ft.MainAxisAlignment.CENTER, spacing=0
                    ),
                ]
            )
        elif toast_type == ToastType.PROMISE:
            return ft.Row(
                [
                    ft.ProgressRing(width=16, height=16, stroke_width=1),
                    ft.Column(
                        content, alignment=ft.MainAxisAlignment.CENTER, spacing=0
                    ),
                ]
            )
        else:
            return ft.Column(content, alignment=ft.MainAxisAlignment.CENTER, spacing=0)


class Toaster:
    def __init__(
        self,
        page,
        expand=False,
        position: ToastPosition | str = ToastPosition.TOP_RIGHT,
        theme: str = "dark",
        default_toast_duration=3,
        default_offset=20,
    ):
        self.theme = theme
        self.page = page
        self.toasts = []
        self.position = (
            position.value if isinstance(position, ToastPosition) else position
        )
        self.default_toast_duration = default_toast_duration
        self.default_offset = default_offset
        self.stack = ft.Stack(
            width=page.window_width,
            height=page.window_height,
            expand=True,
        )
        self.page.overlay.append(self.stack)
        self.is_hovered = False
        self.is_expanded = expand

    def show_toast(
        self,
        message=None,
        text=None,
        description=None,
        toast=None,
        duration=3,
        toast_type="default",
    ):
        toast = (
            toast
            if toast
            else Toast(
                content=message,
                text=text,
                description=description,
                toast_type=toast_type,
            )
        )
        self.set_toast_position(toast, 0)
        self.stack.controls.append(toast)  # Insert the new toast at the top
        self.toasts.insert(0, toast)  # Maintain the order of toasts
        self.reposition_toasts()
        self.page.update()

        if duration > 0:

            def __remove_toast():
                sleep(duration)
                if toast in self.stack.controls:
                    self.remove_toast(toast)

            self.page.run_thread(__remove_toast)

    def remove_toast(self, toast):
        self.stack.controls.remove(toast)
        self.toasts.remove(toast)
        self.reposition_toasts()
        self.page.update()

    def reposition_toasts(self):
        for i, toast in enumerate(self.toasts):
            if self.is_hovered or self.is_expanded:
                self.set_toast_position(toast, i, as_column=True)
            else:
                self.set_toast_position(toast, i)
        self.page.update()

    def set_toast_position(self, toast, index, as_column=False):
        base_offset = self.default_offset
        spacing = 10

        if as_column:
            if "top" in self.position:
                toast.top = base_offset + (index * 60)
                toast.bottom = None
            elif "bottom" in self.position:
                toast.bottom = base_offset + (index * 60)
                toast.top = None
            toast.scale = 1
        else:
            if "top" in self.position:
                toast.top = 20 + (index * 10)  # Adjust this to overlap toasts closely
                toast.bottom = None
            else:
                toast.bottom = 20 + (
                    index * 10
                )  # Adjust this to overlap toasts closely
                toast.top = None
            toast.scale = 1 - (0.05 * index)  # Scale previous toasts down

        if "left" in self.position:
            toast.left = 20
            toast.right = None
        elif "right" in self.position:
            toast.right = 20
            toast.left = None
        else:
            toast.left = None
            toast.right = None

        # Only the top toast handles hover events
        if index == 0 and not self.is_expanded:
            toast.on_hover = self.on_hover
        else:
            toast.on_hover = None

    def on_hover(self, e):
        self.is_hovered = e.data == "true"
        self.reposition_toasts()

    def show_promise_toast(
        self, function, success_message, error_message, descriptive=False
    ):
        promise_toast = Toast(
            text="Loading...",
            toast_type=ToastType.PROMISE,
        )
        self.show_toast(toast=promise_toast, duration=0)

        def run_function():
            try:
                result = function()
                description = result if descriptive else None
                self.page.run_thread(
                    lambda: self.update_toast(
                        promise_toast, success_message, description, ToastType.SUCCESS
                    )
                )
            except Exception as e:
                description = e if descriptive else None
                self.page.run_thread(
                    lambda: self.update_toast(
                        promise_toast, error_message, description, ToastType.ERROR
                    )
                )

        self.page.run_thread(run_function)

    def update_toast(self, toast, message, description, toast_type):
        toast_type = (
            ToastType(toast_type) if isinstance(toast_type, str) else toast_type
        )
        colors = ToastColors[toast_type.name].value["dark"]
        toast.content = toast.default_content(toast_type, message, description, colors)
        toast.bgcolor = colors["bgcolor"]
        toast.border = ft.border.all(1, colors["border_color"])
        self.page.update()
        sleep(3)
        self.remove_toast(toast)
