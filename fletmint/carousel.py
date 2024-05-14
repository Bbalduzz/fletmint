import flet as ft
import threading


class Carousel(ft.UserControl):
    def __init__(
        self,
        images_list,
        animations,
        compact=False,
        descriptive=False,
        transform_factor=1.0,
    ):
        super().__init__()
        self.images_list = images_list
        self.number_of_items = len(images_list)
        self.current_image_index = 0
        self.animation_in, self.animation_out = animations
        self.descriptive = descriptive
        self.compact = compact
        self.transform_factor = transform_factor  # Scaling factor for image sizes
        self.carousel = self.build_carousel()

    def update_image_view(self, index, main_image=False):
        """
        Helper function to create image view for the given index, handling wraparounds.
        If main_image is True, the image will be larger and include a description if descriptive mode is on.
        """
        index = index % self.number_of_items  # Wrap-around logic
        src = self.images_list[index][0]
        description = (
            self.images_list[index][1] if self.descriptive and main_image else ""
        )
        # Apply transform_factor to dimensions
        base_width, base_height = (500, 300) if main_image else (300, 200)
        width = base_width * self.transform_factor
        height = base_height * self.transform_factor
        image = ft.Container(
            ft.Image(
                src=src, fit=ft.ImageFit.FILL, border_radius=ft.border_radius.all(5)
            ),
            margin=5,
        )
        container = ft.Container(image, width=width, height=height)

        if self.descriptive and main_image:
            return ft.Column(
                [container, ft.Text(description)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        return container

    def build_carousel(self):
        def navigate(offset):
            """Updates the current image index and refreshes the carousel view"""
            self.current_image_index = (
                self.current_image_index + offset
            ) % self.number_of_items
            if not self.compact:
                carousel_row.content.controls = [
                    self.update_image_view(self.current_image_index - 1),
                    self.update_image_view(self.current_image_index, main_image=True),
                    self.update_image_view(self.current_image_index + 1),
                ]
            else:
                carousel_row.content.controls = [
                    self.update_image_view(self.current_image_index, main_image=True)
                ]
            self.update()

        if not self.compact:
            carousel_content_row = [
                self.update_image_view(self.current_image_index - 1),
                self.update_image_view(self.current_image_index, main_image=True),
                self.update_image_view(self.current_image_index + 1),
            ]
        else:
            carousel_content_row = [
                self.update_image_view(self.current_image_index, main_image=True)
            ]

        carousel_row = ft.AnimatedSwitcher(
            ft.Row(
                carousel_content_row,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=500,
            switch_in_curve=self.animation_in,
            switch_out_curve=self.animation_out,
        )

        # Navigation Buttons
        prev_button = ft.FloatingActionButton(
            icon=ft.icons.NAVIGATE_BEFORE_ROUNDED,
            on_click=lambda _: navigate(-1),
            bgcolor=ft.colors.TRANSPARENT,
            shape=ft.CircleBorder(),
        )
        next_button = ft.FloatingActionButton(
            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
            on_click=lambda _: navigate(1),
            bgcolor=ft.colors.TRANSPARENT,
            shape=ft.CircleBorder(),
        )

        # Assembling the complete carousel
        return ft.Row(
            [prev_button, carousel_row, next_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def build(self):
        return self.carousel
