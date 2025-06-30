import json

def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def deduplicate_data(data):
    unique_data = []
    seen = set()
    for item in data:
        item_tuple = tuple(item.values())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_data.append(item)
    return unique_data 