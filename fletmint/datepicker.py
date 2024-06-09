import flet as ft
from .text_input import TextInput
from .button import Button, SecondaryButton
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import locale, time


@dataclass
class DatePickerColors:
    container_background_color: str
    container_border_color: str
    weekday_color: str
    selected_date_background_color: str
    today_button_border_color: str
    today_button_background_color: str
    default_day_background_color: str
    today_text_color: str
    filler_day_text_color: str
    default_day_text_color: str
    dropdown_starter_icon_color: str

    @staticmethod
    def dark():
        return DatePickerColors(
            container_background_color="#323741",
            container_border_color="#3d424d",
            weekday_color="#4a505b",
            selected_date_background_color="#1f5eff",
            today_button_border_color="#325de3",
            today_button_background_color="#314276",
            default_day_background_color="#3c414a",
            today_text_color="#ffffff",
            filler_day_text_color="#4a505b",
            default_day_text_color="#b0b8cc",
            dropdown_starter_icon_color="#ffffff",
        )

    @staticmethod
    def light():
        return DatePickerColors(
            container_background_color="#ffffff",
            container_border_color="#e0e4ed",
            weekday_color="#EBEBEB",
            selected_date_background_color="#1f5eff",
            today_button_border_color="#1f5eff",
            today_button_background_color="#1f5eff",
            default_day_background_color="#EBF1FF",
            today_text_color="#ffffff",
            filler_day_text_color="#EBEBEB",
            default_day_text_color="#A8B1C7",
            dropdown_starter_icon_color="#7e879e",
        )


