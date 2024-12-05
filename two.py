import requests

def get_temperature_weatherapi(location, api_key):
    try:
        # URL for the current weather in the location
        url = f"http://api.weatherapi.com/v1/current.json?q={location}&key={api_key}"

        # Send a GET request to WeatherAPI
        response = requests.get(url)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            data = response.json()

            # Extract the temperature from the response
            temperature = data['current']['temp_c']

            # Return the temperature
            return f"The temperature in {location} is {temperature}°C."
        else:
            return f"Error: Unable to fetch weather data for {location}. Status code: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
api_key = "fmxMIQ8KrLoMrBVMFUiojQYjZRnuXqUq"  # Replace with your actual WeatherAPI key
location = "London"  # Replace with your desired location
print(get_temperature_weatherapi(location, api_key))

