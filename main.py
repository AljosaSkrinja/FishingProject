import dearpygui.dearpygui as dpg
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from data_manager import DataManager
from UI.display_manager import DisplayManager
from UI.view_manager import ViewManager
from UI.ui_design import FishingPlanetUI

def main():
    """Main entry point for the application."""
    # Create DearPyGui context
    dpg.create_context()
    dpg.create_viewport(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
    dpg.setup_dearpygui()
    
    # Initialize managers
    data_manager = DataManager()
    display_manager = DisplayManager(data_manager)
    view_manager = ViewManager(display_manager)

    # Create and setup the UI
    FishingPlanetUI(data_manager, display_manager, view_manager)
    
    # Load and display initial data
    display_manager.display_fish_data()
    display_manager.display_lakes_data()
    view_manager.show_rods()  # Show rods by default

    # Start the application
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main() 