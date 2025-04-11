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
    browser.add_cookie({"name": "MUSIC_U", "value": "0037D86860490FB512CE1CE0C35845DF6EFA6303818B4708DA15D70DF446B2B8825CF2EA9439ED6DEDC93D8FD2149D14FDE776CA6DF6F10DB731140D06F6769BEC922C67D6EFEBB09C0322EC03EDA50EA7ACFDF59C697BD7BD72CE64635120DE6E8A3B97762684103B5C8E8E2AD06C6CE26DC69BBF06A02B8EFB871A9AC0829D99FC7935265A9EC452A66A989BD232B40FBD108F58291B325E942BFCDEF3BBF55DDCDF1D348CB0EF9D435B227FBB15FCEBDF29FBA5F09087CC0B94F902869C5C76AA98AB9C702F4742824DCF39226FC57FDF0FCFA1BCB2BFA90FF827AF2F41509BB45EE0E19BEEF0D25918F8A7A9309937F69155B8BA5010F608328B31BD084E9E09C6DCB6AB604BD193EB15C6E1F50F17E3B2AA2977B5E6654F61EF6B3348F48114604C529F6B5A204C3DAD3D35CB6F2DE9F184C2668616F68D654C9455E45F8CCC3014AF566ABF123E76D93C8175F6C6"})
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
