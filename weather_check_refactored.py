#! python3
# weather_check_app.py - Grabs weather for a location, and returns in format usable
# for home automation weather station
from pathlib import Path
import json
import requests
import sys
from datetime import datetime, timezone, timedelta


def fix_time(time_stamp):
    # datetime.fromtimestamp(1654819200, timezone.est)
    #
    utc_time = datetime.fromtimestamp(time_stamp)
    delta = timedelta(hours=5)
    est_time = utc_time - delta
    return est_time


class WeatherRequest:
    def __init__(self, zip_code: str, api_key_file: str, json_data: dict = None):
        """Use input zipcode to make API request from openweather.org -
        WeatherRequest(zip)."""
        self.zip_code = zip_code
        self.api_key_file = open(Path.cwd() / api_key_file)
        self._APPID = self.api_key_file.read()[:-1]  # The [:-1] trims off the newline
        self.json_data = json_data
        if not self.json_data:
            self.json_data = self.get_weather()

    def get_weather(self):
        # see https://openweathermap.org/forecast5 for formatting of url string
        # The following URL and format retrieves a 5 day, 3 hour-interval forecast
        url = f"https://api.openweathermap.org/data/2.5/forecast?zip={self.zip_code}&appid={self._APPID}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()
        print(response.text)
        weather_data = json.loads(response.text)
        return weather_data

    def interpret_json(self, path="parsed_json.txt"):
        with open(path, "a") as important_data_out:
            for x in range(len(self.json_data["list"])):
                # the following if statement only pulls out the weather conditions for noon of each day.
                # remove the "if" statement and un-indent the block within to get all 3-hour intervals
                # for the entire 5 day forecast.
                # Likely will want all of the data points to control plant watering
                if fix_time(self.json_data["list"][x]["dt"]).hour == 12:
                    important_data_out.write(
                        f"""
On the date: {str(fix_time(self.json_data["list"][x]["dt"]))}
The temperature will be: {str(self.json_data["list"][x]["main"]["temp"])}
The conditions will be: {str(self.json_data["list"][x]["weather"][0]["main"])}
                        """
                    )
                else:
                    pass


"""
with open("weather.json", "r") as file:
    weather = WeatherRequest("12345", "path", json.loads(file.read()))
"""
