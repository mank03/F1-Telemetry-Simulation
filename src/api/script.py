from urllib.request import urlopen
import json
import pandas as pd  # Import pandas for data handling


response = urlopen('https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315')
data = json.loads(response.read().decode('utf-8'))

# Convert JSON data to a Pandas DataFrame
car_data = pd.DataFrame(data)

# Display the first few rows of the DataFrame
print("First 5 rows of data:")
print(car_data.head())

# Basic exploration of the data
print("\nData Summary:")
print(car_data.info())

# Example analysis: Average speed by gear
if "n_gear" in car_data.columns and "speed" in car_data.columns:
    avg_speed_by_gear = car_data.groupby("n_gear")["speed"].mean()
    print("\nAverage Speed by Gear:")
    print(avg_speed_by_gear)