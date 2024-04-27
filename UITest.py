import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Initialize Microsoft Edge WebDriver
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_contact_submission(driver):
    driver.get("http://localhost:5000/contact")
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.NAME, "email").send_keys("john@example.com")
    driver.find_element(By.NAME, "subject").send_keys("Test Subject")
    driver.find_element(By.NAME, "webURL").send_keys("http://example.com")
    driver.find_element(By.NAME, "text").send_keys("This is a test message")
    driver.find_element(By.XPATH, "//button").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:5000/"))
    assert "Thank you for contacting us!" in driver.page_source

def test_invalid_contact_submission_missing_email(driver):
    driver.get("http://localhost:5000/contact")
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.NAME, "subject").send_keys("Test Subject")
    driver.find_element(By.NAME, "webURL").send_keys("http://example.com")
    driver.find_element(By.NAME, "text").send_keys("This is a test message")
    driver.find_element(By.XPATH, "//button").click()
    # Assuming you have an error handling mechanism to stay on the same page and show a message
    assert "Please provide your email" in driver.page_source
    assert driver.current_url == "http://localhost:5000/contact"
