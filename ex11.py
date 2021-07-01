import requests

def test_cookies():
    url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"

    get_cookie = requests.post(url, data={"login": "super_admin", "password": "password"})
    assert get_cookie.status_code == 200, "Wrong response code"
    cookie = get_cookie.cookies["auth_cookie"]
    print(f"Cookie value is {cookie}")
    assert cookie, "The cookie value is not available."