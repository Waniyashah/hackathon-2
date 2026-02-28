import urllib.request
import json
import urllib.error

url = "http://localhost:8000/api/auth/signin"
data = {"email": "test@test.com", "password": "password"}
json_data = json.dumps(data).encode('utf-8')
headers = {'Content-Type': 'application/json'}

req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')

print(f"Testing URL: {url}")
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Error Response: {e.read().decode()}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
