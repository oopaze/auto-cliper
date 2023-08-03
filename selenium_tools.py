import os
import time

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By

WAIT_DURATION = 20
UPLOAD_WAIT_LIMIT = 80
DEFAULT_PODFLOW_HASHTAGS = "\n\n#flow #podcast #podpah #clips #cortes #podflowclips"
DEFAULT_SCIENCE_HASHTAGS = "\n\n#flow #podcast #podpah #sacani #ciencia #science #clips #cortes #scienceclips"


def get_webdriver(is_podflow=False):
    profile = "Profile 2" if is_podflow else "Profile 3"

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=profiles")
    options.add_argument(f"profile-directory={profile}")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(WAIT_DURATION)

    return driver


def open_tiktok(driver: webdriver.Chrome):
    driver.get("https://www.tiktok.com/creator-center/upload")


def attache_file_to_the_form(driver: webdriver.Chrome, filepath):
    iframe_xpath = "/html/body/div/div[2]/div[2]/div/div/iframe"
    iframe = driver.find_element(By.XPATH, iframe_xpath)
    driver.switch_to.frame(iframe)

    upload_input_xpath = "/html/body/div[1]/div/div/div/div/div/div/div/input"
    file_field = driver.find_element(By.XPATH, upload_input_xpath)
    file_field.send_keys(filepath)


def configure_video(driver: webdriver.Chrome, is_podflow=False, extra_hashtags=""):
    video_preview_xpath = "/html/body/div[1]/div/div/div/div[2]/div[1]/div"
    driver.find_element(By.XPATH, video_preview_xpath)

    title_input_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div"
    title_input_xpath += "[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/span/span"
    title_input = driver.find_element(By.XPATH, title_input_xpath)
    title_input.send_keys(DEFAULT_PODFLOW_HASHTAGS if is_podflow else DEFAULT_SCIENCE_HASHTAGS)
    title_input.send_keys(extra_hashtags)


def publish_video(driver: webdriver.Chrome):
    publish_button_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[8]/div[2]/button"
    publish_button = driver.find_element(By.XPATH, publish_button_xpath)
    publish_button.click()

    driver.implicitly_wait(UPLOAD_WAIT_LIMIT)

    charge_other_video_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[9]/div/div[2]/div[1]"
    driver.find_element(By.XPATH, charge_other_video_xpath)

    driver.implicitly_wait(WAIT_DURATION)
    driver.switch_to.default_content()


def upload_videos(clips, account, start_flag=None, stop_flag=None, extra_hashtags=""):
    is_podflow = account == "podflow"
    driver = get_webdriver(is_podflow=is_podflow)

    def upload():
        open_tiktok(driver)
        attache_file_to_the_form(driver, os.path.abspath(clip))
        configure_video(driver, is_podflow, extra_hashtags)
        publish_video(driver)
        time.sleep(10)

    for idx, clip in enumerate(clips):
        if stop_flag is not None:
            if stop_flag <= idx:
                driver.quit()
                return

        if start_flag is not None:
            if start_flag > idx:
                continue

        try:

            try:
                upload()
            except UnexpectedAlertPresentException:
                driver.quit()
                driver = get_webdriver(is_podflow=is_podflow)
                upload()

        except Exception as e:
            print(e)
            driver.quit()
