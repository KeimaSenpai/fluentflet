'''
You can also navigate programmatically from anywhere:
def handle_button_click(e):
    window.navigate("settings")

home_view = ft.Column(
    controls=[
        ft.Text("Home View", size=30, color="white"),
        ft.ElevatedButton("Go to Settings", on_click=handle_button_click),
    ],
)
Or create a more complex routing system:
def HomeView(ft.UserControl):
    def __init__(self, window: FluentWindow):
        super().__init__()
        self.window = window
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Home View", size=30, color="white"),
                ft.ElevatedButton(
                    "Go to Profile",
                    on_click=lambda _: self.window.navigate("profile")
                ),
            ],
        )

def main(page: ft.Page):
    window = FluentWindow(
        page,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home"},
            {"icon": FluentIcons.PERSON, "label": "Profile"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings"},
        ],
    )
    
    # Create views with access to the window
    window.add_route("home", HomeView(window))
    window.add_route("profile", ProfileView(window))
    window.add_route("settings", SettingsView(window))
    
    # Start at home
    window.navigate("home")

ft.app(target=main)
You could even add route parameters:
# Usage:
def user_profile(user_id: str = None):
    return ft.Column(
        controls=[
            ft.Text(f"Profile for user {user_id}", size=30, color="white"),
        ],
    )

window.add_route("user_profile", user_profile)
window.navigate("user_profile", user_id="123")
'''

import flet as ft
from fluentflet.components import ListItem, Button, ButtonVariant, ToolTip
from fluentflet.utils import FluentIcon, FluentIcons
from typing import Optional, Any, Callable, Union, Dict

