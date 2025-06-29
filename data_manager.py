from parser import parse_json, deduplicate_data
from config import ROD_TYPES, get_json_path, create_category_name

class DataManager:
    """Handles all data loading, searching, and management operations."""
    
    def __init__(self):
        self.fish_data = None
        self.lakes_data = None
        self.rods_data = {}
        self.rod_categories = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all data files."""
        self.load_fish_data()
        self.load_lakes_data()
        self.load_rods_data()
    
    def load_fish_data(self):
        """Load fish data from JSON file."""
        try:
            self.fish_data = parse_json(get_json_path('fish_data.json'))
        except FileNotFoundError:
            self.fish_data = []
        except Exception as e:
            print(f"Error loading fish data: {str(e)}")
            self.fish_data = []
    
    def load_lakes_data(self):
        """Load lakes data from JSON file."""
        try:
            self.lakes_data = parse_json(get_json_path('lake_data.json'))
        except FileNotFoundError:
            self.lakes_data = []
        except Exception as e:
            print(f"Error loading lakes data: {str(e)}")
            self.lakes_data = []
    
    def process_rod_data(self, rod_data, rod_type, capabilities):
        """Process rod data to add rodtype, category, and format price."""
        processed_rods = []
        category_name = create_category_name(capabilities)
        
        for rod in rod_data:
            # Create a copy of the rod data
            processed_rod = dict(rod)
            
            # Add rodtype and category
            processed_rod['rodtype'] = rod_type
            processed_rod['category'] = category_name
            
            # Create formatted price field
            price_parts = []
            
            if rod.get('baitcoinsCost', 0) > 0:
                price_parts.append(f"{rod['baitcoinsCost']} BC")
            
            if rod.get('clubTokensCost', 0) > 0:
                price_parts.append(f"{rod['clubTokensCost']} CT")
            
            if rod.get('creditsCost', 0) > 0:
                price_parts.append(f"{rod['creditsCost']} CC")
            
            # If no cost specified, show as free
            if not price_parts:
                processed_rod['price'] = "Free"
            else:
                processed_rod['price'] = " + ".join(price_parts)
            
            # Format weight data
            self._format_weight_data(processed_rod)
            
            # Remove old cost fields
            processed_rod.pop('baitcoinsCost', None)
            processed_rod.pop('clubTokensCost', None)
            processed_rod.pop('creditsCost', None)
            
            processed_rods.append(processed_rod)
        
        return processed_rods
    
    def _format_weight_data(self, rod_data):
        """Format line and lure weight data with proper units."""
        # Handle line weight display with combined min/max and units
        if 'rodLineWeightMinimum' in rod_data and 'rodLineWeightMaximum' in rod_data:
            min_weight = rod_data['rodLineWeightMinimum']
            max_weight = rod_data['rodLineWeightMaximum']
            rod_data['lineWeight'] = f"{min_weight}-{max_weight} kg"
            
            # Remove original fields
            rod_data.pop('rodLineWeightMinimum', None)
            rod_data.pop('rodLineWeightMaximum', None)
        
        # Handle lure weight display with combined min/max and units
        if 'rodLureWeightMinimum' in rod_data and 'rodLureWeightMaximum' in rod_data:
            min_weight = rod_data['rodLureWeightMinimum']
            max_weight = rod_data['rodLureWeightMaximum']
            rod_data['lureWeight'] = f"{min_weight}-{max_weight} g"
            
            # Remove original fields
            rod_data.pop('rodLureWeightMinimum', None)
            rod_data.pop('rodLureWeightMaximum', None)
    
    def load_rods_data(self):
        """Load all rod data from JSON files."""
        self.rods_data = {}
        self.rod_categories = {}
        
        for rod_type in ROD_TYPES:
            try:
                rod_data = parse_json(get_json_path(f'{rod_type}.json'))
                
                # Extract capabilities from the top level
                capabilities = {
                    'canUseBobber': rod_data.get('canUseBobber', False),
                    'canUseCastingReel': rod_data.get('canUseCastingReel', False),
                    'canUseLure': rod_data.get('canUseLure', False),
                    'canUseSpinningReel': rod_data.get('canUseSpinningReel', False)
                }
                
                if 'gameRods' in rod_data:
                    raw_rods = rod_data['gameRods']
                else:
                    raw_rods = rod_data
                
                # Process the rod data to add rodtype, category, and format price
                processed_rods = self.process_rod_data(raw_rods, rod_type, capabilities)
                self.rods_data[rod_type] = processed_rods
                
                # Group rods by category
                category_name = create_category_name(capabilities)
                if category_name not in self.rod_categories:
                    self.rod_categories[category_name] = []
                self.rod_categories[category_name].extend(processed_rods)
                
            except FileNotFoundError:
                self.rods_data[rod_type] = []
            except Exception as e:
                print(f"Error loading {rod_type} rods: {str(e)}")
                self.rods_data[rod_type] = []
    
    def get_fish_data(self):
        """Get fish data."""
        return self.fish_data
    
    def get_lakes_data(self):
        """Get lakes data."""
        return self.lakes_data
    
    def get_rods_by_category(self):
        """Get rods organized by category."""
        return self.rod_categories
    
    def search_fish(self, search_term):
        """Search and filter fish data."""
        if not self.fish_data:
            return []
        return [fish for fish in self.fish_data if search_term in fish.get('name', '').lower()]
    
    def search_lakes(self, search_term):
        """Search and filter lakes data."""
        if not self.lakes_data:
            return []
        return [lake for lake in self.lakes_data if search_term in lake.get('name', '').lower()]
    
    def search_rods(self, search_term):
        """Search and filter rods data."""
        filtered_rods = {}
        for rod_type, rods in self.rods_data.items():
            filtered_rods[rod_type] = [rod for rod in rods if search_term in str(rod).lower()]
        return filtered_rods
    
    def get_deduplicated_data(self, data):
        """Get deduplicated data."""
        return deduplicate_data(data)
    
    def get_display_ready_data(self, data):
        """Get data ready for display (deduplicated and processed)."""
        return self.get_deduplicated_data(data)
    
    def process_search_results(self, search_results):
        """Process search results for display."""
        if isinstance(search_results, dict):
            # Handle rod search results (grouped by type)
            processed_results = {}
            for rod_type, rods in search_results.items():
                for rod in rods:
                    category = rod.get('category', 'Unknown')
                    if category not in processed_results:
                        processed_results[category] = []
                    processed_results[category].append(rod)
            return processed_results
        else:
            return search_results
    
    def get_primary_rod_fields(self):
        """Get the list of primary fields to display for rod cards."""
        return ['rodName', 'price', 'rodLength', 'rodAction', 'rodLevel', 'lineWeight', 'lureWeight']
    
    def get_secondary_rod_fields(self):
        """Get the list of secondary fields to display for rod cards."""
        return ['rodtype', 'rodBrand', 'rodGuides', 'rodPieces', 'rodPower']
    
    def format_field_display_name(self, field_name):
        """Format a field name for display."""
        if field_name == 'lineWeight':
            return 'Line Weight'
        elif field_name == 'lureWeight':
            return 'Lure Weight'
        else:
            return field_name.replace('rod', '').capitalize()
    
    def format_field_value(self, field_name, value):
        """Format a field value for display."""
        if isinstance(value, list):
            return ', '.join(value)
        else:
            return str(value) 