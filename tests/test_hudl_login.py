import os
import unittest
from datetime import timedelta
from tempfile import TemporaryDirectory
from unittest import TestCase, skip, skipIf

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# How long to wait for an element to become available
DRIVER_TIMEOUT = timedelta(seconds=30)
# Test credentials
TEST_EMAIL = os.environ.get("HUDL_TEST_EMAIL")
TEST_PASSWORD = os.environ.get("HUDL_TEST_PASSWORD")


def _create_chrome_driver(*, options=None, timeout=DRIVER_TIMEOUT):
    driver = Chrome(options=options or Options())
    driver.implicitly_wait(timeout.total_seconds())
    return driver


def _login(driver, *, email=TEST_EMAIL, password=TEST_PASSWORD, remember_me=False):
    driver.get("https://www.hudl.com/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    if remember_me:
        driver.find_element(By.XPATH, '//*[@for="remember-me"]').click()
        # driver.find_element(By.ID, "remember-me").click()
    driver.find_element(By.ID, "logIn").click()


def _find_logout_element(driver):
    return driver.find_element(By.XPATH, '//*[@data-qa-id="webnav-usermenu-logout"]')


@skipIf(
    not TEST_EMAIL or not TEST_PASSWORD, "test email and test password must be provided"
)
class HudlLogInPageTestCase(TestCase):
    def setUp(self):
        self._driver = _create_chrome_driver()

    def tearDown(self) -> None:
        self._driver.quit()

    def test_login_with_correct_credentials(self):
        _login(self._driver)
        # Check that user account is the right one by checking the email
        self._driver.find_element(By.XPATH, f'//*[normalize-space()="{TEST_EMAIL}"]')
        # Additional check that user logged in and can log out
        _find_logout_element(self._driver)

    def test_login_with_wrong_password(self):
        _login(self._driver, password="wrong_password")
        # Check that error message is displayed and the login button is
        # disabled when password is incorrect
        self._driver.find_element(By.CLASS_NAME, "login-error-container")
        self.assertFalse(self._driver.find_element(By.ID, "logIn").is_enabled())

    def test_login_with_wrong_email(self):
        _login(self._driver, email="wrong_email")
        # Check that LogIn button disabled when email is incorrect
        self.assertFalse(self._driver.find_element(By.ID, "logIn").is_enabled())

    def test_login_with_an_organisation(self):
        self._driver.get("https://www.hudl.com/login")
        # Check that "Log in with organization" button works
        self._driver.find_element(By.ID, "logInWithOrganization").click()

    def test_check_need_help_link(self):
        self._driver.get("https://www.hudl.com/login")
        # Check that "Need help?"" link works
        self._driver.find_element(By.PARTIAL_LINK_TEXT, "Need help?").click()

    def test_check_sign_up_button(self):
        self._driver.get("https://www.hudl.com/login")
        # Check that "Sign Up" link works
        self._driver.find_element(By.PARTIAL_LINK_TEXT, "Sign up").click()

    @skip("not ready")
    def test_remember_me(self):
        # Special case: we want a custom driver
        with TemporaryDirectory() as user_data_directory:
            options = Options()
            options.add_argument(f"--user-data-dir={user_data_directory}")
            options.add_argument("--profile-directory=hudl_test_profile")
            try:
                driver = _create_chrome_driver(options=options)
                # Wait until logged in
                _login(driver, remember_me=True)
                _find_logout_element(driver)
            finally:
                driver.quit()
            try:
                driver = _create_chrome_driver(options=options)
                # Hit the page and expect that we are logged in
                driver.get("https://www.hudl.com/login")
                _find_logout_element(driver)
            finally:
                driver.quit()


if __name__ == "__main__":
    unittest.main()
