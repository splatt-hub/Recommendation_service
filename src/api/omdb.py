import requests
from typing import Optional, List


class OMDBApi:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str) -> Optional[str]:
        params = {
            'apikey': self.api_key,
            't': title,
            'type': 'movie'
        }
        response = requests.get(self.url, {'t': title, 'apikey': self.api_key})
        print(self.api_key)
        print(response.text)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if 'Poster' in data:
                return data['Poster']

        return None

    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path:  # If image isn`t exist
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters
