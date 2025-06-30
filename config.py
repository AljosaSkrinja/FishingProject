import os

JSON_FOLDER = "JsonFolder"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = 'Fishing Planet'

NAV_BUTTON_WIDTH = 200
NAV_BUTTON_HEIGHT = 80
NAV_BUTTON_SPACING = 20

SEARCH_INPUT_WIDTH = 400
SEARCH_INPUT_HEIGHT = 40
SEARCH_BUTTON_WIDTH = 100
SEARCH_BUTTON_HEIGHT = 20

CARD_WIDTH = 300
CARD_HEIGHT = 200

NAVIGATION_BUTTONS = [
    {"label": "Fish", "callback": "show_fish"},
    {"label": "Lakes", "callback": "show_lakes"},
    {"label": "Rod Setup", "callback": "show_rods"}
]

ROD_TYPES = ["match", "casting", "telescopic", "spinning"]

REEL_CAPABILITIES = {
    'canUseCastingReel': 'CastingReel',
    'canUseSpinningReel': 'SpinningReel'
}

BAIT_CAPABILITIES = {
    'canUseBobber': 'Bobber',
    'canUseLure': 'Lure'
}

DEFAULT_CATEGORY = 'Other'

UI_TAGS = {
    'main_window': "Main Window",
    'fish_button': "Fish Button",
    'lakes_button': "Lakes Button",
    'rods_button': "Rods Button",
    'search_input': "search_input",
    'search_button': "Search Button",
    'nav_group': "nav_group",
    'fish_group': "fish_group",
    'lakes_group': "lakes_group",
    'rods_group': "rods_group"
}

def get_json_path(filename):
    return os.path.join(JSON_FOLDER, filename)

def create_category_name(capabilities):
    category_parts = []
    
    for capability_key, category_name in REEL_CAPABILITIES.items():
        if capabilities.get(capability_key, False):
            category_parts.append(category_name)
    
    for capability_key, category_name in BAIT_CAPABILITIES.items():
        if capabilities.get(capability_key, False):
            category_parts.append(category_name)
    
    if not category_parts:
        return DEFAULT_CATEGORY
    
    return '&'.join(category_parts) 