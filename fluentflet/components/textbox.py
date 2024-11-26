import flet as ft
from ..utils import FluentIcon, FluentIcons, FluentIconStyle
from ..utils.fluent_design_system import FluentDesignSystem
from fluentflet.components.button import Button, ButtonVariant

class TextBox(ft.Container):
    def __init__(
        self,
        placeholder: str = "TextBox",
        width: int = 200,
        text_size: int = 14,
        height: int = 32,
        right_icon = None,
        password: bool = False,
        **kwargs
    ):
        # enable **kwargs also for TextField
        textfield_props = set(dir(ft.TextField)) - set(dir(ft.Container))
        # filter out private methods/attributes (those starting with _)
        textfield_props = {prop for prop in textfield_props if not prop.startswith('_')}
        textfield_kwargs = {k: kwargs.pop(k) for k in dict(kwargs) if k in textfield_props}

        super().__init__(**kwargs)
        self.theme = FluentDesignSystem().dark_theme
        self.width = width
        self.height = height + 2
        self.default_bgcolor = self.theme.fills.get_fill("control_fill_default")
        self.bgcolor = self.theme.fills.get_fill("control_fill_default")
        self.focused_bgcolor = self.theme.fills.get_fill("control_fill_secondary")
        self.is_password = password

        self._action = None
        
        # Create the text field with adjusted width for button space
        self.textfield = ft.TextField(
            border=ft.InputBorder.NONE,
            height=height,
            text_size=text_size,
            password=password,
            bgcolor=ft.colors.TRANSPARENT,
            color=ft.colors.WHITE,
            cursor_color=ft.colors.WHITE,
            cursor_height=16,
            cursor_width=1,
            hint_text=placeholder,
            hint_style=ft.TextStyle(
                color=ft.colors.WHITE54,
                size=text_size,
                weight=ft.FontWeight.W_400
            ),
            on_focus=self._handle_focus,
            on_blur=self._handle_blur,
            content_padding=ft.padding.only(left=10, right=40, bottom=12),  # Increased right padding
            **textfield_kwargs
        )
        
        # Create the search button
        self.action_button = Button( #textbutton
            content=right_icon,
            variant=ButtonVariant.HYPERLINK,
            # custom_color=ft.colors.with_opacity(0.786, "#ffffff"),
            width=32,
            height=32,
            on_click=self._handle_button_click
        )

        # Create the bottom border
        self.bottom_border = ft.Container(
            width=width,
            height=1,
            bgcolor=ft.colors.WHITE24,
        )
        
        # Setup container properties
        self.content = ft.Stack(
            controls=[
                # Main content container
                ft.Container(
                    content=self.textfield,
                    width=width,
                    height=height,
                ),
                # Search button positioned on the right
                ft.Container(
                    content=self.action_button,
                    right=4,
                    top=0,
                ),
                # Bottom border positioned at the bottom
                ft.Container(
                    content=self.bottom_border,
                    bottom=0,
                    width=width,
                )
            ],
        )
        self.width = width
        self.bgcolor = self.theme.fills.get_fill("control_fill_default")
        self.border_radius = 4
        self.padding = 0

    def _get_button_icon(self):
        if self.is_password:
            return FluentIcon(name=FluentIcons.EYE_SHOW if self.textfield.password else FluentIcons.EYE_HIDE, style=FluentIconStyle.FILLED, size=16)
        return FluentIcon(name="SEARCH", size=16)

    def _handle_button_click(self, e):
        if self.is_password:
            # Toggle password visibility
            self.textfield.password ^= True
            self.action_button.content = self._get_button_icon()
            self.update()
        elif self._action:
            self._action(e)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, func):
        self._action = func

    def _handle_focus(self, e):
        self.bgcolor = "#1f1f1f"
        self.bottom_border.bgcolor = self.theme.colors.get_color("accent_default")
        self.bottom_border.height = 1.5
        self.update()

    def _handle_blur(self, e):
        self.bgcolor = self.default_bgcolor
        self.bottom_border.bgcolor = ft.colors.WHITE24
        self.bottom_border.height = 1
        self.update()

    @property
    def value(self):
        return self.textfield.value

    @value.setter
    def value(self, value):
        self.textfield.value = value
        self.update()