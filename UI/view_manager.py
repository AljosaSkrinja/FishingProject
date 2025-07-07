import dearpygui.dearpygui as dpg
from config import *

class ViewManager:
    """
    View Manager for Fishing Planet Application
    
    This class manages the switching between different views/sections of the application.
    It handles view state management and coordinates the display of different data sections
    like rods, fish, lakes, etc.
    
    Responsibilities:
    - Switch between different application views
    - Manage view visibility states
    - Clear and refresh view content
    - Coordinate with display manager for data presentation
    """
    
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self.views = {
            'rods': {
                'group': UI_TAGS['rods_group'],
                'display_method': self.display_manager.display_rods_data
            },
            'reels': {
                'group': UI_TAGS['reels_group'],
                'display_method': self.display_manager.display_reels_data
            }
        }
    
    def switch_view(self, target_view):
        """Switch to the specified view and refresh its content"""
        for view_name, view_config in self.views.items():
            dpg.configure_item(view_config['group'], show=(view_name == target_view))
        
        target_config = self.views[target_view]
        dpg.delete_item(target_config['group'], children_only=True)
        target_config['display_method']()
        
        dpg.set_value(UI_TAGS['search_input'], "")
    
    def show_rods(self):
        """Switch to the rods view and display fishing rods data"""
        self.switch_view('rods')
    
    def show_reels(self):
        """Switch to the reels view and display fishing reels data"""
        self.switch_view('reels') 