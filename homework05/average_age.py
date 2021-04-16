from vkapi.config import VK_CONFIG
import requests

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = '459560428'
fields = 'sex'

query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
print(query)
response = requests.get(query)
print(response.json())