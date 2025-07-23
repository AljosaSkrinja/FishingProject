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
    {"label": "Rods", "callback": "show_rods"},
    {"label": "Reels", "callback": "show_reels"}
]

UI_TAGS = {
    'main_window': "Main Window",
    'fish_button': "Fish Button",
    'lakes_button': "Lakes Button",
    'rods_button': "Rods Button",
    'reels_button': "Reels Button",
    'search_input': "search_input",
    'search_button': "Search Button",
    'nav_group': "nav_group",
    'fish_group': "fish_group",
    'lakes_group': "lakes_group",
    'rods_group': "rods_group",
    'reels_group': "reels_group"
}

# Processed data paths
PROCESSED_RODS_PATH = 'ProcessedData/processed_rods.json'
PROCESSED_REELS_PATH = 'ProcessedData/processed_reels.json'

# WIP data paths
FISH_DATA_PATH = 'ProcessedData/fish............'
LAKE_DATA_PATH = 'ProcessedData/lake............'

# Rod field definitions
PRIMARY_ROD_FIELDS = ['name', 'price', 'level', 'lineWeight', 'lureWeight']
SECONDARY_ROD_FIELDS = ['rodtype', 'brand', 'length']

# Reel field definitions
PRIMARY_REEL_FIELDS = ['name', 'price', 'level', 'recovery', 'maxDrag']
SECONDARY_REEL_FIELDS = ['reeltype', 'brand']

# Fallback field definitions (used when data_manager is not available)
FALLBACK_PRIMARY_FIELDS = ['name', 'price', 'level']
FALLBACK_SECONDARY_FIELDS = ['rodtype', 'brand']
FALLBACK_PRIMARY_REEL_FIELDS = ['name', 'price', 'level']
FALLBACK_SECONDARY_REEL_FIELDS = ['reeltype', 'brand']


# UI text constants
MAIN_WINDOW_LABEL = "Main Window"
SEARCH_HINT = "Search here..."
SEARCH_BUTTON_LABEL = "Search"
ADDITIONAL_INFO_LABEL = "Additional Info"
NO_DATA_MESSAGE = "No data available."
NO_RODS_FOUND_MESSAGE = "No rods found matching your search."
NO_REELS_FOUND_MESSAGE = "No reels found matching your search."
CATEGORY_HEADER_FORMAT = "=== {} ==="

# UI spacing constants
CARD_SPACING = 20
CATEGORY_SPACING = 20
WINDOW_PADDING = 40
CARD_ROW_SPACING = 20

# UI index constants
NAVIGATION_GROUP_INDEX = 0
SEARCH_GROUP_INDEX = 1
CHILDREN_INDEX = 1

# UI component type constants
NAVIGATION_COMPONENT = 'navigation'
SEARCH_COMPONENT = 'search'

# Error message constants
ERROR_RECENTERING_MESSAGE = "Error recentering {} bar: {}" 