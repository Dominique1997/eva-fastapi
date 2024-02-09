from requests import get
from utilities.credentials import Credentials

#https://www.theaudiodb.com/free_music_api

class IntegrationTheAudioDB():
    api_key = Credentials.get_audiodb_token()
    baseUrl = f"https://www.theaudiodb.com/api/v1/json/{api_key}/"

    @classmethod
    def search_artist_details_by_artist_name(cls, artistName):
        response_data = get(f"{cls.baseUrl}search.php?s={artistName}")
        print(response_data.json())
        return response_data

    @classmethod
    def search_album_details_by_artist_name(cls, artistName):
        response_data = get(f"{cls.baseUrl}searchalbum.php?s={artistName}")
        return response_data

    @classmethod
    def search_album_details_by_artist_name_and_album_name(cls, artistName, albumName):
        response_data = get(f"{cls.baseUrl}searchalbum.php?s={artistName}&t={albumName}")
        return response_data

    @classmethod
    def search_track_details_by_artist_name_and_album_name(cls, artistName, albumName):
        response_data = get(f"{cls.baseUrl}searchtrack.php?s={artistName}&t={albumName}")
        return response_data

    @classmethod
    def search_discography_by_artist_name_with_album_names_and_year(cls, artistName,):
        response_data = get(f"{cls.baseUrl}discography.php?s={artistName}")
        return response_data
