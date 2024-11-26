import flet as ft
from datetime import datetime, timedelta
import calendar
from time import sleep
from fluentflet.components.button import Button, ButtonVariant
from ..utils import FluentIcon, FluentIcons, FluentIconStyle

class Calendar(ft.Container):
    def __init__(self, on_select=None):
        super().__init__()
        now = datetime.now()
        self.bgcolor = ft.colors.with_opacity(0.2, ft.colors.BLACK)
        self.border_radius = 4
        self.display_date = datetime.now().replace(day=1)
        self.selected_day = {"month": now.month, "day": str(now.day)}
        self.current_day = {"month": now.month, "day": str(now.day)}
        self.view = "days"
        self.scale = ft.transform.Scale(1, alignment=ft.alignment.center)
        self.transform = self.scale
        self.animate_opacity = ft.animation.Animation(300, "easeInOut")
        self.animate_scale = ft.animation.Animation(300, "easeInOut")
        self.width = 340
        self.on_select = on_select
        self.setup_calendar()

    def change_month(self, inc):
        def change(_):
            if self.view == "days":
                if inc:
                    self.display_date = self.display_date.replace(day=28) + timedelta(days=5)
                    self.display_date = self.display_date.replace(day=1)
                else:
                    self.display_date = self.display_date.replace(day=1) - timedelta(days=1)
                    self.display_date = self.display_date.replace(day=1)
            elif self.view == "months":
                year = self.display_date.year + (1 if inc else -1)
                self.display_date = self.display_date.replace(year=year)
            elif self.view == "years":
                year = self.display_date.year + (10 if inc else -10)
                self.display_date = self.display_date.replace(year=year)
            
            self.setup_calendar()
            self.update()
        return change

    def fade_out(self):
        self.opacity = 0
        self.update()

    def fade_in(self):
        self.opacity = 1
        self.update()

    def animate_view_transition(self, going_back=False):
        if going_back:
            self.scale.scale = 0.5
            self.opacity = 0
        else:
            self.scale.scale = 1.5
            self.opacity = 0
        
        self.update()
        self.scale.scale = 1
        self.opacity = 1
        self.update()

    def toggle_view(self, _):
        old_grid = self.content.controls[1]
        old_grid.opacity = 0
        old_grid.scale = ft.transform.Scale(0.5, alignment=ft.alignment.center)
        self.update()
        sleep(0.3)
        
        if self.view == "days":
            self.view = "months"
        elif self.view == "months":
            self.view = "years" 
        elif self.view == "years":
            self.view = "days"
        
        self.setup_calendar()
        new_grid = self.content.controls[1]
        new_grid.opacity = 0  # Start invisible
        new_grid.scale = ft.transform.Scale(1.5, alignment=ft.alignment.center)
        self.update()
        
        sleep(0.1)
        new_grid.opacity = 1  # Fade in
        new_grid.scale = ft.transform.Scale(1, alignment=ft.alignment.center)
        self.update()

    def select_month(self, month_num):
        def select(_):
            self.display_date = self.display_date.replace(month=month_num)
            self.view = "days"
            self.animate_view_transition(False)
            self.setup_calendar()
            self.update()
        return select

    def select_year(self, year):
        def select(_):
            self.display_date = self.display_date.replace(year=year)
            self.view = "months"
            self.animate_view_transition(False)
            self.setup_calendar()
            self.update()
        return select

    def toggle_day_selection(self, day_num):
        def toggle(_):
            current_month = self.display_date.month
            current_year = self.display_date.year
            
            if self.selected_day["month"] == current_month and self.selected_day["day"] == str(day_num):
                self.selected_day = {"month": None, "day": None}
                if self.on_select:
                    self.on_select(None)  # Send None when deselecting
            else:
                self.selected_day = {"month": current_month, "day": str(day_num)}
                # Create datetime object for selected date
                if self.on_select and not day_num.startswith(("-", "+")):  # Only trigger for current month dates
                    selected_date = datetime(
                        year=current_year,
                        month=current_month,
                        day=int(day_num)
                    )
                    self.on_select(selected_date)
            
            self.setup_calendar()
            self.update()
        return toggle

    def setup_calendar(self):
        if self.view == "days":
            self.setup_days_view()
        elif self.view == "months":
            self.setup_months_view()
        else:  # years view
            self.setup_years_view()

    def setup_months_view(self):
        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", 
                "sep", "oct", "nov", "dec"]
        
        header = self.create_header(str(self.display_date.year))
        month_containers = []
        
        for i, month in enumerate(months, 1):
            is_current = i == self.display_date.month
            container = ft.Container(
                ft.Text(month, size=16, color=ft.colors.BLACK if is_current else ft.colors.WHITE70),
                width=70,
                height=70,
                alignment=ft.alignment.center,
                bgcolor="#62cdfe" if is_current else None,
                border_radius=35,
                on_click=self.select_month(i),
            )
            month_containers.append(container)

        grid = ft.Container(
            ft.Column([
                ft.Row(month_containers[i:i+4], 
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                for i in range(0, 12, 4)
            ], spacing=20),
            padding=20,
            bgcolor="#323232",
            animate=ft.animation.Animation(300, "easeInOut"),
            animate_scale=ft.animation.Animation(300, "easeInOut")
        )
        grid.scale = ft.transform.Scale(1, alignment=ft.alignment.center)

        self.content = ft.Column([header, grid], spacing=0, width=self.width)

    def setup_years_view(self):
        base_year = (self.display_date.year // 10) * 10
        header = self.create_header(f"{base_year}–{base_year + 9}")
        year_containers = []
        
        start_year = base_year - 2
        for year in range(start_year, start_year + 16):
            is_current = year == self.display_date.year
            container = ft.Container(
                ft.Text(str(year), size=16, color=ft.colors.BLACK if is_current else ft.colors.WHITE70),
                width=70,
                height=70,
                alignment=ft.alignment.center,
                bgcolor="#62cdfe" if is_current else None,
                border_radius=35,
                on_click=self.select_year(year),
            )
            year_containers.append(container)

        grid = ft.Container(
            ft.Column([
                ft.Row(year_containers[i:i+4],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                for i in range(0, 16, 4)
            ], spacing=20),
            padding=10,
            bgcolor="#323232",
            animate=ft.animation.Animation(300, "easeInOut"),
            animate_scale=ft.animation.Animation(300, "easeInOut")
        )
        grid.scale = ft.transform.Scale(1, alignment=ft.alignment.center)

        self.content = ft.Column([header, grid], spacing=0, width=self.width)

    def setup_days_view(self):
        days = self._get_month_days(self.display_date.year, self.display_date.month)
        weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        month_name = calendar.month_name[self.display_date.month].lower()
        
        header = self.create_header(f"{month_name} {self.display_date.year}")
        weekday_containers = [
            ft.Container(
                ft.Text(day, size=12, color=ft.colors.WHITE),
                alignment=ft.alignment.center,
                padding=5,
            )
            for day in weekdays
        ]

        day_containers = []
        current_month = self.display_date.month
        
        for day in days:
            if day:
                is_selected = (self.selected_day["month"] == current_month and 
                             self.selected_day["day"] == day)
                is_current = (self.current_day["month"] == current_month and 
                            self.current_day["day"] == day)
                
                container = ft.Container(
                        ft.Text(
                            day.lstrip("+-"), 
                            size=16, 
                            color = ft.colors.BLACK if is_current else ("#62cdfe" if is_selected else (ft.colors.WHITE if not day.startswith(("-", "+")) else ft.colors.WHITE24))
                        ),
                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                        bgcolor="#62cdfe" if is_current else None,
                        border=ft.border.all(1, "#62cdfe") if is_selected else None,
                        border_radius=20,
                        on_click=self.toggle_day_selection(day),
                    )
            else:
                container = ft.Container(width=40, height=40)
            day_containers.append(container)

        calendar_grid = ft.Container(
            ft.Column(
                [
                    ft.Row(weekday_containers,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Column(
                        [ft.Row(day_containers[i:i+7],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        for i in range(0, len(day_containers), 7)],
                        spacing=10,
                    )
                ],
                spacing=10,
                tight=True
            ),
            padding=10,
            bgcolor="#323232",
            animate_opacity=300,  # Add animation duration
            opacity=1,  # Initial opacity
            animate=ft.animation.Animation(300, "easeInOut"),
            animate_scale=ft.animation.Animation(300, "easeInOut")
        )
        calendar_grid.scale = ft.transform.Scale(1, alignment=ft.alignment.center)

        self.content = ft.Column([header, calendar_grid], spacing=0, width=self.width)
        return calendar_grid  # Return for animation control

    def create_header(self, title):
        return ft.Container(
            ft.Row(
                [
                    Button(
                        content=ft.Text(title, size=16, color=ft.colors.WHITE),
                        variant=ButtonVariant.HYPERLINK,
                        on_click=self.toggle_view,
                    ),
                    ft.Row(
                        [
                            Button(
                                content=ft.Icon(name=ft.icons.ARROW_DROP_UP, size=20, color="#ffffff"),
                                variant=ButtonVariant.HYPERLINK,
                                on_click=self.change_month(False)
                            ),
                            Button(
                                content=ft.Icon(name=ft.icons.ARROW_DROP_DOWN, size=20, color="#ffffff"),
                                variant=ButtonVariant.HYPERLINK,
                                on_click=self.change_month(True)
                            )
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
            bgcolor="#2b2b2b"
        )

    def _get_month_days(self, year, month):
        # Get days of current month
        matrix = calendar.monthcalendar(year, month)
        
        # Get last days of previous month
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
        
        days = []
        for week in matrix:
            for day in week:
                if day == 0:
                    if len(days) < 7:  # First week
                        # Add days from previous month
                        prev_day = prev_month_days - (6 - len(days)) + 1
                        days.append(f"-{prev_day}")
                    else:  # Last week
                        # Add days from next month
                        next_day = len([d for d in days if d and not d.startswith('-')]) % 31 + 1
                        days.append(f"+{next_day}")
                else:
                    days.append(str(day))
                    
        return days