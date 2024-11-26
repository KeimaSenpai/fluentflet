'''
import flet as ft
from fluentflet.components import ListItem, Button, ButtonVariant, ToolTip
from fluentflet.utils import FluentIcon, FluentIcons

class Titlebar(ft.Container):
    def __init__(self, title="Email", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.top_bar_color = "#1F1F1F"     # Top bar matches nav
        self.height = 50
        self.padding = ft.padding.only(left=20, right=8)
        self.bgcolor = self.top_bar_color
        
        # Initialize the titlebar content
        self.content = self.init_titlebar()

    def init_titlebar(self):
        """Initialize the titlebar content"""
        # Window control buttons
        window_controls = ft.Row(
            controls=[
                Button(
                    content=ft.Icon(ft.icons.REMOVE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.minimize_window(),
                ),
                Button(
                    content=ft.Icon(ft.icons.CROP_SQUARE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.toggle_maximize_window(),
                ),
                Button(
                    content=ft.Icon(ft.icons.CLOSE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.close_window(),
                    on_hover=self.handle_close_hover,
                )
            ],
            spacing=0,
        )

        # Title text and layout
        self.title_text = ft.Text(
            self.title,
            size=20,
            weight=ft.FontWeight.BOLD,
            color="white"
        )

        return ft.Row(
            controls=[
                ft.Row(
                    controls=[self.title_text],
                    spacing=10,
                ),
                ft.Container(expand=True),
                window_controls,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def update_title(self, new_title: str):
        """Update the titlebar text"""
        self.title_text.value = new_title
        self.title_text.update()

    def handle_close_hover(self, e):
        """Handle hover effect for close button"""
        container = e.control
        container.bgcolor = "#c42b1c" if e.data == "true" else None
        container.update()

    def minimize_window(self):
        """Minimize the window"""
        self.page.window.minimized = True

    def toggle_maximize_window(self):
        """Toggle window maximize state"""
        self.page.window.maximized = not self.page.window.maximized

    def close_window(self):
        """Close the window"""
        self.page.window.close()

class NavigationView(ft.Row):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 0
        self.selected_index = 3  # Email selected by default
        self.is_nav_expanded = False  # Track navigation panel state

        # Create nav items content
        nav_items = [
            (FluentIcons.HOME, "Home"),
            (FluentIcons.PERSON, "Profile"),
            (FluentIcons.IMAGE, "Email"),
            (FluentIcons.SETTINGS, "Settings"),
        ]

        self.nav_color = "#1F1F1F"        # Dark nav background
        self.content_color = "#282828"     # Main content area
        self.top_bar_color = "#1F1F1F"     # Top bar matches nav
        
        # Create ListItems for navigation
        self.nav_items = []
        self._nav_item_intern = []
        for idx, (icon, label) in enumerate(nav_items):
            _item = self.create_row(icon, label)
            item = ListItem(
                content=_item,
                on_click=lambda e, i=idx: self.handle_nav_click(i),
                is_dark_mode=True,
            )
            self._nav_item_intern.append(_item)
            self.nav_items.append(item)

        # Left navigation panel
        self.nav_rail = ft.Container(
            content=ft.Column(
                controls=[
                    # Back button at top
                    ft.Container(
                        content=Button(
                            content=FluentIcon(
                                FluentIcons.ARROW_LEFT,
                                size=18,
                                color="white",
                            ),
                            variant=ButtonVariant.HYPERLINK,
                            disabled=True
                        ),
                        margin=ft.margin.only(top=10)
                    ),
                    ft.Container(height=20),
                    ListItem(
                        content=ft.Row(
                            controls=[
                                FluentIcon(
                                    FluentIcons.LIST,
                                    size=18,
                                    color="white"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=lambda e: self.open_navigtion_panel(e),
                        is_dark_mode=True,
                    ),
                    *self.nav_items
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=60,  # Initial width
            padding=ft.padding.only(left=10, right=5),
            bgcolor="#1F1F1F",
            animate=ft.animation.Animation(100, "easeOut"),  # Smooth animation
        )

        self.content_area = ft.Container(
            expand=True,
            content=ft.Stack(
                controls=[
                    # Main column with top bar and content
                    ft.Column(
                        controls=[
                            # Top bar with title
                            ft.WindowDragArea(
                                Titlebar()
                            ),
                            
                            # Main content container
                            ft.Container(
                                expand=True,
                                bgcolor=self.content_color,
                                border_radius=ft.border_radius.only(
                                    top_left=10,
                                )
                            ),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
            ),
        )

        # Add controls to the row
        self.controls = [
            self.nav_rail,
            self.content_area,
        ]

        # Set initial selection
        self.nav_items[self.selected_index].is_selected = True

    def create_row(self, icon, label):
        navigation_item = ft.Row(
            controls=[
                FluentIcon(
                    icon,
                    size=18,
                    color="white"
                ),
                # Add label that will be shown when expanded
                ft.Text(
                    label,
                    color="white",
                    size=14,
                    opacity=0,  # Hidden by default
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=12,
        )
        return navigation_item

    def open_navigtion_panel(self, e=None):
        """Toggle the navigation panel width"""
        self.is_nav_expanded = not self.is_nav_expanded
        
        if self.is_nav_expanded:
            # Expand navigation panel
            self.nav_rail.width = 200
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.START
            
            # Show labels with animation
            for item in self._nav_item_intern:
                label = item.controls[1]  # Get the text label
                label.opacity = 1
                label.update()
                
            # Adjust alignment of nav items
            for item in self._nav_item_intern:
                item.alignment = ft.MainAxisAlignment.START  # Changed from item.content.alignment
                item.update()
                    
        else:
            # Collapse navigation panel
            self.nav_rail.width = 60
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            # Hide labels with animation
            for item in self._nav_item_intern:
                label = item.controls[1]  # Get the text label
                label.opacity = 0
                label.update()
                
            # Reset alignment of nav items
            for item in self._nav_item_intern:
                item.alignment = ft.MainAxisAlignment.CENTER  # Changed from item.content.alignment
                item.update()
            
        # Update the navigation rail
        self.nav_rail.update()

    def handle_nav_click(self, e):
        """Handle navigation item click"""
        index = e if isinstance(e, int) else 0
        
        # Clear previous selection
        for item in self.nav_items:
            item.is_selected = False
        
        # Set new selection
        self.nav_items[index].is_selected = True
        self.selected_index = index
        
        # Update the top bar text using the new Titlebar method
        title_map = ["Home", "Profile", "Email", "Settings"]
        self.titlebar.update_title(title_map[index])

        # Update all nav items to reflect selection state
        for item in self.nav_items:
            item.update()

'''

