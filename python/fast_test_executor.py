#!/usr/bin/env python

from __future__ import unicode_literals
import time
import datetime
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class ChromeWebDriver():

    def __init__(self) -> None:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')

    def get_driver(self):
        return self.driver



def main():
    driver = ChromeWebDriver().get_driver()
    start = datetime.datetime.now()
    driver.get('https://fast.com')
    time.sleep(1)
    driver.execute_script("""
const settings = {
    "minDuration": "5",
    "measureUploadLatency": "true",
    "maxConnections": "8",
    "shouldPersist": "true",
    "showAdvanced": "true",
    "maxDuration": "30",
    "minConnections": "1"
}
Object.keys(settings).forEach(k => localStorage.setItem(k, settings[k]) )
    """)
    driver.get('https://fast.com')

    check_count = 0 
    max_check_count = 120
    speed_indicator_element = None

    while speed_indicator_element is None and check_count < max_check_count:
        try:
            speed_indicator_element = driver.find_element_by_css_selector('#speed-progress-indicator.succeeded')
        except NoSuchElementException as nse:
            check_count += 1
            time.sleep(1)

    end = datetime.datetime.now()

    results = {
        'start': str(start),
        'duration': str(end-start)
    }

    if speed_indicator_element is not None:
        results['status'] = 'success'
        results['speeds'] = {
            'down': float(driver.find_element_by_css_selector('#speed-value').text),
            'up': float(driver.find_element_by_css_selector('#upload-value').text)
        }
        results['data'] = {
            'down': float(driver.find_element_by_css_selector('#down-mb-value').text),
            'up': float(driver.find_element_by_css_selector('#up-mb-value').text),
        }
        results['client'] = {
            'location': driver.find_element_by_css_selector('#user-location').text,
            'ip': driver.find_element_by_css_selector('#user-ip').text,
            'isp': driver.find_element_by_css_selector('#user-isp').text,
        }
    elif check_count >= max_check_count:
        results['status'] = 'error'
        results['message'] = 'Max check count exceeded.'
        driver.save_screenshot('/output_dir/timeout.png')

    print(json.dumps(results))
    driver.quit()

main()