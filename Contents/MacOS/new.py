import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def solar_declination(day_of_year):
    """Calculate the solar declination angle for a given day of the year."""
    return 23.44 * np.sin(np.radians((360 / 365) * (day_of_year - 81)))  # Adjust for March 21st as the Spring Equinox

def daylight_hours(latitude, declination):
    """Calculate the number of daylight hours for a given latitude and solar declination."""
    phi = np.radians(latitude)
    delta = np.radians(declination)
    
    # Compute hour angle
    cos_H = -np.tan(phi) * np.tan(delta)

    # Handle Polar Regions Properly
    lat_abs = np.abs(latitude)
    declination_abs = np.abs(declination)
    
    polar_limit = 90 - lat_abs  # Critical declination for polar conditions
    
    if lat_abs >= 66.5:  
        if declination_abs > polar_limit:  # Sun never sets (24h daylight) or never rises (0h daylight)
            return 24 if np.sign(latitude) == np.sign(declination) else 0  

    # Ensure valid range for arccos
    cos_H = np.clip(cos_H, -1, 1)
    H = np.arccos(cos_H)  # Hour angle in radians
    return (2 * H / np.pi) * 12  # Convert to hours

# Generate latitudes and days of the year
latitudes = np.linspace(-90, 90, 100)
days = np.arange(1, 366)  # Days from 1 to 365 (365 days)

# Calculate the sum of daylight hours for each latitude across the year
total_daylight_hours = []

for latitude in latitudes:
    yearly_daylight = 0
    for day in days:
        declination = solar_declination(day)
        yearly_daylight += daylight_hours(latitude, declination)  # Sum daylight hours for each day
    total_daylight_hours.append(yearly_daylight)

# Print sum of daylight hours for each latitude
for i, latitude in enumerate(latitudes):
    print(f"Latitude {latitude:.1f}°: Total daylight hours throughout the year = {total_daylight_hours[i]:.2f} hours")

# Plot results in 3D
L, D = np.meshgrid(latitudes, days)
daylight = np.array([[daylight_hours(lat, solar_declination(day)) for lat in latitudes] for day in days])

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(L, D, daylight, cmap='viridis')
plt.show()
