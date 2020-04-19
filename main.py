from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import json
import os
from login import mashov_login


XPATH_FILE = 'xpath.json'
LOGIN_FILE = 'login.json'

def main():
    with open(XPATH_FILE) as f:
        xpaths = json.load(f)

    try:
        driver = webdriver.Firefox()

        mashov_login(driver, LOGIN_FILE)

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
        
        previous_window = driver.window_handles[0]
        while not try_click(closest): pass

        while len(driver.window_handles) < 2: pass
        window_after = previous_window
        for win in driver.window_handles:
            if win != previous_window:
                window_after = win
                break
        driver.switch_to.window(window_after)

        while not is_element_present(driver, By.XPATH, xpaths["OnlyAudio"]): pass
        driver.find_element_by_xpath(xpaths["OnlyAudio"]).click()

        print("-----------------------------\nConnected to a class\n-----------------------------")
        
        input("Press enter to close")
    finally:
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




if __name__ == "__main__":
    main()