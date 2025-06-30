from parser import parse_json, deduplicate_data
from config import ROD_TYPES, get_json_path, create_category_name

class DataManager:
    
    def __init__(self):
        self.fish_data = None
        self.lakes_data = None
        self.rods_data = {}
        self.rod_categories = {}
        self.load_all_data()
    
    def load_all_data(self):
        self.load_fish_data()
        self.load_lakes_data()
        self.load_rods_data()
    
    def load_fish_data(self):
        self.fish_data = parse_json(get_json_path('fish_data.json'))
    
    def load_lakes_data(self):
        self.lakes_data = parse_json(get_json_path('lake_data.json'))
    
    def process_rod_data(self, rod_data, rod_type, capabilities):
        processed_rods = []
        category_name = create_category_name(capabilities)
        
        for rod in rod_data:
            processed_rod = dict(rod)
            
            processed_rod['rodtype'] = rod_type
            processed_rod['category'] = category_name
            
            price_parts = []
            
            if rod.get('baitcoinsCost', 0) > 0:
                price_parts.append(f"{rod['baitcoinsCost']} BC")
            
            if rod.get('clubTokensCost', 0) > 0:
                price_parts.append(f"{rod['clubTokensCost']} CT")
            
            if rod.get('creditsCost', 0) > 0:
                price_parts.append(f"{rod['creditsCost']} CC")
            
            if not price_parts:
                processed_rod['price'] = "Free"
            else:
                processed_rod['price'] = " + ".join(price_parts)
            
            self._format_weight_data(processed_rod)
            
            for field in ['baitcoinsCost', 'clubTokensCost', 'creditsCost']:
                processed_rod.pop(field, None)
            
            processed_rods.append(processed_rod)
        
        return processed_rods
    
    def _format_weight_data(self, rod_data):
        weight_configs = [
            ('rodLineWeightMinimum', 'rodLineWeightMaximum', 'lineWeight', 'kg'),
            ('rodLureWeightMinimum', 'rodLureWeightMaximum', 'lureWeight', 'g')
        ]
        
        for min_field, max_field, output_field, unit in weight_configs:
            if min_field in rod_data and max_field in rod_data:
                min_weight = rod_data[min_field]
                max_weight = rod_data[max_field]
                rod_data[output_field] = f"{min_weight}-{max_weight} {unit}"
                
                rod_data.pop(min_field, None)
                rod_data.pop(max_field, None)
    
    def load_rods_data(self):
        self.rods_data = {}
        self.rod_categories = {}
        
        for rod_type in ROD_TYPES:
            rod_data = parse_json(get_json_path(f'{rod_type}.json'))
            
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
            
            processed_rods = self.process_rod_data(raw_rods, rod_type, capabilities)
            self.rods_data[rod_type] = processed_rods
            
            category_name = create_category_name(capabilities)
            if category_name not in self.rod_categories:
                self.rod_categories[category_name] = []
            self.rod_categories[category_name].extend(processed_rods)
    
    def get_fish_data(self):
        return self.fish_data
    
    def get_lakes_data(self):
        return self.lakes_data
    
    def get_rods_by_category(self):
        return self.rod_categories
    
    def search_fish(self, search_term):
        return self._search_data(self.fish_data, search_term, 'name')
    
    def search_lakes(self, search_term):
        return self._search_data(self.lakes_data, search_term, 'name')
    
    def search_rods(self, search_term):
        filtered_rods = {}
        for rod_type, rods in self.rods_data.items():
            filtered_rods[rod_type] = self._search_data(rods, search_term)
        return filtered_rods
    
    def _search_data(self, data, search_term, field_name=None):
        if not data:
            return []
        search_term = search_term.lower()
        if field_name:
            return [item for item in data if search_term in item.get(field_name, '').lower()]
        else:
            return [item for item in data if search_term in str(item).lower()]
    
    def get_deduplicated_data(self, data):
        return deduplicate_data(data)
    
    def get_display_ready_data(self, data):
        return self.get_deduplicated_data(data)
    
    def process_search_results(self, search_results):
        if isinstance(search_results, dict):
            processed_results = {}
            for rods in search_results.values():
                for rod in rods:
                    category = rod.get('category', 'Unknown')
                    if category not in processed_results:
                        processed_results[category] = []
                    processed_results[category].append(rod)
            return processed_results
        else:
            return search_results
    
    def get_primary_rod_fields(self):
        return ['rodName', 'price', 'rodLength', 'rodAction', 'rodLevel', 'lineWeight', 'lureWeight']
    
    def get_secondary_rod_fields(self):
        return ['rodtype', 'rodBrand', 'rodGuides', 'rodPieces', 'rodPower']
    
    def format_field_display_name(self, field_name):
        if field_name == 'lineWeight':
            return 'Line Weight'
        elif field_name == 'lureWeight':
            return 'Lure Weight'
        else:
            return field_name.replace('rod', '').capitalize()
    
    def format_field_value(self, field_name, value):
        if isinstance(value, list):
            return ', '.join(value)
        else:
            return str(value) 