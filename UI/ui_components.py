import dearpygui.dearpygui as dpg
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, NAV_BUTTON_SPACING,
    SEARCH_INPUT_WIDTH, SEARCH_INPUT_HEIGHT, SEARCH_BUTTON_WIDTH, SEARCH_BUTTON_HEIGHT,
    CARD_WIDTH, CARD_HEIGHT,
    UI_TAGS, NAVIGATION_BUTTONS
)

class UIComponents:
    """Handles all UI component creation and layout logic."""
    
    @staticmethod
    def create_main_window():
        """Create the main application window."""
        try:
            return dpg.window(
                label="Main Window", 
                tag=UI_TAGS['main_window'], 
                width=WINDOW_WIDTH, 
                height=WINDOW_HEIGHT, 
                no_title_bar=True, 
                no_collapse=True
            )
        except Exception as e:
            print(f"Error creating main window: {e}")
            raise
    
    @staticmethod
    def create_navigation_bar(callbacks):
        """Create the top navigation bar with centered buttons."""
        try:
            with dpg.group(horizontal=True, tag=UI_TAGS['nav_group']):
                UIComponents._add_centered_navigation_buttons(callbacks)
        except Exception as e:
            print(f"Error creating navigation bar: {e}")
            raise
    
    @staticmethod
    def _add_centered_navigation_buttons(callbacks, parent_group=None):
        """Add navigation buttons with proper centering to specified parent."""
        # Get current viewport width for dynamic centering
        viewport_width = dpg.get_viewport_width()
        
        # Calculate total navigation area width
        nav_area_width = len(NAVIGATION_BUTTONS) * NAV_BUTTON_WIDTH + (len(NAVIGATION_BUTTONS) - 1) * NAV_BUTTON_SPACING
        
        # Add left spacer to center the navigation area
        left_spacer_width = max(0, (viewport_width - nav_area_width) // 2)
        if left_spacer_width > 0:
            if parent_group is not None:
                dpg.add_spacer(width=int(left_spacer_width), parent=parent_group)
            else:
                dpg.add_spacer(width=int(left_spacer_width))
        
        # Add navigation buttons
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
            
            # Add spacing between buttons (except for the last button)
            if i < len(NAVIGATION_BUTTONS) - 1:
                if parent_group is not None:
                    dpg.add_spacer(width=NAV_BUTTON_SPACING, parent=parent_group)
                else:
                    dpg.add_spacer(width=NAV_BUTTON_SPACING)
        
        # Add right spacer to balance the centering
        if left_spacer_width > 0:
            if parent_group is not None:
                dpg.add_spacer(width=int(left_spacer_width), parent=parent_group)
            else:
                dpg.add_spacer(width=int(left_spacer_width))
    
    @staticmethod
    def create_search_bar(search_callback, enter_callback):
        """Create the search input and button centered in the window."""
        try:
            with dpg.group(horizontal=True):
                UIComponents._add_centered_search_components(search_callback, enter_callback)
        except Exception as e:
            print(f"Error creating search bar: {e}")
            raise
    
    @staticmethod
    def _add_centered_search_components(search_callback, enter_callback, parent_group=None):
        """Add search components with proper centering to specified parent."""
        # Get current viewport width for dynamic centering
        viewport_width = dpg.get_viewport_width()
        
        # Calculate total search area width
        search_area_width = SEARCH_INPUT_WIDTH + NAV_BUTTON_SPACING + SEARCH_BUTTON_WIDTH
        
        # Add left spacer to center the search area
        left_spacer_width = max(0, (viewport_width - search_area_width) // 2)
        if left_spacer_width > 0:
            if parent_group is not None:
                dpg.add_spacer(width=int(left_spacer_width), parent=parent_group)
            else:
                dpg.add_spacer(width=int(left_spacer_width))
        
        # Add search input and button
        if parent_group is not None:
            dpg.add_input_text(
                tag=UI_TAGS['search_input'], 
                on_enter=True, 
                callback=enter_callback, 
                hint="Search here...", 
                width=SEARCH_INPUT_WIDTH, 
                height=SEARCH_INPUT_HEIGHT, 
                parent=parent_group
            )
            dpg.add_spacer(width=NAV_BUTTON_SPACING, parent=parent_group)
            dpg.add_button(
                label="Search", 
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
                hint="Search here...", 
                width=SEARCH_INPUT_WIDTH, 
                height=SEARCH_INPUT_HEIGHT
            )
            dpg.add_spacer(width=NAV_BUTTON_SPACING)
            dpg.add_button(
                label="Search", 
                tag=UI_TAGS['search_button'], 
                callback=search_callback, 
                width=SEARCH_BUTTON_WIDTH, 
                height=SEARCH_BUTTON_HEIGHT
            )
        
        # Add right spacer to balance the centering
        if left_spacer_width > 0:
            if parent_group is not None:
                dpg.add_spacer(width=int(left_spacer_width), parent=parent_group)
            else:
                dpg.add_spacer(width=int(left_spacer_width))
    
    @staticmethod
    def create_content_areas():
        """Create the content display areas for fish, lakes, and rods."""
        try:
            dpg.add_group(tag=UI_TAGS['fish_group'])
            dpg.add_group(tag=UI_TAGS['lakes_group'], show=False)
            dpg.add_group(tag=UI_TAGS['rods_group'], show=False)
        except Exception as e:
            print(f"Error creating content areas: {e}")
            raise
    
    @staticmethod
    def create_card_row(cards_in_row, parent_group, available_width, data_manager=None):
        """Create a centered row of cards."""
        try:
            with dpg.group(horizontal=True, parent=parent_group):
                UIComponents._add_centered_cards(cards_in_row, available_width, data_manager)
        except Exception as e:
            print(f"Error creating card row: {e}")
            raise
    
    @staticmethod
    def _add_centered_cards(cards_in_row, available_width, data_manager=None):
        """Add cards with proper centering."""
        # Calculate row width
        row_width = len(cards_in_row) * CARD_WIDTH + (len(cards_in_row) - 1) * 20
        
        # Add left spacer to center the row
        spacer_width = max(0, (available_width - row_width) // 2)
        if spacer_width > 0:
            dpg.add_spacer(width=spacer_width)
        
        # Add cards to the row
        for i, item in enumerate(cards_in_row):
            UIComponents._create_card(item, data_manager)
            
            # Add spacing between cards (except for the last card)
            if i < len(cards_in_row) - 1:
                dpg.add_spacer(width=20)
    
    @staticmethod
    def _create_card(item, data_manager=None):
        """Create a single card with item data."""
        with dpg.child_window(width=CARD_WIDTH, height=CARD_HEIGHT, border=True):
            # Check if this is a rod card (has rodtype field)
            is_rod_card = 'rodtype' in item
            
            if is_rod_card:
                # For rod cards, organize data with collapsible section for less relevant info
                UIComponents._create_rod_card(item, data_manager)
            else:
                # For other cards (fish, lakes), show all data normally
                UIComponents._create_standard_card(item)
    
    @staticmethod
    def _create_rod_card(item, data_manager=None):
        """Create a rod card with collapsible section for less relevant data."""
        # Show primary rod information first
        if data_manager:
            primary_fields = data_manager.get_primary_rod_fields()
            secondary_fields = data_manager.get_secondary_rod_fields()
        else:
            # Fallback to hardcoded fields if data_manager not provided
            primary_fields = ['rodName', 'price', 'rodLength', 'rodAction', 'rodLevel', 'lineWeight', 'lureWeight']
            secondary_fields = ['rodtype', 'rodBrand', 'rodGuides', 'rodPieces', 'rodPower']
        
        for field in primary_fields:
            if field in item:
                value = item[field]
                if data_manager:
                    display_name = data_manager.format_field_display_name(field)
                    display_value = data_manager.format_field_value(field, value)
                    dpg.add_text(f"{display_name}: {display_value}")
                else:
                    # Fallback formatting
                    if isinstance(value, list):
                        dpg.add_text(f"{field.replace('rod', '').capitalize()}: {', '.join(value)}")
                    else:
                        if field == 'lineWeight':
                            dpg.add_text(f"Line Weight: {value}")
                        elif field == 'lureWeight':
                            dpg.add_text(f"Lure Weight: {value}")
                        else:
                            dpg.add_text(f"{field.replace('rod', '').capitalize()}: {value}")
        
        # Create collapsible section for less relevant data
        has_less_relevant = any(field in item for field in secondary_fields)
        
        if has_less_relevant:
            with dpg.collapsing_header(label="Additional Info", default_open=False):
                for field in secondary_fields:
                    if field in item:
                        value = item[field]
                        if data_manager:
                            display_name = data_manager.format_field_display_name(field)
                            display_value = data_manager.format_field_value(field, value)
                            dpg.add_text(f"{display_name}: {display_value}")
                        else:
                            dpg.add_text(f"{field.replace('rod', '').capitalize()}: {value}")
    
    @staticmethod
    def _create_standard_card(item):
        """Create a standard card for non-rod items."""
        for key, value in item.items():
            if isinstance(value, list):
                dpg.add_text(f"{key.capitalize()}: {', '.join(value)}")
            else:
                dpg.add_text(f"{key.capitalize()}: {value}")
    
    @staticmethod
    def recenter_navigation_bar(viewport_width, callbacks, display_manager=None):
        """Recenter the navigation bar when window is resized."""
        try:
            # Get the navigation group
            if display_manager:
                nav_group = display_manager.get_navigation_group()
            else:
                # Fallback to direct access
                nav_group = dpg.get_item_children(UI_TAGS['main_window'])[1][0]
            
            if nav_group:
                # Clear and recreate the navigation bar with new centering
                dpg.delete_item(nav_group, children_only=True)
                UIComponents._add_centered_navigation_buttons(callbacks, nav_group)
        except Exception as e:
            print(f"Error recentering navigation bar: {e}")
    
    @staticmethod
    def recenter_search_bar(viewport_width, search_callback, enter_callback, display_manager=None):
        """Recenter the search bar when window is resized."""
        try:
            # Get the search bar group
            if display_manager:
                search_group = display_manager.get_search_group()
            else:
                # Fallback to direct access
                search_group = dpg.get_item_children(UI_TAGS['main_window'])[1][1]
            
            if search_group:
                # Clear and recreate the search bar with new centering
                dpg.delete_item(search_group, children_only=True)
                UIComponents._add_centered_search_components(search_callback, enter_callback, search_group)
        except Exception as e:
            print(f"Error recentering search bar: {e}") 