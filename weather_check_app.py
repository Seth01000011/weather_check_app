#! python3
# weather_check_app.py - Grabs weather for a location, and returns in format usable
# for home automation weather station
from pathlib import Path
import json, requests, sys

if len(sys.argv) < 2:
    # print("Usage: weather_check_app.py city_name state_code 2_letter_country_code")
    # The above is commented out since I will move to zip-based forecast request
    print("Usage: weather_check_app.py zip_code [optional - 2 digit country]")
    sys.exit()
api_key_file = open(Path.cwd() / "openweather_api_key.txt")
APPID = api_key_file.read()[:-1]
print(APPID)
# location is in format [zip_code] alone or [zip_code],[country_code]
if len(sys.argv) > 2:
    location = ",".join(sys.argv[1:])
else:
    location = sys.argv[1]
# url = "https://api.openweathermap.org/data/2.5/forecast?q=%s&cnt=3&appid=%s" % (
# The above is commented out - it uses city/state/country code request
# I want to use zip code request
# See https://openweathermap.org/forecast5 for api stuffs.
url = f"https://api.openweathermap.org/data/2.5/forecast?zip={location}&appid={APPID}&units=imperial"
# url = raw_url[:-1]  # this strips of the 'carriage return' python automatically adds
#   into the string. Causes auth problems with APPID.
print(url)
response = requests.get(url)

response.raise_for_status()
# uncomment to see raw JSON
print(response.text)
# load json data into python variable
weather_data = json.loads(response.text)
weather_data_to_file = open("weather_forecast.json", "w")
weather_data_to_file.write(response.text)
weather_data_to_file.close()
# print weather description
print("Current weather in %s: " % (location))
# The below format is not valid for how openweather returns calls
# print(w[0]["weather"][0]["main"], "-", w[0]["weather"][0]["description"])
print()
"""
print("Day after tomorrow: ")
print(w[2]["weather"][0]["main"], "-", w[2]["weather"][0]["description"])
"""
