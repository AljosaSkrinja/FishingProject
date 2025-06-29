import dearpygui.dearpygui as dpg
from config import UI_TAGS
from UI.ui_components import UIComponents

class FishingPlanetUI:
    """Main UI controller that handles UI design and user interactions."""
    
    def __init__(self, data_manager, display_manager, view_manager):
        self.data_manager = data_manager
        self.display_manager = display_manager
        self.view_manager = view_manager
        
        # Setup callbacks first
        self.setup_callbacks()
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the main UI window and components."""
        # Set resize callback
        dpg.set_viewport_resize_callback(self.resize_callback)
        
        # Create main window and components
        with UIComponents.create_main_window():
            UIComponents.create_navigation_bar(self.callbacks)
            UIComponents.create_search_bar(self.search_callback, self.on_enter)
            UIComponents.create_content_areas()
    
    def setup_callbacks(self):
        """Setup callback methods for navigation and search."""
        self.callbacks = {
            'show_fish': self.view_manager.show_fish,
            'show_lakes': self.view_manager.show_lakes,
            'show_rods': self.view_manager.show_rods
        }
    
    def search_callback(self):
        """Handle search functionality."""
        search_term = dpg.get_value(UI_TAGS['search_input']).lower()
        self.display_manager.display_search_results(search_term)
    
    def on_enter(self):
        """Handle Enter key press in search input."""
        self.search_callback()
    
    def resize_callback(self):
        """Handle window resize events."""
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        
        # Resize main window
        dpg.configure_item(UI_TAGS['main_window'], width=viewport_width, height=viewport_height)
        
        # Recenter UI components
        UIComponents.recenter_navigation_bar(viewport_width, self.callbacks, self.display_manager)
        UIComponents.recenter_search_bar(viewport_width, self.search_callback, self.on_enter, self.display_manager)
        
        # Refresh current view
        self.display_manager.refresh_current_view() 