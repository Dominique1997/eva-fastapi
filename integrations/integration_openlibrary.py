from requests import get

#https://openlibrary.org/dev/docs/api/search

class IntegrationOpenLibrary():
    baseUrl = "https://openlibrary.org"
    @classmethod
    def search_by_title(cls, bookTitle:str):
        response_data = get(f"{cls.baseUrl}/search.json?title={bookTitle}")
        return response_data

    #https://openlibrary.org/search.json?title=harry%20potter
    @classmethod
    def search_by_author(cls, author):
        response_data = get(f"{cls.baseUrl}/authors.json?q={author}")
        return response_data
