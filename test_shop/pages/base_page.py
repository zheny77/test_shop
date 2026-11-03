import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Низкоуровневое взаимодействие с браузером. Только явные ожидания."""

    TIMEOUT = 10

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    @allure.step("Открыть страницу {url}")
    def open(self, url: str):
        self.driver.get(url)
        return self

    @allure.step("Найти видимый элемент {locator}")
    def find_visible(self, locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Клик по элементу {locator}")
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    @allure.step("Ввести текст в {locator}")
    def type_text(self, locator, text: str):
        element = self.find_visible(locator)
        element.clear()
        if text:
            element.send_keys(text)
        return self

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator) -> str:
        return self.find_visible(locator).text.strip()

    @allure.step("Проверить, виден ли элемент {locator}")
    def is_visible(self, locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    @allure.step("Дождаться вхождения '{part}' в URL")
    def wait_url_contains(self, part: str):
        self.wait.until(EC.url_contains(part))
        return self
