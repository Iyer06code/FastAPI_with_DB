
import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:8000/send-email"
data = {
    "sender": "4mh23cs129a@gmail.com",
    "receiver": "nandishd2005@gmail.com",
    "content": "Test email from antigravity verification"
}
headers = {"Content-Type": "application/json"}

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Error Detail: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
