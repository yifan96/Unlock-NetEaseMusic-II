# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008962F92E81C8029D9C5BF31DE5125D7F69987B112965B98EA3F57215AE6E68AFB9A4606C0A893FA6078582244B84150A2BDDBA80CC80ADE421B505723DC0150B4AA05FC63E567D055A55BBC07305E4A288138F5FDE9EC4C563F697060EE83C2E6137947662020C8D682F52072C26A894714283C0C9626A7132C094EBD68A4F26017DA6A018CA59B5B908340FB03C8758908362F07132F2E9E3B5A6892AA715FFE1C9A517D8E484948A6EF98D70967EA3E28379E4AEA3938582C29DF9B8AD234FC92C1C8F0FC8F627AC103BFE23A3C60A2B347741AD80D9A527744BB225EC44F4C9E9391B11B1FA30DBA7A93C5BD117A9FAF7029A0E6B212B4A439456B9CEEF2625F060D1252A584D9BAEB7202CC9E557E8E64930E2C05E59E10F23B90B37FD401CDAC1DEE48CB02DF848D60224186547ACB1620E2EE948EDF47C64DDEDA2BE4B40A138AE38BD564078E3275DE5342819"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
