import json
from preprocessing import process_file

def test_preprocess_data():
    # Paths to the JSON file and the schema
    json_filepath = 'data/2024_FEBRUARY.json'
    schema_filepath = 'schemas/Semantic.schema.json'

    # Process the data
    data = process_file(json_filepath, schema_filepath)

    # Check that the data is not None
    assert data is not None, "No data was returned after processing."

    # Check for non-empty extraction
    assert len(data['activitySegments']) > 0, "No activity segments were extracted."
    assert len(data['placeVisits']) > 0, "No place visits were extracted."

    # Optionally check for specific content details
    # Example: Assert that all extracted activities have a 'duration'
    for activity in data['activitySegments']:
        assert 'duration' in activity, "Activity segment without duration."

# Run pytest in the console to execute this test
