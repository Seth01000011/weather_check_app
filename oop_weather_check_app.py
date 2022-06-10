#! python3
# weather_check_app.py - Grabs weather for a location, and returns in format usable
# for home automation weather station
from pathlib import Path
import json, requests, sys
from datetime import datetime, timezone, timedelta


class WeatherRequest:
    def __init__(self, zip_code, api_key_file):
        """Use input zipcode to make API request from openweather.org -
        WeatherRequest(zip)."""
        self.zip_code = zip_code
        self.api_key_file = open(Path.cwd() / api_key_file)
        self._APPID = self.api_key_file.read()[:-1]  # The [:-1] trims off the newline
        # char due to reading from the text file

    def get_weather(self):
        # see https://openweathermap.org/forecast5 for formatting of url string
        # The following URL and format retrieves a 5 day, 3 hour-interval forecast
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?zip={self.zip_code}&appid={self._APPID}&units=imperial"
        response = requests.get(self.url)
        response.raise_for_status()
        print(response.text)
        # Load json data into python variable, save it to file
        weather_data = json.loads(response.text)
        weather_data_to_file = open("weather_forecast.json", "a")
        weather_data_to_file.write(response.text)
        weather_data_to_file.close()
        # print weather description
        return weather_data

    def interpret_json(self):
        raw_data = open("weather_forecast.json", "r")
        data = json.loads(raw_data.read())
        important_data_out = open("parsed_json.txt", "a")
        for x in range(len(data)):
            important_data_out.write("On the date: ")
            important_data_out.write(str(self.fix_time(data["list"][x]["dt"])))
            important_data_out.write("\n")
            important_data_out.write("The temperature will be: ")
            important_data_out.write(str(data["list"][x]["main"]["temp"]))
            important_data_out.write("\n")
            important_data_out.write("The conditions will be: ")
            important_data_out.write(str(data["list"][x]["weather"][0]["main"]))
            important_data_out.write("\n")
        important_data_out.close()

    def fix_time(self, time_stamp):
        # datetime.fromtimestamp(1654819200, timezone.est)
        #
        utc_time = datetime.fromtimestamp(time_stamp)
        delta = timedelta(hours=5)
        est_time = utc_time - delta
        return est_time
