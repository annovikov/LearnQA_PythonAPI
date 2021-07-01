import requests

def test_cookies():
    url = "https://playground.learnqa.ru/api/homework_header"

    get_header = requests.get(url)
    assert get_header.status_code == 200, "Wrong response code"
    header = get_header.headers
    print(header)
    assert header, "The header value is not available."