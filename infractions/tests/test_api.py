import requests
import json
import datetime as dt

now = dt.datetime.now()
now_json = now.strftime("%Y-%m-%dT%H:%M:%SZ")

url = "http://127.0.0.1:8000/api/infracciones"
headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}
data = {
    "vehiculo_id": "cck-312",
    "timestamp": now_json,
    "comentarios": "Test Multa 2 usando AUTH"
}

data_json = json.dumps(data)

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    try:
        response_data = response.json()
        print(response_data)
    except requests.exceptions.JSONDecodeError:
        print("Response was not JSON, raw response:", response.text)
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response content:", response.text)
