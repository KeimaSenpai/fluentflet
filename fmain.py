import flet as ft
from fluentflet.components import (
    Button, ButtonVariant, 
    Checkbox, CheckState,
    Slider, SliderOrientation,
    Radio, RadioGroup,
    TextBox,
    Calendar,
    Toggle, 
    Expander,
    Dropdown,
    ListItem
)
from fluentflet.window import FluentWindow, Titlebar
from fluentflet.utils import FluentIcon, FluentIcons, FluentIconStyle

class DisplayGroup(ft.Container):
    def __init__(
        self,
        title: str,
        widgets: list = None,
        **kwargs
    ):
        # Extract widget path from the first widget if available
        widget_path = "fluentflet.components"
        
        # Create header with title and path
        header = ft.Column([
            ft.Text(
                value=title,
                size=32,
                weight=ft.FontWeight.BOLD,
                color="#ffffff"
            ),
            ft.Text(
                value=widget_path,
                size=14,
                color="#808080"
            )
        ], spacing=5)
        
        # Create content column for widgets
        self.content_column = ft.Column(
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        )
        
        if widgets:
            self.content_column.controls.extend(widgets)
        
        # Combine header and content
        main_column = ft.Column([
            header,
            self.content_column
        ], spacing=20)
        
        super().__init__(
            content=main_column,
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            border_radius=8,
            expand=True,
            **kwargs
        )

    def add(self, item):
        """Add a widget to the group"""
        self.content_column.controls.append(item)
        self.update()

    def remove(self, item):
        """Remove a widget from the group"""
        self.content_column.controls.remove(item)
        self.update()

    def clear(self):
        """Remove all widgets"""
        self.content_column.controls.clear()
        self.update()

class DisplayItem(ft.Container):
    def __init__(
        self,
        title: str = "",
        content: ft.Control = None,
        **kwargs
    ):
        self.title = ft.Text(
            value=title,
            size=14,
            weight=ft.FontWeight.NORMAL,
            color="#ffffff"
        )
        
        # Create main content with source code section
        main_content = ft.Column([
            # Widget display
            ft.Container(
                content=ft.Row([content]),
                bgcolor=ft.colors.with_opacity(.6, "#1e1e1e"),
                padding=20,
                border_radius=ft.border_radius.only(top_left=8, top_right=8),
                expand=True
            ) if content else None,
            
            # Source code section
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Source code", color="#808080"),
                        Button(
                            FluentIcon(FluentIcons.COPY, size=14, color="#ffffff"),
                            variant=ButtonVariant.HYPERLINK
                            # on_click=lambda _: self.copy_source_code(source_code)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                bgcolor=ft.colors.with_opacity(.6, "#2d2d2d"),
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8)
            ) if content else None
        ], spacing=1)
        
        super().__init__(
            content=ft.Column(
                [
                    self.title,
                    main_content
                ] if content else [self.title],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=0, vertical=10),
            border_radius=8,
            **kwargs
        )

def on_drag_enter(point):
    print(f"Drag entered at {point}")
    
def on_drag_over(point):
    print(f"Dragging over {point}")
    
def on_drag_leave():
    print("Drag left")
    
def on_files_dropped(files):
    print(f"Got files: {files}")

