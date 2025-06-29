import dearpygui.dearpygui as dpg
from config import UI_TAGS

class ViewManager:
    """Handles view switching and navigation logic."""
    
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self.views = {
            'fish': {
                'group': UI_TAGS['fish_group'],
                'display_method': self.display_manager.display_fish_data
            },
            'lakes': {
                'group': UI_TAGS['lakes_group'],
                'display_method': self.display_manager.display_lakes_data
            },
            'rods': {
                'group': UI_TAGS['rods_group'],
                'display_method': self.display_manager.display_rods_data
            }
        }
    
    def switch_view(self, target_view):
        """Switch to the specified view, hiding all others."""
        # Hide all views
        for view_name, view_config in self.views.items():
            dpg.configure_item(view_config['group'], show=(view_name == target_view))
        
        # Clear the target view and display data
        target_config = self.views[target_view]
        dpg.delete_item(target_config['group'], children_only=True)
        target_config['display_method']()
        
        # Clear search input
        dpg.set_value(UI_TAGS['search_input'], "")
    
    def show_fish(self):
        """Show fish data and hide other sections."""
        self.switch_view('fish')
    
    def show_lakes(self):
        """Show lakes data and hide other sections."""
        self.switch_view('lakes')
    
    def show_rods(self):
        """Show rods data."""
        self.switch_view('rods') 