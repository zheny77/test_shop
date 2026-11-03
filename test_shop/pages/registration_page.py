import allure
from selenium.webdriver.common.by import By

from data.user import UserData
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    PATH = "/parabank/register.htm"

    FIRST_NAME = (By.ID, "customer.firstName")
    LAST_NAME = (By.ID, "customer.lastName")
    ADDRESS = (By.ID, "customer.address.street")
    CITY = (By.ID, "customer.address.city")
    STATE = (By.ID, "customer.address.state")
    ZIP_CODE = (By.ID, "customer.address.zipCode")
    PHONE = (By.ID, "customer.phoneNumber")
    SSN = (By.ID, "customer.ssn")
    USERNAME = (By.ID, "customer.username")
    PASSWORD = (By.ID, "customer.password")
    CONFIRM = (By.ID, "repeatedPassword")
    REGISTER_BTN = (By.CSS_SELECTOR, "input[value='Register']")

    SUCCESS_TITLE = (By.CSS_SELECTOR, "#rightPanel h1.title")
    SUCCESS_TEXT = (By.CSS_SELECTOR, "#rightPanel p")

    # ids сообщений об ошибках у каждого поля
    ERRORS = {
        "first_name": (By.ID, "customer.firstName.errors"),
        "last_name": (By.ID, "customer.lastName.errors"),
        "address": (By.ID, "customer.address.street.errors"),
        "city": (By.ID, "customer.address.city.errors"),
        "state": (By.ID, "customer.address.state.errors"),
        "zip_code": (By.ID, "customer.address.zipCode.errors"),
        "ssn": (By.ID, "customer.ssn.errors"),
        "username": (By.ID, "customer.username.errors"),
        "password": (By.ID, "customer.password.errors"),
        "confirm": (By.ID, "repeatedPassword.errors"),
    }

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url.rstrip("/")

    @allure.step("Открыть страницу регистрации")
    def open_page(self):
        self.open(self.base_url + self.PATH)
        self.find_visible(self.FIRST_NAME)
        return self

    @allure.step("Ввести имя: {value}")
    def set_first_name(self, value: str):
        return self.type_text(self.FIRST_NAME, value)

    @allure.step("Ввести фамилию: {value}")
    def set_last_name(self, value: str):
        return self.type_text(self.LAST_NAME, value)

    @allure.step("Ввести адрес: {value}")
    def set_address(self, value: str):
        return self.type_text(self.ADDRESS, value)

    @allure.step("Ввести город: {value}")
    def set_city(self, value: str):
        return self.type_text(self.CITY, value)

    @allure.step("Ввести штат/регион: {value}")
    def set_state(self, value: str):
        return self.type_text(self.STATE, value)

    @allure.step("Ввести индекс: {value}")
    def set_zip_code(self, value: str):
        return self.type_text(self.ZIP_CODE, value)

    @allure.step("Ввести телефон: {value}")
    def set_phone(self, value: str):
        return self.type_text(self.PHONE, value)

    @allure.step("Ввести SSN: {value}")
    def set_ssn(self, value: str):
        return self.type_text(self.SSN, value)

    @allure.step("Ввести логин: {value}")
    def set_username(self, value: str):
        return self.type_text(self.USERNAME, value)

    @allure.step("Ввести пароль")
    def set_password(self, value: str):
        return self.type_text(self.PASSWORD, value)

    @allure.step("Повторить пароль")
    def set_confirm(self, value: str):
        return self.type_text(self.CONFIRM, value)

    @allure.step("Заполнить всю форму регистрации")
    def fill_form(self, user: UserData):
        return (self.set_first_name(user.first_name)
                .set_last_name(user.last_name)
                .set_address(user.address)
                .set_city(user.city)
                .set_state(user.state)
                .set_zip_code(user.zip_code)
                .set_phone(user.phone)
                .set_ssn(user.ssn)
                .set_username(user.username)
                .set_password(user.password)
                .set_confirm(user.confirm))

    @allure.step("Нажать кнопку Register")
    def submit(self):
        return self.click(self.REGISTER_BTN)

    @allure.step("Получить текст ошибки поля '{field}'")
    def get_error(self, field: str) -> str:
        return self.get_text(self.ERRORS[field])

    @allure.step("Проверить ошибку поля '{field}': '{expected}'")
    def should_have_error(self, field: str, expected: str):
        actual = self.get_error(field)
        assert actual == expected, f"Ожидали '{expected}', получили '{actual}'"
        return self

    @allure.step("Проверить, что остались на странице регистрации")
    def should_stay_on_registration(self):
        assert "register.htm" in self.driver.current_url
        return self

    @allure.step("Проверить успешную регистрацию для '{username}'")
    def should_be_registered(self, username: str):
        title = self.get_text(self.SUCCESS_TITLE)
        assert title == f"Welcome {username}", f"Заголовок: '{title}'"
        text = self.get_text(self.SUCCESS_TEXT)
        assert "Your account was created successfully" in text, text
        return self
