import flet as ft
from enum import Enum
from pathlib import Path
import re

from fluentflet.utils import FluentIcon, FluentIconStyle, FluentIcons  # Import the enum
from fluentflet.components import *

def main(page: ft.Page):
    page.title = "FluentFlet Icons Browser"
    page.icon = "fluentflet/static/fluentflet.png"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width=900
    page.blur_effect = True
    page.padding = 20

    def show_icon_details(icon: FluentIcons, style: FluentIconStyle):
        details_panel.visible = True
        icon_text = details_panel.content.controls[0]
        icon_previews = details_panel.content.controls[1]  # This is now the Row with both containers
        details = details_panel.content.controls[2]
        
        icon_text.value = icon.value
        
        # Update both preview containers
        regular_preview = icon_previews.controls[0]
        filled_preview = icon_previews.controls[1]
        
        try:
            regular_preview.content = ft.Column([
                FluentIcon(icon, style=FluentIconStyle.REGULAR, size=48),
                ft.Text("Regular", size=12, color="#666666")
            ], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        except FileNotFoundError:
            regular_preview.content = ft.Text("Not available", size=12, color="#666666")

        try:
            filled_preview.content = ft.Column([
                FluentIcon(icon, style=FluentIconStyle.FILLED, size=48),
                ft.Text("Filled", size=12, color="#666666")
            ], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        except FileNotFoundError:
            filled_preview.content = ft.Text("Not available", size=12, color="#666666")
        
        # Update copy fields
        details.controls[1].controls[0].value = icon.value  # Icon name
        details.controls[3].controls[0].value = icon.name  # Enum name
        details.controls[5].controls[0].value = f"FluentIcons.{icon.name}"  # Python import
        
        page.update()

    def select_icon(event, icon: FluentIcons, style: FluentIconStyle):
        for container in icon_grid.controls:
            if container:
                container.border = None
        event.control.border = ft.border.all(2, "#62cdfe")
        icon_grid.update()
        show_icon_details(icon, style)


    def create_icon_tile(icon: FluentIcons, style: FluentIconStyle) -> ft.Container:
        try:
            return ft.Container(
                content=ft.Column(
                    [
                        FluentIcon(icon, style=style),
                        ft.Text(icon.value, size=12, text_align=ft.TextAlign.CENTER)
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.only(top=15, bottom=10, right=15, left=15),
                bgcolor=ft.colors.with_opacity(0.578, "#1e1e1e"),
                border_radius=4,
                on_click=lambda e: select_icon(e, icon, style)
            )
        except FileNotFoundError:
            return None

    def filter_icons(e):
        search_term = e.control.value.lower()
        for container in icon_grid.controls:
            if container:
                icon_name = container.content.controls[1].value  # Get text from container
                container.visible = search_term in icon_name.lower()
        icon_grid.update()
    
    # Left side - Icon Browser
    left_panel = ft.Column([
        ft.Text("Icons", size=30, weight=ft.FontWeight.BOLD),
        TextBox(
            placeholder="Search icons",
            width=1000,
            on_change=lambda e: filter_icons(e)
        ),
        icon_grid := ft.GridView(
            expand=True,
            max_extent=100,
            spacing=10,
            run_spacing=10,
        )
    ], expand=True)
    
    # Right side - Details Panel
    details_panel = ft.Container(
        content=ft.Column([
            ft.Text("", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(  # Regular preview
                    content=None,
                    padding=20,
                    bgcolor=ft.colors.with_opacity(0.578, "#1e1e1e"),
                    border_radius=4,
                    width=100,
                    height=100,
                ),
                ft.Container(  # Filled preview
                    content=None,
                    padding=20,
                    bgcolor=ft.colors.with_opacity(0.578, "#1e1e1e"),
                    border_radius=4,
                    width=100,
                    height=100,
                ),
            ], spacing=20),
            ft.Column([
                ft.Text("Icon name", color="#666666"),
                ft.Row([
                    ft.Text("", size=16),
                    Button(content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"), variant=ButtonVariant.DEFAULT)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Python enum name", color="#666666", size=14),
                ft.Row([
                    ft.Text("", size=16),
                    Button(content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"), variant=ButtonVariant.DEFAULT)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Python", color="#666666", size=14),
                ft.Row([
                    ft.Text("", size=16),
                    Button(content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"), variant=ButtonVariant.DEFAULT)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], spacing=20)
        ], spacing=30),
        width=400,
        bgcolor=ft.colors.with_opacity(0.578, "#1a1a1a"),
        padding=30,
        border_radius=4,
    )


    # Layout with Row
    layout = ft.Row([
        left_panel,
        details_panel
    ], expand=True)

    details_panel.visible = False
    page.add(layout)

    # Load all icons at once using the enum
    icons = []
    for i, icon in enumerate(FluentIcons):
        # Create both regular and filled versions
        icons.extend([
            create_icon_tile(icon, FluentIconStyle.REGULAR),
            # create_icon_tile(icon, FluentIconStyle.FILLED)
        ])
    
    icon_grid.controls = [icon for icon in icons if icon is not None]
    page.update()  # Update the page once at the end instead of the grid
    # page.update()

ft.app(target=main)