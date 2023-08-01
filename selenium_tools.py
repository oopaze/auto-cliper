from selenium import webdriver


def get_webdriver(is_podflow=False):
    profile = "Profile 2" if is_podflow else "Profile 3"

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=profiles")
    options.add_argument(f"profile-directory={profile}")
    driver = webdriver.Chrome(options=options)

    driver.get('http://www.tiktok.com/')

    return driver


if __name__ == "__main__":
    get_webdriver(True)
