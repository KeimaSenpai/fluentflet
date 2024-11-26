from dataclasses import dataclass, field
from typing import Optional
import flet as ft

import flet as ft
import re
import colorsys

def parse_number(value: str) -> float:
    """Parse number from string, handling percentages"""
    value = value.strip()
    if value.endswith('%'):
        return float(value.rstrip('%')) / 100
    return float(value)

def create_flet_color(color_str: str, override_opacity: float = None) -> str:
    """Convert color string to Flet color with opacity"""
    if color_str == "transparent":
        return ft.colors.with_opacity(0, "#000000")
    
    if color_str.startswith("#"):
        opacity = override_opacity if override_opacity is not None else 1.0
        return ft.colors.with_opacity(opacity, color_str)
    
    try:
        # Remove hsla( or hsl( and ) and split by commas
        color_str = color_str.replace("hsla(", "").replace("hsl(", "").replace(")", "")
        parts = [part.strip() for part in color_str.split(",")]
        
        # Parse values
        h = float(parts[0]) / 360  # colorsys expects hue in [0, 1]
        s = parse_number(parts[1])  # saturation as [0, 1]
        l = parse_number(parts[2])  # lightness as [0, 1]
        a = parse_number(parts[3]) if len(parts) > 3 else 1.0  # alpha as [0, 1]
        
        # Convert HSL to RGB using colorsys
        r, g, b = colorsys.hls_to_rgb(h, l, s)  # Note: colorsys uses HLS order
        
        # Convert RGB floats to hex
        hex_color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
        
        # Use the alpha from the color string unless overridden
        opacity = override_opacity if override_opacity is not None else a
        return ft.colors.with_opacity(opacity, hex_color)
        
    except Exception as e:
        print(f"Error parsing color: {e} for color {color_str}")
        return color_str

@dataclass
class AccentColors:
    accent_light_3: str = "191, 98%, 80%"
    accent_light_2: str = "199, 99%, 69%"
    accent_light_1: str = "205, 100%, 49%"
    accent_base: str = "206, 100%, 42%"
    accent_dark_1: str = "209, 100%, 36%"
    accent_dark_2: str = "215, 100%, 29%"
    accent_dark_3: str = "226, 100%, 20%"

@dataclass
class FontFamilies:
    font_family_fallback: str = '"Segoe UI", -apple-system, ui-sans-serif, system-ui, BlinkMacSystemFont, Helvetica, Arial, sans-serif'
    font_family_text: str = '"Segoe UI Variable Text", "Seoge UI Variable Static Text", var(--fds-font-family-fallback)'
    font_family_small: str = '"Segoe UI Variable Small", "Seoge UI Variable Static Small", var(--fds-font-family-fallback)'
    font_family_display: str = '"Segoe UI Variable Display", "Seoge UI Variable Static Display", var(--fds-font-family-fallback)'

@dataclass
class FontSizes:
    caption_font_size: str = "12px"
    body_font_size: str = "14px"
    body_large_font_size: str = "18px"
    subtitle_font_size: str = "20px"
    title_font_size: str = "28px"
    title_large_font_size: str = "40px"
    display_font_size: str = "68px"

@dataclass
class ControlProperties:
    control_corner_radius: int = 4
    overlay_corner_radius: int = 8
    control_slow_duration: int = 333
    control_normal_duration: int = 250
    control_fast_duration: int = 167
    control_faster_duration: int = 83

@dataclass
class ControlFills:
    control_fill_transparent: str = "transparent"
    control_fill_default: str = "hsla(0, 0%, 100%, 0.061)"
    control_fill_secondary: str = "hsla(0, 0%, 100%, 0.084)"
    control_fill_tertiary: str = "hsla(0, 0%, 100%, 0.033)"
    control_fill_disabled: str = "hsla(0, 0%, 100%, 0.042)"
    control_fill_input_active: str = "hsla(0, 0%, 12%, 70%)"
    control_strong_fill_default: str = "hsla(0, 0%, 100%, 54.42%)"
    control_strong_fill_disabled: str = "hsla(0, 0%, 100%, 24.65%)"
    control_solid_fill_default: str = "hsl(0, 0%, 27%)"
    
    def get_fill(self, fill_name: str, override_opacity: float = None) -> str:
        fill_value = getattr(self, fill_name)
        return create_flet_color(fill_value, override_opacity)


