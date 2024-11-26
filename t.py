import flet as ft
import fluentflet.utils as ffu
import platform
import sys

def main(page: ft.Page):
    page.title = "test page"
    
    ffu._apply_blur()

    page.add(
        ft.Text(f"Flet version: {ft.version.version}"),
        ft.Text(f"Python version: {sys.version.split()[0]}"),
        ft.Text(f"OS version: {platform.platform()}")
    )

ft.app(main)