import folium
import matplotlib.pyplot as plt

def plot_commutes(commutes):
    m = folium.Map(location=[52.3676, 4.9041], zoom_start=12)
    for commute in commutes:
        start_coords = (commute['startLocation']['latitudeE7'] / 1e7, commute['startLocation']['longitudeE7'] / 1e7)
        end_coords = (commute['endLocation']['latitudeE7'] / 1e7, commute['endLocation']['longitudeE7'] / 1e7)
        folium.PolyLine(locations=[start_coords, end_coords], color='blue').add_to(m)
    return m

def plot_transport_modes(modes_count):
    plt.figure(figsize=(10, 6))
    plt.bar(modes_count.keys(), modes_count.values())
    plt.xlabel('Transport Mode')
    plt.ylabel('Count')
    plt.title('Commute Transport Modes')
    plt.xticks(rotation=45)
    plt.show()
