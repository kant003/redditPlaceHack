import requests
import re
import json

username ="XXXX",
password: "YYYY",
color_index_in=2
canvas_index=0
x=0
y=0

client = requests.Session()
client.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    }
)

r = client.get(
    "https://www.reddit.com/login",
)
#print(r.text)
x = re.search(r'csrf_token.*value="(.*)"', str(r.text))
print(x.group(1))

csrf_token=x.group(1)


data = {
    "username": username,
    "password": password,
    "dest": "https://new.reddit.com/",
    "csrf_token": csrf_token,
}

r = client.post(
    "https://www.reddit.com/login",
    data=data,
)

#print(r.text)

r = client.get(
    "https://new.reddit.com/",
)

v=str(r.text)


x2 = re.search(r'accessToken":"(.*)"', v)
print(x2.group(1))


i=x2.group(1).index('"')
access_token_in=x2.group(1)[0:i]



url = "https://gql-realtime-2.reddit.com/query"

payload = json.dumps(
    {
        "operationName": "setPixel",
        "variables": {
            "input": {
                "actionName": "r/replace:set_pixel",
                "PixelMessageData": {
                    "coordinate": {"x": x, "y": y},
                    "colorIndex": color_index_in,
                    "canvasIndex": canvas_index,
                },
            }
        },
        "query": "mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
)
headers = {
    "origin": "https://hot-potato.reddit.com",
    "referer": "https://hot-potato.reddit.com/",
    "apollographql-client-name": "mona-lisa",
    "Authorization": "Bearer " + access_token_in,
    "Content-Type": "application/json",
}

response = requests.request(
    "POST",
    url,
    headers=headers,
    data=payload,
)

print(response.text)
