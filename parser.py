import json

def parse_json(file_path):
    """Parse a JSON file and return its contents."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error parsing JSON file: {e}")
        return {}

def deduplicate_data(data):
    """Remove duplicate items from a list of dictionaries."""
    unique_data = []
    seen = set()
    for item in data:
        item_tuple = tuple(item.values())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_data.append(item)
    return unique_data 