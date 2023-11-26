import datetime
import json
from utilities.credentials import Credentials
from requests import post, get

class IntegrationHomeAssistant:
    main_url = "http://192.168.1.234:8123"
    ha_token = Credentials.get_home_assistant_token()
    list_services = []

    @classmethod
    def load_information(cls):
        cls.list_services = json.loads(cls._get_api_services())

    @classmethod
    def check_tag(cls, tag):
        for service_data in cls.list_services:
            if tag in service_data["services"]:
                cls._post_api_services_by_domain_by_service(service_data["domain"], tag)
    @classmethod
    def _get_api(cls, url_suffix="/api/"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_config(cls, url_suffix="/api/config"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_events(cls, url_suffix="/api/events"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_services(cls, url_suffix="/api/services"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_history_by_period_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/history/period/"):
        return cls.perform_get(url_suffix + timestamp)

    @classmethod
    def _get_api_logbook_by_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/logbook/"):
        return cls.perform_get(url_suffix + timestamp)

    @classmethod
    def _get_api_states(cls, url_suffix="/api/states"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_states_by_entity_id(cls, entity_id: str, url_suffix="/api/states/"):
        return cls.perform_get(url_suffix + entity_id)

    @classmethod
    def _get_api_error_log(cls, url_suffix="/api/error_log"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_camera_proxy_by_camera_entity_id(cls, entity_id: str, url_suffix="/api/camera_proxy/"):
        return cls.perform_get(url_suffix + entity_id)

    @classmethod
    def _get_api_calendars(cls, url_suffix="/api/calendars"):
        return cls.perform_get(url_suffix)

    @classmethod
    def _get_api_calendars_by_calendar_entity_id(cls, entity_id: str, url_suffix="/api/calendars/"):
        return cls.perform_get(url_suffix + entity_id)

    @classmethod
    def _post_api_states_by_entity_id(cls):
        pass

    @classmethod
    def _post_api_events_by_event_type(cls):
        pass

    @classmethod
    def _post_api_services_by_domain_by_service(cls, domain, service):
        cls.perform_post(f"/api/services/{domain}/{service}")

    @classmethod
    def _post_api_template(cls):
        pass

    @classmethod
    def _post_api_config_core_check_config(cls):
        pass

    @classmethod
    def _post_api_intent_handle(cls):
        pass

    @classmethod
    def get_header(cls):
        return {"Authorization": f"Bearer {cls.ha_token}", "Content-Type": "application/json"}

    @classmethod
    def perform_post(cls, endpoint):
        response = post(cls.main_url+endpoint, headers=cls.get_header())
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(response.status_code)

    @classmethod
    def perform_get(cls, endpoint):
        print("------------------------------------------------------------------------------------------------")
        response = get(cls.main_url+endpoint, headers=cls.get_header())
        if response.status_code == 200 or response.status_code == 201:
            return json.dumps(response.json())
        else:
            print(response.status_code)

