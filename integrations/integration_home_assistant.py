import datetime
import json
from utilities.credentials import Credentials
from requests import post, get

class IntegrationHomeAssistant:
    baseUrl = "http://192.168.1.234:8123"
    ha_token = Credentials.get_home_assistant_token()
    @classmethod
    def get_api(cls, url_suffix="/api/"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_config(cls, url_suffix="/api/config"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_events(cls, url_suffix="/api/events"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_services(cls, url_suffix="/api/services"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_history_by_period_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/history/period/"):
        return cls._perform_get(url_suffix + timestamp)

    @classmethod
    def get_api_logbook_by_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/logbook/"):
        return cls._perform_get(url_suffix + timestamp)

    @classmethod
    def get_api_states(cls, url_suffix="/api/states"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_states_by_entity_id(cls, entity_id: str, url_suffix="/api/states/"):
        return cls._perform_get(url_suffix + entity_id)

    @classmethod
    def get_api_error_log(cls, url_suffix="/api/error_log"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_camera_proxy_by_camera_entity_id(cls, entity_id: str, url_suffix="/api/camera_proxy/"):
        return cls._perform_get(url_suffix + entity_id)

    @classmethod
    def get_api_calendars(cls, url_suffix="/api/calendars"):
        return cls._perform_get(url_suffix)

    @classmethod
    def get_api_calendars_by_calendar_entity_id(cls, entity_id: str, url_suffix="/api/calendars/"):
        return cls._perform_get(url_suffix + entity_id)

    @classmethod
    def post_api_states_by_entity_id(cls):
        pass

    @classmethod
    def post_api_events_by_event_type(cls):
        pass

    @classmethod
    def post_api_services_by_domain_by_service(cls, domain, service):
        return cls._perform_post(f"/api/services/{domain}/{service}")

    @classmethod
    def post_api_template(cls):
        pass

    @classmethod
    def post_api_config_core_check_config(cls):
        pass

    @classmethod
    def post_api_intent_handle(cls):
        pass

    @classmethod
    def _get_header(cls):
        return {"Authorization": f"Bearer {cls.ha_token}", "Content-Type": "application/json"}

    @classmethod
    def _perform_post(cls, endpoint):
        response = post(cls.baseUrl+endpoint, headers=cls._get_header())
        return response

    @classmethod
    def _perform_get(cls, endpoint):
        response = get(cls.baseUrl+endpoint, headers=cls._get_header(), timeout=5)
        return response
