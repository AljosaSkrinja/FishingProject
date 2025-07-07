import dearpygui.dearpygui as dpg
from config import *
from UI.ui_components import UIComponents

class UICardLayout:
    """
    UI Card Layout Manager for Fishing Planet Application
    
    This class handles the layout and positioning of data cards in the UI.
    It manages grid layouts, responsive design, and card organization for
    displaying fishing equipment data in an organized grid format.
    
    Responsibilities:
    - Calculate responsive layout parameters
    - Group data into grid rows
    - Display cards in organized layouts
    - Handle empty data states
    - Manage card spacing and positioning
    """
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def display_cards(self, data, parent_group):
        """Display cards in a responsive grid layout within the parent group"""
        if not data:
            self._show_no_data_message(parent_group)
            return
        available_width, cards_per_row = self.calculate_layout_parameters()
        rows = self.group_data_into_rows(data, cards_per_row)
        for row in rows:
            UIComponents.create_card_row(row, parent_group, available_width, self.data_manager)
    
    def calculate_layout_parameters(self):
        """Calculate responsive layout parameters based on viewport size"""
        viewport_width = dpg.get_viewport_width()
        available_width = viewport_width - WINDOW_PADDING
        cards_per_row = max(1, int(available_width / (CARD_WIDTH + CARD_ROW_SPACING)))
        return available_width, cards_per_row
    
    def group_data_into_rows(self, data, cards_per_row):
        """Group data items into rows for grid layout display"""
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
    
    def _show_no_data_message(self, parent_group):
        """Display a message when no data is available to show"""
        dpg.add_text(NO_DATA_MESSAGE, parent=parent_group) 