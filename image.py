import requests


class StreetView:

    def __init__(self, api_key):
        self.api_key = api_key

    def download_street_view_image(self, lat, lng, heading, file_name):
        
        url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},{lng}&heading={heading}&source=outdoor&key={self.api_key}"

        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        return response.content
