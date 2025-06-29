import dearpygui.dearpygui as dpg
from config import UI_TAGS, CARD_WIDTH, CARD_HEIGHT
from UI.ui_components import UIComponents

class DisplayManager:
    """Handles all display logic for cards and data presentation."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.display_methods = {
            'fish': self.display_fish_data,
            'lakes': self.display_lakes_data,
            'rods': self.display_rods_data
        }
    
    def display_cards(self, data, parent_group):
        """Display data items as cards in a centered grid layout."""
        try:
            # Get display-ready data from data manager
            display_data = self.data_manager.get_display_ready_data(data)
            
            if not display_data:
                self._show_no_data_message(parent_group)
                return
            
            # Get layout parameters
            available_width, cards_per_row = self.calculate_layout_parameters()
            
            # Group data into rows
            rows = self.group_data_into_rows(display_data, cards_per_row)
            
            # Display each row
            for row in rows:
                UIComponents.create_card_row(row, parent_group, available_width, self.data_manager)
                
        except Exception as e:
            self._show_error_message(parent_group, f"Error displaying data: {str(e)}")
    
    def calculate_layout_parameters(self):
        """Calculate layout parameters for card display."""
        viewport_width = dpg.get_viewport_width()
        available_width = viewport_width - 40  # 20px margin on each side
        cards_per_row = max(1, int(available_width / (CARD_WIDTH + 20)))  # 20px spacing
        return available_width, cards_per_row
    
    def group_data_into_rows(self, data, cards_per_row):
        """Group data items into rows for display."""
        rows = []
        current_row = []
        
        for item in data:
            current_row.append(item)
            
            if len(current_row) >= cards_per_row:
                rows.append(current_row)
                current_row = []
        
        # Add remaining items as the last row
        if current_row:
            rows.append(current_row)
        
        return rows
    
    def get_navigation_group(self):
        """Get the navigation group element."""
        try:
            return dpg.get_item_children(UI_TAGS['main_window'])[1][0]
        except Exception as e:
            print(f"Error getting navigation group: {e}")
            return None
    
    def get_search_group(self):
        """Get the search bar group element."""
        try:
            return dpg.get_item_children(UI_TAGS['main_window'])[1][1]
        except Exception as e:
            print(f"Error getting search group: {e}")
            return None
    
    def _show_no_data_message(self, parent_group):
        """Show a message when no data is available."""
        dpg.add_text("No data available.", parent=parent_group)
    
    def _show_error_message(self, parent_group, message):
        """Show an error message."""
        dpg.add_text(message, parent=parent_group)
    
    def display_fish_data(self):
        """Display fish data."""
        try:
            fish_data = self.data_manager.get_fish_data()
            self.display_cards(fish_data, UI_TAGS['fish_group'])
        except Exception as e:
            self._show_error_message(UI_TAGS['fish_group'], f"Error displaying fish: {str(e)}")
    
    def display_lakes_data(self):
        """Display lakes data."""
        try:
            lakes_data = self.data_manager.get_lakes_data()
            self.display_cards(lakes_data, UI_TAGS['lakes_group'])
        except Exception as e:
            self._show_error_message(UI_TAGS['lakes_group'], f"Error displaying lakes: {str(e)}")
    
    def display_rods_data(self):
        """Display all rods data organized by category."""
        try:
            rods_by_category = self.data_manager.get_rods_by_category()
            
            if not rods_by_category:
                self._show_no_data_message(UI_TAGS['rods_group'])
                return
            
            # Display rods by category
            for category_name, rods in rods_by_category.items():
                # Add category header
                dpg.add_text(f"=== {category_name} ===", parent=UI_TAGS['rods_group'])
                
                # Display rods in this category
                self.display_cards(rods, UI_TAGS['rods_group'])
                
                # Add some spacing between categories
                dpg.add_spacer(height=20, parent=UI_TAGS['rods_group'])
                
        except Exception as e:
            self._show_error_message(UI_TAGS['rods_group'], f"Error displaying rods: {str(e)}")
    
    def display_search_results(self, search_term):
        """Display search results based on current view."""
        try:
            if dpg.is_item_visible(UI_TAGS['fish_group']):
                self._display_search_results_generic('fish', search_term, UI_TAGS['fish_group'])
            elif dpg.is_item_visible(UI_TAGS['lakes_group']):
                self._display_search_results_generic('lakes', search_term, UI_TAGS['lakes_group'])
            elif dpg.is_item_visible(UI_TAGS['rods_group']):
                self._display_search_results_rods(search_term)
        except Exception as e:
            print(f"Error displaying search results: {e}")
    
    def _display_search_results_generic(self, data_type, search_term, group_tag):
        """Generic method to display search results for fish and lakes."""
        try:
            # Get search method based on data type
            search_method = getattr(self.data_manager, f'search_{data_type}')
            filtered_data = search_method(search_term)
            
            dpg.delete_item(group_tag, children_only=True)
            
            if filtered_data:
                self.display_cards(filtered_data, group_tag)
            else:
                dpg.add_text(f"No {data_type} found matching your search.", parent=group_tag)
        except Exception as e:
            self._show_error_message(group_tag, f"Error searching {data_type}: {str(e)}")
    
    def _display_search_results_rods(self, search_term):
        """Display filtered rods search results with category grouping."""
        try:
            filtered_rods = self.data_manager.search_rods(search_term)
            dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
            
            # Process search results using data manager
            processed_results = self.data_manager.process_search_results(filtered_rods)
            
            if processed_results:
                self._display_rods_by_category(processed_results)
            else:
                dpg.add_text("No rods found matching your search.", parent=UI_TAGS['rods_group'])
        except Exception as e:
            self._show_error_message(UI_TAGS['rods_group'], f"Error searching rods: {str(e)}")
    
    def _display_rods_by_category(self, rods_by_category):
        """Display rods organized by category."""
        for category_name, rods in rods_by_category.items():
            # Add category header
            dpg.add_text(f"=== {category_name} ===", parent=UI_TAGS['rods_group'])
            
            # Display rods in this category
            self.display_cards(rods, UI_TAGS['rods_group'])
            
            # Add some spacing between categories
            dpg.add_spacer(height=20, parent=UI_TAGS['rods_group'])
    
    def refresh_current_view(self):
        """Refresh the currently visible view to update card layout."""
        try:
            if dpg.is_item_visible(UI_TAGS['fish_group']):
                dpg.delete_item(UI_TAGS['fish_group'], children_only=True)
                self.display_fish_data()
            elif dpg.is_item_visible(UI_TAGS['lakes_group']):
                dpg.delete_item(UI_TAGS['lakes_group'], children_only=True)
                self.display_lakes_data()
            elif dpg.is_item_visible(UI_TAGS['rods_group']):
                dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
                self.display_rods_data()
        except Exception as e:
            print(f"Error refreshing current view: {e}") 