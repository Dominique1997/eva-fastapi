from requests import get

#https://www.themealdb.com/api.php

class IntegrationTheMealDB():
    baseUrl = "http://www.themealdb.com/api/json/v1/1/"

    @classmethod
    def search_meal_by_name(cls, mealName):
        response_data = get(f"{cls.baseUrl}search.php?s={mealName}")
        return response_data

    @classmethod
    def search_random_meal(cls):
        response_data = get(f"{cls.baseUrl}random.php")
        return response_data

    @classmethod
    def search_meal_by_ingredient(cls, ingredient):
        response_data = get(f"{cls.baseUrl}filter.php?i={ingredient}")
        return response_data

    @classmethod
    def search_meal_by_area(cls, area):
        response_data = get(f"{cls.baseUrl}filter.php?a={area}")
        return response_data