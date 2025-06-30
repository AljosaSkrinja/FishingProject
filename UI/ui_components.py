import dearpygui.dearpygui as dpg
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, NAV_BUTTON_SPACING,
    SEARCH_INPUT_WIDTH, SEARCH_INPUT_HEIGHT, SEARCH_BUTTON_WIDTH, SEARCH_BUTTON_HEIGHT,
    CARD_WIDTH, CARD_HEIGHT,
    UI_TAGS, NAVIGATION_BUTTONS
)

class UIComponents:
    
    @staticmethod
    def create_main_window():
        return dpg.window(
            label="Main Window", 
            tag=UI_TAGS['main_window'], 
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            no_title_bar=True, 
            no_collapse=True
        )
    
    @staticmethod
    def create_navigation_bar(callbacks):
        with dpg.group(horizontal=True, tag=UI_TAGS['nav_group']):
            UIComponents._add_centered_navigation_buttons(callbacks)
    
    @staticmethod
    def _add_spacer(width=None, height=None, parent_group=None):
        kwargs = {}
        if width is not None:
            kwargs['width'] = width
        if height is not None:
            kwargs['height'] = height
        if parent_group is not None:
            kwargs['parent'] = parent_group
        
        dpg.add_spacer(**kwargs)
    
    @staticmethod
    def _add_centered_navigation_buttons(callbacks, parent_group=None):
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
    
    @staticmethod
    def create_search_bar(search_callback, enter_callback):
        with dpg.group(horizontal=True):
            UIComponents._add_centered_search_components(search_callback, enter_callback)
    
    @staticmethod
    def _add_centered_search_components(search_callback, enter_callback, parent_group=None):
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
                hint="Search here...", 
                width=SEARCH_INPUT_WIDTH, 
                height=SEARCH_INPUT_HEIGHT, 
                parent=parent_group
            )
            UIComponents._add_spacer(width=NAV_BUTTON_SPACING, parent_group=parent_group)
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
            UIComponents._add_spacer(width=NAV_BUTTON_SPACING)
            dpg.add_button(
                label="Search", 
                tag=UI_TAGS['search_button'], 
                callback=search_callback, 
                width=SEARCH_BUTTON_WIDTH, 
                height=SEARCH_BUTTON_HEIGHT
            )
        
        if left_spacer_width > 0:
            UIComponents._add_spacer(width=int(left_spacer_width), parent_group=parent_group)
    
    @staticmethod
    def create_content_areas():
        dpg.add_group(tag=UI_TAGS['fish_group'])
        dpg.add_group(tag=UI_TAGS['lakes_group'], show=False)
        dpg.add_group(tag=UI_TAGS['rods_group'], show=False)
    
    @staticmethod
    def create_card_row(cards_in_row, parent_group, available_width, data_manager=None):
        with dpg.group(horizontal=True, parent=parent_group):
            UIComponents._add_centered_cards(cards_in_row, available_width, data_manager)
    
    @staticmethod
    def _add_centered_cards(cards_in_row, available_width, data_manager=None):
        row_width = len(cards_in_row) * CARD_WIDTH + (len(cards_in_row) - 1) * 20
        spacer_width = max(0, (available_width - row_width) // 2)
        
        if spacer_width > 0:
            UIComponents._add_spacer(width=spacer_width)
        
        for i, item in enumerate(cards_in_row):
            UIComponents._create_card(item, data_manager)
            
            if i < len(cards_in_row) - 1:
                UIComponents._add_spacer(width=20)
    
    @staticmethod
    def _create_card(item, data_manager=None):
        with dpg.child_window(width=CARD_WIDTH, height=CARD_HEIGHT, border=True):
            is_rod_card = 'rodtype' in item
            
            if is_rod_card:
                UIComponents._create_rod_card(item, data_manager)
            else:
                UIComponents._create_standard_card(item)
    
    @staticmethod
    def _create_rod_card(item, data_manager=None):
        primary_fields = data_manager.get_primary_rod_fields() if data_manager else ['rodName', 'price', 'rodLength', 'rodAction', 'rodLevel', 'lineWeight', 'lureWeight']
        secondary_fields = data_manager.get_secondary_rod_fields() if data_manager else ['rodtype', 'rodBrand', 'rodGuides', 'rodPieces', 'rodPower']
        
        UIComponents._display_fields(item, primary_fields, data_manager)
        
        if any(field in item for field in secondary_fields):
            with dpg.collapsing_header(label="Additional Info", default_open=False):
                UIComponents._display_fields(item, secondary_fields, data_manager)
    
    @staticmethod
    def _create_standard_card(item):
        UIComponents._display_fields(item, item.keys())
    
    @staticmethod
    def _display_fields(item, fields, data_manager=None):
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
        display_name = field.replace('rod', '').capitalize()
        if field == 'lineWeight':
            display_name = 'Line Weight'
        elif field == 'lureWeight':
            display_name = 'Lure Weight'
        
        if isinstance(value, list):
            dpg.add_text(f"{display_name}: {', '.join(value)}")
        else:
            dpg.add_text(f"{display_name}: {value}")
    
    @staticmethod
    def recenter_navigation_bar(callbacks, display_manager=None):
        UIComponents._recenter_component('navigation', display_manager, 
                                       lambda: UIComponents._add_centered_navigation_buttons(callbacks, 
                                           display_manager.get_navigation_group() if display_manager else None))
    
    @staticmethod
    def recenter_search_bar(search_callback, enter_callback, display_manager=None):
        UIComponents._recenter_component('search', display_manager,
                                       lambda: UIComponents._add_centered_search_components(search_callback, enter_callback,
                                           display_manager.get_search_group() if display_manager else None))
    
    @staticmethod
    def _recenter_component(component_type, display_manager, recreate_func):
        try:
            if display_manager:
                group = getattr(display_manager, f'get_{component_type}_group')()
            else:
                group = dpg.get_item_children(UI_TAGS['main_window'])[1][0 if component_type == 'navigation' else 1]
            
            if group:
                dpg.delete_item(group, children_only=True)
                recreate_func()
        except Exception as e:
            print(f"Error recentering {component_type} bar: {e}") 