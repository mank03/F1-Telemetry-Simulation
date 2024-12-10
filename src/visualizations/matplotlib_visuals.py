import matplotlib.pyplot as plt
import pandas as pd  # Make sure this line is included

def plot_speed_vs_gear(car_data):
    plt.scatter(car_data["n_gear"], car_data["speed"], c="blue", label="Speed vs Gear")
    plt.xlabel("Gear")
    plt.ylabel("Speed (km/h)")
    plt.title("Speed vs Gear Plot")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_throttle_over_time(car_data):
    # Convert 'date' from string to datetime and handle the timezone properly
    car_data['date'] = pd.to_datetime(car_data['date'], format='ISO8601', errors='coerce')

    # Ensure all timestamps are in the same timezone (UTC)
    car_data['date'] = car_data['date'].dt.tz_convert('UTC')

    # Set the known start of the race timestamp (ensure it's in UTC)
    race_start_time = pd.to_datetime("2023-09-15T13:00:46.362000+00:00")

    # Filter data for the first 1 minute of the race
    one_minute_data = car_data[car_data['date'] <= (race_start_time + pd.Timedelta(minutes=1))]


    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(one_minute_data['date'], one_minute_data['brake'], label='Brake (%)', color='b')
    
    plt.title('Brake Over Time (First Minute)')
    plt.xlabel('Time')
    plt.ylabel('Brake (%)')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate time labels for readability
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.legend()
    plt.show()
