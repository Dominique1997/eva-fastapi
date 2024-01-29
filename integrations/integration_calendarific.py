from requests import get
from utilities.credentials import Credentials
from datetime import datetime

#https://calendarific.com/api-documentation

class IntegrationCalendarific():
    api_key = Credentials.get_calendarific_token()
    baseUrl = f"https://calendarific.com/api/v2/holidays?api_key={api_key}"

    @classmethod
    def get_all_holidays_by_year_and_country_code(cls, country_code, year=datetime.now().year):
        response_data = get(f"{cls.baseUrl}&country={country_code}&year={year}")
        return response_data