class DatePicker(ft.UserControl):
    def __init__(
        self,
        tz_info=timezone.utc,
        left_content=None,
        max_width=300,
        is_dropdown=True,
        multi_select_mode=True,
        show_today=True,
        animated=False,
        on_date_choosen=None,
        on_cancel=None,
        theme: ft.ThemeMode | str = ft.ThemeMode.DARK,
        drodown_icons=[
            ft.icons.ARROW_DROP_DOWN_ROUNDED,
            ft.icons.ARROW_DROP_UP_ROUNDED,
        ],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.tz_info = tz_info
        self.left_content = left_content
        self.max_width = max_width
        self.is_dropdown = is_dropdown
        self.show_today = show_today
        self.on_date_choosen = on_date_choosen
        self.on_cancel = on_cancel
        self.multi_select_mode = multi_select_mode
        self.animated = animated
        self.dropdown_icons = drodown_icons
        self.selected_dates = set()
        self.current_month = datetime.now(self.tz_info).month
        self.current_year = datetime.now(self.tz_info).year
        self.colors = (
            DatePickerColors.dark()
            if theme == ft.ThemeMode.DARK
            else DatePickerColors.light()
        )
        self.show_splash = False
        self._dropdown_starter_bounds = None
        self.previous_selected_button = None

    def did_mount(self):
        self.page.on_scroll = self.on_page_scroll
        self.page.update()

    def on_page_scroll(self, e):
        if self.show_splash:
            if e.event_type == "update":
                new_position_y = (
                    self._dropdown_starter_bounds["bottom_left"][1] - e.pixels
                )

                # Check if the new position is within the viewport
                if self.is_within_viewport(new_position_y):
                    self.page.splash = self.update_dropdown_position(
                        (
                            self._dropdown_starter_bounds["bottom_left"][0],
                            new_position_y,
                        )
                    )
                else:
                    # hide the splash if it is out of viewport
                    self.page.splash = None

                self.page.update()

    def is_within_viewport(self, y_position):
        viewport_height = self.page.height
        return 0 <= y_position <= viewport_height

    def __on_selected_date(self, e):
        dates = [date.strftime("%Y-%m-%d") for date in self.selected_dates]
        if self.is_dropdown:
            self.dropdown_starter.content.content.controls[0].content.content.controls[
                0
            ].value = ", ".join(dates)
            self.unfocus_dropdown()
            if self.animated:
                self.animate_dropdown(toggle=False)
            self.close_calendar_dropdown()
        if self.on_date_choosen:
            self.on_date_choosen(self.selected_dates)

    def __on_cancel(self, e):
        if self.is_dropdown:
            self.unfocus_dropdown()
            self.close_calendar_dropdown()
        if self.on_cancel:
            self.on_cancel()

    def unfocus_dropdown(self):
        self.dropdown_starter.content.content.controls[0].remove_hover_state(None)
        self.dropdown_starter.content.content.controls[1].content = ft.Icon(
            name=self.dropdown_icons[0],
            color=self.colors.dropdown_starter_icon_color,
            size=25,
        )
        self.dropdown_starter.update()

    def close_calendar_dropdown(self):
        self.page.splash = None
        self.show_splash = False
        self.page.update()

    def adjust_month(self, change):
        new_month = self.current_month + change
        if new_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif new_month < 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month = new_month
        self.update_calendar()

    def update_calendar(self):
        self.calendarpicker.content.controls[1] = self.build_calendar()
        self.calendarpicker.content.controls[0].controls[1].value = datetime(
            self.current_year, self.current_month, 1
        ).strftime("%B %Y")
        self.calendarpicker.update()

    def build_calendar(self):
        grid = ft.GridView(
            controls=[
                ft.Container(
                    ft.Text(day, color=self.colors.weekday_color),
                    alignment=ft.alignment.center,
                )
                for day in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
            ],
            runs_count=7,
            spacing=4,
            run_spacing=4,
            padding=ft.padding.all(10),
        )

        self.today = datetime.now(self.tz_info)
        start_of_month = datetime(self.current_year, self.current_month, 1)
        start_day_of_week = start_of_month.weekday()
        end_of_month = start_of_month.replace(
            month=start_of_month.month % 12 + 1, day=1
        ) - timedelta(days=1)
        days_in_month = end_of_month.day

        filler_days = (start_day_of_week + 7) % 7
        for i in range(filler_days):
            day = (start_of_month - timedelta(days=filler_days - i)).day
            grid.controls.append(self.create_day_button(str(day), is_filler=True))

        for i in range(1, days_in_month + 1):
            day = datetime(self.current_year, self.current_month, i)
            if not self.show_today:
                is_today = False
            else:
                is_today = (
                    self.current_month == self.today.month
                    and self.current_year == self.today.year
                    and i == self.today.day
                )
            button = self.create_day_button(str(i), is_today=is_today, day_date=day)
            grid.controls.append(button)

        next_month_day_count = (7 - (end_of_month.weekday() + 1)) % 7
        for i in range(1, next_month_day_count + 1):
            grid.controls.append(self.create_day_button(str(i), is_filler=True))

        return grid

    def create_day_button(self, text, is_today=False, is_filler=False, day_date=None):
        bgcolor = (
            self.colors.today_button_background_color
            if is_today
            else ""
            if is_filler
            else self.colors.default_day_background_color
        )
        bordercolor = (
            self.colors.today_button_border_color
            if is_today
            else ft.colors.with_opacity(0, "white")
            if is_filler
            else self.colors.default_day_background_color
        )
        button = ft.TextButton(
            text=text,
            width=50,
            height=50,
            data=day_date,
            on_click=self.select_day,
            style=ft.ButtonStyle(
                bgcolor=bgcolor,
                side=ft.BorderSide(1, bordercolor),
                color=self.colors.today_text_color
                if is_today
                else self.colors.filler_day_text_color
                if is_filler
                else self.colors.default_day_text_color,
                shape=ft.ContinuousRectangleBorder(radius=12),
                padding=2,
            ),
        )
        if is_filler:
            button.enabled = False
        return button

    def select_day(self, e):
        day_button = e.control
        day_date = day_button.data
        if not day_date:
            return

        if self.multi_select_mode:
            if day_date in self.selected_dates:
                self.selected_dates.remove(day_date)
                day_button.style.bgcolor = self.colors.default_day_background_color
                day_button.style.color = self.colors.default_day_text_color
            else:
                self.selected_dates.add(day_date)
                day_button.style.bgcolor = self.colors.selected_date_background_color
                day_button.style.color = self.colors.today_text_color
        else:
            for button in self.calendarpicker.content.controls[1].controls:
                if (
                    isinstance(button, ft.TextButton)
                    and button.data in self.selected_dates
                ):
                    button.style.bgcolor = self.colors.default_day_background_color
                    button.style.color = self.colors.default_day_text_color
                    button.update()

            self.selected_dates.clear()
            self.selected_dates.add(day_date)
            day_button.style.bgcolor = self.colors.selected_date_background_color
            day_button.style.color = self.colors.today_text_color

        day_button.update()

    def animate_dropdown(self, toggle=False):
        self.calendarpicker.height = 0 if not toggle else 350
        self.calendarpicker.opacity = 0 if not toggle else 1
        self.calendarpicker.update()
        time.sleep(0.4)

    def build_calendarpicker(self):
        def on_control_click(e):
            print(e.control)

        if not self.left_content:
            self.left_content = SecondaryButton(
                height=40, width=130, on_click=self.__on_cancel
            )

        self.calendarpicker = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ARROW_CIRCLE_LEFT_ROUNDED,
                                icon_color=self.colors.default_day_text_color,
                                on_click=lambda e: self.adjust_month(-1),
                            ),
                            ft.Text(
                                datetime(
                                    self.current_year, self.current_month, 1
                                ).strftime("%B %Y"),
                                size=15,
                            ),
                            ft.IconButton(
                                icon=ft.icons.ARROW_CIRCLE_RIGHT_ROUNDED,
                                icon_color=self.colors.default_day_text_color,
                                on_click=lambda e: self.adjust_month(1),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.build_calendar(),
                    ft.Row(
                        [
                            self.left_content,
                            Button(
                                height=40,
                                width=130,
                                label="Choose Date",
                                on_click=self.__on_selected_date,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=2,
            ),
            padding=10,
            bgcolor=self.colors.container_background_color,
            border=ft.border.all(2, self.colors.container_border_color),
            border_radius=10,
            width=self.max_width,
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=3,
                color=ft.colors.BLACK,
                offset=ft.Offset(0, 1),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

        if self.animated:
            self.calendarpicker.opacity = 0
            self.calendarpicker.height = 0
            self.calendarpicker.animate = ft.animation.Animation(
                duration=400, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT
            )
            self.calendarpicker.animate_opacity = ft.animation.Animation(
                duration=400, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT
            )
            # self.calendarpicker.update()

        return self.calendarpicker

    def build_dropdown_calendarpicker(self):
        self.calendar_dropdown = self.build_calendarpicker()
        self.dropdown_starter = ft.Container(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap_down=self.toggle_dropdown,
                content=ft.Stack(
                    [
                        TextInput(dense=True),
                        ft.Container(
                            ft.Icon(
                                name=self.dropdown_icons[0],
                                color=self.colors.default_day_text_color,
                                size=25,
                            ),
                            right=0,
                            bottom=17,
                            padding=ft.padding.only(right=20),
                        ),
                    ]
                ),
            ),
            width=self.max_width,
        )
        return self.dropdown_starter

    def toggle_dropdown(self, e):
        if self.show_splash:
            if self.animated:
                self.animate_dropdown(toggle=False)
            self.unfocus_dropdown()
            self.close_calendar_dropdown()
        else:
            self.dropdown_starter.content.content.controls[0].set_hover_state(None)
            self.dropdown_starter.content.content.controls[1].content = ft.Icon(
                name=self.dropdown_icons[1],
                color=self.colors.default_day_text_color,
                size=25,
            )
            self._dropdown_starter_bounds = self.calculate_bounds(e)
            self.page.splash = self.update_dropdown_position(
                self._dropdown_starter_bounds["bottom_left"]
            )
            self.show_splash = True

        self.dropdown_starter.update()
        self.page.update()
        if self.animated:
            time.sleep(0.01)
            self.animate_dropdown(toggle=True)

    def calculate_bounds(self, event, height=50):
        top_left = (event.global_x - event.local_x, event.global_y - event.local_y)
        return {
            "top_left": top_left,
            "top_right": (top_left[0] + self.max_width, top_left[1]),
            "bottom_left": (top_left[0], top_left[1] + float(height)),
            "bottom_right": (top_left[0] + self.max_width, top_left[1] + float(height)),
        }

    def update_dropdown_position(self, bottom_left):
        dropdown = self.calendar_dropdown
        dropdown.top = bottom_left[1] + 20
        dropdown.left = bottom_left[0]
        return dropdown

    def build(self):
        if self.is_dropdown:
            return self.build_dropdown_calendarpicker()
        else:
            return self.build_calendarpicker()
