# This file fetches and processes telemetry data.

import requests

def get_location_data(session_key, driver_number, date_start, date_end):
    url = f"https://api.openf1.org/v1/location?session_key={session_key}&driver_number={driver_number}&date>={date_start}&date<{date_end}"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_car_data(session_key, driver_number, date_start, date_end):
    url = f"https://api.openf1.org/v1/car_data?driver_number={driver_number}&session_key={session_key}&date>={date_start}&date<{date_end}"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_lap_data(session_key, driver_number):
    url = f"https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_number}"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")