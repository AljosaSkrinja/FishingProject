import dearpygui.dearpygui as dpg
from config import *
from UI.ui_components import UIComponents

class MainUIOrchestrator:
    """
    Main UI orchestrator for the Fishing Planet application.
    
    This class coordinates all UI components and manages the overall application interface.
    It handles the main window setup, callbacks, and coordinates between different UI managers.
    """
    
    def __init__(self, data_manager, display_manager, view_manager):
        self.data_manager = data_manager
        self.display_manager = display_manager
        self.view_manager = view_manager
        
        self.setup_callbacks()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the main UI layout and components"""
        dpg.set_viewport_resize_callback(self.resize_callback)
        
        with UIComponents.create_main_window():
            UIComponents.create_navigation_bar(self.callbacks)
            UIComponents.create_search_bar(self.search_callback, self.on_enter)
            UIComponents.create_content_areas()
    
    def setup_callbacks(self):
        """Setup callback mappings for UI interactions"""
        self.callbacks = {
            'show_rods': self.view_manager.show_rods,
            'show_reels': self.view_manager.show_reels
        }
    
    def search_callback(self):
        """Handle search input changes"""
        search_term = dpg.get_value(UI_TAGS['search_input']).lower()
        self.display_manager.display_search_results(search_term)
    
    def on_enter(self):
        """Handle Enter key press in search field"""
        self.search_callback()
    
    def resize_callback(self):
        """Handle window resize events"""
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        
        dpg.configure_item(UI_TAGS['main_window'], width=viewport_width, height=viewport_height)
        
        UIComponents.recenter_navigation_bar(self.callbacks, self.display_manager)
        UIComponents.recenter_search_bar(self.search_callback, self.on_enter, self.display_manager)
        
        self.display_manager.refresh_current_view() 