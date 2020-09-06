import json
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.relativedelta import relativedelta
from login import mashov_login


XPATH_FILE = 'xpath.json'
LOGIN_FILE = 'login.json'
NOT_STARTED = "This XML file does not appear to have any style information associated with it. The document tree is shown below."
timeout = 10

def main():
    with open(XPATH_FILE) as f:
        xpaths = json.load(f)

    today = datetime.today()
    next_date = next_7am(today)
    time_delta = (next_date - datetime.now()).total_seconds()
    print("Sleeping for {} seconds(until {})".format(str(time_delta), next_date))
    time.sleep(time_delta)

    try:
        while True:
            driver = webdriver.Firefox()

            mashov_login(driver, LOGIN_FILE)

            while not is_element_present(driver, By.XPATH, xpaths["CoronaPage"]): pass
            driver.find_element_by_xpath(xpaths["CoronaPage"]).click()

            while not is_element_present(driver, By.XPATH, xpaths["CheckFever"]): pass
            while not try_click(driver.find_element_by_xpath(xpaths["CheckFever"])): pass
            
            while not is_element_present(driver, By.XPATH, xpaths["CheckBidud"]): pass
            while not try_click(driver.find_element_by_xpath(xpaths["CheckBidud"])): pass


            while not is_element_present(driver, By.XPATH, xpaths["CoronaAccept"]): pass
            driver.find_element_by_xpath(xpaths["CoronaAccept"]).click()

            print("-----------------------------\Have fun in class(jk, it's not possible)!\n-----------------------------")
            today = datetime.today()
            next_date = next_7am(today)
            time_delta = (next_date - datetime.now()).total_seconds()
            print("Sleeping for {} seconds(until {})".format(str(time_delta), next_date))
            time.sleep(time_delta)
            driver.close()
    finally:
        for win in driver.window_handles:
            driver.close()


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


def next_7am(dt):
    relative_days = (dt.hour >= 7)
    absolute_kwargs = dict(hour=7, minute=1, second=0, microsecond=0)
    return dt + relativedelta(days=relative_days, **absolute_kwargs)


if __name__ == "__main__":
    main()
