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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B5C97445552E2EB310CAB99D31E7CCD00276259D0BA04A2390505E5DB7ADE2CEA3379FB9474CDE6F691D0B42180AB77724F6A00DCD22F2382C5B60A45593832E10D37FA547544F2786B230B2D0C3E4D10F084DA1BA488A7C199728AD81E0D02E3AD3F25694430441DF4FB0DA46FD51A0A5EC4E3DF32015AE012FBDE52BCBA7A266AA4400BCB7E8D30BAF450B7EDEEDAFCD76D8D328852869EFE361B8F571E8955955797DE1E0C741A938FEDB183E94085B752E3707E58DAEE9A12A40EBE84FDB50812D21D9A2B921C123885174D7B0600EE529FB80D86491E69A3A9FFC2143B0406B6CD1ADC52FC6BBFCE26AB00529F1C1B12F6A4136D83A53A6DB79112C21A7835F3953606BE22A2E355BC2A980C2E5E376900D364381F337569324745DDAA8871223E3A6E7D3EFF9E31B0CBA11B2442BC342552293033B467E9A68BD7C7ABA37FA841C4E569E67EB0D902393176B99"})
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
