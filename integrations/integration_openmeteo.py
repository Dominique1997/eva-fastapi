import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import json
from datetime import datetime, timedelta


def epochToDateTime(epochTime):
    return datetime.utcfromtimestamp(int(epochTime)/1000)

class IntegrationOpenMeto:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/gfs"

    @classmethod
    def _get_rain_hourly(cls):
        param = {
            "latitude": 50.965,
            "longitude": 5.5008,
            "hourly": ["rain"],
            "timezone": "Europe/Berlin"
        }
        response = cls.openmeteo.weather_api(cls.url, params=param)[0]
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(response.Hourly().Time(), unit="s"),
            end=pd.to_datetime(response.Hourly().TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=response.Hourly().Interval()),
            inclusive="left"
        )}
        hourly_data["rain"] = response.Hourly().Variables(0).ValuesAsNumpy()
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_results = json.loads(hourly_dataframe.to_json(orient='records'))
        for hourly_result in hourly_results:
            time_stamp = epochToDateTime(hourly_result["date"])
            hourly_result["date"] = time_stamp.strftime("%Y-%m-%d")
            hourly_result["hour"] = time_stamp.strftime("%H")
        return hourly_results

    @classmethod
    def _get_snowfall_hourly(cls):
        param = {
            "latitude": 50.965,
            "longitude": 5.5008,
            "hourly": ["snowfall"],
            "timezone": "Europe/Berlin"
        }
        response = cls.openmeteo.weather_api(cls.url, params=param)[0]
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(response.Hourly().Time(), unit="s"),
            end=pd.to_datetime(response.Hourly().TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=response.Hourly().Interval()),
            inclusive="left"
        )}
        hourly_data["snowfall"] = response.Hourly().Variables(0).ValuesAsNumpy()
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_results = json.loads(hourly_dataframe.to_json(orient='records'))
        for hourly_result in hourly_results:
            time_stamp = epochToDateTime(hourly_result["date"])
            hourly_result["date"] = time_stamp.strftime("%Y-%m-%d")
            hourly_result["hour"] = time_stamp.strftime("%H")
        return hourly_results

    @classmethod
    def _get_cloud_cover_hourly(cls):
        param = {
            "latitude": 50.965,
            "longitude": 5.5008,
            "hourly": ["cloud_cover"],
            "timezone": "Europe/Berlin"
        }
        response = cls.openmeteo.weather_api(cls.url, params=param)[0]
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(response.Hourly().Time(), unit="s"),
            end=pd.to_datetime(response.Hourly().TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=response.Hourly().Interval()),
            inclusive="left"
        )}
        hourly_data["cloud_cover"] = response.Hourly().Variables(0).ValuesAsNumpy()
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_results = json.loads(hourly_dataframe.to_json(orient='records'))
        for hourly_result in hourly_results:
            time_stamp = epochToDateTime(hourly_result["date"])
            hourly_result["date"] = time_stamp.strftime("%Y-%m-%d")
            hourly_result["hour"] = time_stamp.strftime("%H")
        return hourly_results

    @classmethod
    def get_rain_percentage(cls, days_to_add: int = 0):
        date_check = datetime.now() + timedelta(days=days_to_add)
        data = cls._get_rain_hourly()
        rain_data = [rain_info for rain_info in data if rain_info["date"] == date_check.strftime("%Y-%m-%d")
                     and rain_info["hour"] >= date_check.strftime("%H")]
        rain_avg = sum(rain_info["rain"] for rain_info in rain_data) / len(rain_data)
        return rain_avg

    @classmethod
    def get_snowfall_percentage(cls, days_to_add: int = 0):
        date_check = datetime.now() + timedelta(days=days_to_add)
        snowfall_data = cls._get_snowfall_hourly()
        data = [rain_info for rain_info in snowfall_data if rain_info["date"] == date_check.strftime("%Y-%m-%d")
                     and rain_info["hour"] >= date_check.strftime("%H")]
        snowfall_avg = sum(rain_info["snowfall"] for rain_info in data) / len(data)
        return snowfall_avg

    @classmethod
    def get_cloud_cover_percentage(cls, days_to_add: int = 0):
        date_check = datetime.now() + timedelta(days=days_to_add)
        cloud_cover_data = cls._get_cloud_cover_hourly()
        data = [rain_info for rain_info in cloud_cover_data if rain_info["date"] == date_check.strftime("%Y-%m-%d")
                     and rain_info["hour"] >= date_check.strftime("%H")]
        cloud_cover_avg = sum(rain_info["cloud_cover"] for rain_info in cloud_cover_data) / len(cloud_cover_data)
        return cloud_cover_avg
