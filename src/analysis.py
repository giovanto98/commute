import json
import os
import pandas as pd
from datetime import timedelta
from dateutil.parser import parse
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Constants for home and work addresses in Amsterdam
HOME_ADDRESS = "Sloterkade 112, 1058 HL Amsterdam, Nederland"
WORK_ADDRESS = "Kattenburgerstraat 5, 1018 JA Amsterdam, Nederland"
HOME_COORDINATES = (52.352354, 4.852443)
WORK_COORDINATES = (52.373705, 4.914739)

def load_processed_data(filepath):
    """Loads processed data from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def parse_duration(duration):
    """Calculates the duration between start and end timestamps."""
    start = parse(duration['startTimestamp'])
    end = parse(duration['endTimestamp'])
    return end - start

def is_address_match(visit_address, target_address):
    """Checks if the provided addresses match, ignoring case."""
    return visit_address.lower() == target_address.lower()

def analyze_place_visits_by_address(data, home_address, work_address, min_duration_minutes=30):
    """Analyzes place visits and filters them based on duration and address match."""
    relevant_visits = []
    for visit in data.get('placeVisits', []):
        visit_address = visit['location'].get('address', "")
        duration = parse_duration(visit['duration'])

        if duration >= timedelta(minutes=min_duration_minutes):
            if is_address_match(visit_address, home_address):
                near_label = 'Home'
            elif is_address_match(visit_address, work_address):
                near_label = 'Work'
            else:
                continue

            visit_details = {
                'address': visit_address,
                'duration': duration,
                'start': parse(visit['duration']['startTimestamp']),
                'end': parse(visit['duration']['endTimestamp']),
                'near': near_label
            }
            relevant_visits.append(visit_details)
    return relevant_visits

def find_commutes(visits):
    """Identifies commutes between home and work based on consecutive visits."""
    commutes = []
    visits.sort(key=lambda x: x['start'])  # Sorting by start time
    for i in range(len(visits) - 1):
        if visits[i]['near'] != visits[i + 1]['near'] and (visits[i + 1]['start'] - visits[i]['end']) <= timedelta(hours=1):
            commutes.append((visits[i], visits[i + 1]))
    return commutes

def analyze_activity_segments(data, commutes):
    """Analyzes activity segments that occur during the identified commutes."""
    activity_segments = []
    for commute in commutes:
        start_time = commute[0]['end']
        end_time = commute[1]['start']
        for segment in data.get('activitySegments', []):
            segment_start = parse(segment['duration']['startTimestamp'])
            segment_end = parse(segment['duration']['endTimestamp'])
            if start_time <= segment_start < segment_end <= end_time:
                detailed_segment = {
                    'activityType': segment.get('activityType'),
                    'confidence': segment.get('confidence'),
                    'duration': segment.get('duration'),
                    'startLocation': segment.get('startLocation'),
                    'endLocation': segment.get('endLocation'),
                    'waypointPath': segment.get('waypointPath')
                }
                activity_segments.append(detailed_segment)
    return activity_segments

def save_commutes_to_json(commutes, filename):
    """Saves identified commutes into a JSON file."""
    folder_path = 'processed'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as file:
        json.dump(commutes, file, indent=4)

def main():
    processed_data = load_processed_data('processed/processed_data.json')

    visits_by_address = analyze_place_visits_by_address(processed_data, HOME_ADDRESS, WORK_ADDRESS)
    commutes = find_commutes(visits_by_address)
    activities = analyze_activity_segments(processed_data, commutes)

    print(f"Total relevant visits by address: {len(visits_by_address)}")
    print(f"Total identified commutes: {len(commutes)}")
    print(f"Activities during commutes: {len(activities)}")

    save_commutes_to_json(activities, 'commutes.json')

if __name__ == '__main__':
    main()

