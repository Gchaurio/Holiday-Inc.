import unittest
from . import AppTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTests(AppTest):
    
    def test_admin(self):
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        password = self.driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("admin")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("admin")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/start/admin/aprove"))
        actualUrl = "http://localhost:5000/start/admin/aprove"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_unregistered_user_login(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/register")
        assert "Register" in driver.title
        password = driver.find_element(By.NAME, "password")
        password.clear()
        password.send_keys("test")
        user = driver.find_element(By.NAME, "username")
        user.clear()
        user.send_keys("test")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("test")
        lastname = driver.find_element(By.NAME, "lastname")
        lastname.send_keys("test")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_login_unauthorized(self):
        self.test_registerNonRegisteredUser()
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        password = self.driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("test")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("test")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = self.driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Account has not been verified by admin."):
                self.assertEqual(e.text,"Account has not been verified by admin.")

    def test_login_incorrect_username(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        password = driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("test")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("test")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Incorrect username."):
                self.assertEqual(e.text,"Incorrect username.")

    def test_admin_copy(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/register")
        assert "Register" in driver.title
        password = driver.find_element(By.NAME, "password")
        password.clear()
        password.send_keys("admin")
        user = driver.find_element(By.NAME, "username")
        user.clear()
        user.send_keys("admin")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("admin")
        lastname = driver.find_element(By.NAME, "lastname")
        lastname.send_keys("admin")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/register"))
        actualUrl = "http://localhost:5000/auth/register"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "User admin is already registered."):
                self.assertEqual(e.text,"User admin is already registered.")
    
    def test_login_incorrect_password(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        password = driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("test")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("incorrect")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Incorrect password."):
                self.assertEqual(e.text,"Incorrect password.")

    def test_admin_reject(self):
        self.test_registerNonRegisteredUser()
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        password = self.driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("admin")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("admin")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/start/approve"))
        actualUrl = "http://localhost:5000/start/approve"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        user_button = self.driver.find_element(By.ID, "user")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/start/approve"))
        actualUrl = "http://localhost:5000/start/approve"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        reject_button = self.driver.find_element(By.NAME, "reject")
        reject_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/start/approve"))
        actualUrl = "http://localhost:5000/start/approve"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)


    def test_create_project(self):
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        password = self.driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("admin")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("admin")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/user/admin"))
        actualUrl = "http://localhost:5000/user/admin"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        user_button = self.driver.find_element(By.ID, "proyect")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/start/create_project.html"))
        actualUrl = "http://localhost:5000/start/create_project.html"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_proyect_button = self.driver.find_element(By.NAME, "create-proyect")
        create_proyect_button.click()
        proyect_description = self.driver.find_element(By.ID, "description")
        proyect_description.send_keys("test_project")
        proyect_starting_date = self.driver.find_element(By.ID, "init")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2021-01-01")
        proyect_end_date = self.driver.find_element(By.ID, "end")
        proyect_end_date.click()
        proyect_end_date.send_keys("2022-01-01")
        proyect_description.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/start/create_project.html"))
        actualUrl = "http://localhost:5000/start/create_project.html"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)


if __name__ == '__main__':
    unittest.main()