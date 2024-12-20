import requests
import datetime

URL = "http://localhost:8080"

def test_root():
    response = requests.get(URL)
    print(type(response))
    print(response.json())
    assert response.status_code == 200


def test_create_user():
    payload = {
            "email": "sudheer@gmail.com",
            "password": "sudheer@123"
        }
    response = requests.post(URL+"/user", json=payload)
    response_payload = response.json()
    assert response.status_code == 200
    assert response_payload['id'] != None
    assert response_payload['email'] == payload['email']
    # assert response_payload['created_at'] == datetime.datetime.now()
    assert response_payload['posts'] == []