import json

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_relevant_data(data):
    relevant_data = {
        "activitySegments": [],
        "placeVisits": []
    }
    
    for item in data.get('timelineObjects', []):
        if 'activitySegment' in item:
            segment = item['activitySegment']
            relevant_data['activitySegments'].append({
                "activityType": segment.get('activityType'),
                "confidence": segment.get('confidence'),
                "duration": segment.get('duration'),
                "startLocation": segment.get('startLocation'),
                "endLocation": segment.get('endLocation'),
                "waypointPath": {
                    "confidence": segment.get('waypointPath', {}).get('confidence'),
                    "distanceMeters": segment.get('waypointPath', {}).get('distanceMeters'),
                    "travelMode": segment.get('waypointPath', {}).get('travelMode')
                }
            })
        
        if 'placeVisit' in item:
            visit = item['placeVisit']
            location = visit.get('location', {})
            relevant_data['placeVisits'].append({
                "duration": {
                    "startTimestamp": visit['duration'].get('startTimestamp'),
                    "endTimestamp": visit['duration'].get('endTimestamp')
                },
                "location": {
                    "latitudeE7": location.get('latitudeE7'),
                    "longitudeE7": location.get('longitudeE7'),
                    "accuracyMetres": location.get('accuracyMetres'),
                    "address": location.get('address')
                },
                "locationConfidence": visit.get('locationConfidence')
            })
    
    return relevant_data

def process_file(json_filepath):
    data = load_json(json_filepath)
    processed_data = extract_relevant_data(data)
    processed_file_path = 'processed/processed_data.json'  # Updated path
    with open(processed_file_path, 'w') as file:
        json.dump(processed_data, file, indent=4)
    return processed_data


# Example usage within the project
if __name__ == '__main__':
    json_filepath = 'data/2024_FEBRUARY.json'
    processed_data = process_file(json_filepath)
    print("Processed data saved to 'processed_data.json'")
