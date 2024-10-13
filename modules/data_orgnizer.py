import json
from datetime import datetime

def combine_json(plan_history_json='./memory/plan_history_cache.json', code_history_json='./memory/code_history_cache.json', combined_json_path='./memory/combined_history_cache.json'):
    # Load the two JSON files
    with open(plan_history_json, 'r') as f:
        plan_json = json.load(f)
    with open(code_history_json, 'r') as f:
        code_json = json.load(f)

    # Combine the two JSON files
    combined_data = plan_json + code_json

    # Convert the timestamp strings to datetime objects, sort the combined JSON by timestamp, and convert the timestamps back to strings
    combined_data.sort(key=lambda x: datetime.strptime(list(x.keys())[0], '%Y-%m-%d,%H:%M:%S'))
    
    # Save the sorted, combined JSON to a new file
    with open(combined_json_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False)
    print("Combined history saved to", combined_json_path)

if __name__ == "__main__":
    combine_json()