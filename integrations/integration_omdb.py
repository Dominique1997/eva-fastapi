from requests import get
import urllib
from utilities.credentials import Credentials

#http://www.omdbapi.com/

class IntegrationOMDB():
    api_key = Credentials.get_omdb_token()
    baseUrl = f"http://www.omdbapi.com/?apikey={api_key}&"

    @classmethod
    def search_by_title(cls, movieTitle: str):
        response_data = get(f"{cls.baseUrl}t={movieTitle}")
        return response_data
