from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time
import json


MASHOV_URL = 'https://web.mashov.info/students/login'
XPATH_FILE = 'xpath.json'


def is_element_present(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


def get_creds(login_file):
    if not os.path.exists(login_file):
        raise ValueError("Login file doesn't exist")

    with open(login_file) as json_file:
        try:
            data = json.load(json_file)
            if not all(key in data for key in ["Username", "Password", "SchoolId"]):
                raise ValueError("Not all json values exists")
        except json.decoder.JSONDecodeError:
            raise ValueError("Login json file is not valid")
    return data


def mashov_login(driver, login_file):
    global MASHOV_URL

    creds = get_creds(login_file)
    username = creds['Username']
    password = creds['Password']
    school_id = creds['SchoolId']

    driver.get(MASHOV_URL)
    
    with open(XPATH_FILE) as f:
        xpaths = json.load(f)


    while not is_element_present(driver, By.XPATH, xpaths["SchoolIdInput"]): pass

    # get school
    input_element = driver.find_element_by_xpath(xpaths["SchoolIdInput"])
    input_element.send_keys(school_id)
    driver.find_elements_by_xpath(xpaths["SchoolIdBoxes"])[0].click()

    # username
    driver.find_element_by_xpath(xpaths["UsernameInput"]).send_keys(username)
    # password
    driver.find_element_by_xpath(xpaths["PasswordInput"]).send_keys(password)
    # login
    driver.find_element_by_xpath(xpaths["LoginButton"]).click()
