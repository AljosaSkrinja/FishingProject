import dearpygui.dearpygui as dpg
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from data_manager import DataManager
from UI.display_manager import DisplayManager
from UI.view_manager import ViewManager
from UI.main_ui_orchestrator import MainUIOrchestrator
import json


def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    dpg.create_context()
    dpg.create_viewport(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
    dpg.setup_dearpygui()
    

    
    data_manager = DataManager()
    display_manager = DisplayManager(data_manager)
    view_manager = ViewManager(display_manager)
    
    # Setup the UI components
    ui_orchestrator = MainUIOrchestrator(data_manager, display_manager, view_manager)
    ui_orchestrator.setup_ui()
        
    # Skip fish and lake data - only show rods
    view_manager.show_rods()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main() 