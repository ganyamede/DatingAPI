import base64
import os

import requests
import json

gmail = 'оксана4300@gmail.com'

r = requests.post(
    url='http://127.0.0.1/api/sign',
    headers={"Content-Type": "application/json"},
    data=json.dumps({'gmail': gmail, 'password': '12345678'})
)

access_token = r.json()['key']['access_token']

#
# url = "http://127.0.0.1/api/update"
# headers = {"Authorization": "Bearer {access_token}".format(access_token=access_token)}
#
# data = {
#     "name": "Вадим",
#     'age': 19,
#     'city': 'Kyiv',
#     'description': 'я ем сало',
#     'sex': 1,
#     'search_sex': 2
# }
#
# img_list =  ['app/storage/img/photo1.jpg','app/storage/img/photo2.jpg']
# files = [('files', open(photo, 'rb')) for photo in img_list]
# response = requests.post(url, headers=headers, data=data)

# print(response.json())

# # Инфа о себе
#
# url = "http://127.0.0.1/api/select"
# headers = {"Authorization": "Bearer {access_token}".format(access_token=access_token)}
#
# request = requests.get(url, headers=headers)
# print(request.json())
#

url = 'http://127.0.0.1/api/search/'
headers = {"Authorization": "Bearer {access_token}".format(access_token=access_token)}
#
# req_get_profile = requests.get(
#     url=url,
#     headers=headers
# ).json()

req_post_like = requests.post(
    url='http://127.0.0.1/api/getLike/',
    headers=headers,
)
print(req_post_like.json())

data = req_post_like.json()

ike = requests.get(
    url='http://127.0.0.1/api/matchAll',
    headers=headers
)
print(ike.json())

# req_post_skip = requests.get(
#     url=url,
#     headers=headers,
#     data = {''}
# )

