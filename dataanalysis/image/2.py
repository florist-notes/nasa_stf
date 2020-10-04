import requests

api_key = 'acc_c300ad844f148f7'
api_secret = 'efef0345caf30ccb8588b17885b15bb7'
image_url = 'https://upload.wikimedia.org/wikipedia/commons/a/a6/The_Rim_Fire_in_the_Stanislaus_National_Forest_near_in_California_began_on_Aug._17%2C_2013-0004.jpg'

response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
    auth=(api_key, api_secret))

print(response.json())
