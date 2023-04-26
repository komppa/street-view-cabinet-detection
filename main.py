import googlemaps
from googlemaps.convert import decode_polyline
import numpy as np
import folium


def plot_map(coordinates):
    # Calculate the center of the map as the average of latitudes and longitudes
    center_lat = sum(coord['lat'] for coord in coordinates) / len(coordinates)
    center_lng = sum(coord['lng'] for coord in coordinates) / len(coordinates)
    
    # Create a map centered at the calculated center
    map = folium.Map(location=[center_lat, center_lng], zoom_start=14)
    
    # Add the coordinates as a PolyLine to the map
    polyline = folium.PolyLine([(coord['lat'], coord['lng']) for coord in coordinates], color="blue", weight=2.5, opacity=1)
    polyline.add_to(map)

    # Optionally, add markers for each coordinate
    for coord in coordinates:
        folium.Marker([coord['lat'], coord['lng']]).add_to(map)
    
    return map

def interpolate_points(coords, num_points=1000):
    latitudes = [coord['lat'] for coord in coords]
    longitudes = [coord['lng'] for coord in coords]
    
    latitudes_interp = np.interp(np.linspace(0, len(latitudes), num_points), np.arange(len(latitudes)), latitudes)
    longitudes_interp = np.interp(np.linspace(0, len(longitudes), num_points), np.arange(len(longitudes)), longitudes)
    
    return [{'lat': lat, 'lng': lng} for lat, lng in zip(latitudes_interp, longitudes_interp)]


def distribute_points(coords, min_distance=10, max_distance=20):
    new_coords = [coords[0]]
    current_coord = coords[0]

    for coord in coords[1:]:
        lat1, lng1 = current_coord['lat'], current_coord['lng']
        lat2, lng2 = coord['lat'], coord['lng']
        
        distance = np.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2) * 111000
        
        if min_distance <= distance <= max_distance:
            new_coords.append(coord)
            current_coord = coord
        elif distance > max_distance:
            num_extra_points = int(distance // max_distance)
            step = 1 / (num_extra_points + 1)
            
            for t in np.arange(step, 1, step):
                lat_new = lat1 + t * (lat2 - lat1)
                lng_new = lng1 + t * (lng2 - lng1)
                new_coords.append({'lat': lat_new, 'lng': lng_new})
                
            new_coords.append(coord)
            current_coord = coord

    return new_coords

def get_route_polyline(api_key, origin, destination):
    gmaps = googlemaps.Client(key=api_key)
    directions = gmaps.directions(origin, destination)
    polyline = directions[0]['overview_polyline']['points']
    return polyline

def get_route_coordinates(polyline):
    return decode_polyline(polyline)


def main():

    api_key = ''
    origin = ''
    destination = ''

    polyline = get_route_polyline(api_key, origin, destination)

    coordinates = np.array(get_route_coordinates(polyline))

    coordinates = interpolate_points(coordinates, num_points=1000)

    coordinates = distribute_points(coordinates, 10, 20)

    map = plot_map(coordinates)
    map.save('map.html')


if __name__ == "__main__":
    main()