@dataclass
class BackgroundProperties:
    solid_background_base: str
    solid_background_secondary: str
    solid_background_tertiary: str
    solid_background_quarternary: str
    layer_background_default: str
    layer_background_alt: str
    card_background_default: str
    card_background_secondary: str
    smoke_background_default: str
    
    def get_background(self, background_name: str, override_opacity: float = None) -> str:
        background_value = getattr(self, background_name)
        return create_flet_color(background_value, override_opacity)


@dataclass
class ThemeColors:
    text_primary: str
    text_secondary: str
    text_tertiary: str
    text_disabled: str
    accent_default: str
    accent_secondary: str
    accent_tertiary: str
    accent_disabled: str
    accent_text_primary: str
    accent_text_secondary: str
    accent_text_tertiary: str
    accent_text_disabled: str
    text_on_accent_primary: str
    text_on_accent_secondary: str
    text_on_accent_disabled: str
    text_on_accent_selected: str
    
    def get_color(self, color_name: str, override_opacity: float = None) -> str:
        color_value = getattr(self, color_name)
        return create_flet_color(color_value, override_opacity)
@dataclass
class SystemColors:
    system_attention: str
    system_success: str
    system_caution: str
    system_critical: str
    system_neutral: str
    system_solid_neutral: str
    system_background_attention: str
    system_background_success: str
    system_background_caution: str
    system_background_critical: str
    system_background_solid_attention: str
    system_background_solid_neutral: str
    
    def get_color(self, color_name: str, opacity: float = 1.0) -> str:
        color_value = getattr(self, color_name)
        return create_flet_color(color_value, opacity)

@dataclass
class Shadows:
    card_shadow: str = "0px 2px 4px rgba(0, 0, 0, 0.04)"
    tooltip_shadow: str = "0px 4px 8px rgba(0, 0, 0, 0.14)"
    flyout_shadow: str = "0px 8px 16px rgba(0, 0, 0, 0.14)"
    dialog_shadow: str = "0px 32px 64px rgba(0, 0, 0, 0.1876), 0px 2px 21px rgba(0, 0, 0, 0.1474)"
    inactive_window_shadow: str = "0px 16px 32px rgba(0, 0, 0, 0.18), 0px 2px 10.67px rgba(0, 0, 0, 0.1474)"
    active_window_shadow: str = "0px 32px 64px rgba(0, 0, 0, 0.28), 0px 2px 21px rgba(0, 0, 0, 0.22)"

@dataclass
class LightTheme:
    colors: ThemeColors = field(default_factory=lambda: ThemeColors(
        text_primary="hsla(0, 0%, 0%, 89.56%)",
        text_secondary="hsla(0, 0%, 0%, 60.63%)",
        text_tertiary="hsla(0, 0%, 0%, 44.58%)",
        text_disabled="hsla(0, 0%, 0%, 36.14%)",
        accent_default="hsl(209, 100%, 36%)",
        accent_secondary="hsla(209, 100%, 36%, 90%)",
        accent_tertiary="hsla(209, 100%, 36%, 80%)",
        accent_disabled="hsla(0, 0%, 0%, 21.69%)",
        accent_text_primary="hsl(215, 100%, 29%)",
        accent_text_secondary="hsl(226, 100%, 20%)",
        accent_text_tertiary="hsl(209, 100%, 36%)",
        accent_text_disabled="hsla(0, 0%, 0%, 36.14%)",
        text_on_accent_primary="hsl(0, 0%, 100%)",
        text_on_accent_secondary="hsla(0, 0%, 100%, 70%)",
        text_on_accent_disabled="hsla(0, 0%, 100%, 70%)",
        text_on_accent_selected="hsl(0, 0%, 100%)"
    ))
    fills: ControlFills = field(default_factory=lambda: ControlFills(
        control_fill_transparent="transparent",
        control_fill_default="hsla(0, 0%, 100%, 70%)",
        control_fill_secondary="hsla(0, 0%, 98%, 50%)",
        control_fill_tertiary="hsla(0, 0%, 98%, 30%)",
        control_fill_disabled="hsla(0, 0%, 98%, 30%)",
        control_fill_input_active="hsl(0, 0%, 100%)",
        control_strong_fill_default="hsla(0, 0%, 0%, 44.58%)",
        control_strong_fill_disabled="hsla(0, 0%, 0%, 31.73%)",
        control_solid_fill_default="hsl(0, 0%, 100%)"
    ))
    backgrounds: BackgroundProperties = field(default_factory=lambda: BackgroundProperties(
        solid_background_base="hsl(0, 0%, 95%)",
        solid_background_secondary="hsl(0, 0%, 93%)",
        solid_background_tertiary="hsl(0, 0%, 98%)",
        solid_background_quarternary="hsl(0, 0%, 100%)",
        layer_background_default="hsla(0, 0%, 100%, 50%)",
        layer_background_alt="hsl(0, 0%, 100%)",
        card_background_default="hsla(0, 0%, 100%, 70%)",
        card_background_secondary="hsla(0, 0%, 96%, 50%)",
        smoke_background_default="hsla(0, 0%, 0%, 30%)"
    ))

