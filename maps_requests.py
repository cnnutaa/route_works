import ssl
import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

base_url = "https://maps.googleapis.com/maps/api/directions/json?"

maps_key = os.environ.get("GOOGLE_MAPS_API_KEY")
token = os.environ["SLACK_API_TOKEN"]

origin = os.environ.get("ORIGIN")
destination = os.environ.get("DESTINATION")

params = {
    "origin": origin,
    "destination": destination,
    "traffic_model": "optimistic",
    "departure_time": int(datetime.now().timestamp()),
    "alternatives": "true",
    "key": maps_key
         }


response = requests.get(base_url, params=params)

routes = response.json()

slack_message = ""

for route in routes['routes']:
    road = route['summary']
    leg = route['legs'][0]
    distance = leg['distance']['text'] if "distance" in leg else ""
    duration = leg['duration']['text'] if "duration" in leg else ""
    duration_in_traffic = leg['duration_in_traffic']['text'] if "duration_in_traffic" in leg else ""
    slack_message += f"{road} - {distance} - {duration} - {duration_in_traffic}\n"


print(response.text)





ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE




client = WebClient(token=token, ssl=ssl_context)

try:
    response = client.chat_postMessage(channel='#can_test', text=slack_message)
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")