# UI Module - Fishing Planet Application

This folder contains all the UI-related components for the Fishing Planet application. The UI is built using DearPyGui and follows a modular architecture for better maintainability and separation of concerns.

## File Structure

### Core UI Files

#### `main_ui_orchestrator.py`
- **Purpose**: Main UI orchestrator that coordinates all UI components
- **Responsibilities**: 
  - Sets up the main application window
  - Manages UI callbacks and event handling
  - Coordinates between different UI managers
  - Handles window resize events
- **Key Class**: `MainUIOrchestrator`

#### `display_manager.py`
- **Purpose**: Manages data display and presentation
- **Responsibilities**:
  - Displays fishing rods data organized by category
  - Handles search results display
  - Manages view refreshing and updates
  - Coordinates with card layout system
- **Key Class**: `DisplayManager`

#### `view_manager.py`
- **Purpose**: Manages switching between different application views
- **Responsibilities**:
  - Switches between different sections (rods, fish, lakes, etc.)
  - Manages view visibility states
  - Clears and refreshes view content
  - Coordinates with display manager
- **Key Class**: `ViewManager`

### Layout and Components

#### `ui_card_layout.py`
- **Purpose**: Handles card layout and grid positioning
- **Responsibilities**:
  - Calculates responsive layout parameters
  - Groups data into grid rows
  - Displays cards in organized layouts
  - Handles empty data states
- **Key Class**: `UICardLayout`

#### `ui_components.py`
- **Purpose**: Factory class for creating all UI components
- **Responsibilities**:
  - Creates main window and navigation elements
  - Builds search functionality
  - Creates content areas and card displays
  - Handles responsive layout adjustments
- **Key Class**: `UIComponents`

## Architecture Overview

```
MainUIOrchestrator (main_ui_orchestrator.py)
├── DisplayManager (display_manager.py)
│   └── UICardLayout (ui_card_layout.py)
├── ViewManager (view_manager.py)
└── UIComponents (ui_components.py)
```

## Key Design Principles

1. **Separation of Concerns**: Each file has a specific responsibility
2. **Modularity**: Components can be easily modified or extended
3. **Responsive Design**: UI adapts to different window sizes
4. **Data-Driven**: UI components are driven by data from the data manager

## Usage

The UI system is designed to work with a data manager that provides fishing equipment data. The main entry point is the `MainUIOrchestrator` class, which coordinates all other components.

## Dependencies

- `dearpygui`: Main GUI framework
- `config.py`: Configuration constants and settings
- `data_manager.py`: Data management and processing 