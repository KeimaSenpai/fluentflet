'''
import flet as ft
from typing import Union
from enum import Enum
from ..utils import FluentIcon

class ButtonVariant(Enum):
    DEFAULT = "default"
    ACCENT = "accent"
    HYPERLINK = "hyperlink"
    TOGGLE = "toggle"

class Button(ft.TextButton):
    def __init__(
        self,
        content: Union[str, ft.Control] = None,
        variant: ButtonVariant = ButtonVariant.DEFAULT,
        height=35,
        custom_color=None,
        **kwargs
    ):
        self.is_toggled = False
        self._variant = variant
        
        # Define style configurations for each variant
        styles = {
            ButtonVariant.DEFAULT: {
                "bgcolor": {
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(0.061, "#ffffff"),
                    # ft.ControlState.HOVERED: ft.colors.with_opacity(0.084, "#ffffff"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.033, "#ffffff"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.042, "#ffffff")
                },
                "side": {
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.with_opacity(0.0578, "#ffffff")),
                    ft.ControlState.HOVERED: ft.BorderSide(1, ft.colors.with_opacity(0.078, "#ffffff")),
                },
                "color": {
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(1, "#ffffff"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.786, "#ffffff"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.368, "#ffffff"),
                }
            },
            ButtonVariant.ACCENT: {
                "bgcolor": {
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(1, "#62cdfe"),
                    ft.ControlState.HOVERED: ft.colors.with_opacity(0.9, "#62cdfe"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.8, "#62cdfe"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.16, "#ffffff")
                },
                "side": {
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.with_opacity(0.08, "#000000")),
                    ft.ControlState.HOVERED: ft.BorderSide(1, ft.colors.with_opacity(0.078, "#ffffff")),
                },
                "color": {
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(1, "#000000"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.53, "#000000"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.368, "#000000"),
                }
            },
            ButtonVariant.HYPERLINK: {
                "bgcolor": { 
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(0, "#ffffff"),
                    ft.ControlState.HOVERED: ft.colors.with_opacity(0.06, "#ffffff"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.0419, "#ffffff"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.0, "#ffffff")
                },
                "color": {
                    ft.ControlState.DEFAULT: ft.colors.with_opacity(1, "#9aecfe"),
                    ft.ControlState.PRESSED: ft.colors.with_opacity(0.8, "#9aecfe"),
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.368, "#ffffff"),
                },
                "side": ft.BorderSide(0, ft.colors.with_opacity(0, "#000000")),
            }
        }

        # Get style configuration for the selected variant
        self.styles = styles
        style_config = self._get_style_config()

        is_icon_only = isinstance(content, (ft.Icon, ft.Image, FluentIcon))
        if not is_icon_only:
            content = content if isinstance(content, ft.Control) else ft.Text(content)

        # Create button style with conditional padding
        button_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            bgcolor=style_config["bgcolor"],
            side=style_config["side"],
            color=style_config["color"] if not custom_color else custom_color,
            overlay_color=ft.colors.TRANSPARENT,
            padding=ft.padding.all(4) if is_icon_only else ft.padding.only(right=18, left=18, top=4, bottom=6),
            visual_density=ft.VisualDensity.STANDARD,
            animation_duration=100,
        )

        # Set width based on content
        width = kwargs.pop('width', None)
        if width is None:
            width = 32 if is_icon_only else None  # Auto width for text

        # Store the original on_click handler if provided
        self._user_on_click = kwargs.pop('on_click', None)
        
        super().__init__(
            content=content,
            style=button_style,
            width=width,
            height=32 if is_icon_only else height,
            on_click=self._handle_click,
            **kwargs
        )

    def _get_style_config(self):
        if self._variant == ButtonVariant.TOGGLE:
            return self.styles[ButtonVariant.ACCENT if self.is_toggled else ButtonVariant.DEFAULT]
        return self.styles[self._variant]

    def _handle_click(self, e):
        if self._variant == ButtonVariant.TOGGLE:
            self.is_toggled = not self.is_toggled
            style_config = self._get_style_config()
            self.style.bgcolor = style_config["bgcolor"]
            self.style.side = style_config["side"]
            self.style.color = style_config["color"]
            self.update()
        
        if self._user_on_click:
            self._user_on_click(e)

'''

import flet as ft
from typing import Union
from enum import Enum
from ..utils import FluentIcon
from ..utils.fluent_design_system import FluentDesignSystem

class ButtonVariant(Enum):
    DEFAULT = "default"
    ACCENT = "accent"
    HYPERLINK = "hyperlink"
    TOGGLE = "toggle"