@dataclass
class DarkTheme:
    colors: ThemeColors = field(default_factory=lambda: ThemeColors(
        text_primary="hsla(0, 0%, 100%, 100%)",
        text_secondary="hsla(0, 0%, 100%, 78.6%)",
        text_tertiary="hsla(0, 0%, 100%, 54.42%)",
        text_disabled="hsla(0, 0%, 100%, 36.28%)",
        accent_default="hsl(199, 99%, 69%)",
        accent_secondary="hsla(199, 99%, 69%, 90%)",
        accent_tertiary="hsla(199, 99%, 69%, 80%)",
        accent_disabled="hsla(0, 0%, 100%, 15.81%)",
        accent_text_primary="hsl(191, 98%, 80%)",
        accent_text_secondary="hsl(191, 98%, 80%)",
        accent_text_tertiary="hsl(199, 99%, 69%)",
        accent_text_disabled="hsla(0, 0%, 100%, 36.28%)",
        text_on_accent_primary="hsl(0, 0%, 0%)",
        text_on_accent_secondary="hsla(0, 0%, 0%, 0.5)",
        text_on_accent_disabled="hsla(0, 0%, 100%, 0.53)",
        text_on_accent_selected="hsl(0, 0%, 100%)"
    ))
    fills: ControlFills = field(default_factory=lambda: ControlFills(
        control_fill_transparent="transparent",
        control_fill_default="hsla(0, 0%, 100%, 0.061)",
        control_fill_secondary="hsla(0, 0%, 100%, 0.084)",
        control_fill_tertiary="hsla(0, 0%, 100%, 0.033)",
        control_fill_disabled="hsla(0, 0%, 100%, 0.042)",
        control_fill_input_active="hsla(0, 0%, 12%, 70%)",
        control_strong_fill_default="hsla(0, 0%, 100%, 54.42%)",
        control_strong_fill_disabled="hsla(0, 0%, 100%, 24.65%)",
        control_solid_fill_default="hsl(0, 0%, 27%)"
    ))
    backgrounds: BackgroundProperties = field(default_factory=lambda: BackgroundProperties(
        solid_background_base="hsl(0, 0%, 13%)",
        solid_background_secondary="hsl(0, 0%, 11%)",
        solid_background_tertiary="hsl(0, 0%, 16%)",
        solid_background_quarternary="hsl(0, 0%, 17%)",
        layer_background_default="hsla(0, 0%, 23%, 30%)",
        layer_background_alt="hsla(0, 0%, 100%, 5.38%)",
        card_background_default="hsla(0, 0%, 100%, 5.12%)",
        card_background_secondary="hsla(0, 0%, 100%, 3.26%)",
        smoke_background_default="hsla(0, 0%, 0%, 30%)"
    ))

@dataclass
class FluentDesignSystem:
    accent_colors: AccentColors = field(default_factory=AccentColors)
    font_families: FontFamilies = field(default_factory=FontFamilies)
    font_sizes: FontSizes = field(default_factory=FontSizes)
    control_properties: ControlProperties = field(default_factory=ControlProperties)
    light_theme: LightTheme = field(default_factory=LightTheme)
    dark_theme: DarkTheme = field(default_factory=DarkTheme)
    system_colors: SystemColors = field(default_factory=lambda: SystemColors(
        system_attention="hsl(209, 100%, 36%)",
        system_success="hsl(120, 78%, 27%)",
        system_caution="hsl(36, 100%, 31%)",
        system_critical="hsl(5, 75%, 44%)",
        system_neutral="hsla(0, 0%, 0%, 44.58%)",
        system_solid_neutral="hsl(0, 0%, 54%)",
        system_background_attention="hsla(0, 0%, 96%, 50%)",
        system_background_success="hsl(115, 58%, 92%)",
        system_background_caution="hsl(47, 100%, 90%)",
        system_background_critical="hsl(355, 85%, 95%)",
        system_background_solid_attention="hsl(0, 0%, 97%)",
        system_background_solid_neutral="hsl(0, 0%, 95%)"
    ))
    shadows: Shadows = field(default_factory=Shadows)


