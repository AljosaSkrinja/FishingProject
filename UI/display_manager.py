import dearpygui.dearpygui as dpg
from config import UI_TAGS, CARD_WIDTH, CARD_HEIGHT
from UI.ui_components import UIComponents

class DisplayManager:
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.display_methods = {
            'fish': self.display_fish_data,
            'lakes': self.display_lakes_data,
            'rods': self.display_rods_data
        }
    
    def display_cards(self, data, parent_group):
        display_data = self.data_manager.get_display_ready_data(data)
        if not display_data:
            self._show_no_data_message(parent_group)
            return
        available_width, cards_per_row = self.calculate_layout_parameters()
        rows = self.group_data_into_rows(display_data, cards_per_row)
        for row in rows:
            UIComponents.create_card_row(row, parent_group, available_width, self.data_manager)
    
    def calculate_layout_parameters(self):
        viewport_width = dpg.get_viewport_width()
        available_width = viewport_width - 40
        cards_per_row = max(1, int(available_width / (CARD_WIDTH + 20)))
        return available_width, cards_per_row
    
    def group_data_into_rows(self, data, cards_per_row):
        rows = []
        current_row = []
        
        for item in data:
            current_row.append(item)
            
            if len(current_row) >= cards_per_row:
                rows.append(current_row)
                current_row = []
        
        if current_row:
            rows.append(current_row)
        
        return rows
    
    def get_navigation_group(self):
        return dpg.get_item_children(UI_TAGS['main_window'])[1][0]
    
    def get_search_group(self):
        return dpg.get_item_children(UI_TAGS['main_window'])[1][1]
    
    def _show_no_data_message(self, parent_group):
        dpg.add_text("No data available.", parent=parent_group)
    
    def display_fish_data(self):
        self._display_data(self.data_manager.get_fish_data, UI_TAGS['fish_group'])
    
    def display_lakes_data(self):
        self._display_data(self.data_manager.get_lakes_data, UI_TAGS['lakes_group'])
    
    def display_rods_data(self):
        self._display_rods_by_category(self.data_manager.get_rods_by_category())
    
    def _display_data(self, get_data_method, group_tag):
        data = get_data_method()
        self.display_cards(data, group_tag)
    
    def _display_rods_by_category(self, rods_by_category):
        if not rods_by_category:
            self._show_no_data_message(UI_TAGS['rods_group'])
            return
        for category_name, rods in rods_by_category.items():
            dpg.add_text(f"=== {category_name} ===", parent=UI_TAGS['rods_group'])
            self.display_cards(rods, UI_TAGS['rods_group'])
            dpg.add_spacer(height=20, parent=UI_TAGS['rods_group'])
    
    def display_search_results(self, search_term):
        view_mapping = {
            UI_TAGS['fish_group']: ('fish', self._display_search_results_generic),
            UI_TAGS['lakes_group']: ('lakes', self._display_search_results_generic),
            UI_TAGS['rods_group']: (None, self._display_search_results_rods)
        }
        
        for group_tag, (data_type, method) in view_mapping.items():
            if dpg.is_item_visible(group_tag):
                if data_type:
                    method(data_type, search_term, group_tag)
                else:
                    method(search_term)
                break
    
    def _display_search_results_generic(self, data_type, search_term, group_tag):
        search_method = getattr(self.data_manager, f'search_{data_type}')
        filtered_data = search_method(search_term)
        dpg.delete_item(group_tag, children_only=True)
        if filtered_data:
            self.display_cards(filtered_data, group_tag)
        else:
            dpg.add_text(f"No {data_type} found matching your search.", parent=group_tag)
    
    def _display_search_results_rods(self, search_term):
        filtered_rods = self.data_manager.search_rods(search_term)
        dpg.delete_item(UI_TAGS['rods_group'], children_only=True)
        processed_results = self.data_manager.process_search_results(filtered_rods)
        if processed_results:
            self._display_rods_by_category(processed_results)
        else:
            dpg.add_text("No rods found matching your search.", parent=UI_TAGS['rods_group'])
    
    def refresh_current_view(self):
        view_mapping = {
            UI_TAGS['fish_group']: self.display_fish_data,
            UI_TAGS['lakes_group']: self.display_lakes_data,
            UI_TAGS['rods_group']: self.display_rods_data
        }
        for group_tag, display_method in view_mapping.items():
            if dpg.is_item_visible(group_tag):
                dpg.delete_item(group_tag, children_only=True)
                display_method()
                break 