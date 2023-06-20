from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from headers import HEADERS_LIST
from selenium.webdriver.support.wait import WebDriverWait
from sendmail import send_noti_email

def get_headers():
    headers = {'User-Agent': random.choice(HEADERS_LIST)}
    return headers

def get_webdriver():
    options = Options()
    options.add_argument(f'user-agent={get_headers()}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    return driver



# the function opens "https://bassliner.org/de/fahrten/fusion-festival-2023-3" with selenium and checks if the tickets are available
# if the tickets are available, the function sends an email to the user
# the function is called by the main function
def fusionchecker():
    driver = get_webdriver()
    driver.get("https://bassliner.org/de/fahrten/fusion-festival-2023-3")
    WebDriverWait(driver, timeout=30).until(lambda driver: driver.execute_script(
        'return document.readyState') == 'complete')
    # scroll down a bit
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    # get two journey sections "bsl-journey"
    journeys = driver.find_elements(By.CLASS_NAME,
                        'bsl-journey',
    )
    # close the first one
    journeys[0].find_element(By.CLASS_NAME,
                             "icon-close",
    ).click()
    time.sleep(1)
    # now click on the input field of the second one:
    journeys[1].find_element(By.ID,
                             "journey-stations",
    ).click()
    time.sleep(5)
    journeys[1].find_element(By.ID,
                             "vs1__option-0").click()
    time.sleep(2)


    # choose the monday
    # now find elements with class "bsl-journey__day". click on the one that contains "Mon" substring
    days = driver.find_elements(By.CLASS_NAME,
                        'bsl-journey__day',
    )
    for day in days:
        if "Di." in day.text:
            day.click()
            time.sleep(2)
            break
    WebDriverWait(driver, timeout=30).until(lambda driver: driver.execute_script(
        'return document.readyState') == 'complete')
    # now get the tickets by iterating over divs inside the div with class "bsl-journey__tours-body"
    tours_body = driver.find_element(By.CLASS_NAME,
                        'bsl-journey__tours-body',
    )
    # get tours by iterating over divs inside the div with classname that starts with "collapse returningJourney-tour-":
    tours = tours_body.find_elements(By.XPATH,
                        '//div[starts-with(@class, "collapse show returningJourney-tour-")]',
    )

    # check if div's style attribute contains "display: none", if not print the text of the div
    available_tickets = {}
    for tour in tours:
        if "display: none" not in tour.get_attribute("style"):
            # check if the text contains "ausgebucht", if not send an email to the user
            if "ausgebucht" not in tour.text:
                key = tour.find_element(By.CLASS_NAME,"bsl-tour__col-time").text
                try:
                    value = tour.find_element(By.CLASS_NAME,"bsl-tour__col-seats").find_elements(By.TAG_NAME,"span")[-1].text
                except:
                    value = "some available"

                available_tickets[key] = value
    
    return available_tickets
        
