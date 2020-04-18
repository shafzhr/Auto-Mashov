import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


def is_element_present(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False

def try_click(element):
    try:
        element.click()
        return True
    except WebDriverException:
        return False

with open("xpath.json") as f:
    xpaths = json.load(f)

try:
    driver = webdriver.Firefox()
    driver.get("https://web.mashov.info/students/#!/login/")

    input("Login and press enter")

    while not is_element_present(driver, By.XPATH, xpaths["ClassesPage"]): pass
    driver.find_element_by_xpath(xpaths["ClassesPage"]).click()

    while not is_element_present(driver, By.XPATH, xpaths["ClassesList"]): pass
    classes = driver.find_element_by_xpath(xpaths["ClassesList"]).find_elements_by_xpath("//a[@href]")
    
    times = {}
    for c in classes:
        span = c.find_element_by_xpath(xpaths["ClassStartTime"])
        time = span.text.split(':', 1)[1][1:]
        time = datetime.strptime(time, "%d/%m/%Y %H:%M")
        times[time] = c

    sorted_classes_times = sorted(times.keys())
    closest = times[sorted_classes_times[0]]
    while not try_click(closest): pass
    

    input("Press enter in order to close")
finally:
    driver.close()