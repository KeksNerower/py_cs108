import vkapi.friends as fr
from vkapi.config import VK_CONFIG

import requests


# Some data for query
domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]

# Code
code = """return API.wall.get({
    "owner_id": "",
    "domain": "itmoru",
    "offset": 0,
    "count": 1,
    "filter": "owner",
    "extended": 0,
    "fields": "",
    "v": "5.126"
});"""

response = requests.post(
    url=f"{domain}/execute",
        data={
            "code": code,
            "access_token": access_token,  # PUT YOUR ACCESS TOKEN HERE
            "v": v,
        }
)