def main(page: ft.Page):
    # Initialize the design system
    design = FluentDesignSystem()
    # We'll use dark theme for this example
    theme = design.dark_theme
    
    # Set page properties
    page.bgcolor = theme.backgrounds.get_background("solid_background_base")
    page.padding = 20
    page.spacing = 20
    
    def handle_theme_toggle(e):
        nonlocal theme
        if theme == design.dark_theme:
            theme = design.light_theme
        else:
            theme = design.dark_theme
        
        # Update colors
        page.bgcolor = theme.backgrounds.get_background("solid_background_base")
        header_text.color = theme.colors.get_color("text_primary")
        description.color = theme.colors.get_color("text_secondary")
        for btn in [primary_button, secondary_button]:
            btn.bgcolor = (theme.colors.get_color("accent_default") 
                         if btn == primary_button 
                         else theme.fills.get_fill("control_fill_default", 0.061))
            btn.color = (theme.colors.get_color("text_on_accent_primary") 
                        if btn == primary_button 
                        else theme.colors.get_color("text_primary"))
            btn.update()
        card.bgcolor = theme.backgrounds.get_background("card_background_default", 0.0512)  # 5.12%
        page.update()

    def create_button(text: str, primary: bool = False):
        opacity = 1.0 if primary else 0.061  # Use the same opacity as in the design system
        return ft.ElevatedButton(
            text=text,
            bgcolor=theme.colors.get_color("accent_default") if primary 
                   else theme.fills.get_fill("control_fill_default", opacity),
            color=theme.colors.get_color("text_on_accent_primary") if primary 
                  else theme.colors.get_color("text_primary"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=design.control_properties.control_corner_radius
                ),
            ),
            elevation=0,
        )

    # Create components
    header_text = ft.Text(
        "Fluent Design Example",
        size=int(design.font_sizes.title_font_size.replace("px", "")),
        color=theme.colors.get_color("text_primary"),
        font_family=design.font_families.font_family_display,
        weight=ft.FontWeight.BOLD,
    )
    
    description = ft.Text(
        "This is a sample page showing the Fluent Design System implemented in Flet.",
        size=int(design.font_sizes.body_font_size.replace("px", "")),
        color=theme.colors.get_color("text_secondary"),
        font_family=design.font_families.font_family_text,
    )

    primary_button = create_button("Primary Button", primary=True)
    secondary_button = create_button("Secondary Button")
    
    # Create a card with correct opacity
    card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Card Title",
                    size=int(design.font_sizes.subtitle_font_size.replace("px", "")),
                    color=theme.colors.get_color("text_primary"),
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "This is a card component using Fluent Design System styles.",
                    size=int(design.font_sizes.body_font_size.replace("px", "")),
                    color=theme.colors.get_color("text_secondary"),
                ),
                ft.Row(
                    controls=[
                        create_button("Card Action", primary=True),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ],
            spacing=15,
        ),
        bgcolor=theme.backgrounds.get_background("card_background_default", 0.0512),  # 5.12%
        padding=20,
        border_radius=design.control_properties.overlay_corner_radius,
        shadow=ft.BoxShadow(
            spread_radius=4,
            blur_radius=8,
            color=ft.colors.with_opacity(0.1, "#000000"),
        )
    )
    
    # Theme toggle button
    theme_toggle = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_color=theme.colors.get_color("text_primary"),
        on_click=handle_theme_toggle,
        tooltip="Toggle theme",
    )

    # Add everything to the page
    page.add(
        ft.Row([header_text, theme_toggle], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        description,
        ft.Row([primary_button, secondary_button], spacing=10),
        card,
    )

# ft.app(target=main)