import json

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

SUPPORTED_BROWSERS = ("chrome", "firefox")


def pytest_addoption(parser):
    parser.addoption("--browser", action="append", default=[],
                     choices=SUPPORTED_BROWSERS,
                     help="chrome / firefox; можно указать несколько раз "
                          "(по умолчанию запускаются оба)")
    parser.addoption("--headless", action="store_true", help="Без окна браузера")
    parser.addoption("--base-url", default="https://parabank.parasoft.com",
                     help="Базовый URL приложения")


def pytest_generate_tests(metafunc):
    """Мультибраузерность: каждый тест запускается в каждом выбранном браузере."""
    if "driver" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("--browser") or list(SUPPORTED_BROWSERS)
        metafunc.parametrize("driver", browsers, indirect=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняем результат каждой фазы теста, чтобы фикстура знала о падении."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Фикстура для получения url."""
    return request.config.getoption("--base-url")


def _create_driver(name: str, headless: bool):
    if name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        # включаем сбор логов консоли и сети
        options.set_capability("goog:loggingPrefs",
                               {"browser": "ALL", "performance": "ALL"})
        return webdriver.Chrome(options=options)
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    return driver


def _attach_diagnostics(driver, name: str):
    allure.attach(driver.get_screenshot_as_png(), name="screenshot",
                  attachment_type=allure.attachment_type.PNG)
    allure.attach(driver.current_url, name="url",
                  attachment_type=allure.attachment_type.TEXT)

    # логи консоли браузера (get_log поддерживает только Chrome)
    try:
        entries = driver.get_log("browser")
        text = "\n".join(f"[{e['level']}] {e['message']}" for e in entries)
    except Exception:
        text = "Логи консоли недоступны для этого браузера"
    allure.attach(text or "Консоль пуста", name="browser_console_log",
                  attachment_type=allure.attachment_type.TEXT)

    # сетевые запросы
    try:
        if name == "chrome":
            requests = []
            for e in driver.get_log("performance"):
                msg = json.loads(e["message"])["message"]
                if msg["method"] in ("Network.requestWillBeSent",
                                     "Network.responseReceived"):
                    requests.append(msg)
            network = json.dumps(requests, ensure_ascii=False, indent=2)
        else:
            network = json.dumps(driver.execute_script(
                "return performance.getEntriesByType('resource').map(r => ({"
                "url: r.name, type: r.initiatorType, duration: r.duration,"
                "status: r.responseStatus}));"), ensure_ascii=False, indent=2)
    except Exception as exc:
        network = f"Не удалось получить сетевые запросы: {exc}"
    allure.attach(network, name="network_requests",
                  attachment_type=allure.attachment_type.JSON)


@pytest.fixture
def driver(request):
    """Фикстура получения и удаления драйвера (+ артефакты при падении)."""
    name = request.param
    drv = _create_driver(name, request.config.getoption("--headless"))
    drv.implicitly_wait(0)  # неявное ожидание = 0, используем только явные
    yield drv
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        _attach_diagnostics(drv, name)
    drv.quit()
