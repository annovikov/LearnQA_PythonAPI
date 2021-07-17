from requests import Response
import json.decoder
from datetime import datetime
from lib.my_requests import MyRequests
import allure

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in last reponse."
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find headers with name {headers_name} in last response."
        return response.headers[headers_name]

    @staticmethod
    def get_json_value(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Fromat. Response text is {response.text}."

        assert name in response_as_dict, f"Response JSON doesn't have key {name}."
        return response_as_dict[name]

    @allure.step("Generate registration data for new user")
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f'{base_part}{random_part}@{domain}'
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    @allure.step("Create new user")
    def create_user(self):
        user_data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=user_data)
        return self.get_json_value(response, "id"), user_data


