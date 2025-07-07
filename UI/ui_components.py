import dearpygui.dearpygui as dpg
from config import *

class UIComponents:
    """
    UI Components Factory Class
    
    This class provides static methods for creating and managing all UI components
    in the Fishing Planet application. It handles:
    - Main window creation
    - Navigation bar components
    - Search functionality
    - Content areas
    - Card layouts and display
    - Responsive layout adjustments
    """
    
    # ==================== MAIN WINDOW CREATION ====================
    
    @staticmethod
    def create_main_window():
        """Create the main application window"""
        return dpg.window(
            label=MAIN_WINDOW_LABEL, 
            tag=UI_TAGS['main_window'], 
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            no_title_bar=True, 
            no_collapse=True
        )
    
    # ==================== NAVIGATION BAR COMPONENTS ====================
    
    @staticmethod
    def create_navigation_bar(callbacks):
        """Create the main navigation bar with centered buttons"""
        with dpg.group(horizontal=True, tag=UI_TAGS['nav_group']):
            UIComponents._add_centered_navigation_buttons(callbacks)
    
    @staticmethod
    def _add_centered_navigation_buttons(callbacks, parent_group=None):
        """Add navigation buttons with proper centering and spacing"""
        viewport_width = dpg.get_viewport_width()
        total_width = len(NAVIGATION_BUTTONS) * NAV_BUTTON_WIDTH + (len(NAVIGATION_BUTTONS) - 1) * NAV_BUTTON_SPACING
        left_spacer_width = max(0, (viewport_width - total_width) // 2)
        
        if left_spacer_width > 0:
            UIComponents._add_spacer(width=int(left_spacer_width), parent_group=parent_group)
        
        for i, button_config in enumerate(NAVIGATION_BUTTONS):
            callback_method = callbacks[button_config['callback']]
            if parent_group is not None:
                dpg.add_button(
                    label=button_config['label'], 
                    tag=f"{button_config['label'].lower().replace(' ', '_')}_button",
                    width=NAV_BUTTON_WIDTH, 
                    height=NAV_BUTTON_HEIGHT, 
                    callback=callback_method,
                    parent=parent_group
                )
            else:
                dpg.add_button(
                    label=button_config['label'], 
                    tag=f"{button_config['label'].lower().replace(' ', '_')}_button",
                    width=NAV_BUTTON_WIDTH, 
                    height=NAV_BUTTON_HEIGHT, 
                    callback=callback_method
                )
            
            if i < len(NAVIGATION_BUTTONS) - 1:
                UIComponents._add_spacer(width=NAV_BUTTON_SPACING, parent_group=parent_group)
        
        if left_spacer_width > 0:
            UIComponents._add_spacer(width=int(left_spacer_width), parent_group=parent_group)
    
    # ==================== SEARCH BAR COMPONENTS ====================
    
    @staticmethod
    def create_search_bar(search_callback, enter_callback):
        """Create the search bar with input field and search button"""
        with dpg.group(horizontal=True):
            UIComponents._add_centered_search_components(search_callback, enter_callback)
    
    @staticmethod
    def _add_centered_search_components(search_callback, enter_callback, parent_group=None):
        """Add search components with proper centering and spacing"""
        viewport_width = dpg.get_viewport_width()
        search_area_width = SEARCH_INPUT_WIDTH + NAV_BUTTON_SPACING + SEARCH_BUTTON_WIDTH
        left_spacer_width = max(0, (viewport_width - search_area_width) // 2)
        
        if left_spacer_width > 0:
            UIComponents._add_spacer(width=int(left_spacer_width), parent_group=parent_group)
        
        if parent_group is not None:
            dpg.add_input_text(
                tag=UI_TAGS['search_input'], 
                on_enter=True, 
                callback=enter_callback, 
                hint=SEARCH_HINT, 
                width=SEARCH_INPUT_WIDTH, 
                height=SEARCH_INPUT_HEIGHT, 
                parent=parent_group
            )
            UIComponents._add_spacer(width=NAV_BUTTON_SPACING, parent_group=parent_group)
            dpg.add_button(
                label=SEARCH_BUTTON_LABEL, 
                tag=UI_TAGS['search_button'], 
                callback=search_callback, 
                width=SEARCH_BUTTON_WIDTH, 
                height=SEARCH_BUTTON_HEIGHT, 
                parent=parent_group
            )
        else:
            dpg.add_input_text(
                tag=UI_TAGS['search_input'], 
                on_enter=True, 
                callback=enter_callback, 
                hint=SEARCH_HINT, 
                width=SEARCH_INPUT_WIDTH, 
                height=SEARCH_INPUT_HEIGHT
            )
            UIComponents._add_spacer(width=NAV_BUTTON_SPACING)
            dpg.add_button(
                label=SEARCH_BUTTON_LABEL, 
                tag=UI_TAGS['search_button'], 
                callback=search_callback, 
                width=SEARCH_BUTTON_WIDTH, 
                height=SEARCH_BUTTON_HEIGHT
            )
        
        if left_spacer_width > 0:
            UIComponents._add_spacer(width=int(left_spacer_width), parent_group=parent_group)
    
    # ==================== CONTENT AREA CREATION ====================
    
    @staticmethod
    def create_content_areas():
        """Create content areas for different data sections"""
        dpg.add_group(tag=UI_TAGS['rods_group'])
        dpg.add_group(tag=UI_TAGS['reels_group'])
    
    # ==================== CARD LAYOUT AND DISPLAY ====================
    
    @staticmethod
    def create_card_row(cards_in_row, parent_group, available_width, data_manager=None):
        """Create a row of cards with proper spacing and centering"""
        with dpg.group(horizontal=True, parent=parent_group):
            UIComponents._add_centered_cards(cards_in_row, available_width, data_manager)
    
    @staticmethod
    def _add_centered_cards(cards_in_row, available_width, data_manager=None):
        """Add cards to a row with proper centering and spacing"""
        row_width = len(cards_in_row) * CARD_WIDTH + (len(cards_in_row) - 1) * CARD_ROW_SPACING
        spacer_width = max(0, (available_width - row_width) // 2)
        
        if spacer_width > 0:
            UIComponents._add_spacer(width=spacer_width)
        
        for i, item in enumerate(cards_in_row):
            UIComponents._create_card(item, data_manager)
            
            if i < len(cards_in_row) - 1:
                UIComponents._add_spacer(width=CARD_SPACING)
    
    @staticmethod
    def _create_card(item, data_manager=None):
        """Create an individual card container"""
        with dpg.child_window(width=CARD_WIDTH, height=CARD_HEIGHT, border=True):
            # Determine if this is a rod or reel based on available fields
            if 'rodtype' in item:
                UIComponents._create_rod_card(item, data_manager)
            elif 'reeltype' in item:
                UIComponents._create_reel_card(item, data_manager)
            else:
                # Show error for unknown item type
                dpg.add_text("Error: Unknown item type", color=(255, 0, 0))
                dpg.add_text(f"Item: {item.get('name', 'Unknown')}")
                dpg.add_text("Missing 'rodtype' or 'reeltype' field")
    
    @staticmethod
    def _create_rod_card(item, data_manager=None):
        """Create the content for a fishing rod card"""
        primary_fields = data_manager.get_primary_rod_fields() if data_manager else FALLBACK_PRIMARY_FIELDS
        secondary_fields = data_manager.get_secondary_rod_fields() if data_manager else FALLBACK_SECONDARY_FIELDS
        
        UIComponents._display_fields(item, primary_fields, data_manager)
        
        if any(field in item for field in secondary_fields):
            with dpg.collapsing_header(label=ADDITIONAL_INFO_LABEL, default_open=False):
                UIComponents._display_fields(item, secondary_fields, data_manager)
    
    @staticmethod
    def _create_reel_card(item, data_manager=None):
        """Create the content for a fishing reel card"""
        primary_fields = data_manager.get_primary_reel_fields() if data_manager else FALLBACK_PRIMARY_REEL_FIELDS
        secondary_fields = data_manager.get_secondary_reel_fields() if data_manager else FALLBACK_SECONDARY_REEL_FIELDS
        
        UIComponents._display_fields(item, primary_fields, data_manager)
        
        if any(field in item for field in secondary_fields):
            with dpg.collapsing_header(label=ADDITIONAL_INFO_LABEL, default_open=False):
                UIComponents._display_fields(item, secondary_fields, data_manager)
    
    @staticmethod
    def _display_fields(item, fields, data_manager=None):
        """Display item fields with proper formatting"""
        for field in fields:
            if field in item:
                value = item[field]
                if data_manager:
                    display_name = data_manager.format_field_display_name(field)
                    display_value = data_manager.format_field_value(field, value)
                    dpg.add_text(f"{display_name}: {display_value}")
                else:
                    UIComponents._format_field_display(field, value)
    
    @staticmethod
    def _format_field_display(field, value):
        """Format field display when data manager is not available"""
        display_name = field.replace('rod', '').capitalize()
        if field == 'lineWeight':
            display_name = 'Line Weight'
        elif field == 'lureWeight':
            display_name = 'Lure Weight'
        
        if isinstance(value, list):
            dpg.add_text(f"{display_name}: {', '.join(value)}")
        else:
            dpg.add_text(f"{display_name}: {value}")
    
    # ==================== RESPONSIVE LAYOUT UTILITIES ====================
    
    @staticmethod
    def recenter_navigation_bar(callbacks, display_manager=None):
        """Recenter the navigation bar on window resize"""
        UIComponents._recenter_component(NAVIGATION_COMPONENT, display_manager, 
                                       lambda: UIComponents._add_centered_navigation_buttons(callbacks, 
                                           display_manager.get_navigation_group() if display_manager else None))
    
    @staticmethod
    def recenter_search_bar(search_callback, enter_callback, display_manager=None):
        """Recenter the search bar on window resize"""
        UIComponents._recenter_component(SEARCH_COMPONENT, display_manager,
                                       lambda: UIComponents._add_centered_search_components(search_callback, enter_callback,
                                           display_manager.get_search_group() if display_manager else None))
    
    @staticmethod
    def _recenter_component(component_type, display_manager, recreate_func):
        """Generic method to recenter UI components"""
        try:
            if display_manager:
                group = getattr(display_manager, f'get_{component_type}_group')()
            else:
                group = dpg.get_item_children(UI_TAGS['main_window'])[CHILDREN_INDEX][NAVIGATION_GROUP_INDEX if component_type == NAVIGATION_COMPONENT else SEARCH_GROUP_INDEX]
            
            if group:
                dpg.delete_item(group, children_only=True)
                recreate_func()
        except Exception as e:
            print(ERROR_RECENTERING_MESSAGE.format(component_type, e))
    
    # ==================== UTILITY METHODS ====================
    
    @staticmethod
    def _add_spacer(width=None, height=None, parent_group=None):
        """Add a spacer element with optional dimensions and parent"""
        kwargs = {}
        if width is not None:
            kwargs['width'] = width
        if height is not None:
            kwargs['height'] = height
        if parent_group is not None:
            kwargs['parent'] = parent_group
        
        dpg.add_spacer(**kwargs) 