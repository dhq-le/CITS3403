import unittest
import time
from threading import Thread
from werkzeug.serving import make_server

from app import create_app, db
from app.models import Usernames
from config import TestingConfig

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ServerThread(Thread):
    def __init__(self, app):
        super().__init__()
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

class SeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Flask app with testing config
        app = create_app(TestingConfig)
        app.testing = True
        cls.server = ServerThread(app)
        cls.server.start()
        time.sleep(1)

        # Initialize in-memory database and add a test user
        with app.app_context():
            db.create_all()
            u = Usernames(username="selenium_user", height=170, weight=65, dob=19900101)
            u.set_password("selenium_pass")
            db.session.add(u)
            db.session.commit()

        # Launch headless Chrome
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        # Log in to reuse session
        cls._login()

    @classmethod
    def _login(cls):
        cls.driver.get("http://127.0.0.1:5000/login")
        # Debug: dump login page HTML
        print(cls.driver.page_source)
        WebDriverWait(cls.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        cls.driver.find_element(By.ID, "usernameInput").send_keys("selenium_user")
        # reveal password field
        cls.driver.find_element(By.ID, "to-password").click()
        WebDriverWait(cls.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "passwordInput"))
        )
        cls.driver.find_element(By.ID, "passwordInput").send_keys("selenium_pass")
        cls.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # Debug: dump post-login page HTML and URL
        print("Post-login URL:", cls.driver.current_url)
        print(cls.driver.page_source)
        # login redirect: wait for dashboard welcome header
        WebDriverWait(cls.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header.dashboard-header h1"))
        )

    def test_00_signup_creates_account(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/signup")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print(self.driver.page_source)
        driver.find_element(By.NAME, "username").send_keys("new_user")
        driver.find_element(By.NAME, "password").send_keys("new_pass")
        driver.find_element(By.NAME, "height").send_keys("180")
        driver.find_element(By.NAME, "weight").send_keys("75")
        driver.find_element(By.NAME, "dob").send_keys("19900202")
        # submit and wait for login page to load
        driver.find_element(By.TAG_NAME, "form").submit()
        # Debug: print current URL and page HTML after signup submit
        print("After signup URL:", driver.current_url)
        print(driver.page_source)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "usernameInput"))
        )
        # verify success flash message on login page
        self.assertTrue(driver.find_element(By.ID, "usernameInput").is_displayed())

    def test_01_dashboard_access(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("Welcome back", driver.page_source)

    def test_02_logout_and_redirect(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/logout")
        WebDriverWait(driver, 5).until(
            EC.url_contains("/")
        )
        self.assertIn("Login", driver.page_source)

    def test_03_protected_redirect(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "usernameInput"))
        )
        self.assertIn("Login", driver.page_source)

    def test_04_profile_page_loads(self):
        # ensure user is logged in for profile access
        self._login()
        driver = self.driver

        # Click the Profile button in the navbar
        driver.get("http://127.0.0.1:5000/")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "ProfileButton"))
        ).click()

        # Wait for the profile details container to appear
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-details"))
        )

        # Confirm that the profile-details section displays the username
        self.assertIn("Username:", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.shutdown()
        cls.server.join()

if __name__ == "__main__":
    unittest.main()
