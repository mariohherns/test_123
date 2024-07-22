import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from utils.jira_integration import log_defect_to_jira

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestLogin:
    @pytest.fixture()
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # Implicit wait for all elements
        yield driver
        driver.quit()

    def test_page_title(self, driver):
        logger.info("Navigating to the web form page.")
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")

        logger.info("Checking page title.")
        title = driver.title

        logger.info(f"Page title is: {title}")
        try:
            assert title == "Login Page", "Page title does not match"
        except AssertionError as e:
            log_defect_to_jira("Login Page Title Mismatch", str(e))
            raise


    def test_form_submission(self, driver):
        logger.info("Navigating to the web form page.")
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")

        logger.info("Locating and filling in the text box.")
        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-text"))
        )
        text_box.send_keys("Selenium")
        assert text_box.get_attribute('value') == "Selenium", "Text box not filled correctly"

        logger.info("Locating and filling in the password box.")
        password_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-password"))
        )
        password_box.send_keys("LOVES")
        assert password_box.get_attribute('value') == "LOVES", "Password box not filled correctly"

        logger.info("Locating and filling in the text area.")
        text_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-textarea"))
        )
        text_area.send_keys("This is not working properly we are testing one 2 t ")
        assert text_area.get_attribute('value') == "This is not working properly we are testing one 2 t ", "Text area not filled correctly"

        logger.info("Selecting an option from the dropdown.")
        data_drop_down_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-select"))
        )
        data_drop_down_select.send_keys("One")
        assert data_drop_down_select.get_attribute('value') == "1", "Dropdown select not filled correctly"

        logger.info("Filling in the data list.")
        data_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-datalist"))
        )
        data_list.send_keys("San Francisco")
        assert data_list.get_attribute('value') == "San Francisco", "Datalist not filled correctly"

        logger.info("Submitting the form.")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
        )
        submit_button.click()

        logger.info("Verifying login success.")
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "success-message"))
        )
        try:
            assert "Welcome" in success_message.text, "Login failed"
        except AssertionError as e:
            log_defect_to_jira("Login Failure", str(e))
            raise

