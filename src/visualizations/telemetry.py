# This file fetches and processes telemetry data.

import requests

def get_location_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/location?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_car_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/car_data?driver_number={driver_number}&session_key={session_key}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_lap_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
def get_stints_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
        
def get_pit_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/pit?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_race_control_data(session_key, meeting_key):
    url = f"https://api.openf1.org/v1/race_control?session_key={session_key}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
def get_radio_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/team_radio?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
def get_interval_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/intervals?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
def get_position_data(session_key, meeting_key, driver_number):
    url = f"https://api.openf1.org/v1/position?session_key={session_key}&driver_number={driver_number}&meeting_key={meeting_key}"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")