import flet as ft
from fluentflet.components import ListItem, Button, ButtonVariant, ToolTip
from fluentflet.utils import FluentIcon, FluentIcons
from typing import Optional, Any, Callable, Union

class Titlebar(ft.Container):
    def __init__(
        self, 
        title: str = "fluent flet", 
        icon: str | ft.Control | None = None,
        icon_size: int = 20,
        **kwargs
    ):
        # Remove our custom parameters from kwargs before passing to super()
        titlebar_kwargs = {
            'title': title,
            'icon': icon,
            'icon_size': icon_size
        }
        
        # Initialize Container with remaining kwargs
        super().__init__(**kwargs)
        
        # Store our custom parameters
        self.title = titlebar_kwargs['title']
        self.icon = titlebar_kwargs['icon']
        self.icon_size = titlebar_kwargs['icon_size']
        
        # Set default properties
        self.top_bar_color = "#1F1F1F"
        self.height = 50
        self.padding = ft.padding.only(left=20, right=8)
        self.bgcolor = kwargs.get('bgcolor', self.top_bar_color)
        
        # Initialize the titlebar content
        self.content = self.init_titlebar()

    def init_titlebar(self):
        window_controls = ft.Row(
            controls=[
                Button(
                    content=ft.Icon(ft.icons.REMOVE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.minimize_window(),
                ),
                Button(
                    content=ft.Icon(ft.icons.CROP_SQUARE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.toggle_maximize_window(),
                ),
                Button(
                    content=ft.Icon(ft.icons.CLOSE, color="#ffffff", size=16),
                    variant=ButtonVariant.HYPERLINK,
                    on_click=lambda _: self.close_window(),
                    on_hover=self.handle_close_hover,
                )
            ],
            spacing=0,
        )

        self.title_text = ft.Text(
            self.title,
            size=14,
            weight=ft.FontWeight.BOLD,
            color="white"
        )

        return ft.Row(
            controls=[
                ft.Row(
                    controls=[self.icon, self.title_text],
                    spacing=10,
                ),
                # ft.Container(expand=True),
                window_controls,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def set_title(self, new_title: str):
        """Set the title text value without updating"""
        self.title_text.value = new_title

    def update_title(self, new_title: str):
        """Update the title text and refresh the control"""
        self.title_text.value = new_title
        if self.page:  # Only update if added to page
            self.title_text.update()

    def handle_close_hover(self, e):
        container = e.control
        container.bgcolor = "#c42b1c" if e.data == "true" else None
        container.update()

    def minimize_window(self):
        self.page.window.minimized = True

    def toggle_maximize_window(self):
        self.page.window.maximized = not self.page.window.maximized

    def close_window(self):
        self.page.window.close()

class FluentWindow:
    def __init__(
        self,
        page: ft.Page,
        navigation_items=None,
        selected_index=0,
        window_title: Union[str, Titlebar] = "Fluent Flet",
        colors=None,
        nav_width_collapsed=55,
        nav_width_expanded=200,
        animation_duration=100,
        show_back_button=True,
    ):
        self._page = page
        self._page.window.title_bar_hidden = True
        self._page.window.title_bar_buttons_hidden = True
        self._page.padding = 0
        
        self.colors = {
            "nav_bg": "#1F1F1F",
            "content_bg": "#282828",
            "title_bar_bg": "#1F1F1F",
            "icon_color": "white",
            "text_color": "white",
            "hover_color": "#c42b1c"
        }
        if colors:
            self.colors.update(colors)
        
        self._page.bgcolor = self.colors["nav_bg"]
        
        # Initialize main layout components
        self.navigation_items = navigation_items or [
            {"icon": FluentIcons.HOME, "label": "Home"},
            {"icon": FluentIcons.PERSON, "label": "Profile"},
            {"icon": FluentIcons.IMAGE, "label": "Email"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings"},
        ]
        
        # Handle window_title based on type
        self.titlebar = (window_title if isinstance(window_title, Titlebar) 
                        else Titlebar(title=str(window_title)))
        
        # Create the main layout
        self.create_layout(
            nav_width_collapsed=nav_width_collapsed,
            nav_width_expanded=nav_width_expanded,
            animation_duration=animation_duration,
            show_back_button=show_back_button,
            selected_index=selected_index
        )
        
        # Set up window event handling
        self._page.window.on_event = self._handle_window_event

        self.routes = {}
        self.current_route = None

    def add_route(self, route: str, view_builder: Callable[..., ft.Control]):
        """Add a route with a view builder that can accept parameters"""
        self.routes[route] = view_builder

    def navigate(self, route: str, **params):
        """Navigate to a route with parameters"""
        if route in self.routes:
            view = self.routes[route](**params) if callable(self.routes[route]) else self.routes[route]
            self.content_container.content.controls = [view]
            self.content_container.update()
            self.current_route = route

    def create_layout(self, nav_width_collapsed, nav_width_expanded, 
                     animation_duration, show_back_button, selected_index):
        """Create the main layout"""
        # Create navigation items
        self.nav_items = []
        self._nav_item_intern = []
        
        for idx, item in enumerate(self.navigation_items):
            _item = self.create_nav_row(item["icon"], item["label"])
            list_item = ListItem(
                content=_item,
                on_click=lambda e, i=idx: self.handle_nav_click(i),
                is_dark_mode=True,
            )
            self._nav_item_intern.append(_item)
            self.nav_items.append(list_item)

        # Create navigation rail
        nav_controls = []
        if show_back_button:
            nav_controls.extend([
                ft.Container(
                    content=Button(
                        content=FluentIcon(
                            FluentIcons.ARROW_LEFT,
                            size=18,
                            color=self.colors["icon_color"],
                        ),
                        variant=ButtonVariant.HYPERLINK,
                        disabled=True
                    ),
                    margin=ft.margin.only(top=10)
                ),
                ft.Container(height=20),
            ])
        
        nav_controls.extend([
            Button(
                content = FluentIcon(
                    FluentIcons.LIST,
                    size=18,
                    color=self.colors["icon_color"]
                ),
                on_click=lambda e: self.toggle_navigation_panel(e),
                variant=ButtonVariant.HYPERLINK,
                is_dark_mode=True,
            ),
            *self.nav_items
        ])

        self.nav_rail = ft.Container(
            content=ft.Column(
                controls=nav_controls,
                spacing=2,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=nav_width_collapsed,
            padding=ft.padding.only(left=10, right=5),
            bgcolor=self.colors["nav_bg"],
            animate=ft.animation.Animation(animation_duration, "easeOut"),
        )

        # Create content area
        self.content_container = ft.Container(
            expand=True,
            bgcolor=self.colors["content_bg"],
            border_radius=ft.border_radius.only(top_left=10),
            content=ft.Column(
                controls=[],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            padding=10,
        )

        # Set initial selection
        self.selected_index = selected_index
        self.is_nav_expanded = False
        self.nav_width_collapsed = nav_width_collapsed
        self.nav_width_expanded = nav_width_expanded
        
        if selected_index < len(self.nav_items):
            self.nav_items[selected_index].is_selected = True

        # Create main layout
        self.main_layout = ft.Row(
            controls=[
                self.nav_rail,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.WindowDragArea(self.titlebar),
                            self.content_container,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ),
            ],
            expand=True,
            spacing=0,
        )

        # Add to page
        self._page.add(self.main_layout)

    def create_nav_row(self, icon, label):
        return ft.Row(
            controls=[
                FluentIcon(
                    icon,
                    size=18,
                    color=self.colors["icon_color"]
                ),
                ft.Text(
                    label,
                    color=self.colors["text_color"],
                    size=14,
                    opacity=0,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=12,
        )

    def toggle_navigation_panel(self, e=None):
        self.is_nav_expanded = not self.is_nav_expanded
        
        if self.is_nav_expanded:
            self.nav_rail.width = self.nav_width_expanded
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.START
            
            for item in self._nav_item_intern:
                item.controls[1].opacity = 1
                item.alignment = ft.MainAxisAlignment.START
                item.update()
        else:
            self.nav_rail.width = self.nav_width_collapsed
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            for item in self._nav_item_intern:
                item.controls[1].opacity = 0
                item.alignment = ft.MainAxisAlignment.CENTER
                item.update()
        
        self.nav_rail.update()

    def handle_nav_click(self, index):
        """Handle navigation item click and route change"""
        # Clear previous selection
        for item in self.nav_items:
            item.is_selected = False
        
        # Set new selection
        self.nav_items[index].is_selected = True
        self.selected_index = index
        
        # Navigate to the corresponding route
        route = self.navigation_items[index]["label"].lower()
        self.navigate(route)
        
        # Update navigation items' visual state
        for item in self.nav_items:
            item.update()

    def add(self, *controls):
        """Add controls to the content area"""
        self.content_container.content.controls = list(controls)
        
        # Ensure controls expand horizontally if they support it
        for control in controls:
            if hasattr(control, 'expand') and not isinstance(control, (ft.Text, ft.Icon)):
                control.expand = True
            if hasattr(control, 'width'):
                control.width = None  # Remove any fixed width to allow expansion
        
        self.content_container.update()

    def _handle_window_event(self, e):
        if e.data == "close":
            self._page.window.destroy()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._page, name)

def main(page: ft.Page):

    custom_titlebar = Titlebar(
        title="fluent flet",
        icon=ft.Image(src="fluentflet/static/fluentflet.png", width=18, height=18),
    )

    window = FluentWindow(
        page,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home"},
            {"icon": FluentIcons.PERSON, "label": "Profile"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings"},
        ],
        window_title=custom_titlebar
    )


    # Create your views
    home_view = ft.Column(
        controls=[
            ft.Text("Home View", size=30, color="white"),
            ft.ElevatedButton("Home Action"),
        ],
    )
    
    profile_view = ft.Column(
        controls=[
            ft.Text("Profile View", size=30, color="white"),
            ft.TextField(label="Name", border_color="white"),
        ],
    )
    
    settings_view = ft.Column(
        controls=[
            ft.Text("Settings View", size=30, color="white"),
            ft.Switch(label="Dark Mode", value=True),
        ],
    )
    
    # Add routes
    window.add_route("home", home_view)
    window.add_route("profile", profile_view)
    window.add_route("settings", settings_view)
    
    # Set initial route
    window.navigate("home")

ft.app(target=main)