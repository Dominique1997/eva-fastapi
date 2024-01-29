from requests import get

#https://www.thecocktaildb.com/api.php

class IntegrationTheCocktailDB():
    baseUrl = "http://www.thecocktaildb.com/api/json/v1/1/"

    @classmethod
    def search_cocktail_by_name(cls, cocktailName):
        response_data = get(f"{cls.baseUrl}search.php?s={cocktailName}")
        return response_data

    @classmethod
    def search_random_cocktail(cls):
        response_data = get(f"{cls.baseUrl}random.php")
        return response_data

    @classmethod
    def search_cocktail_by_ingredient(cls, ingredient):
        response_data = get(f"{cls.baseUrl}filter.php?i={ingredient}")
        return response_data

    @classmethod
    def search_alcoholic_cocktails(cls):
        response_data = get(f"{cls.baseUrl}filter.php?a=Alcoholic")
        return response_data

    @classmethod
    def search_non_alcoholic_cocktails(cls):
        response_data = get(f"{cls.baseUrl}filter.php?a=Non_Alcoholic")
        return response_data

    @classmethod
    def search_cocktails_by_glass(cls, glassType):
        response_data = get(f"{cls.baseUrl}filter.php?g={glassType}")
        return response_data
