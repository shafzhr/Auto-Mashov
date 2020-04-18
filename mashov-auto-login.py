from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time
import json

login_file = 'login.json'
mashov_url = 'https://web.mashov.info/students/login'
driver_path = r"C:\Users\Ophir\Desktop\auto-mashov"

username = ''
password = ''
school_id = ''


def is_element_present(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


def get_username_and_password():
    global login_file
    global username
    global password
    global school_id

    if not os.path.exists(login_file):
        return False

    with open('login.json') as json_file:
        try:
            data = json.load(json_file)

            username = data['Username']
            password = data['Password']
            school_id = data['School id']

        except json.decoder.JSONDecodeError:
            print("invalid file")
            return False
        return True


def mashov_login():
    global driver_path
    global mashov_url
    global username
    global password
    global school_id

    driver = webdriver.Firefox(driver_path)

    driver.get(mashov_url)

    while not is_element_present(driver, By.XPATH, '//*[@id="mat-input-2"]'):
        pass

    # get school
    input_element = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
    input_element.send_keys(school_id)
    driver.find_elements_by_xpath("//mat-option")[0].click()

    # id
    driver.find_element_by_xpath('//*[@id="mat-input-0"]').send_keys(username)
    # password
    driver.find_element_by_xpath('//*[@id="mat-input-1"]').send_keys(password)
    # login
    driver.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/div/button').click()

    while not is_element_present(driver, By.XPATH, '//*[@id="mainView"]/mat-sidenav-content/mshv-student-dashboard/mat-card/mat-card-content/div[2]/mat-card[2]'):
        pass


    # online class

    while True:
        try:
            driver.find_element_by_xpath('//*[@id="mainView"]/mat-sidenav-content/mshv-student-dashboard/mat-card/mat-card-content/div[2]/mat-card[2]').click()
            break
        except ElementClickInterceptedException:
            continue


if __name__ == '__main__':
    valid = get_username_and_password()
    if valid:
        mashov_login()
