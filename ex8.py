import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url)
token = response.json()["token"]
delay = response.json()["seconds"]
print(response.json())

response2 = requests.get(url, params={"token": token})
print(response2.json()["status"])
assert response2.json()["status"] == "Job is NOT ready"

time.sleep(delay)

response3 = requests.get(url, params={"token": token})
status = response3.json()["status"]
result = response3.json()["result"]
assert status == "Job is ready"
assert result, "The field 'result' is not avaible"
print(f"{status}. The result is {result}.")
