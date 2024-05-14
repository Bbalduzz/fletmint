import flet as ft
from enum import Enum
from dataclasses import dataclass


@dataclass
class UserProfileColors:
    avatar_background_color: str
    locked_status_background_color: str
    open_status_background_color: str
    username_text_color: str
    hyperlink_text_color: str

    @staticmethod
    def dark():
        return UserProfileColors(
            avatar_background_color="#4a4c58",
            locked_status_background_color="#9da1ad",
            open_status_background_color="#325f4c",
            username_text_color="#afb0b5",
            hyperlink_text_color="#626470",
        )

    @staticmethod
    def light():
        return UserProfileColors(
            avatar_background_color="#4a4c58",
            locked_status_background_color="#c2d3ff",
            open_status_background_color="#325f4c",
            username_text_color="#838ca5",
            hyperlink_text_color="#c6cad6",
        )


class ProfileStatus(Enum):
    PRIVATE = "private"
    OPEN = "open"
    NONE = None


class UserProfile(ft.Container):
    def __init__(
        self,
        username,
        avatar_foreground_img,
        width=60,
        height=60,
        status=ProfileStatus.PRIVATE,
        theme_mode=ft.ThemeMode.DARK,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.username = username
        self.status = status
        self.width = width
        self.height = height
        self.avatar = avatar_foreground_img
        self.colors = (
            UserProfileColors.dark()
            if theme_mode == ft.ThemeMode.DARK
            else UserProfileColors.light()
        )

        # Avatar and lock icon containers
        avatar_container = ft.Container(
            content=ft.CircleAvatar(
                bgcolor=self.colors.avatar_background_color,
                radius=10,
            ),
            width=self.width,
            height=self.height,
            alignment=ft.alignment.bottom_right,
        )

        flet_icon = (
            ft.icons.LOCK_ROUNDED
            if self.status == ProfileStatus.PRIVATE
            else ft.icons.LOCK_OPEN_ROUNDED
        )

        lock_icon = ft.Container(
            content=ft.Icon(
                flet_icon,
                color=self.colors.locked_status_background_color,
                size=11,
            ),
            width=self.width,
            height=self.height,
            alignment=ft.alignment.bottom_right,
            padding=ft.padding.only(bottom=4, right=4),
        )

        avatar = ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_src=self.avatar,
                    radius=30,
                ),
                ft.Container(content=ft.Stack([avatar_container, lock_icon])),
            ],
            height=self.width,
            width=self.height,
        )

        # User's name
        name = ft.Text(
            self.username, size=self.width / 3, color=self.colors.username_text_color
        )
        view_profile = ft.Text(
            "View profile", color=self.colors.hyperlink_text_color, size=self.width / 5
        )

        profile_action_row = ft.Row(
            [
                avatar,
                ft.Column(
                    [
                        name,
                        view_profile,
                    ],
                    alignment=ft.alignment.top_left,
                    spacing=0,
                ),
            ],
            alignment=ft.alignment.center,
            spacing=self.width / 6,  # Adjust spacing as needed
        )

        # Set the container's main content
        self.content = profile_action_row

    def did_mount(self):
        self.colors = (
            UserProfileColors.dark()
            if self.page.theme_mode == ft.ThemeMode.DARK
            else UserProfileColors.light()
        )
        self.update()
