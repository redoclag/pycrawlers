import requests
from bs4 import BeautifulSoup
headers = {
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'
}

login_data= {
    "scope":"",
     "grant_type":"password",
    # "signup_v3_endpoints_web":null,
     "email":"",
     "password":"",
    #"address":null
}
with requests.Session() as s:

    url = "https://www.instacart.com"
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    token = soup.find(attrs={"name": "csrf-token"})["content"]
    print (token)
    login_data["authenticity_token"] = token
    print(login_data)
    r = s.post(url, data = login_data, headers = headers)

    print(r.content)
