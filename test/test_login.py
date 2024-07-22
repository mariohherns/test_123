import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestWebForm:
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()

    def test_page_title(self, driver):
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        title = driver.title
        print(f"Page title is: {title}")
        assert title == "Web form", "Page title does not match"

    def test_form_submission(self, driver):
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        driver.implicitly_wait(5)

        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-text"))
        )
        assert text_box is not None, "Text box not found"

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
        )
        assert submit_button is not None, "Submit button not found"

        password_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-password"))
        )
        password_box.send_keys("LOVES")
        assert password_box.get_attribute('value') == "LOVES", "Password box not filled correctly"

        text_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-textarea"))
        )
        text_area.send_keys("This is not working properly we are testing one 2 t ")
        assert text_area.get_attribute('value') == "This is not working properly we are testing one 2 t ", "Text area not filled correctly"

        data_drop_down_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-select"))
        )
        data_drop_down_select.send_keys("One")
        assert data_drop_down_select.get_attribute('value') == "1", "Dropdown select not filled correctly"

        data_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "my-datalist"))
        )
        data_list.send_keys("San Francisco")
        assert data_list.get_attribute('value') == "San Francisco", "Datalist not filled correctly"

        text_box.send_keys("Selenium")
        submit_button.click()

        message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "message"))
        )
        assert "Received" in message.text, "Form submission failed"
        print(f"Message: {message.text}")
