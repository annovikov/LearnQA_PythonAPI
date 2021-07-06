import requests

url_pass = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
pass_list = []

with open("../wiki_pass.txt", "r") as p:
    for item in p:
        item1 = item.rstrip('\n\,\, \'')
        pass_list.append(item1)

print(pass_list)
for i in pass_list:
    new_list = str(pass_list).split('", "')
print(new_list)


#for password in pass_list:
#    get_cookie = requests.post(url_pass, data={"login": "super_admin", "password": password})
#    cookie = print(get_cookie.cookies["auth_cookie"])
#    check_cookie = requests.post(url_check_cookie, data={"cookie":cookie})
#    print(check_cookie.text)
#    if check_cookie.text == "You are authorized":
#        print("Rigth password")
#        break

