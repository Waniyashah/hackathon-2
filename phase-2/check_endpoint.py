import urllib.request
import json
import urllib.error

url = "http://localhost:8000/api/auth/signin"
data = {"email": "test@test.com", "password": "password123"}
json_data = json.dumps(data).encode('utf-8')

req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'}, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode())
except urllib.error.URLError as e:
    print(f"URLError: {e.reason}")
