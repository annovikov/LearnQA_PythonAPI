from requests import Response
import json.decoder

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
