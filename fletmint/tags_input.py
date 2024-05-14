import flet as ft
from .text_input import TextInput
from .badge import Badge
from dataclasses import dataclass


@dataclass
class TagsInputColors:
    tag_background_color: str
    tag_content_color: str

    @staticmethod
    def dark():
        return TagsInputColors(
            tag_background_color="#325f4c", tag_content_color="#30b562"
        )

    @staticmethod
    def light():
        return TagsInputColors(
            tag_background_color="#b3f5c9", tag_content_color="#4db972"
        )


class TagsInput(ft.Stack):
    def __init__(
        self, max_width=500, max_tags=float("inf"), theme=ft.ThemeMode.DARK, **kwargs
    ):
        super().__init__(**kwargs)
        self.tags = []  # List to hold the tags
        self.max_width = max_width
        self.max_tags = max_tags
        self.colors = (
            TagsInputColors.dark()
            if theme == ft.ThemeMode.DARK
            else TagsInputColors.light()
        )

        # Initialize the text field and tags container
        self.text_field = TextInput(
            on_submit=self.handle_text_submit,
            dense=False,
            width=self.max_width,
        )
        self.tags_container = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.END,
            scroll=True,
            width=self.max_width - 30,
        )

        # Define the tags input stack content
        self.controls = [
            self.text_field,
            ft.Container(self.tags_container, left=15, bottom=16),
        ]

    def did_mount(self):
        self.colors = (
            TagsInputColors.light()
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else TagsInputColors.dark()
        )
        self.update()

    def handle_text_submit(self, e):
        tag_text = e.control.value.strip()
        if tag_text:
            self.create_tag(
                tag_text,
                {
                    "bgcolor": self.colors.tag_background_color,
                    "color": self.colors.tag_content_color,
                },
            )
            e.control.value = ""
            self.update_tags_display()

    def create_tag(self, tag_text, colors):
        if len(self.tags) < self.max_tags:
            self.add_tag(tag_text, colors)

    def add_tag(self, tag_text, colors):
        if len(self.tags) < self.max_tags and tag_text not in self.tags:
            tag = Badge(
                badge_text=tag_text,
                colors=colors,
                icon=ft.icons.CLOSE,
                on_click=lambda e, badge_text=tag_text: self.remove_tag(e, badge_text),
            )
            self.tags.append(tag_text)
            self.tags_container.controls.append(tag)
            self.update_tags_display()
        else:
            self.text_field.suffix = f"{len(self.tags)}/{self.max_tags} tags"
            self.text_field.update()

    def remove_tag(self, event, tag_text):
        for control in self.tags_container.controls:
            if isinstance(control, Badge) and control.badge_text == tag_text:
                self.tags_container.controls.remove(control)
                break
        self.tags.remove(tag_text)
        self.update_tags_display()

    def update_tags_display(self):
        self.tags_container.update()
        self.text_field.update()
