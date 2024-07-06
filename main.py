import requests
from datetime import datetime
import os

GENDER = "MALE"
WEIGHT_KG = "84"
HEIGHT_CM = "173.5"
AGE = "24"

app_id = os.environ["APP_ID"]
app_key = os.environ["APP_KEY"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

exercise_text = input("Tell me which exercise you did: ")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoints = os.environ["SHEET_ENDPOİNT"]

headers = {
    "x-app-id": app_id,
    "x-app-key": app_key,
    "x-remote-user-id": 0
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d%m%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["Exercise"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoints, json=sheet_inputs, auth=(username, password))
    print(sheet_response.text)
