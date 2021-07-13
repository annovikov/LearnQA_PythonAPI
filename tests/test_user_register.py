import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):

    accounts = [
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "lastName": "learnqa", "email": "email45example.com"}, ("Invalid email format")),
        ({"username": "learnqa", "firstName": "learanqa", "lastName": "learnqa", "email": "email45example.com"}, ("The following required params are missed: password")),
        ({"password": "123", "firstName": "learanqa", "lastName": "learnqa", "email": "email45example.com"}, ("The following required params are missed: username")),
        ({"password": "123", "username": "learnqa", "lastName": "learnqa", "email": "email45example.com"}, ("The following required params are missed: firstName")),
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "email": "email45example.com"}, ("The following required params are missed: lastName")),
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "lastName": "learnqa"}, ("The following required params are missed: email")),
        ({"password": "123", "username": "l", "firstName": "learanqa", "lastName": "learnqa", "email": "email@45example.com"}, ("The value of 'username' field is too short")),
        ({"password": "123", "username": "c"*251, "firstName": "learanqa", "lastName": "learnqa", "email": "email45@example.com"}, ("The value of 'username' field is too long"))
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        print(response.text)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("accounts", accounts)
    def test_create_invalid_user(self, accounts):
        response = requests.post('https://playground.learnqa.ru/api/user/', data=accounts[0])
        Assertions.assert_code_status(response, 400)
        print(response.text)
        Assertions.assert_response_text(response, accounts[1])
