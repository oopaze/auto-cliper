import os

from selenium import webdriver
from selenium.webdriver.common.by import By

WAIT_DURATION = 20
UPLOAD_WAIT_LIMIT = 80
DEFAULT_PODFLOW_HASHTAGS = "\n\n#flow #podpah #clips #cortes #podflowclips #viral #fy"
DEFAULT_SCIENCE_HASHTAGS = "\n\n#flow #podpah #sacani #ciencia #science #clips #cortes #scienceclips #viral #fy"


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


def configure_video(driver: webdriver.Chrome, is_podflow=False):
    video_preview_xpath = "/html/body/div[1]/div/div/div/div[2]/div[1]/div"
    driver.find_element(By.XPATH, video_preview_xpath)

    title_input_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div"
    title_input_xpath += "[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/span/span"
    title_input = driver.find_element(By.XPATH, title_input_xpath)
    title_input.send_keys(DEFAULT_PODFLOW_HASHTAGS if is_podflow else DEFAULT_SCIENCE_HASHTAGS)

    second_thumb_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/img[2]"
    second_thumb = driver.find_element(By.XPATH, second_thumb_xpath)
    second_thumb.click()


def publish_video(driver: webdriver.Chrome):
    publish_button_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[8]/div[2]/button"
    publish_button = driver.find_element(By.XPATH, publish_button_xpath)
    publish_button.click()

    driver.implicitly_wait(UPLOAD_WAIT_LIMIT)

    charge_other_video_xpath = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[9]/div/div[2]/div[1]"
    driver.find_element(By.XPATH, charge_other_video_xpath)

    driver.implicitly_wait(WAIT_DURATION)


def upload_videos(clips_path, account):
    clips = os.listdir(clips_path)

    is_podflow = account == "podflow"

    driver = get_webdriver(is_podflow=is_podflow)

    for clip in clips:
        open_tiktok(driver)
        attache_file_to_the_form(driver, clip)
        configure_video(driver, is_podflow)
        publish_video(driver)
