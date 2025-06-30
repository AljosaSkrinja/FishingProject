import dearpygui.dearpygui as dpg
from config import UI_TAGS
from UI.ui_components import UIComponents

class FishingPlanetUI:
    def __init__(self, data_manager, display_manager, view_manager):
        self.data_manager = data_manager
        self.display_manager = display_manager
        self.view_manager = view_manager
        
        self.setup_callbacks()
        
        self.setup_ui()
    
    def setup_ui(self):
        dpg.set_viewport_resize_callback(self.resize_callback)
        
        with UIComponents.create_main_window():
            UIComponents.create_navigation_bar(self.callbacks)
            UIComponents.create_search_bar(self.search_callback, self.on_enter)
            UIComponents.create_content_areas()
    
    def setup_callbacks(self):
        self.callbacks = {
            'show_fish': self.view_manager.show_fish,
            'show_lakes': self.view_manager.show_lakes,
            'show_rods': self.view_manager.show_rods
        }
    
    def search_callback(self):
        search_term = dpg.get_value(UI_TAGS['search_input']).lower()
        self.display_manager.display_search_results(search_term)
    
    def on_enter(self):
        self.search_callback()
    
    def resize_callback(self):
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        
        dpg.configure_item(UI_TAGS['main_window'], width=viewport_width, height=viewport_height)
        
        UIComponents.recenter_navigation_bar(self.callbacks, self.display_manager)
        UIComponents.recenter_search_bar(self.search_callback, self.on_enter, self.display_manager)
        
        self.display_manager.refresh_current_view() 