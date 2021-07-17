import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        print(register_data)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")


    def test_edit_by_not_auth_user(self):
        new_user = BaseCase.create_user(self)
        print(new_user)
        print(new_user[0])
        print(new_user[1]["email"])
        new_name = "Super_name"
        response = MyRequests.put(f"/user/{new_user[0]}", data={"firstName": new_name})
        Assertions.assert_response_text(response, "Auth token not supplied")
        Assertions.assert_code_status(response, 400)

    def test_edit_user_by_other_user(self):
        # CREATE TWO USERS
        new_user1 = BaseCase.create_user(self)
        new_user2 = BaseCase.create_user(self)

        # LOGIN USER1
        login_data = {
            'email': new_user1[1]["email"],
            'password': new_user1[1]["password"]
        }
        response1 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT USER2
        new_name = "SuperName"
        response2 = MyRequests.put(f"/user/{new_user2[0]}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response2, 200)

        # LOGIN USER2 AND CHECK NEW NAME
        login_data2 = {
            'email': new_user2[1]["email"],
            'password': new_user2[1]["password"]
        }
        response3 = MyRequests.post("/user/login", data=login_data2)
        Assertions.assert_code_status(response3, 200)

        auth_sid2 = self.get_cookie(response3, "auth_sid")
        token2 = self.get_header(response3, "x-csrf-token")

        response4 = MyRequests.get(f"/user/{new_user2[0]}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2})
        expected_name = new_user2[1]["firstName"]
        actual_name = response4.json()["firstName"]
        Assertions.assert_json_value_by_name(response4, "firstName", expected_name , f"Wrong FirstName. Actual {actual_name}, but should be {new_name}.")



    wrong_data = [
        ({'email': "testexample.com"}, ("Invalid email format")),
        ({'firstName': "q"}, ("Too short value for field firstName"))
    ]

    @pytest.mark.parametrize("wrong_data", wrong_data)
    def test_edit_short_name(self, wrong_data):
        # CREATE
        new_user1 = BaseCase.create_user(self)

        # LOGIN USER1
        login_data = {
            'email': new_user1[1]["email"],
            'password': new_user1[1]["password"]
        }
        response1 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        response2 = MyRequests.put(f"/user/{new_user1[0]}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data=wrong_data[0]
                                   )
        Assertions.assert_code_status(response2, 400)
        print(response2.text)
        Assertions.assert_response_text(response2, wrong_data[1])
