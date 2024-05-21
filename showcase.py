import flet as ft
from fletmint import *


def main(page: ft.Page):
    page.fonts = {
        "JetBrainsMono": "C:\\Users\\edoar\\Documents\\work\\fletmint_dev\\dev\\JetBrainsMono-Regular.ttf",
        "SourceCodePro": "/Users/edoardo/Projects/flet-lucide/SourceCodePro.ttf",
    }
    page.window_width = 1680
    page.window_height = 850
    page.padding = 50
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = True
    page.bgcolor = "#22242a"

    def checkbox_changed(e):
        print(f"Checkbox value changed to {e}")

    def toggle_change(e):
        print(f"Toggle value changed")

    def get_selected_dates(e):
        print(calendar.selected_dates)

    def change_theme(value):
        page.theme_mode = ft.ThemeMode.LIGHT if value else ft.ThemeMode.DARK
        slider.toggle_theme()
        page.update()

    def show_password(e):
        e.control.parent.parent.controls[0].password ^= True
        e.control.parent.parent.controls[0].update()
        e.control.icon = (
            ft.icons.LOCK_OPEN_ROUNDED
            if e.control.icon == ft.icons.LOCK_ROUNDED
            else ft.icons.LOCK_ROUNDED
        )
        e.control.update()

    # == flethoff ==
    tab_switch = TabSwitch(
        ["Label", "Label", "Label"],
        on_switch=lambda value: print(f"Switched to tab {value}"),
    )
    toggle_switch = ToggleSwitch(on_switch=change_theme)
    checkboxes = ft.Column(
        [
            CheckBox(
                disabled=False, label="Label", checked=False, on_click=checkbox_changed
            ),
            CheckBox(
                disabled=False, label="Label", checked=True, on_click=checkbox_changed
            ),
            CheckBox(
                disabled=True, label="Label", checked=False, on_click=checkbox_changed
            ),
        ]
    )
    radio_group = ft.RadioGroup(
        content=ft.Column(
            [
                Radio(
                    value="red",
                    label="Label",
                ),
                Radio(
                    value="blue",
                    label="Label",
                ),
                Radio(
                    value="green",
                    label="Label",
                ),
            ]
        )
    )
    buttons = ft.Column(
        [Button(), Button(disabled=True), DestructiveButton(), SecondaryButton()]
    )
    dropdown = Dropdown(
        max_width=250,
        controls=[
            "figma",
            "sketch",
            "invision studio",
            "framer",
            "adobe xd",
        ],
        on_select=lambda e: print(f"Selected: {e}"),
    )
    user_profile = UserProfile(
        username="Edoardo B.",
        avatar_foreground_img="https://fiverr-res.cloudinary.com/image/upload/t_profile_original,q_auto,f_auto/v1/attachments/profile/photo/e6ee5c5f29487a42edba6bd2914fee74-1707225777335/002e6712-84fc-4d83-9b26-e5fd2f26739a.jpg",
        status=ProfileStatus.PRIVATE,
    )
    tags_input = TagsInput(max_width=300)
    text_input = TextInput(
        prefix=ft.Icon(name=ft.icons.SEARCH, color=ft.colors.GREY_200, size=18),
        suffix=ft.CircleAvatar(
            foreground_image_src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
            radius=30,
        ),
    )
    password_input = TextInput(
        password=True,
        suffix=ft.IconButton(
            icon=ft.icons.LOCK_ROUNDED,
            icon_color="#e3e2e2",
            icon_size=10,
            splash_radius=0,
            on_click=show_password,
        ),
    )
    inputs = ft.Row(
        [text_input, password_input, tags_input],
        width=page.window_width,
    )
    stepper = Stepper(initial_value=123)
    slider = Slider(theme_mode=page.theme_mode)
    toggles = ft.Column(
        [
            Toggle(label="Light", value=False, on_change=toggle_change),
            Toggle(label="Dark", on_change=toggle_change),
        ]
    )

    calendar_dropdown = DatePicker(
        is_dropdown=True,
        show_today=False,
        multi_select_mode=True,
        left_content=ft.TextButton(
            text="Share Dates",
            on_click=lambda e: print(calendar_dropdown.selected_dates),
        ),
        on_date_choosen=lambda values: print(
            f"Selected dates: {[value.strftime('%Y-%m-%d') for value in values]}"
        ),
    )
    calendar = DatePicker(
        is_dropdown=False,
        show_today=True,
        multi_select_mode=False,
        on_date_choosen=lambda values: print(
            f"Selected dates: {[value.strftime('%d-%m-%y') for value in values]}"
        ),
        on_cancel=lambda: print("DatePicker on_cancel fired"),
    )
    badge = Badge(
        badge_text="Success",
        colors=BadgeColors.WARNING,
        icon=ft.icons.CLOSE,
        on_click=lambda e: print("cliked"),
    )
    badge2 = Badge(
        badge_text="Warning",
        colors=BadgeColors.SUCCESS,
        icon=ft.icons.CLOSE,
        on_click=lambda e: print("cliked"),
    )
    bagde3 = Badge(
        badge_text="Error",
        colors=BadgeColors.ERROR,
        icon=ft.icons.CLOSE,
        on_click=lambda e: print("cliked"),
    )

    audio_player = AudioPlayer(
        url="https://dn720301.ca.archive.org/0/items/the-concert-for-george-harrison/Concert%20for%20George%20Disc%202%2F17%20While%20My%20Guitar%20Gently%20Weeps.mp3"
    )
    page.overlay.append(audio_player.audio)

    video_player = VideoPlayer(
        playlist=[
            ft.VideoMedia(
                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
            ),
            ft.VideoMedia(
                "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
            ),
            ft.VideoMedia(
                "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
            ),
        ],
        player_title="Demo video by Bbalduzz",
    )

    carousel = Carousel(
        [
            (
                "https://images.unsplash.com/photo-1714891203404-b25f32706e0a?q=80&w=2370&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "image description 1",
            ),
            (
                "https://images.unsplash.com/photo-1714837291207-4985c06c9a60?q=80&w=2371&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "image description 2",
            ),
            (
                "https://images.unsplash.com/photo-1715109429876-e00fbe6c4ae3?q=80&w=2370&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "image description 3",
            ),
            (
                "https://plus.unsplash.com/premium_photo-1714115035000-023149febb01?q=80&w=2370&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "image description 4",
            ),
            (
                "https://images.unsplash.com/photo-1714836992953-b8f7b4dc8afc?q=80&w=2371&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "image description 5",
            ),
        ],
        [ft.AnimationCurve.EASE_IN, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED],
        compact=False,
        descriptive=False,
        transform_factor=0.5,
    )

    code_editor = Code(
        language="python",
        # font="https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",
        height=800,
        theme=CodeTheme.AYU_DARK,
        read_only=False,
    )

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text("Text Input", color=ft.colors.GREY_600),
                                text_input,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Password Input", color=ft.colors.GREY_600),
                                password_input,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Tags Input", color=ft.colors.GREY_600),
                                tags_input,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Stepper", color=ft.colors.GREY_600),
                                stepper,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Tabs", color=ft.colors.GREY_600),
                                tab_switch,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Button", color=ft.colors.GREY_600),
                                buttons,
                            ]
                        ),
                    ]
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text("Dropdown", color=ft.colors.GREY_600),
                                dropdown,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Calendar (dropdown=True)", color=ft.colors.GREY_600
                                ),
                                calendar_dropdown,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Calendar", color=ft.colors.GREY_600),
                                calendar,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Badges", color=ft.colors.GREY_600),
                                ft.Row([badge, badge2, bagde3]),
                            ]
                        ),
                    ]
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text("CheckBoxes", color=ft.colors.GREY_600),
                                checkboxes,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Radio Group", color=ft.colors.GREY_600),
                                radio_group,
                            ],
                        ),
                        ft.Column(
                            [
                                ft.Text("Toggle Switch", color=ft.colors.GREY_600),
                                toggle_switch,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Slider", color=ft.colors.GREY_600),
                                slider,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Toggles", color=ft.colors.GREY_600),
                                toggles,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("User Profile", color=ft.colors.GREY_600),
                                user_profile,
                            ]
                        ),
                    ]
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text("Carousel", color=ft.colors.GREY_600),
                                carousel,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Audio Player", color=ft.colors.GREY_600),
                                audio_player,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Video Player", color=ft.colors.GREY_600),
                                video_player,
                            ]
                        ),
                    ]
                ),
            ],
            spacing=30,
        ),
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Code Editor", color=ft.colors.GREY_600),
                        code_editor,
                    ]
                ),
            ]
        ),
    )
    tag_text = "Bbalduzz"
    tag_colors = {"bgcolor": "#5b4e42", "color": "#c28845"}
    tags_input.create_tag(tag_text, tag_colors)


ft.app(target=main)
