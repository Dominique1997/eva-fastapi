import datetime
import json

from credentials import Credentials
from requests import post, get


class IntegrationHomeAssistant:
    main_url = "http://192.168.1.191:8123"
    ha_token = Credentials.get_home_assistant_token()

    @classmethod
    def _get_api(cls, url_suffix="/api/"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_api_config(cls, url_suffix="/api/config"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_api_events(cls, url_suffix="/api/events"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_api_services(cls, url_suffix="/api/services"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_api_history_by_period_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/history/period/"):
        cls.perform_get(url_suffix + timestamp)
    @classmethod
    def _get_api_logbook_by_timestamp(cls, timestamp: datetime.datetime, url_suffix=f"/api/logbook/"):
        cls.perform_get(url_suffix + timestamp)
    @classmethod
    def _get_api_states(cls, url_suffix="/api/states"):
        states = cls.perform_get(url_suffix)
        for state in states:
            print(state)
            print(state["entity_id"])
            print(state["state"])
            if "friendly_name" in state["attributes"]:
                print(state["attributes"]["friendly_name"])
    @classmethod
    def _get_api_states_by_entity_id(cls, entity_id: str, url_suffix="/api/states/"):
        cls.perform_get(url_suffix + entity_id)
    @classmethod
    def _get_api_error_log(cls, url_suffix="/api/error_log"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_camera_proxy_by_camera_entity_id(cls, entity_id: str, url_suffix="/api/camera_proxy/"):
        cls.perform_get(url_suffix + entity_id)
    @classmethod
    def _get_api_calendars(cls, url_suffix="/api/calendars"):
        cls.perform_get(url_suffix)
    @classmethod
    def _get_api_calendars_by_calendar_entity_id(cls, entity_id: str, url_suffix="/api/calendars/"):
        cls.perform_get(url_suffix + entity_id)
    @classmethod
    def _post_api_states_by_entity_id(cls):
        pass
    @classmethod
    def _post_api_events_by_event_type(cls):
        pass
    @classmethod
    def _post_api_services_by_domain_by_service(cls):
        pass
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
            print(response.json())
            return response.json()
        else:
            print(response.status_code)
    @classmethod
    def perform_get(cls, endpoint):
        print("------------------------------------------------------------------------------------------------")
        response = get(cls.main_url+endpoint, headers=cls.get_header())
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(response.status_code)

#IntegrationHomeAssistant._get_api()
##IntegrationHomeAssistant._get_api_calendars()
##IntegrationHomeAssistant._get_api_calendars_by_calendar_entity_id()
#IntegrationHomeAssistant._get_api_config()
##IntegrationHomeAssistant._get_api_error_log()
#IntegrationHomeAssistant._get_api_events()
##IntegrationHomeAssistant._get_api_history_by_period_timestamp()
##IntegrationHomeAssistant._get_api_logbook_by_timestamp()
#IntegrationHomeAssistant._get_api_services()
IntegrationHomeAssistant._get_api_states()
##IntegrationHomeAssistant._get_api_states_by_entity_id()
##IntegrationHomeAssistant._get_camera_proxy_by_camera_entity_id()
