from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure


@allure.epic("Deletion cases")
class TestUserDelete(BaseCase):
    @allure.tag("Negative test")
    @allure.description("Try delete user, with can't be deleted")
    def test_del_user2(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}

        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)

        response2 = MyRequests.delete("/user/2")
        Assertions.assert_code_status(response2, 400)

    @allure.tag("Positive test")
    @allure.description("Deletion of new user")
    def test_del_new_user(self):
        # CREATE
        new_user = BaseCase.create_user(self)

        # LOGIN USER
        login_data = {
            'email': new_user[1]["email"],
            'password': new_user[1]["password"]
        }
        response1 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(f"/user/{new_user[0]}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        Assertions.assert_code_status(response2, 200)

        # CHECK THAT USER DELETED
        response3 = MyRequests.get(f"/user/{new_user[0]}")
        Assertions.assert_response_text(response3, "User not found")

    @allure.tag("Negative test")
    @allure.description("Deletion user by other user")
    def test_del_user_by_other_user(self):
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

        # DELETE USER2 BY USER1
        response2 = MyRequests.delete(f"/user/{new_user2[0]}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        print(response2.content)
        Assertions.assert_code_status(response2, 200)

        # TRY TO LOGIN USER2
        login_data2 = {
            'email': new_user2[1]["email"],
            'password': new_user2[1]["password"]
        }
        response3 = MyRequests.post("/user/login", data=login_data2)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "user_id")
