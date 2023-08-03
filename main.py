from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from credentials import *
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import requests

web_path = f"https://www.messenger.com/t/{threadID}"
driver = webdriver.Chrome()
driver.get(web_path)
sleep(1)

def get_day_name():
    dt = datetime.now()
    day_name = dt.strftime('%A')
    return day_name

day_name = get_day_name()

def get_weather():
    city_name = 'Gdańsk'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api}&q={city_name}&days=1&aqi=yes&alerts=no'
    request = requests.get(url)
    data = request.json()
    # date = data['forecast']['forecastday'][0]['date']
    max_temp = data['forecast']['forecastday'][0]['day']['maxtemp_c']
    min_temp = data['forecast']['forecastday'][0]['day']['mintemp_c']
    condition = data['forecast']['forecastday'][0]['day']['condition']['text']

    return max_temp, min_temp, condition

max_temp, min_temp, condition = get_weather()

def login():
    driver.find_element(By.XPATH, "//button[@title='Allow all cookies' and @type='submit']").click()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(pas)
    driver.find_element(By.ID, "loginbutton").click()


def create_messege(max_temp, min_temp, condition, day_name):
    message = f'{max_temp}, {min_temp}, {condition}, {day_name}'

    return message

message = create_messege(max_temp, min_temp, condition, day_name)

print(message)


def send_messege(message):
    send = driver.find_element(By.XPATH, "//div[contains(@class, 'xzsf02u x1a2a7pz x1n2onr6')]")
    send.send_keys(message)
    enter = driver.find_element(By.XPATH, "//div[contains(@class, 'xzsf02u x1a2a7pz x1n2onr6')]")
    enter.send_keys(Keys.RETURN)
# xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x1iyjqo2 x1gh3ibb xisnujt xeuugli x1odjw0f notranslate

def main():
    try:
        login()
        sleep(5)
        send_messege(message)
    except Exception as e:
        print(f'Error occurred: {e}')
    # Wait for user input before exiting the script
    input("Press Enter to close the browser...")


if __name__ == "__main__":
    main()
