import requests
import math


'''
This module contains functions for getting nearby panorama ids and positions
for a given location (lat, lng).

Also, heading can be calculated by using two positions (lat, lng). This can be
used if we are downloading images that are not 360 degrees therefore we need
to calculate the heading for each image to track road ditch where cabinet could be.

The function get_nearby_panorama_ids() returns a dictionary with two keys:
    - panorama_ids: a set of panorama ids
    - panorama_positions: a list of dictionaries with lat and lng keys

NOTE:   The function get_panorama_id requires the Google Maps API key.
NOTE:   We are only getting panoramas that are taken by Google. Other panoramas are unfortunately not supported
        becuase our downloader that uses these panorama ids only supports Google panoramas.
'''


def get_panorama_id(api_key, lat, lng):
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    # TODO currently we are only interested in panoramas that are
    # taken by Google. We should also consider other panoramas.
    if data.get('status') == 'OK' and "Google" in data.get('copyright'):
        return data['pano_id']
    else:
        return None

def get_nearby_panorama_ids(api_key, lat, lng, radius=60, step=10):

    panorama_ids = []
    panorama_positions = []

    for x in range(-radius, radius + 1, step):
        for y in range(-radius, radius + 1, step):
            if x * x + y * y <= radius * radius:

                lat_offset = x / 111111
                lng_offset = y / (111111 * math.cos(lat * math.pi / 180))

                pano_id = get_panorama_id(api_key, lat + lat_offset, lng + lng_offset)
                
                if pano_id and pano_id not in panorama_ids:
                    panorama_ids.append(pano_id)
                    panorama_positions.append({
                        "lat": lat + lat_offset,
                        "lng": lng + lng_offset
                    })

    return {
        "panorama_ids": panorama_ids,
        "panorama_positions": panorama_positions
    }

def calculate_heading(point1, point2):
    lat1, lng1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lng2 = math.radians(point2[0]), math.radians(point2[1])

    dLng = lng2 - lng1
    y = math.sin(dLng) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLng)
    heading = math.degrees(math.atan2(y, x))

    return (heading + 360) % 360


# Usage example how to get nearby panorama ids and positions
# for a given location (lat, lng)
api_key = ''
lat, lng = 66, 25
data = get_nearby_panorama_ids(api_key, lat, lng)
print(data)
