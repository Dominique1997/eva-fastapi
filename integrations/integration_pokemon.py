from requests import get

#https://pokeapi.co/docs/v2

class IntegrationPokemon():
    baseUrl = "https://pokeapi.co/api/v2"

    @classmethod
    def get_berry_by_name(cls, berry_name):
        response_data = get(f"{cls.baseUrl}/berry/{berry_name}")
        return response_data

    @classmethod
    def get_berry_firmness(cls, berry_name):
        response_data = get(f"{cls.baseUrl}/berry-firmness/{berry_name}")
        return response_data

    @classmethod
    def get_berry_flavors(cls, berry_name):
        response_data = get(f"{cls.baseUrl}/berry-flavor/{berry_name}")
        return response_data

    @classmethod
    def get_contest_types_by_contest_name(cls, contest_name):
        response_data = get(f"{cls.baseUrl}/contest-type/{contest_name}")
        return response_data

    @classmethod
    def get_contest_effect_by_contest_name(cls, contest_name):
        response_data = get(f"{cls.baseUrl}/contest-type/{contest_name}")
        response_data = get(f"{cls.baseUrl}/contest-effect/{response_data.json()['id']}")
        return response_data

    @classmethod
    def get_super_contest_effect_by_contest_name(cls, contest_name):
        response_data = get(f"{cls.baseUrl}/contest-type/{contest_name}")
        response_data = get(f"{cls.baseUrl}/super-contest-effect/{response_data.json()['id']}")
        return response_data

    @classmethod
    def get_encounter_methods(cls, encounter_method):
        response_data = get(f"{cls.baseUrl}/encounter-method/{encounter_method}")
        return response_data

    @classmethod
    def get_encounter_conditions(cls, encounter_condition):
        response_data = get(f"{cls.baseUrl}/encounter-method/{encounter_condition}")
        return response_data

    @classmethod
    def get_encounter_condition_values(cls, encounter_condition_value):
        response_data = get(f"{cls.baseUrl}/encounter-method/{encounter_condition_value}")
        return response_data

    @classmethod
    def get_encounter_condition_values(cls, encounter_condition_value):
        response_data = get(f"{cls.baseUrl}/encounter-method/{encounter_condition_value}")
        return response_data