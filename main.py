from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from cred import *
from selenium.webdriver.common.keys import Keys
import requests


web_path = f"https://www.messenger.com/t/{threadID}"
driver = webdriver.Chrome()
driver.get(web_path)
sleep(1)

def get_weather():
    city_name = 'Gdańsk'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api}&q={city_name}&days=1&aqi=yes&alerts=no'
    request = requests.get(url)
    data = request.json()

    date = data['forecast']['forecastday'][0]['date']
    max_temp = data['forecast']['forecastday'][0]['day']['maxtemp_c']
    min_temp = data['forecast']['forecastday'][0]['day']['mintemp_c']
    condition = data['forecast']['forecastday'][0]['day']['condition']['text']

    return date, max_temp, min_temp, condition

weather_parameter = get_weather()


def login():
    driver.find_element(By.XPATH, "//button[@title='Allow all cookies' and @type='submit']").click()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(pas)
    driver.find_element(By.ID, "loginbutton").click()


def create_messege(weather_parameter):
    message = f'{weather_parameter}'

    return message

message = create_messege(weather_parameter)

print(message)


def send_messege(message):
    driver.find_element(By.XPATH, "//div[contains(@class, 'xzsf02u')]").send_keys(message)
    driver.find_element(By.XPATH, "//div[contains(@class, 'xzsf02u')]").send_keys(Keys.RETURN)


def main():
    try:
        login()
        sleep(5)
        send_messege(message)
    except Exception as e:
        print(f'Error occurred: {e}')
        sleep(1)

    # Wait for user input before exiting the script
    input("Press Enter to close the browser...")


if __name__ == "__main__":
    main()


