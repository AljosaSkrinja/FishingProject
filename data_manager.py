from parser import parse_json
from config import *

class DataManager:
    
    def __init__(self):
        self.rods_data = {}
        self.rod_categories = {}
        self.reels_data = {}
        self.reel_categories = {}
        self.load_rods_data()
        self.load_reels_data()
    
    def load_rods_data(self):
        self.rods_data = {}
        self.rod_categories = {}
        
        # Load processed rods data
        processed_rods = parse_json(PROCESSED_RODS_PATH)
        
        # Organize data in categories
        for rod in processed_rods:
            rod_type = rod['rodtype']
            category = rod['category']
            
            if rod_type not in self.rods_data:
                self.rods_data[rod_type] = []
            self.rods_data[rod_type].append(rod)
            
            if category not in self.rod_categories:
                self.rod_categories[category] = []
            self.rod_categories[category].append(rod)
    
    def load_reels_data(self):
        self.reels_data = {}
        self.reel_categories = {}
        
        # Load processed reels data
        processed_reels = parse_json(PROCESSED_REELS_PATH)
        
        # Organize data in categories
        for reel in processed_reels:
            reel_type = reel.get('reeltype', 'Unknown')
            category = reel.get('category', 'Unknown')
            
            if reel_type not in self.reels_data:
                self.reels_data[reel_type] = []
            self.reels_data[reel_type].append(reel)
            
            if category not in self.reel_categories:
                self.reel_categories[category] = []
            self.reel_categories[category].append(reel)
    
    def get_rods_by_category(self):
        return self.rod_categories
    
    def get_reels_by_category(self):
        return self.reel_categories
      
    def search_rods(self, search_term):
        filtered_rods = {}
        search_term = search_term.lower()
        
        for rod_type, rods in self.rods_data.items():
            filtered_rods[rod_type] = [
                rod for rod in rods 
                if search_term in str(rod).lower()
            ]
        return filtered_rods
    
    def search_reels(self, search_term):
        filtered_reels = {}
        search_term = search_term.lower()
        
        for reel_type, reels in self.reels_data.items():
            filtered_reels[reel_type] = [
                reel for reel in reels 
                if search_term in str(reel).lower()
            ]
        return filtered_reels
    
    def process_search_results(self, search_results):
        if not isinstance(search_results, dict):
            return search_results
            
        processed_results = {}
        for rods in search_results.values():
            for rod in rods:
                category = rod.get('category', 'Unknown')
                if category not in processed_results:
                    processed_results[category] = []
                processed_results[category].append(rod)
        return processed_results
    
    def process_reel_search_results(self, search_results):
        if not isinstance(search_results, dict):
            return search_results
            
        processed_results = {}
        for reels in search_results.values():
            for reel in reels:
                category = reel.get('category', 'Unknown')
                if category not in processed_results:
                    processed_results[category] = []
                processed_results[category].append(reel)
        return processed_results
    
    def get_primary_rod_fields(self):
        return PRIMARY_ROD_FIELDS
    
    def get_secondary_rod_fields(self):
        return SECONDARY_ROD_FIELDS
    
    def get_primary_reel_fields(self):
        return PRIMARY_REEL_FIELDS
    
    def get_secondary_reel_fields(self):
        return SECONDARY_REEL_FIELDS
    
    def format_field_display_name(self, field_name):
        if field_name == 'lineWeight':
            return 'Line Weight'
        elif field_name == 'lureWeight':
            return 'Lure Weight'
        else:
            return field_name.replace('rod', '').replace('reel', '').capitalize()
    
    def format_field_value(self, field_name, value):
        if isinstance(value, list):
            return ', '.join(value)
        else:
            return str(value) 