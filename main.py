import requests
from datetime import datetime
import os

GENDER = input("What is your gender (m/f)? ")
WEIGHT_KG = input("What is your weight, in kg? ")
HEIGHT_CM = input("What is your height, in cm? ")
AGE = input("What is your age, in years? ")

# APP_ID = os.getenv("YOUR_APP_ID")

# API_KEY = os.environ['YOUR_API_KEY']
APP_ID = "694db304"
print(APP_ID)
API_KEY = "9938ea2a5061eddc569598dba7609ebe"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/f1b34fdbaa5836c601807f88cd7639fb/myWorkouts/workouts"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    #No Auth
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)


    #Basic Auth
    # sheet_response = requests.post(
    #     sheet_endpoint,
    #     json=sheet_inputs,
    #     auth=(
    #         os.environ["USERNAME"],
    #         os.environ["PASSWORD"],
    #     )
    # )

    #Bearer Token
    bearer_headers = {
    "Authorization": f"Bearer secrettoken"
    }
    sheet_response = requests.post(
        sheet_endpoint, 
        json=sheet_inputs, 
        headers=bearer_headers
    )

    print(sheet_response.text)
