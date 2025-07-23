import dearpygui.dearpygui as dpg
from config import *
from UI.ui_components import UIComponents
from UI.ui_card_layout import UICardLayout

class DisplayManager:
    """
    Display Manager for Fishing Planet Application
    
    This class manages the display and presentation of data in the UI.
    It coordinates between the data manager and UI components to show
    fishing equipment data in an organized and user-friendly manner.
    
    Responsibilities:
    - Display fishing rods data by category
    - Handle search results display
    - Manage view refreshing and updates
    - Coordinate with card layout system
    """
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.card_layout = UICardLayout(data_manager)
        self.display_methods = {
            'rods': self.display_rods_data,
            'reels': self.display_reels_data
        }
    
    def get_navigation_group(self):
        """Get the navigation group UI element"""
        return dpg.get_item_children(UI_TAGS['main_window'])[CHILDREN_INDEX][NAVIGATION_GROUP_INDEX]
    
    def get_search_group(self):
        """Get the search group UI element"""
        return dpg.get_item_children(UI_TAGS['main_window'])[CHILDREN_INDEX][SEARCH_GROUP_INDEX]
    
    def display_rods_data(self):
        """Display all fishing rods data organized by category"""
        self._display_rods_by_category(self.data_manager.get_rods_by_category())
    
    def display_reels_data(self):
        """Display all fishing reels data organized by category"""
        self._display_reels_by_category(self.data_manager.get_reels_by_category())
    
    def _display_rods_by_category(self, rods_by_category):
        """Display rods grouped by their categories with headers"""
        if not rods_by_category:
            self.card_layout._show_no_data_message(UI_TAGS['rods_group'])
            return
        for category_name, rods in rods_by_category.items():
            dpg.add_text(CATEGORY_HEADER_FORMAT.format(category_name), parent=UI_TAGS['rods_group'])
            self.card_layout.display_cards(rods, UI_TAGS['rods_group'])
            dpg.add_spacer(height=CATEGORY_SPACING, parent=UI_TAGS['rods_group'])
    
    def _display_reels_by_category(self, reels_by_category):
        """Display reels grouped by their categories with headers"""
        if not reels_by_category:
            self.card_layout._show_no_data_message(UI_TAGS['reels_group'])
            return
        for category_name, reels in reels_by_category.items():
            dpg.add_text(CATEGORY_HEADER_FORMAT.format(category_name), parent=UI_TAGS['reels_group'])
            self.card_layout.display_cards(reels, UI_TAGS['reels_group'])
            dpg.add_spacer(height=CATEGORY_SPACING, parent=UI_TAGS['reels_group'])
    
    def display_search_results(self, search_term):
        """Display search results for the given search term"""
        filtered_rods = self.data_manager.search_rods(search_term)
        dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
        processed_results = self.data_manager.process_search_results(filtered_rods)
        if processed_results:
            self._display_rods_by_category(processed_results)
        else:
            dpg.add_text(NO_RODS_FOUND_MESSAGE, parent=UI_TAGS['rods_group'])
    
    def display_reel_search_results(self, search_term):
        """Display search results for reels"""
        filtered_reels = self.data_manager.search_reels(search_term)
        dpg.delete_item(UI_TAGS['reels_group'], children_only=True)
        processed_results = self.data_manager.process_reel_search_results(filtered_reels)
        if processed_results:
            self._display_reels_by_category(processed_results)
        else:
            dpg.add_text(NO_REELS_FOUND_MESSAGE, parent=UI_TAGS['reels_group'])
    
    def refresh_current_view(self):
        """Refresh the current view by clearing and redisplaying data"""
        dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
        self.display_rods_data()
    
    def refresh_current_view_responsive(self):
        """Refresh the current view with responsive layout recalculation"""
        # Determine which view is currently active
        rods_visible = dpg.is_item_visible(UI_TAGS['rods_group'])
        reels_visible = dpg.is_item_visible(UI_TAGS['reels_group'])
        
        if rods_visible:
            # Clear and redisplay rods with responsive layout
            dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
            self.display_rods_data()
        elif reels_visible:
            # Clear and redisplay reels with responsive layout
            dpg.delete_item(UI_TAGS['reels_group'], children_only=True)
            self.display_reels_data() 