import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

print("--Point 1---")
response = requests.post(url)
print(response.text)

print("--Point 2---")
response = requests.head(url, data={"method": "HEAD"})
print(response.text)

print("--Point 3---")
response = requests.get(url, params={"method": "GET"})
print(response.text)

print("--Point 4---")
methodType = ["POST", "GET", "PUT", "DELETE"]
for rm in methodType:
    print(f"Check {rm} method")
    for mt in methodType:
        if rm == "GET":
            resp = requests.request(rm, url, params={"method": mt})
            print(f"Request type={rm}, param={mt}, response={resp.text}")
        else:
            resp = requests.request(rm, url, data={"method": mt})
            print(f"Request type={rm}, param={mt}, response={resp.text}")
        if rm ==mt and resp.text == "Wrong method provided":
            print(f"Request type={rm}, param={mt}, response={resp.text}, This is wrong case")
