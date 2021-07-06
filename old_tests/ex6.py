import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(response.url)
redirect = response.history
print(f"Количество редиректов {len(redirect)}")