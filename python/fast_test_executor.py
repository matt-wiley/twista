#!/usr/bin/env python

from __future__ import unicode_literals

import os
from os.path import exists

import sys

import time
import datetime
import random
import json

from selenium import webdriver
import selenium
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

    check_count = 0 
    max_check_count = 120
    speed_value_element = None

    while speed_value_element is None and check_count < max_check_count:
        try:
            speed_value_element = driver.find_element_by_css_selector('#speed-value.succeeded')
        except NoSuchElementException as nse:
            check_count += 1
            time.sleep(0.2)

    end = datetime.datetime.now()

    results = {
        'start': str(start),
        'duration': str(end-start)
    }

    if speed_value_element is not None:
        results['status'] = 'success'
        results['speeds'] = {
            'down': int(speed_value_element.text)
        }
        print(json.dumps(results, indent=4))
    elif check_count >= max_check_count:
        results['status'] = 'error'
        results['message'] = 'Max check count exceeded.'
        driver.save_screenshot('/output_dir/timeout.png')

    driver.quit()

main()