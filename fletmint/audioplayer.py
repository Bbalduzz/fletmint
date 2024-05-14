import flet as ft


class AudioPlayer(ft.UserControl):
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.audio_state = {
            "is_playing": False,
            "is_paused": False,
            "is_stopped": False,
            "duration": 0,
            "current_position": 0,
        }
        self.kwargs = kwargs
        self.setup_audio()
        self.build_audioplayer()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{int(mins):02}:{int(secs):02}"

    def update_total_time(self):
        self.total_time.value = self.format_time(self.audio_state["duration"])
        self.total_time.update()

    def update_duration(self, seconds):
        self.audio_state["current_position"] = seconds
        self.position_slider.value = (
            (seconds / self.audio_state["duration"]) * self.position_slider.max
            if self.audio_state["duration"] > 0
            else 0
        )
        self.position_slider.update()
        self.time_elapsed.value = self.format_time(seconds)
        self.time_elapsed.update()

    def on_slider_change(self, e):
        new_position = (e.control.value / 100) * self.audio_state["duration"]
        self.audio.position = new_position * 1000  # Set position in milliseconds
        self.update_duration(new_position)

    def seek(self, seconds):
        new_position = max(
            0,
            min(
                self.audio_state["duration"],
                self.audio_state["current_position"] + seconds,
            ),
        )  # Ensure within bounds
        self.audio.position = new_position * 1000  # Set position in milliseconds
        self.update_duration(new_position)

    def handle_play_or_pause(self, e):
        if self.audio_state["is_playing"]:
            self.audio.pause()
            self.audio_state["is_playing"] = False
            self.audio_state["is_paused"] = True
            new_icon = ft.Icon(name=ft.icons.PLAY_ARROW_ROUNDED)
        # Check if the audio is paused
        elif self.audio_state["is_paused"]:
            self.audio.resume()
            self.audio_state["is_playing"] = True
            self.audio_state["is_paused"] = False
            new_icon = ft.Icon(name=ft.icons.PAUSE_ROUNDED)
        # If the audio is neither playing nor paused (stopped or initial state)
        elif self.audio_state["is_stopped"]:
            self.audio_state["is_playing"] = False
            self.audio_state["is_paused"] = False
            self.audio_state["is_stopped"] = False
            new_icon = ft.Icon(name=ft.icons.PLAY_ARROW_ROUNDED)
        else:
            self.audio.play()
            self.audio_state["is_playing"] = True
            self.audio_state["is_paused"] = False
            self.audio_state["is_stopped"] = False
            new_icon = ft.Icon(name=ft.icons.PAUSE_ROUNDED)

        if self.play_button.content != new_icon:
            self.play_button.content = new_icon
            self.play_button.update()

    def setup_audio(self):
        self.audio = ft.Audio(
            src=self.url,
            autoplay=False,
            volume=1,
            balance=0,
            on_loaded=lambda _: print("Audio Loaded"),
            on_duration_changed=lambda e: (
                self.audio_state.update({"duration": int(e.data) / 1000}),
                self.update_total_time(),
            ),
            on_position_changed=lambda e: self.update_duration(int(e.data) / 1000),
            on_state_changed=lambda e: (
                print("State changed:", e.data),
                self.audio_state.update(
                    {"is_playing": e.data == "playing", "is_paused": e.data == "paused"}
                ),
            ),
            on_seek_complete=lambda e: (
                self.audio_state.update({"is_stopped": True}),
                self.handle_play_or_pause(e),
            ),
        )

    def build_audioplayer(self):
        self.time_elapsed = ft.Text("00:00")
        self.total_time = ft.Text("00:00")
        self.position_slider = ft.Slider(
            thumb_color=ft.colors.with_opacity(0, "white"),
            overlay_color=ft.colors.with_opacity(0, "white"),
            secondary_track_value=ft.colors.with_opacity(0, "white"),
            active_color="#1f5eff",
            inactive_color="#323741",
            max=100,
            on_change=self.on_slider_change,
        )
        self.play_button = ft.TextButton(
            on_click=self.handle_play_or_pause,
            content=ft.Icon(name=ft.icons.PLAY_ARROW_ROUNDED),
            style=ft.ButtonStyle(
                color="#ffffff",
                bgcolor="#1f5eff",
                shape=ft.CircleBorder(),
                padding=15,
            ),
        )
        self.audio_player = ft.Container(
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.REPLAY_10_ROUNDED,
                                icon_color="#ffffff,0.5",
                                on_click=lambda _: self.seek(-10),
                            ),
                            self.play_button,
                            ft.IconButton(
                                icon=ft.icons.FORWARD_10_ROUNDED,
                                icon_color="#ffffff,0.5",
                                on_click=lambda _: self.seek(10),
                            ),
                        ],
                        spacing=0,
                    ),
                    self.position_slider,
                    ft.Row(
                        [
                            self.time_elapsed,
                            ft.Text("/"),
                            self.total_time,
                        ],
                        spacing=1,
                    ),
                ],
                spacing=3,
            ),
            width=450,
            padding=ft.padding.symmetric(vertical=5, horizontal=15),
            bgcolor="#323741",
            border=ft.border.all(1, "#3d424d"),
            border_radius=14,
        )

    def build(self):
        return self.audio_player
