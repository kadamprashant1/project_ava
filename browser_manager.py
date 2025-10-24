# browser_manager.py
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

class BrowserManager:
    def __init__(self, config):
        self.config = config
        self.driver = self._create_driver()

    def _create_driver(self):
        options = Options()
        if self.config.getboolean('HEADLESS'):
            options.add_argument('--headless')
        options.add_argument(f"user-agent={self.config.get('USER_AGENT')}")
        
        webdriver_path = self.config.get('WEBDRIVER_PATH')
        if webdriver_path:
            service = Service(webdriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            # Assumes chromedriver is in PATH if not specified
            driver = webdriver.Chrome(options=options)
            
        implicit_wait = self.config.getint('IMPLICIT_WAIT')
        page_load_timeout = self.config.getint('PAGE_LOAD_TIMEOUT')
        
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        return driver

    def go_to_url(self, url):
        logging.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def get_page_source(self):
        return self.driver.page_source

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)
        logging.info(f"Screenshot saved to {filename}")

    def find_element(self, by, value):
        try:
            return WebDriverWait(self.driver, self.config.getint('IMPLICIT_WAIT')).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logging.error(f"Element with {by}={value} not found within timeout.")
            return None

    def click_element(self, selector_type, selector_value):
        element = self.find_element(selector_type, selector_value)
        if element:
            try:
                element.click()
                logging.info(f"Clicked element with {selector_type}={selector_value}")
            except StaleElementReferenceException:
                logging.warning("StaleElementReferenceException caught. Retrying find and click.")
                element = self.find_element(selector_type, selector_value)
                if element:
                    element.click()
            except Exception as e:
                logging.error(f"Could not click element: {e}")


    def type_text(self, selector_type, selector_value, text):
        element = self.find_element(selector_type, selector_value)
        if element:
            element.clear()
            element.send_keys(text)
            logging.info(f"Typed '{text}' into element with {selector_type}={selector_value}")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info("Scrolled to bottom of the page.")

    def execute_script(self, js):
        return self.driver.execute_script(js)

    def close_browser(self):
        logging.info("Closing browser.")
        self.driver.quit()
