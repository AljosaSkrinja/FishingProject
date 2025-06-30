import dearpygui.dearpygui as dpg
from config import UI_TAGS

class ViewManager:
    
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
        for view_name, view_config in self.views.items():
            dpg.configure_item(view_config['group'], show=(view_name == target_view))
        
        target_config = self.views[target_view]
        dpg.delete_item(target_config['group'], children_only=True)
        target_config['display_method']()
        
        dpg.set_value(UI_TAGS['search_input'], "")
    
    def show_fish(self):
        self.switch_view('fish')
    
    def show_lakes(self):
        self.switch_view('lakes')
    
    def show_rods(self):
        self.switch_view('rods') 