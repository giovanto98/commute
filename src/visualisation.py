import json
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse

def load_commute_data(filepath):
    """Load commute data from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def prepare_data_for_plotting(data):
    """Convert loaded data into a DataFrame for easier manipulation, checking for missing 'segments'."""
    records = []
    for commute in data:
        # Safely access 'segments' if they exist, else skip to the next commute
        if 'segments' in commute:
            for segment in commute['segments']:
                start_time = parse(segment['startTimestamp'])
                records.append({
                    'Date': start_time.date(),
                    'Time': start_time.time(),
                    'TransportMode': segment.get('activityType', 'Unknown')  # Default to 'Unknown' if not present
                })
        else:
            print(f"Warning: No segments found for commute from {commute.get('start')} to {commute.get('end')}")
    return pd.DataFrame(records)

def plot_commute_days(df):
    """Plot a bar chart of the days on which commuting occurred."""
    commute_days = df['Date'].value_counts().sort_index()
    commute_days.plot(kind='bar', color='skyblue', figsize=(10, 5))
    plt.title('Commute Days Overview')
    plt.xlabel('Date')
    plt.ylabel('Number of Commutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_commute_times(df):
    """Plot a histogram of the times of day at which commuting occurred."""
    times = pd.to_datetime(df['Time'].astype(str)).dt.hour
    times.plot(kind='hist', bins=24, range=(0,24), rwidth=0.8, color='green', alpha=0.7)
    plt.title('Commute Time Distribution')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.xticks(range(0, 25, 1))
    plt.tight_layout()
    plt.show()

def plot_transport_modes(df):
    """Plot a pie chart of the transport modes used for commuting."""
    transport_modes = df['TransportMode'].value_counts()
    transport_modes.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(transport_modes))))
    plt.title('Transport Modes Used for Commuting')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def main():
    data = load_commute_data('./processed/commutes.json')
    df = prepare_data_for_plotting(data)
    if not df.empty:
        plot_commute_days(df)
        plot_commute_times(df)
        plot_transport_modes(df)
    else:
        print("No data available for plotting.")

if __name__ == '__main__':
    main()
