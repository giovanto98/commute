import json
from datetime import timedelta
from dateutil.parser import parse

# Constants for Home and Work Addresses
HOME_ADDRESS = "Sloterkade 112, 1058 HL Amsterdam, Nederland"
WORK_ADDRESS = "Kattenburgerstraat 5, 1018 JA Amsterdam, Nederland"

def load_processed_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def parse_duration(duration):
    start = parse(duration['startTimestamp'])
    end = parse(duration['endTimestamp'])
    return end - start

def is_address_match(visit_address, target_address):
    """Check if the visit address matches the target address."""
    return visit_address.lower() == target_address.lower()

def analyze_place_visits_by_address(data, home_address, work_address, min_duration_minutes=30):
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
                continue  # Skip visits that do not match either address

            visit_details = {
                'address': visit_address,
                'duration': duration,
                'start': parse(visit['duration']['startTimestamp']),
                'end': parse(visit['duration']['endTimestamp']),
                'near': near_label
            }
            relevant_visits.append(visit_details)
            #print(f"Visit near {near_label}: {visit_details}")  # Debugging output

    return relevant_visits



def main():
    processed_data = load_processed_data('processed/processed_data.json')
    visits = analyze_place_visits_by_address(processed_data, HOME_ADDRESS, WORK_ADDRESS)
    print(f"Total relevant visits identified: {len(visits)}")

if __name__ == '__main__':
    main()