class Button(ft.TextButton):
    def __init__(
        self,
        content: Union[str, ft.Control] = None,
        variant: ButtonVariant = ButtonVariant.DEFAULT,
        height=35,
        custom_color=None,
        design_system: FluentDesignSystem = None,
        is_dark_mode: bool = True,
        **kwargs
    ):
        self.is_toggled = False
        self._variant = variant
        self.design_system = design_system or FluentDesignSystem()
        self.theme = self.design_system.dark_theme if is_dark_mode else self.design_system.light_theme
        
        # Define style configurations for each variant using design system colors
        styles = {
            ButtonVariant.DEFAULT: {
                "bgcolor": {
                    ft.ControlState.DEFAULT: self.theme.fills.get_fill("control_fill_default"),
                    # ft.ControlState.HOVERED: self.theme.fills.get_fill("control_fill_secondary"),
                    ft.ControlState.PRESSED: self.theme.fills.get_fill("control_fill_tertiary"),
                    ft.ControlState.DISABLED: self.theme.fills.get_fill("control_fill_disabled")
                },
                "side": {
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.with_opacity(0.0578, "#ffffff")),
                    ft.ControlState.HOVERED: ft.BorderSide(1, ft.colors.with_opacity(0.078, "#ffffff")),
                },
                "color": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color("text_primary"),
                    ft.ControlState.PRESSED: self.theme.colors.get_color("text_secondary"),
                    ft.ControlState.DISABLED: self.theme.colors.get_color("text_disabled"),
                }
            },
            ButtonVariant.ACCENT: {
                "bgcolor": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color("accent_default"),
                    ft.ControlState.HOVERED: self.theme.colors.get_color("accent_secondary"),
                    # ft.ControlState.PRESSED: self.theme.colors.get_color("accent_tertiary"),
                    ft.ControlState.DISABLED: self.theme.colors.get_color("accent_disabled")
                },
                "side": {
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.with_opacity(0.08, "#000000")),
                    ft.ControlState.HOVERED: ft.BorderSide(1, ft.colors.with_opacity(0.078, "#ffffff")),
                },
                "color": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color("text_on_accent_primary"),
                    ft.ControlState.PRESSED: self.theme.colors.get_color("text_on_accent_secondary"),
                    ft.ControlState.DISABLED: self.theme.colors.get_color("text_on_accent_disabled"),
                }
            },
            ButtonVariant.HYPERLINK: {
                "bgcolor": { 
                    ft.ControlState.DEFAULT: self.theme.fills.get_fill("control_fill_transparent"),
                    ft.ControlState.HOVERED: self.theme.fills.get_fill("control_fill_secondary", 0.06),
                    # ft.ControlState.PRESSED: self.theme.fills.get_fill("control_fill_tertiary"),
                    ft.ControlState.DISABLED: self.theme.fills.get_fill("control_fill_transparent")
                },
                "color": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color("accent_default"),
                    ft.ControlState.PRESSED: self.theme.colors.get_color("accent_tertiary"),
                    ft.ControlState.DISABLED: self.theme.colors.get_color("text_disabled"),
                },
                "side": ft.BorderSide(0, ft.colors.with_opacity(0, "#000000")),
            }
        }

        # Get style configuration for the selected variant
        self.styles = styles
        style_config = self._get_style_config()

        is_icon_only = isinstance(content, (ft.Icon, ft.Image, FluentIcon))
        if not is_icon_only:
            content = content if isinstance(content, ft.Control) else ft.Text(
                content,
                size=int(self.design_system.font_sizes.body_font_size.replace("px", "")),
                font_family=self.design_system.font_families.font_family_text,
            )

        # Create button style with conditional padding and corner radius from design system
        button_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=self.design_system.control_properties.control_corner_radius),
            bgcolor=style_config["bgcolor"],
            side=style_config["side"],
            color=style_config["color"] if not custom_color else custom_color,
            overlay_color=ft.colors.TRANSPARENT,
            padding=ft.padding.all(4) if is_icon_only else ft.padding.only(right=18, left=18, top=4, bottom=6),
            visual_density=ft.VisualDensity.STANDARD,
            animation_duration=self.design_system.control_properties.control_fast_duration,
        )

        # Set width based on content
        width = kwargs.pop('width', None)
        if width is None:
            width = 32 if is_icon_only else None  # Auto width for text

        # Store the original on_click handler if provided
        self._user_on_click = kwargs.pop('on_click', None)
        
        super().__init__(
            content=content,
            style=button_style,
            width=width,
            height=32 if is_icon_only else height,
            on_click=self._handle_click,
            **kwargs
        )

    def _get_style_config(self):
        if self._variant == ButtonVariant.TOGGLE:
            return self.styles[ButtonVariant.ACCENT if self.is_toggled else ButtonVariant.DEFAULT]
        return self.styles[self._variant]

    def _handle_click(self, e):
        if self._variant == ButtonVariant.TOGGLE:
            self.is_toggled = not self.is_toggled
            style_config = self._get_style_config()
            self.style.bgcolor = style_config["bgcolor"]
            self.style.side = style_config["side"]
            self.style.color = style_config["color"]
            self.update()
        
        if self._user_on_click:
            self._user_on_click(e)
            
    def update_theme(self, is_dark_mode: bool = True):
        """Update button theme colors"""
        self.theme = self.design_system.dark_theme if is_dark_mode else self.design_system.light_theme
        # Recreate styles with new theme
        self.styles = self._create_styles()
        # Update button style
        style_config = self._get_style_config()
        self.style.bgcolor = style_config["bgcolor"]
        self.style.side = style_config["side"]
        self.style.color = style_config["color"]
        self.update()