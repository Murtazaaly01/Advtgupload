from bot import Config
from selenium import webdriver

async def chrome_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.binary_location = Config.GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=Config.CHROMEDRIVER_PATH, chrome_options=option)
    return driver