def main(page: ft.Page):
    page.title = "Fluent Flet"
    page.icon = "fluentflet/static/fluentflet.png"
    page.window.width = 800
    page.accepts_drops = True

    window = FluentWindow(
        page,
        window_titlebar=Titlebar(
            title="Fluent Flet Components", 
            icon=ft.Image(src="fluentflet/static/fluentflet.png", width=24, height=24)
        ),
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home"},
            {"icon": FluentIcons.SYMBOLS, "label": "Fluent icons"},
            {"type": "divider"},
            {"icon": FluentIcons.CONTROL_BUTTON, "label": "Button"},
            {"icon": FluentIcons.CHECKBOX_CHECKED, "label": "Checkbox"},
            {"icon": FluentIcons.RADIO_BUTTON, "label": "Radio"},
            {"icon": FluentIcons.TOGGLE_LEFT, "label": "Toggle"},
            {"icon": FluentIcons.TEXT_FIELD, "label": "TextBox"},
            {"icon": FluentIcons.COMMENT, "label": "Dropdown"},
            {"icon": FluentIcons.SPACEBAR, "label": "Slider"},
            {"icon": FluentIcons.CALENDAR_EMPTY, "label": "Calendar"},
            {"icon": FluentIcons.LIST, "label": "ListItem"},
            {"icon": FluentIcons.CHEVRON_DOWN, "label": "Expander"},
            {"icon": FluentIcons.COLOR, "label": "Colors & theme"}
        ],
        bottom_navigation_items=[
            {"type": "divider"},
            {"icon": FluentIcons.INFO, "label": "About"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings"},
        ],
        colors={
            "nav_bg": "#1F1F1F",
            "content_bg": "#282828",
        }
    )

    # Home View
    home_view = DisplayGroup(title = "home", widgets=[
        DisplayItem(
            title="Welcome to Fluent Flet Components",
            content=ft.Column([
                ft.Text("A showcase of individual Fluent Flet widgets", size=20, color="white"),
                ft.Text("Select a component from the navigation menu to see detailed examples.", 
                       color="#808080", size=16),
            ])
        )
    ])

    # Slider Page
    slider_view = DisplayGroup(title="Slider", widgets=[
        DisplayItem(
            title="Horizontal Slider",
            content=Slider(
                value=50,
                min=0,
                max=100,
                on_change=lambda e: print(f"Value: {round(e.current_value)}")
            )
        ),
        DisplayItem(
            title="Vertical Slider",
            content=ft.Container(
                content=Slider(
                    value=50,
                    orientation=SliderOrientation.VERTICAL,
                ),
                height=220
            )
        )
    ])

    # Button Page
    button_view = DisplayGroup(title="Button", widgets=[
        DisplayItem(
            title="Standard Button",
            content=Button(content=ft.Text("Standard"), on_click=lambda e: print("Button clicked"))
        ),
        DisplayItem(
            title="Accent Button",
            content=Button("Accent", variant=ButtonVariant.ACCENT)
        ),
        DisplayItem(
            title="Toggle Button",
            content=Button("Toggle", variant=ButtonVariant.TOGGLE)
        ),
        DisplayItem(
            title="Icon Button",
            content=Button(content=FluentIcon(name=FluentIcons.ADD, size=15))
        ),
        DisplayItem(
            title="Hyperlink Button",
            content=Button("Hyperlink", variant=ButtonVariant.HYPERLINK)
        ),
        DisplayItem(
            title="Disabled Button",
            content=Button(content=ft.Text("Standard"), disabled=True)
        ),
        DisplayItem(
            title="Disabled Accent Button",
            content=Button(content=ft.Text("Accent"), variant=ButtonVariant.ACCENT, disabled=True)
        ),
        DisplayItem(
            title="Disabled Toggle Button",
            content=Button("Toggle", variant=ButtonVariant.TOGGLE, disabled=True)
        ),
        DisplayItem(
            title="Disabled Icon Button",
            content=Button(content=FluentIcon(name=FluentIcons.ADD, size=15), disabled=True)
        ),
        DisplayItem(
            title="Disabled Hyperlink Button",
            content=Button(content=ft.Text("Hyperlink"), variant=ButtonVariant.HYPERLINK, disabled=True)
        )
    ])

    # Checkbox Page
    checkbox_view = DisplayGroup(title="Checkbox", widgets=[
        DisplayItem(
            title="Two-state Checkbox",
            content=Checkbox(label="Two-state Checkbox", on_change=lambda state: print(state))
        ),
        DisplayItem(
            title="Three-state Checkbox",
            content=Checkbox(label="Three-state Checkbox", three_state=True, on_change=lambda state: print(state))
        ),
        DisplayItem(
            title="Initially Checked Three-state Checkbox",
            content=Checkbox(label="Three-state (Initially Checked)", state=CheckState.CHECKED, three_state=True)
        ),
        DisplayItem(
            title="Initially Indeterminate Three-state Checkbox",
            content=Checkbox(label="Three-state (Initially Indeterminate)", state=CheckState.INDETERMINATE, three_state=True)
        ),
        DisplayItem(
            title="Disabled Checkbox",
            content=Checkbox(label="Disabled", disabled=True)
        ),
        DisplayItem(
            title="Disabled Checked Checkbox",
            content=Checkbox(label="Disabled Checked", state=CheckState.CHECKED, disabled=True)
        ),
        DisplayItem(
            title="Disabled Indeterminate Checkbox",
            content=Checkbox(label="Disabled Indeterminate", state=CheckState.INDETERMINATE, disabled=True)
        )
    ])

    # Radio Page
    radio_view = DisplayGroup(title="Radio", widgets=[
        DisplayItem(
            title="Radio Group",
            content=RadioGroup(
                content=ft.Column([
                    Radio(value="radio1", label="Option 1"),
                    Radio(value="radio2", label="Option 2"),
                    Radio(value="radio3", label="Option 3", disabled=True),
                ]),
                # value="option1",
                on_change=lambda value: print("Radio changed:", value)
            )
        ),
        DisplayItem(
            title="Standard Radio Button",
            content=Radio(value="option1", label="Option 1")
        ),
        DisplayItem(
            title="Disabled Radio Button",
            content=Radio(value="option4", label="Disabled Option", disabled=True)
        )
    ])

    # Toggle Page
    toggle_view = DisplayGroup(title="Toggle", widgets=[
        DisplayItem(
            title="Standard Toggle",
            content=Toggle(label="Standard Toggle")
        ),
        DisplayItem(
            title="Custom Label Toggle",
            content=Toggle(label={"on_content": "ON", "off_content": "OFF"})
        ),
        DisplayItem(
            title="Initially On Toggle",
            content=Toggle(label="Initially On", value=True)
        ),
        DisplayItem(
            title="Disabled Toggle",
            content=Toggle(label="Disabled Toggle", disabled=True)
        )
    ])

    # TextBox Page
    textbox_view = DisplayGroup(title="TextBox", widgets=[
        DisplayItem(
            title="Standard TextBox",
            content=TextBox(placeholder="TextBox", width=500, on_change=lambda e: print(e.control.value))
        ),
        DisplayItem(
            title="Password TextBox",
            content=TextBox(
                placeholder="Password TextBox", 
                width=500, 
                right_icon=FluentIcon(name=FluentIcons.EYE_SHOW, style=FluentIconStyle.FILLED, size=16), 
                password=True
            )
        )
    ])

    # Dropdown Page
    dropdown_view = DisplayGroup(title="Dropdown", widgets=[
        DisplayItem(
            title="Standard Dropdown",
            content=Dropdown(
                options=["Option 1", "Option 2", "Option 3"],
                initial_value="Option 1"
            )
        ),
        DisplayItem(
            title="Disabled Dropdown",
            content=Dropdown(
                options=["Disabled Option 1", "Disabled Option 2"],
                initial_value="Disabled Option 1",
                disabled=True
            )
        )
    ])

    # Calendar Page
    calendar_view = DisplayGroup(title="Calendar", widgets=[
        DisplayItem(
            title="Standard Calendar",
            content=Calendar(
                on_select=lambda date: print(f"Selected: {date.strftime('%Y-%m-%d') if date else 'None'}")
            )
        )
    ])

    # ListItem Page
    listitem_view = DisplayGroup(title="List Item",widgets=[
        DisplayItem(
            title="Basic ListItem",
            content=ListItem(content=ft.Text("Standard List Item")),
        ),
        DisplayItem(
            title="ListView",
            content=ft.ListView(
                spacing=2,
                height=300,
                controls=[
                    ListItem(content=ft.Text("Standard List Item")),
                    ListItem(
                        content=ft.Row([
                            FluentIcon(name=FluentIcons.PERSON),
                            ft.Text("List Item with Icon")
                        ])
                    ),
                    ListItem(
                        content=ft.Row([
                            ft.Text("List Item with Checkbox"),
                            Checkbox()
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
                ]
            )
        )
    ])

    # Expander Page
    expander_view = DisplayGroup(title="Expander", widgets=[
        DisplayItem(
            title="Basic Expander",
            content=Expander(
                header="Basic String Header",
                content=ft.Column([
                    ft.Text("This is some content"),
                    Button(ft.Text("Click me"), variant=ButtonVariant.DEFAULT)
                ])
            )
        ),
        DisplayItem(
            title="Expander with Icon Header",
            content=Expander(
                header=ft.Row([
                    FluentIcon(name=FluentIcons.EDIT_SETTINGS, style=FluentIconStyle.FILLED, size=15, color="#ffffff"),
                    ft.Text("Header with Icon")
                ]),
                content=ft.Text("Content with fancy header")
            )
        ),
        DisplayItem(
            title="Expander with Interactive Header",
            content=Expander(
                header=ft.Row([
                    Checkbox(),
                    ft.Text("Header with Action")
                ]),
                content=ft.Text("Content with fancy header")
            )
        )
    ])

    # Add all routes
    window.add_route("home", home_view)
    window.add_route("button", button_view)
    window.add_route("checkbox", checkbox_view)
    window.add_route("radio", radio_view)
    window.add_route("toggle", toggle_view)
    window.add_route("textbox", textbox_view)
    window.add_route("dropdown", dropdown_view)
    window.add_route("slider", slider_view)
    window.add_route("calendar", calendar_view)
    window.add_route("listitem", listitem_view)
    window.add_route("expander", expander_view)

    def create_icons_browser():
        class SelectedIcon:
            def __init__(self):
                self.value = None
                self.name = None
                self.python_enum = None
        
        selected_icon = SelectedIcon()

        def show_icon_details(icon: FluentIcons, style: FluentIconStyle):
            details_panel.visible = True
            icon_text = details_panel.content.controls[0]
            icon_previews = details_panel.content.controls[1]
            details = details_panel.content.controls[2]

            selected_icon.value = icon.value
            selected_icon.name = icon.name
            selected_icon.python_enum = f"FluentIcons.{icon.name}"
            
            icon_text.value = icon.value
            
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

            icon_value = icon.value
            icon_name = icon.name
            icon_python =  f"FluentIcons.{icon.name}"
            
            details.controls[1].controls[0].value = icon.value
            details.controls[3].controls[0].value = icon.name
            details.controls[5].controls[0].value = f"FluentIcons.{icon.name}"
            
            details_panel.update()

        def copy_value(e):
            if state.icon_value:
                page.set_clipboard(selected_icon.value)

        def copy_name(e):
            if state.icon_name:
                page.set_clipboard(selected_icon.name)

        def copy_python(e):
            if state.icon_python:
                page.set_clipboard(selected_icon.python_enum)

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
                    icon_name = container.content.controls[1].value
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
                    ft.Container(
                        content=None,
                        padding=20,
                        bgcolor=ft.colors.with_opacity(0.578, "#1e1e1e"),
                        border_radius=4,
                        width=100,
                        height=100,
                    ),
                    ft.Container(
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
                        Button(
                            content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"),
                            variant=ButtonVariant.DEFAULT,
                            on_click=lambda _: page.set_clipboard(selected_icon.value)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text("Python enum name", color="#666666", size=14),
                    ft.Row([
                        ft.Text("", size=16),
                        Button(
                            content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"),
                            variant=ButtonVariant.DEFAULT,
                            on_click=lambda _: page.set_clipboard(selected_icon.name)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text("Python", color="#666666", size=14),
                    ft.Row([
                        ft.Text("", size=16),
                        Button(
                            content=FluentIcon(name=FluentIcons.COPY, size=16, color="#ffffff"),
                            variant=ButtonVariant.DEFAULT,
                            on_click=lambda _: page.set_clipboard(selected_icon.python_enum)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) 
                ], spacing=20)
            ], spacing=30),
            width=400,
            bgcolor=ft.colors.with_opacity(0.578, "#1a1a1a"),
            padding=30,
            border_radius=4,
        )

        details_panel.visible = False

        # Layout with Row
        layout = ft.Row([
            left_panel,
            details_panel
        ], expand=True)

        # Load icons
        icons = [create_icon_tile(icon, FluentIconStyle.REGULAR) for icon in FluentIcons]
        icon_grid.controls = [icon for icon in icons if icon is not None]

        return layout

    window.add_route("fluent icons", create_icons_browser())

    # Set initial route
    window.navigate("home")

ft.app(target=main)