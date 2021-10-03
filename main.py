import os.path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver_url = os.path.abspath('geckodriver')
url = 'https://store.steampowered.com/'
load_dotenv('config.env')


class SteamBot:

    def __init__(self) -> None:
        self._options = webdriver.FirefoxOptions()
        self._driver = webdriver.Firefox(executable_path=fr'{driver_url}', options=self._options)
        self._username = os.environ.get('USERNAME_STEAM')
        self._password = os.environ.get('PASSWORD_STEAM')

    def close_browser(self) -> None:
        self._driver.close()
        self._driver.quit()

    def xpath_exist(self, xpath):
        try:
            self._driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    def login(self):
        driver = self._driver
        driver.get(url)
        driver.implicitly_wait(5)

        driver.find_element_by_class_name('global_action_link').click()
        driver.implicitly_wait(5)

        driver.find_element_by_xpath('//input[@id="input_username"]').send_keys(self._username)
        driver.find_element_by_xpath('//input[@id="input_password"]').send_keys(self._password)
        driver.implicitly_wait(3)

        driver.find_element_by_xpath('//button[@type="submit"]').click()
        driver.implicitly_wait(5)

        if self.xpath_exist('//input[@id="twofactorcode_entry"]'):
            code = input('Please input 2-factor code: ')
            driver.find_element_by_xpath('//input[@id="twofactorcode_entry"]').send_keys(code)
            driver.implicitly_wait(2)
            driver.find_element_by_id('login_twofactorauth_buttonset_entercode').find_element_by_class_name('leftbtn').click()
            driver.implicitly_wait(5)

        driver.find_element_by_class_name('user_avatar').click()


if __name__ == '__main__':
    bot = SteamBot()
    bot.login()
    bot.close_browser()
