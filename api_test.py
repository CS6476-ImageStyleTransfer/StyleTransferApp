import base64
import requests
import json

with open("images/DSCF0316_l.JPG", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())


payload = {'image': my_string.decode('ascii'), 'style': 'Shinkai'}
url = "http://localhost:5000/tf"

headers = {
    'Content-Type': "application/json",
    }

response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

print(response.text)