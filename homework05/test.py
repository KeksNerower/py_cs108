from vkapi.config import VK_CONFIG
import requests


domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
# user_id = '459560428'
# fields = 'sex'
source_uid = '459560428'
target_uid = '248008'
target_uids = []#['4744933']
order = ""
count = ""
offset = ""

# query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
query = f"{domain}/friends.getMutual?\
            access_token={access_token}&\
            source_uid={source_uid}&\
            target_uid={target_uid}&\
            target_uids={'' if (target_uids == None or target_uids == []) else ','.join(target_uids)}&\
            order={order}&\
            count={count}&\
            offset={offset}&\
            v={v}".replace(" ", "")
print(query)
response = requests.get(query)
print(response.json())