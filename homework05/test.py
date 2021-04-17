from vkapi.config import VK_CONFIG
import requests
import vkapi.friends as fr

# domain = VK_CONFIG["domain"]
# access_token = VK_CONFIG["access_token"]
# v = VK_CONFIG["version"]
# # user_id = '459560428'
# # fields = 'sex'
# source_uid = '459560428'
# target_uids = ['817934', '437397158']#['4744933']
# order = ""
# count = ""
# offset = 0

# # query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
# query = f"{domain}/friends.getMutual?\
#             access_token={access_token}&\
#             source_uid={source_uid}&\
#             target_uids={'' if (target_uids == None or target_uids == []) else ','.join(target_uids)}&\
#             order={order}&\
#             count={count}&\
#             offset={offset}&\
#             v={v}".replace(" ", "")
# print(query)
# response = requests.get(query)
# print(response.json())

friends_response = fr.get_friends(user_id=817934, fields=["nickname"])
active_users = [user["id"] for user in friends_response.items if not user.get("deactivated") and not user.get("is_closed")]
print(len(active_users))

mutual_friends = fr.get_mutual(source_uid=817934, target_uids=active_users)

print(mutual_friends)