from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from credentials import *
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import requests
import openai
import unicodedata

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
    rain_chance = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']

    return max_temp, min_temp, condition, rain_chance

max_temp, min_temp, condition , rain_chance = get_weather()

def chatgpt_api():
    openai.api_key = openai_api

    prompt = f'your character traits is funny, nice, full of positive energy. Your taks will be to generate funny, positive with emoji morning welcome message including paraments like temperature=from {max_temp}°C to {min_temp}°C, weather description={condition}, chanse of rain={rain_chance}, name of the week={day_name}. At the end of a messege give me short fun fact. You will reply only with a welcome message that includes the paraments I mention above and end your message at the end of fun fact and dont write anything else. Use emojis only supported by unicode'

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    gpt_answer = completion.choices[0].message.content

    return gpt_answer

gpt_answer = chatgpt_api()

def login():
    driver.find_element(By.XPATH, "//button[@title='Allow all cookies' and @type='submit']").click()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(pas)
    driver.find_element(By.ID, "loginbutton").click()

def convert_messege(text):
    normalized_text = unicodedata.normalize('NFC', text)
    char_bmp = ''.join(char for char in normalized_text if ord(char) <= 0xFFFF)
    return char_bmp

message = convert_messege(gpt_answer)

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
        sleep(1)
        driver.close()
    except Exception as e:
        print(f'Error occurred: {e}')

if __name__ == "__main__":
    main()