class NavigationDivider(ft.Container):
    def __init__(self):
        super().__init__(
            height=.5,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#393939",
            width=180
        )

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
        self.top_bar_color = "transparent" # "#1F1F1F"
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
            weight=ft.FontWeight.NORMAL,
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
        bottom_navigation_items=None,
        selected_index=0,
        window_titlebar: Union[str, Titlebar] = "Fluent Flet",
        colors=None,
        nav_width_collapsed=50,
        nav_width_expanded=200,
        animation_duration=100,
        show_back_button=True,
    ):
        self._page = page
        self._page.window.title_bar_hidden = True
        self._page.window.title_bar_buttons_hidden = True
        self._page.theme = ft.Theme(scrollbar_theme=ft.ScrollbarTheme(thickness=0.0))
        self._page.accepts_drops = True
        self._page.blur_effect = True
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
        if self._page.blur_effect:
            self.colors["content_bg"] = ft.colors.with_opacity(0.3, self.colors["content_bg"])
            self.colors["nav_bg"] = ft.colors.with_opacity(0.3, self.colors["nav_bg"])
        
        self._page.bgcolor = self.colors["nav_bg"]
        
        # Initialize main layout components
        self.navigation_items = navigation_items or [{"icon": FluentIcons.HOME, "label": "Home"}]
        self.bottom_navigation_items = bottom_navigation_items or [{"icon": FluentIcons.SETTINGS, "label": "Settings"},]
        
        # Handle window_title based on type
        self.titlebar = (window_titlebar if isinstance(window_titlebar, Titlebar) 
                        else Titlebar(title=str(window_titlebar)))
        
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

    def add_navigation_divider(self, after_index: int):
        """Add a divider after the specified navigation item index"""
        if 0 <= after_index < len(self.nav_items):
            divider = NavigationDivider()
            self.nav_items.insert(after_index + 1, divider)
            self._nav_item_intern.insert(after_index + 1, divider)

    def create_nav_item(self, item: Dict, index: int) -> ft.Control:
        """Create either a navigation item or a divider based on the item type"""
        if item.get("type") == "divider":
            return NavigationDivider()
        else:
            _item = self.create_nav_row(item["icon"], item["label"])
            list_item = ListItem(
                content=_item,
                on_click=lambda e, i=index: self.handle_nav_click(i),
                is_dark_mode=True,
            )
            self._nav_item_intern.append(_item)
            return list_item

    def create_layout(self, nav_width_collapsed, nav_width_expanded, 
                    animation_duration, show_back_button, selected_index):
        """Create the main layout"""
        # Create navigation items
        self.nav_items = []
        self._nav_item_intern = []
        
        # Track the actual index (excluding dividers) for navigation
        self.nav_index_map = {}
        actual_index = 0
        
        # Create top navigation items
        for idx, item in enumerate(self.navigation_items):
            nav_item = self.create_nav_item(item, actual_index)
            self.nav_items.append(nav_item)
            
            if item.get("type") != "divider":
                self.nav_index_map[actual_index] = idx
                actual_index += 1

        # Create navigation rail with scrollable list
        nav_top_controls = []
        if show_back_button:
            nav_top_controls.extend([
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
        
        nav_top_controls.append(
            Button(
                content=FluentIcon(
                    FluentIcons.TEXT_ALIGN_JUSTIFY,
                    size=18,
                    color=self.colors["icon_color"]
                ),
                on_click=lambda e: self.toggle_navigation_panel(e),
                variant=ButtonVariant.HYPERLINK,
                is_dark_mode=True,
            )
        )

        # Create bottom navigation items
        bottom_nav_items = []
        for idx, item in enumerate(self.bottom_navigation_items):
            nav_item = self.create_nav_item(item, actual_index + idx)
            bottom_nav_items.append(nav_item)

        # Create the navigation rail with top, scrollable middle, and bottom sections
        self.nav_rail = ft.Container(
            content=ft.Column(
                controls=[
                    # Top section with back button and menu toggle
                    ft.Container(
                        ft.Column(
                            controls=nav_top_controls,
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            # margin=ft.margin.only(left=5)
                        ),
                        margin=ft.margin.only(left=5)
                    ),
                    # Middle section with scrollable navigation
                    ft.Container(
                        content=ft.Column(
                            controls=self.nav_items,
                            spacing=2,
                            scroll=ft.ScrollMode.HIDDEN,  # Enable scrolling
                        ),
                        expand=True,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # Clip overflow content
                    ),
                    # Bottom section
                    ft.Column(
                        controls=bottom_nav_items,
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ) if bottom_nav_items else None
                ],
                spacing=0,
                expand=True
            ),
            width=nav_width_collapsed,
            padding=ft.padding.only(left=5, right=5, bottom=10),
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
        
        # Set initial selection (accounting for dividers)
        self.select_nav_item(selected_index)

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
                if isinstance(item, ft.Row):  # Skip dividers
                    item.controls[1].opacity = 1
                    item.alignment = ft.MainAxisAlignment.START
                    item.update()
        else:
            self.nav_rail.width = self.nav_width_collapsed
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            for item in self._nav_item_intern:
                if isinstance(item, ft.Row):  # Skip dividers
                    item.controls[1].opacity = 0
                    item.alignment = ft.MainAxisAlignment.CENTER
                    item.update()
        
        self.nav_rail.update()

    def select_nav_item(self, index: int):
        """Select a navigation item, accounting for dividers"""
        # Clear all selections
        for item in self.nav_items:
            if isinstance(item, ListItem):
                item.is_selected = False
        
        # Find the actual item to select
        actual_idx = self.nav_index_map.get(index)
        if actual_idx is not None:
            item = self.nav_items[actual_idx]
            if isinstance(item, ListItem):
                item.is_selected = True
                self.selected_index = index

    def handle_nav_click(self, index: int):
        """Handle navigation item click and route change"""
        self.select_nav_item(index)
        
        # Navigate to the corresponding route
        actual_idx = self.nav_index_map.get(index)
        if actual_idx is not None:
            route = self.navigation_items[actual_idx]["label"].lower()
            self.navigate(route)
        
        # Update navigation items' visual state
        for item in self.nav_items:
            if isinstance(item, ListItem):
                item.update()

    def add(self, *controls):
        """Override add to use our content container"""
        self.content_container.content.controls = list(controls)
        for control in controls:
            if hasattr(control, 'expand') and not isinstance(control, (ft.Text, ft.Icon)):
                control.expand = True
            if hasattr(control, 'width'):
                control.width = None
        self.content_container.update()

    def _handle_window_event(self, e):
        if e.data == "close":
            self._page.window.destroy()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._page, name)