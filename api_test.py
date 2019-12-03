import requests
import json

payload = {'img_url': 'https://www.cbronline.com/wp-content/uploads/2016/06/what-is-URL-770x503.jpg', 'style': 'Shinkai'}
url = "http://localhost:5000/tf"

headers = {
    'Content-Type': "application/json",
    }

response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

print(response.text)