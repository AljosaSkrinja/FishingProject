import json
import os
from config import JSON_FOLDER, ROD_TYPES, get_json_path, create_category_name

class DataProcessor:
    
    def __init__(self):
        self.processed_folder = "ProcessedData"
        self._ensure_processed_folder()
    
    def _ensure_processed_folder(self):
        if not os.path.exists(self.processed_folder):
            os.makedirs(self.processed_folder)
    
    def process_all_data(self):
        self.process_rods_data()
    
    def process_rods_data(self):
        all_rods = []
        
        for rod_type in ROD_TYPES:
            rod_data = self._load_json(f'{rod_type}.json')
            
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
            
            for rod in raw_rods:
                processed_rod = self._process_single_rod(rod, rod_type, capabilities)
                all_rods.append(processed_rod)
        
        self._save_json('processed_rods.json', all_rods)
    
    def _process_single_rod(self, rod, rod_type, capabilities):
        category_name = create_category_name(capabilities)
        
        price_parts = []
        if rod.get('baitcoinsCost', 0) > 0:
            price_parts.append(f"{rod['baitcoinsCost']} BC")
        if rod.get('clubTokensCost', 0) > 0:
            price_parts.append(f"{rod['clubTokensCost']} CT")
        if rod.get('creditsCost', 0) > 0:
            price_parts.append(f"{rod['creditsCost']} CC")
        
        if not price_parts:
            price = "Free"
        else:
            price = " + ".join(price_parts)
        
        processed_rod = {
            'id': rod.get('id', ''),
            'name': rod.get('rodName', 'Unknown Rod'),
            'brand': rod.get('rodBrand', 'Unknown'),
            'length': f"{rod.get('rodLength', 0)}m",
            'action': rod.get('rodAction', 'Unknown'),
            'power': rod.get('rodPower', 'Unknown'),
            'level': rod.get('rodLevel', 'Unknown'),
            'price': price,
            'category': category_name,
            'rodtype': rod_type,
            'guides': rod.get('rodGuides', 'Unknown'),
            'pieces': rod.get('rodPieces', 'Unknown')
        }
        
        # Only add weight fields if they have valid values
        line_weight = self._format_weight_range(rod, 'rodLineWeightMinimum', 'rodLineWeightMaximum', 'kg')
        if line_weight != "Unknown":
            processed_rod['lineWeight'] = line_weight
        
        lure_weight = self._format_weight_range(rod, 'rodLureWeightMinimum', 'rodLureWeightMaximum', 'g')
        if lure_weight != "Unknown":
            processed_rod['lureWeight'] = lure_weight
        
        return processed_rod
    
    def _format_weight_range(self, rod_data, min_field, max_field, unit):
        if min_field in rod_data and max_field in rod_data:
            min_weight = rod_data[min_field]
            max_weight = rod_data[max_field]
            return f"{min_weight}-{max_weight} {unit}"
        return "Unknown"
    
    def _load_json(self, filename):
        file_path = os.path.join(JSON_FOLDER, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    
    def _save_json(self, filename, data):
        file_path = os.path.join(self.processed_folder, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

class ProcessDataScript:
    
    @staticmethod
    def main():
        print("Processing raw data...")
        processor = DataProcessor()
        processor.process_all_data()
        print("Data processing complete! Check the ProcessedData folder.")

if __name__ == "__main__":
    ProcessDataScript.main() 